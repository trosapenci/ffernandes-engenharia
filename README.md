# FFernandes Engenharia e Construção Ltda. — Full-Stack Web & API (`06_FFernandes_Engenharia`)

Aplicação Web Full-Stack (Frontend + Backend REST API v1 + SQLite WAL + Docker) construída exclusivamente com **100% dos dados reais e identidade visual oficial** absorvidos de `https://ffernandes.eng.br` e `https://ffernandes.eng.br/portfolio`.

---

## 1. Destaques da Arquitetura

- **Fidelidade Absoluta de Dados (Zero Invenção):**
  - **Identidade Institucional:** Missão, Visão, Valores e os 4 Diferenciais Competitivos transcritos palavra por palavra para HTML5 semântico e acessível, mantendo visualização opcional dos painéis originais em alta resolução.
  - **8 Especialidades de Engenharia:** *Instalações Elétricas* (Energia e Potência, Infraestrutura para Sistemas, SPDA, Quadros e Bombas) e *Instalações Hidráulicas* (Água Potável e Reservatórios, Esgoto e Pluviais, Gás GLP, Combate a Incêndio).
  - **Portfólio Interativo com as 7 Obras Reais:**
    1. *Condomínio TRIO — Alto de Pinheiros (São Paulo/SP)*
    2. *Heineken Campus (Heineken House) — Parque Villa-Lobos (São Paulo/SP)* (Parceria: `RMR Engenharia` e `DC Set`)
    3. *Data Center — Município de Paulínia (SP)* (Parceria: `Enerwatt Engenharia`)
    4. *Shopping Vautier Premium (São Paulo/SP)* (Retrofit 26 novas lojas)
    5. *Shopping All Brás (São Paulo/SP)* (Retrofit 316 novas bancas e 9 boxes)
    6. *Simba Safari (São Paulo/SP)* (7 disciplinas em parceria com `Planem Engenharia`)
    7. *Clube Bayer Santo Amaro (São Paulo/SP)* (Retrofit Hidráulico 1.200m² & As-Built em parceria com `ACE Engenharia`)
  - **Matriz Filtrável dos 30 Clientes e Parceiros Oficiais:** Logotipos otimizados em `.webp` categorizados por setor (*Construtoras & Engenharia*, *Varejo, Atacado & Shopping*, *Saúde, Química & Farmácias*, *Setor Público, Energia & Institucional*), **sem uso de faixas contínuas (`marquee`)**.

---

## 2. Como Executar

### Opção A — Servidor Python Nativo (Sem Dependências Externas)
```bash
python3 backend/server.py
```
Acesse em: `http://localhost:8090`

### Opção B — Docker & Docker Compose
```bash
docker compose up -d --build
```
Acesse em: `http://localhost:8090`

---

## 3. Endpoints da API REST (`v1`)

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Healthcheck da aplicação, status do SQLite e contadores do acervo |
| `GET` | `/api/v1/company` | Dados institucionais oficiais (Missão, Visão, Valores, Diferenciais, Contatos) |
| `GET` | `/api/v1/services` | Lista das 8 especialidades (`?division=eletrica` ou `hidraulica`) |
| `GET` | `/api/v1/portfolio` | Lista das 7 obras reais (`?category=residencial\|corporativo\|infraestrutura\|shopping\|complexos`) |
| `GET` | `/api/v1/clients` | Lista dos 30 clientes oficiais (`?sector=engenharia\|varejo\|saude\|publico`) |
| `POST` | `/api/v1/leads` | Registro de solicitação de orçamento com suporte a `Idempotency-Key` e validação RFC 7807 |
