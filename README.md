# Banking ETL & Data Lakehouse Architecture

Este repositório contém uma solução completa (Full-Stack) voltada para o setor bancário, focando em engenharia de software e processamento de dados legados de alta performance. O sistema simula a ingestão assíncrona de transações financeiras, higienização de dados em lote, desvio de anomalias (DLQ) e auditoria de governança.

## 🛠️ Arquitetura do Ecossistema
* **`main.py` (Back-end Assíncrono):** Desenvolvido em Python com FastAPI para expor endpoints rápidos de ingestão de dados.
* **Higienização Baseada em Regras:** Validação extrema e limpeza de CPFs corrompidos vindos de logs do legado utilizando expressões regulares.
* **Resiliência e Observabilidade (DLQ):** Desvio de falhas críticas de layout para logs isolados (Dead Letter Queue), garantindo auditoria sem interromper os serviços.
* **Arquitetura Lakehouse:** Persistência relacional simulando a separação física de camadas (Bronze para dados brutos originais e Silver para dados tratados).
* **`index.html` (Painel Analítico Front-end):** Dashboard construído com HTML5, CSS3 e JavaScript Vanilla integrado diretamente via Fetch API assíncrona para expor relatórios de conformidade em tempo real.
* **`test_pipeline.py`:** Gerador automatizado de dados em lote no formato CSV para simulação de cenários complexos do mundo real.
* **`analise_auditoria.py`:** Script analítico de métricas SQL para checagem de volumetria e integridade dos dados locais.

## 📦 Dependências e Infraestrutura
* **Linguagens e Ferramentas:** Python, SQL, JavaScript (Vanilla), HTML5, CSS3 e Docker.
* **Framework Back-end:** FastAPI, Uvicorn, Pydantic (mapeados em `requirements.txt`).
* **Banco de Dados:** SQLite nativo para persistência local veloz.

## 🚀 Como Executar a Aplicação
1. Instale as dependências: `pip install -r requirements.txt`
2. Suba o servidor de desenvolvimento: `uvicorn main:app --reload`
3. Abra o arquivo `index.html` diretamente no seu navegador para visualizar o painel integrado à API operacional.
