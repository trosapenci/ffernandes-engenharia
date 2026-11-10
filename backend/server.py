#!/usr/bin/env python3
"""
FFernandes Engenharia e Construção Ltda. — High-Reliability REST API & Static Server
Arquitetura: Clean RESTful API (v1) + RFC 7807 Problem Details + Idempotency-Key + SQLite WAL
"""

import json
import mimetypes
import os
import re
import sqlite3
import time
import urllib.parse
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from seed_data import DB_PATH, init_and_seed_db

ROOT_DIR = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8090"))
HOST = os.environ.get("HOST", "0.0.0.0")

# Garantir MIME types modernos
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")

# Rate Limiter simples em memória (IP -> lista de timestamps)
RATE_LIMIT_WINDOW_SEC = 60
RATE_LIMIT_MAX_POSTS = 15
_rate_limit_store: dict[str, list[float]] = {}

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


class FFernandesAPIHandler(BaseHTTPRequestHandler):
    server_version = "FFernandesEngine/1.0"

    def _send_common_headers(self, request_id: str) -> None:
        self.send_header("X-Request-Id", request_id)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Idempotency-Key, X-Request-Id")

    def _send_json(self, status_code: int, payload: dict, request_id: str, content_type: str = "application/json") -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self._send_common_headers(request_id)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_problem_details(
        self,
        status_code: int,
        title: str,
        detail: str,
        request_id: str,
        problem_type: str = "about:blank",
        invalid_params: list[dict] | None = None,
    ) -> None:
        """Padronização de erros RFC 7807 (application/problem+json)."""
        problem = {
            "type": problem_type,
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": self.path,
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if invalid_params:
            problem["invalid_params"] = invalid_params
        self._send_json(status_code, problem, request_id, content_type="application/problem+json")

    def do_OPTIONS(self) -> None:
        request_id = self.headers.get("X-Request-Id") or str(uuid.uuid4())
        self.send_response(204)
        self._send_common_headers(request_id)
        self.end_headers()

    def do_GET(self) -> None:
        request_id = self.headers.get("X-Request-Id") or str(uuid.uuid4())
        parsed = urllib.parse.urlparse(self.path)
        route = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if route.startswith("/api/"):
            self._handle_api_get(route, query, request_id)
            return

        self._serve_static(route, request_id)

    def _handle_api_get(self, route: str, query: dict, request_id: str) -> None:
        try:
            with get_db_connection() as conn:
                if route in ("/api/v1/health", "/api/health"):
                    p_count = conn.execute("SELECT COUNT(*) FROM portfolio_projects").fetchone()[0]
                    c_count = conn.execute("SELECT COUNT(*) FROM official_clients").fetchone()[0]
                    s_count = conn.execute("SELECT COUNT(*) FROM engineering_services").fetchone()[0]
                    l_count = conn.execute("SELECT COUNT(*) FROM leads_orcamento").fetchone()[0]
                    self._send_json(
                        200,
                        {
                            "status": "ok",
                            "service": "ffernandes-engenharia-api",
                            "version": "1.0.0",
                            "database": "connected",
                            "counts": {
                                "portfolio_projects": p_count,
                                "official_clients": c_count,
                                "engineering_services": s_count,
                                "leads_received": l_count,
                            },
                            "request_id": request_id,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        },
                        request_id,
                    )
                    return

                if route in ("/api/v1/company", "/api/company"):
                    row = conn.execute("SELECT * FROM company_profile WHERE id = 1").fetchone()
                    if not row:
                        self._send_problem_details(404, "Not Found", "Perfil institucional não encontrado.", request_id)
                        return
                    data = dict(row)
                    data["values"] = json.loads(data.pop("values_json"))
                    data["differentials"] = json.loads(data.pop("differentials_json"))
                    self._send_json(200, {"data": data}, request_id)
                    return

                if route in ("/api/v1/services", "/api/services"):
                    division = query.get("division", [None])[0]
                    if division:
                        rows = conn.execute(
                            "SELECT * FROM engineering_services WHERE division_slug = ? ORDER BY specialty_order ASC",
                            (division,),
                        ).fetchall()
                    else:
                        rows = conn.execute(
                            "SELECT * FROM engineering_services ORDER BY division_slug ASC, specialty_order ASC"
                        ).fetchall()
                    self._send_json(200, {"total": len(rows), "data": [dict(r) for r in rows]}, request_id)
                    return

                if route in ("/api/v1/portfolio", "/api/portfolio"):
                    category = query.get("category", [None])[0]
                    if category and category != "todas":
                        rows = conn.execute(
                            "SELECT * FROM portfolio_projects WHERE category_slug = ? ORDER BY display_order ASC",
                            (category,),
                        ).fetchall()
                    else:
                        rows = conn.execute(
                            "SELECT * FROM portfolio_projects ORDER BY display_order ASC"
                        ).fetchall()
                    items = []
                    for r in rows:
                        d = dict(r)
                        d["disciplines"] = json.loads(d.pop("disciplines_json"))
                        d["gallery"] = json.loads(d.pop("gallery_json"))
                        items.append(d)
                    self._send_json(200, {"total": len(items), "data": items}, request_id)
                    return

                if route in ("/api/v1/clients", "/api/clients"):
                    sector = query.get("sector", [None])[0]
                    if sector and sector != "todos":
                        rows = conn.execute(
                            "SELECT * FROM official_clients WHERE sector_slug = ? ORDER BY id ASC",
                            (sector,),
                        ).fetchall()
                    else:
                        rows = conn.execute("SELECT * FROM official_clients ORDER BY id ASC").fetchall()
                    self._send_json(200, {"total": len(rows), "data": [dict(r) for r in rows]}, request_id)
                    return

                self._send_problem_details(
                    404,
                    "Endpoint Não Encontrado",
                    f"A rota '{route}' não existe na API v1 da FFernandes Engenharia.",
                    request_id,
                    problem_type="https://ffernandes.eng.br/probs/not-found",
                )
        except Exception as exc:
            self._send_problem_details(
                500,
                "Erro Interno do Servidor",
                f"Falha ao processar requisição: {type(exc).__name__}",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/internal-error",
            )

    def do_POST(self) -> None:
        request_id = self.headers.get("X-Request-Id") or str(uuid.uuid4())
        parsed = urllib.parse.urlparse(self.path)
        route = parsed.path

        if route not in ("/api/v1/leads", "/api/leads"):
            self._send_problem_details(
                404,
                "Endpoint Não Encontrado",
                f"A rota POST '{route}' não existe.",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/not-found",
            )
            return

        # Rate Limiting por IP
        client_ip = self.client_address[0] if self.client_address else "unknown"
        now = time.time()
        history = [t for t in _rate_limit_store.get(client_ip, []) if now - t < RATE_LIMIT_WINDOW_SEC]
        if len(history) >= RATE_LIMIT_MAX_POSTS:
            self._send_problem_details(
                429,
                "Limite de Requisições Excedido",
                "Muitas solicitações enviadas em curto intervalo. Aguarde um minuto e tente novamente.",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/rate-limit-exceeded",
            )
            return
        history.append(now)
        _rate_limit_store[client_ip] = history

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > 65536:
            self._send_problem_details(
                400,
                "Payload Inválido",
                "O corpo da requisição está vazio ou excede o tamanho máximo permitido (64KB).",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/invalid-payload",
            )
            return

        try:
            body = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except Exception:
            self._send_problem_details(
                400,
                "JSON Malformado",
                "Não foi possível decodificar o JSON enviado.",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/malformed-json",
            )
            return

        # Validação estrita dos campos (RFC 7807 invalid_params)
        contact_name = str(body.get("contact_name", "")).strip()
        company_name = str(body.get("company_name", "")).strip()
        phone_whatsapp = str(body.get("phone_whatsapp", "")).strip()
        email = str(body.get("email", "")).strip()
        discipline_interest = str(body.get("discipline_interest", "")).strip()
        project_location = str(body.get("project_location", "")).strip()
        message = str(body.get("message", "")).strip()

        invalid_params = []
        if len(contact_name) < 2:
            invalid_params.append({"name": "contact_name", "reason": "Informe seu nome completo (mínimo 2 caracteres)."})
        if len(phone_whatsapp) < 8:
            invalid_params.append({"name": "phone_whatsapp", "reason": "Informe um telefone ou WhatsApp válido com DDD."})
        if not EMAIL_REGEX.match(email):
            invalid_params.append({"name": "email", "reason": "Informe um endereço de e-mail corporativo ou pessoal válido."})
        if not discipline_interest:
            invalid_params.append({"name": "discipline_interest", "reason": "Selecione a disciplina de interesse."})
        if len(message) < 5:
            invalid_params.append({"name": "message", "reason": "Descreva brevemente a necessidade do projeto (mínimo 5 caracteres)."})

        if invalid_params:
            self._send_problem_details(
                422,
                "Erro de Validação dos Dados do Orçamento",
                "Um ou mais campos obrigatórios apresentam formato inválido.",
                request_id,
                problem_type="https://ffernandes.eng.br/probs/validation-error",
                invalid_params=invalid_params,
            )
            return

        idempotency_key = self.headers.get("Idempotency-Key") or body.get("idempotency_key")
        if idempotency_key:
            idempotency_key = str(idempotency_key).strip()[:128]

        try:
            with get_db_connection() as conn:
                if idempotency_key:
                    existing = conn.execute(
                        "SELECT * FROM leads_orcamento WHERE idempotency_key = ?",
                        (idempotency_key,),
                    ).fetchone()
                    if existing:
                        lead_dict = dict(existing)
                        wa_url = self._build_whatsapp_url(lead_dict)
                        self._send_json(
                            200,
                            {
                                "status": "idempotent_replay",
                                "message": "Solicitação técnica já registrada anteriormente.",
                                "lead_id": lead_dict["id"],
                                "whatsapp_redirect_url": wa_url,
                                "data": lead_dict,
                            },
                            request_id,
                        )
                        return

                lead_id = f"lead-{uuid.uuid4().hex[:12]}"
                created_at = datetime.now(timezone.utc).isoformat()
                conn.execute(
                    """
                    INSERT INTO leads_orcamento (
                        id, idempotency_key, contact_name, company_name, phone_whatsapp,
                        email, discipline_interest, project_location, message, client_ip, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        lead_id,
                        idempotency_key,
                        contact_name,
                        company_name,
                        phone_whatsapp,
                        email,
                        discipline_interest,
                        project_location,
                        message,
                        client_ip,
                        created_at,
                    ),
                )
                conn.commit()

                lead_record = {
                    "id": lead_id,
                    "contact_name": contact_name,
                    "company_name": company_name,
                    "phone_whatsapp": phone_whatsapp,
                    "email": email,
                    "discipline_interest": discipline_interest,
                    "project_location": project_location,
                    "message": message,
                    "created_at": created_at,
                }
                wa_url = self._build_whatsapp_url(lead_record)
                self._send_json(
                    201,
                    {
                        "status": "created",
                        "message": "Solicitação registrada com sucesso na central técnica da FFernandes Engenharia.",
                        "lead_id": lead_id,
                        "whatsapp_redirect_url": wa_url,
                        "data": lead_record,
                    },
                    request_id,
                )
        except Exception as exc:
            self._send_problem_details(
                500,
                "Erro ao Registrar Solicitação",
                f"Não foi possível persistir o registro: {type(exc).__name__}",
                request_id,
            )

    @staticmethod
    def _build_whatsapp_url(lead: dict) -> str:
        empresa_str = f" ({lead['company_name']})" if lead.get("company_name") else ""
        local_str = f"\n• Local da Obra: {lead['project_location']}" if lead.get("project_location") else ""
        text = (
            f"Olá, equipe FFernandes Engenharia!\n\n"
            f"Solicito atendimento técnico pelo site:\n"
            f"• Nome: {lead['contact_name']}{empresa_str}\n"
            f"• Disciplina: {lead['discipline_interest']}{local_str}\n"
            f"• Telefone: {lead['phone_whatsapp']}\n"
            f"• E-mail: {lead['email']}\n"
            f"• Escopo/Mensagem: {lead['message']}"
        )
        return f"https://wa.me/5511977008643?text={urllib.parse.quote(text)}"

    def _serve_static(self, route: str, request_id: str) -> None:
        if route in ("/", "/index.html", "/portfolio", "/dicas", "/contato"):
            target = ROOT_DIR / "index.html"
        else:
            clean_rel = os.path.normpath(route.lstrip("/"))
            if clean_rel.startswith(".."):
                self._send_problem_details(403, "Acesso Negado", "Caminho inválido.", request_id)
                return
            target = (ROOT_DIR / clean_rel).resolve()
            if not str(target).startswith(str(ROOT_DIR)):
                self._send_problem_details(403, "Acesso Negado", "Caminho fora do diretório raiz.", request_id)
                return

        if not target.exists() or not target.is_file():
            self._send_problem_details(404, "Arquivo Não Encontrado", f"O recurso '{route}' não existe.", request_id)
            return

        ctype, _ = mimetypes.guess_type(str(target))
        if not ctype:
            ctype = "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype = f"{ctype}; charset=utf-8"

        raw = target.read_bytes()
        self.send_response(200)
        self._send_common_headers(request_id)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        if "/assets/" in route:
            self.send_header("Cache-Control", "public, max-age=86400")
        else:
            self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} - {fmt % args}")


def run_server() -> None:
    init_and_seed_db()
    server = ThreadingHTTPServer((HOST, PORT), FFernandesAPIHandler)
    print(f"==================================================================")
    print(f" FFernandes Engenharia — Full-Stack Server Ativo")
    print(f" URL Local:    http://localhost:{PORT}")
    print(f" Healthcheck:  http://localhost:{PORT}/api/v1/health")
    print(f" Banco SQLite: {DB_PATH}")
    print(f"==================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        server.server_close()


if __name__ == "__main__":
    run_server()
