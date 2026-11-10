#!/usr/bin/env python3
"""
População Determinística do Banco SQLite (ffernandes.db)
100% Dados Reais Absorvidos de https://ffernandes.eng.br e https://ffernandes.eng.br/portfolio
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ffernandes.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

COMPANY_DATA = {
    "id": 1,
    "legal_name": "FFernandes Engenharia e Construção Ltda.",
    "brand_name": "FFernandes Engenharia de Projetos",
    "years_badge": "12 Anos",
    "headline": "Inovação e Excelência em Projetos Complementares",
    "subheadline": "SOLUÇÕES INTELIGENTES PARA CONSTRUÇÕES MODERNAS",
    "essence_summary": (
        "A FFernandes Engenharia e Construção Ltda. é referência no desenvolvimento de projetos "
        "de Instalações Elétricas e Hidráulicas, com foco total em excelência técnica, qualidade "
        "e pontualidade rigorosa."
    ),
    "mission": (
        "Atuar no segmento de engenharia civil com projetos complementares de alta precisão "
        "para diversos tipos de edificações."
    ),
    "vision": (
        "Ser referência em baixo custo, executividade e longevidade, garantindo a qualidade "
        "superior do produto final."
    ),
    "values": [
        "Ética e Transparência",
        "Compromisso com Prazos",
        "Inovação e Sustentabilidade",
        "Valorização do Investimento",
    ],
    "differentials": [
        {
            "title": "Equipe Qualificada",
            "description": (
                "Profissionais com ampla vivência no segmento da construção civil, "
                "garantindo expertise técnica em cada detalhe do projeto."
            ),
            "icon": "users-shield",
        },
        {
            "title": "Otimização de Custos",
            "description": (
                "Busca contínua por soluções que diminuam o tempo de execução in-loco "
                "e otimizem o investimento global do cliente."
            ),
            "icon": "trending-down-cost",
        },
        {
            "title": "Conformidade Total",
            "description": (
                "Aplicação rigorosa das normativas vigentes e atendimento integral às normas "
                "das concessionárias locais de energia e saneamento."
            ),
            "icon": "clipboard-check",
        },
        {
            "title": "Qualidade e Eficiência",
            "description": (
                "Máxima qualidade em todas as etapas, desde o estudo preliminar até o "
                "projeto executivo liberado para obra."
            ),
            "icon": "layers-blueprint",
        },
    ],
    "technical_signature": "EXCELÊNCIA TÉCNICA QUE TRANSFORMA PROJETOS EM RESULTADOS CONCRETOS.",
    "normative_note": "PROJETOS DESENVOLVIDOS SOB AS MAIS RIGOROSAS NORMAS TÉCNICAS E DE CONCESSIONÁRIAS LOCAIS.",
    "address": "Rua Lajedo, 48 - Bairro Jardim Veronia",
    "city_state": "São Paulo / SP",
    "phone_display": "(11) 97700-8643",
    "whatsapp_url": "https://wa.me/5511977008643",
    "email": "contato@ffernandes.eng.br",
    "instagram_handle": "@ffer2014",
    "instagram_url": "https://www.instagram.com/ffer2014/?__pwa=1",
}

SERVICES_DATA = [
    # Instalações Elétricas
    ("ele-01", "eletrica", "Instalações Elétricas", "Sistemas de Energia e Potência", 1, "zap"),
    ("ele-02", "eletrica", "Instalações Elétricas", "Infraestrutura para Sistemas", 2, "cpu"),
    ("ele-03", "eletrica", "Instalações Elétricas", "SPDA (Para-raios)", 3, "shield-lightning"),
    ("ele-04", "eletrica", "Instalações Elétricas", "Projetos de Quadros e Bombas", 4, "sliders"),
    # Instalações Hidráulicas
    ("hid-01", "hidraulica", "Instalações Hidráulicas", "Água Potável e Reservatórios", 1, "droplet"),
    ("hid-02", "hidraulica", "Instalações Hidráulicas", "Sistemas de Esgoto e Pluviais", 2, "git-Pull-request"),
    ("hid-03", "hidraulica", "Instalações Hidráulicas", "Instalações de Gás GLP", 3, "flame"),
    ("hid-04", "hidraulica", "Instalações Hidráulicas", "Sistemas de Combate a Incêndio", 4, "fire-extinguisher"),
]

PORTFOLIO_DATA = [
    {
        "id": "proj-01",
        "slug": "condominio-trio-alto-de-pinheiros",
        "display_order": 1,
        "title": "Condomínio TRIO — Alto de Pinheiros",
        "location": "R. Antônio de Gouvêia Giudice × Pça. Beethoven — Alto de Pinheiros, São Paulo/SP",
        "category_slug": "residencial",
        "category_label": "Residencial Alto Padrão",
        "partner_name": "F.Fernandes Engenharia",
        "area_or_scale": "3 Casas Exclusivas de Alto Padrão",
        "official_description": (
            "Onde o Luxo Encontra a Perfeição no Alto de Pinheiros. Descubra o Trio, um condomínio "
            "exclusivo de apenas 3 casas de alto padrão nas prestigiadas R. Antônio de Gouvêia Giudice "
            "X Pça Beethoven no Alto de Pinheiros. A excelência é garantida pela F.Fernandes Engenharia, "
            "responsável por todos os projetos de instalações elétricas e hidráulicas, assegurando "
            "funcionalidade impecável e o mais alto padrão de segurança e conforto. Viva a exclusividade "
            "que você merece."
        ),
        "disciplines": ["Instalações Elétricas", "Instalações Hidráulicas"],
        "cover_image": "assets/img/portfolio/crops/crop-01-condominio-trio.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-01-condominio-trio.webp",
            "assets/img/portfolio/prancha-01-condominio-trio.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-01-condominio-trio.webp",
    },
    {
        "id": "proj-02",
        "slug": "heineken-campus-parque-villa-lobos",
        "display_order": 2,
        "title": "Heineken Campus (Heineken House) — Parque Villa-Lobos",
        "location": "Parque Villa-Lobos — São Paulo/SP",
        "category_slug": "corporativo",
        "category_label": "Corporativo, Cultura & Brand Experience",
        "partner_name": "RMR Engenharia (@rmrengenharia) e DC Set (@dcset)",
        "area_or_scale": "Complexo Cultural, Gastronomia & Lifestyle",
        "official_description": (
            "A Heineken House chegou ao Parque Villa-Lobos e nossa equipe fez parte dessa história. "
            "Nós da F.Fernandes Engenharia desenvolvemos os projetos de Instalações Elétricas e Hidráulicas "
            "deste espaço que une gastronomia, cultura, música, bem-estar e lifestyle em um dos principais "
            "parques urbanos de São Paulo. Um empreendimento que reforça o potencial do Villa-Lobos como "
            "destino de experiências de marca e ocupações culturais e que tem a nossa assinatura técnica "
            "por dentro. Que venham novos desafios e cases de sucesso em parceria com a @rmrengenharia e @dcset"
        ),
        "disciplines": ["Instalações Elétricas", "Instalações Hidráulicas"],
        "cover_image": "assets/img/portfolio/crops/crop-02-heineken-campus.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-02-heineken-campus.webp",
            "assets/img/portfolio/crops/crop-02b-heineken-aerial.webp",
            "assets/img/portfolio/prancha-02-heineken-campus.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-02-heineken-campus.webp",
    },
    {
        "id": "proj-03",
        "slug": "data-center-municipio-de-paulinia",
        "display_order": 3,
        "title": "Data Center — Município de Paulínia",
        "location": "Município de Paulínia / SP",
        "category_slug": "infraestrutura",
        "category_label": "Data Center & Infraestrutura Crítica",
        "partner_name": "Enerwatt Engenharia",
        "area_or_scale": "Reservatório Torre & Casa de Bombas",
        "official_description": (
            "DATA CENTER MUNICÍPIO DE PAULÍNIA — Projeto: Reservatório Torre e casa de bombas para "
            "reserva de Incêndio e Hidrantes. Em parceria com: Enerwatt Engenharia."
        ),
        "disciplines": [
            "Água Potável e Reservatórios",
            "Projetos de Quadros e Bombas",
            "Sistemas de Combate a Incêndio",
        ],
        "cover_image": "assets/img/portfolio/crops/crop-03-datacenter-paulinia.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-03-datacenter-paulinia.webp",
            "assets/img/portfolio/crops/crop-03b-datacenter-torre.webp",
            "assets/img/portfolio/prancha-03-datacenter-paulinia.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-03-datacenter-paulinia.webp",
    },
    {
        "id": "proj-04",
        "slug": "shopping-vautier-premium",
        "display_order": 4,
        "title": "Shopping Vautier Premium",
        "location": "Canindé / Brás — São Paulo/SP",
        "category_slug": "shopping",
        "category_label": "Shopping Centers & Varejo",
        "partner_name": "Shopping Vautier",
        "area_or_scale": "26 Novas Lojas (Retrofit)",
        "official_description": (
            "SHOPPING VAUTIER PREMIUM — PROJETOS RETROFIT COMPLEMENTARES (26 NOVAS LOJAS)."
        ),
        "disciplines": [
            "Projetos Retrofit Complementares",
            "Instalações Elétricas",
            "Instalações Hidráulicas",
        ],
        "cover_image": "assets/img/portfolio/crops/crop-04-shopping-vautier.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-04-shopping-vautier.webp",
            "assets/img/portfolio/prancha-04-vautier-allbras.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-04-vautier-allbras.webp",
    },
    {
        "id": "proj-05",
        "slug": "shopping-all-bras",
        "display_order": 5,
        "title": "Shopping All Brás",
        "location": "Brás — São Paulo/SP",
        "category_slug": "shopping",
        "category_label": "Shopping Centers & Varejo",
        "partner_name": "All Brás Shopping",
        "area_or_scale": "316 Novas Bancas e 9 Boxes (Retrofit)",
        "official_description": (
            "SHOPPING ALL BRÁS — PROJETOS RETROFIT COMPLEMENTARES (316 NOVAS BANCAS E 9 BOXES)."
        ),
        "disciplines": [
            "Projetos Retrofit Complementares",
            "Instalações Elétricas",
            "Instalações Hidráulicas",
        ],
        "cover_image": "assets/img/portfolio/crops/crop-05-shopping-allbras.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-05-shopping-allbras.webp",
            "assets/img/portfolio/prancha-04-vautier-allbras.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-04-vautier-allbras.webp",
    },
    {
        "id": "proj-06",
        "slug": "simba-safari-sao-paulo",
        "display_order": 6,
        "title": "Simba Safari — Complexo Turístico e Ambiental",
        "location": "São Paulo / SP",
        "category_slug": "complexos",
        "category_label": "Lazer, Esporte & Complexos",
        "partner_name": "Planem Engenharia",
        "area_or_scale": "7 Disciplinas de Infraestrutura Completa",
        "official_description": (
            "SIMBA SAFARI — DESENVOLVIMENTO E EXECUÇÃO DE PROJETOS EM: Energia, Sistemas, Água potável, "
            "Castelo d'água, Esgoto, Gás GLP, Águas pluviais. Em parceria com: PLANEM ENGENHARIA."
        ),
        "disciplines": [
            "Sistemas de Energia e Potência",
            "Infraestrutura para Sistemas",
            "Água Potável e Castelo d'Água",
            "Sistemas de Esgoto e Águas Pluviais",
            "Instalações de Gás GLP",
        ],
        "cover_image": "assets/img/portfolio/crops/crop-06-simba-safari.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-06-simba-safari.webp",
            "assets/img/portfolio/crops/crop-06b-simba-entrada.webp",
            "assets/img/portfolio/prancha-05-simba-safari.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-05-simba-safari.webp",
    },
    {
        "id": "proj-07",
        "slug": "clube-bayer-santo-amaro",
        "display_order": 7,
        "title": "Clube Bayer Santo Amaro",
        "location": "Santo Amaro — Município de São Paulo/SP",
        "category_slug": "complexos",
        "category_label": "Lazer, Esporte & Complexos",
        "partner_name": "ACE Engenharia",
        "area_or_scale": "Aprox. 1.200 m² (Retrofit & As-Built)",
        "official_description": (
            "CLUBE BAYER STO. AMARO - MUNICÍPIO DE SÃO PAULO | RETROFIT REFORMA HIDRÁULICA. "
            "APROX.: 1200m2 | PROJETOS AS-BUILT INSTALAÇÕES HIDROSSANITÁRIAS. Parceiro: ACE ENGENHARIA."
        ),
        "disciplines": [
            "Retrofit Reforma Hidráulica",
            "Projetos As-Built Hidrossanitários",
        ],
        "cover_image": "assets/img/portfolio/crops/crop-07-clube-bayer.webp",
        "gallery": [
            "assets/img/portfolio/crops/crop-07-clube-bayer.webp",
            "assets/img/portfolio/crops/crop-07b-clube-bayer-piscina.webp",
            "assets/img/portfolio/prancha-06-clube-bayer.webp",
        ],
        "board_image": "assets/img/portfolio/prancha-06-clube-bayer.webp",
    },
]

CLIENTS_DATA = [
    (1, "Atacadão", "varejo", "Varejo, Atacado & Shopping", "client-01-atacadao"),
    (2, "Bayer", "saude", "Saúde, Química & Farmácias", "client-02-bayer"),
    (3, "Enelpa Instalações", "engenharia", "Construtoras & Engenharia", "client-03-enelpa"),
    (4, "Toledo Ferrari Construtora e Incorporadora", "engenharia", "Construtoras & Engenharia", "client-04-toledo-ferrari"),
    (5, "Corpo de Bombeiros da PMESP", "publico", "Setor Público, Energia & Institucional", "client-05-bombeiros-pmesp"),
    (6, "Assaí Atacadista", "varejo", "Varejo, Atacado & Shopping", "client-06-assai"),
    (7, "Prefeitura de São Paulo — Subprefeitura Freguesia/Brasilândia", "publico", "Setor Público, Energia & Institucional", "client-07-prefeitura-sp"),
    (8, "Cambur Construtora e Incorporadora", "engenharia", "Construtoras & Engenharia", "client-08-cambur"),
    (9, "Drogaria São Paulo", "saude", "Saúde, Química & Farmácias", "client-09-drogaria-sp"),
    (10, "EverSun Energia", "publico", "Setor Público, Energia & Institucional", "client-10-eversun"),
    (11, "Helbor Incorporadora", "engenharia", "Construtoras & Engenharia", "client-11-helbor"),
    (12, "HH — Henrique & Henrique Engenharia", "engenharia", "Construtoras & Engenharia", "client-12-hh-engenharia"),
    (13, "Irmãs Hospitaleiras", "saude", "Saúde, Química & Farmácias", "client-13-irmas-hospitaleiras"),
    (14, "JRJ Engenharia", "engenharia", "Construtoras & Engenharia", "client-14-jrj-engenharia"),
    (15, "SBN — Sociedade Brasileira de Neurocirurgia", "saude", "Saúde, Química & Farmácias", "client-15-sbn-neurocirurgia"),
    (16, "Drogarias Pacheco", "saude", "Saúde, Química & Farmácias", "client-16-drogarias-pacheco"),
    (17, "Mutual Engenharia Inteligente", "engenharia", "Construtoras & Engenharia", "client-17-mutual-engenharia"),
    (18, "Farmácias Pague Menos", "saude", "Saúde, Química & Farmácias", "client-18-pague-menos"),
    (19, "Planem Engenharia", "engenharia", "Construtoras & Engenharia", "client-19-planem-engenharia"),
    (20, "Ragazzo!", "varejo", "Varejo, Atacado & Shopping", "client-20-ragazzo"),
    (21, "RMR Engenharia", "engenharia", "Construtoras & Engenharia", "client-21-rmr-engenharia"),
    (22, "Rock & Ribs Steakhouse", "varejo", "Varejo, Atacado & Shopping", "client-22-rock-and-ribs"),
    (23, "Projeto Pense Bem! — SBN / Ministério da Saúde", "publico", "Setor Público, Energia & Institucional", "client-23-pense-bem-sbn"),
    (24, "PCON Construtora", "engenharia", "Construtoras & Engenharia", "client-24-pcon-construtora"),
    (25, "All Brás Shopping", "varejo", "Varejo, Atacado & Shopping", "client-25-all-bras-shopping"),
    (26, "Shopping Vautier", "varejo", "Varejo, Atacado & Shopping", "client-26-shopping-vautier"),
    (27, "Zabo Engenharia", "engenharia", "Construtoras & Engenharia", "client-27-zabo-engenharia"),
    (28, "Enerwatt Engenharia", "engenharia", "Construtoras & Engenharia", "client-28-enerwatt-engenharia"),
    (29, "Corpo de Bombeiros — Viatura de Combate a Incêndio", "publico", "Setor Público, Energia & Institucional", "client-29-bombeiros-viatura"),
    (30, "TAEL Instalações", "publico", "Setor Público, Energia & Institucional", "client-30-tael"),
]


def init_and_seed_db(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        conn.execute(
            """
            INSERT OR REPLACE INTO company_profile (
                id, legal_name, brand_name, years_badge, headline, subheadline,
                essence_summary, mission, vision, values_json, differentials_json,
                technical_signature, normative_note, address, city_state,
                phone_display, whatsapp_url, email, instagram_handle, instagram_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                COMPANY_DATA["id"],
                COMPANY_DATA["legal_name"],
                COMPANY_DATA["brand_name"],
                COMPANY_DATA["years_badge"],
                COMPANY_DATA["headline"],
                COMPANY_DATA["subheadline"],
                COMPANY_DATA["essence_summary"],
                COMPANY_DATA["mission"],
                COMPANY_DATA["vision"],
                json.dumps(COMPANY_DATA["values"], ensure_ascii=False),
                json.dumps(COMPANY_DATA["differentials"], ensure_ascii=False),
                COMPANY_DATA["technical_signature"],
                COMPANY_DATA["normative_note"],
                COMPANY_DATA["address"],
                COMPANY_DATA["city_state"],
                COMPANY_DATA["phone_display"],
                COMPANY_DATA["whatsapp_url"],
                COMPANY_DATA["email"],
                COMPANY_DATA["instagram_handle"],
                COMPANY_DATA["instagram_url"],
            ),
        )

        for srv in SERVICES_DATA:
            conn.execute(
                """
                INSERT OR REPLACE INTO engineering_services (
                    id, division_slug, division_title, specialty_name, specialty_order, icon_name
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                srv,
            )

        for p in PORTFOLIO_DATA:
            conn.execute(
                """
                INSERT OR REPLACE INTO portfolio_projects (
                    id, slug, display_order, title, location, category_slug, category_label,
                    partner_name, area_or_scale, official_description, disciplines_json,
                    cover_image, gallery_json, board_image
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    p["id"],
                    p["slug"],
                    p["display_order"],
                    p["title"],
                    p["location"],
                    p["category_slug"],
                    p["category_label"],
                    p["partner_name"],
                    p["area_or_scale"],
                    p["official_description"],
                    json.dumps(p["disciplines"], ensure_ascii=False),
                    p["cover_image"],
                    json.dumps(p["gallery"], ensure_ascii=False),
                    p["board_image"],
                ),
            )

        for c_id, c_name, c_sector, c_label, c_file in CLIENTS_DATA:
            conn.execute(
                """
                INSERT OR REPLACE INTO official_clients (
                    id, name, sector_slug, sector_label, logo_webp, logo_png
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    c_id,
                    c_name,
                    c_sector,
                    c_label,
                    f"assets/img/clients/{c_file}.webp",
                    f"assets/img/clients/{c_file}.png",
                ),
            )
        conn.commit()


if __name__ == "__main__":
    init_and_seed_db()
    print(f"[OK] Banco SQLite inicializado e populado em: {DB_PATH}")
