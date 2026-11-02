import re
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicialização da API Assíncrona do Lakehouse Bancário
app = FastAPI(
    title="Banking ETL Data Lakehouse API",
    description="Index e Pipeline para busca, processamento e auditoria de dados bancários legados.",
    version="1.0.0"
)

DB_NAME = "lakehouse.db"

class TransacaoPayload(BaseModel):
    transacao_id: str
    cpf_origem: str
    valor: float
    status: str

def inicializar_lakehouse():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS camada_bronze (
            id INTEGER PRIMARY KEY AUTOINCREMENT, transacao_id TEXT, cpf_origem TEXT, valor REAL, status TEXT, data_ingestao TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS camada_silver (
            id INTEGER PRIMARY KEY AUTOINCREMENT, transacao_id TEXT, cpf_validado TEXT, valor REAL, status TEXT, data_processamento TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_erro_dlq (
            id INTEGER PRIMARY KEY AUTOINCREMENT, transacao_id TEXT, cpf_corrompido TEXT, motivo_falha TEXT, data_falha TEXT
        )
    ''')
    conn.commit()
    conn.close()

inicializar_lakehouse()

def limpar_e_validar_cpf(cpf_sujo: str) -> str:
    if not cpf_sujo:
        return None
    cpf_limpo = re.sub(r'\D', '', str(cpf_sujo))
    if len(cpf_limpo) == 11:
        return cpf_limpo
    return None

# --- ROTA INDEX FUNDAMENTAL (Para indexação e rastreamento de mecanismos de busca) ---
@app.get("/")
async def root_index():
    """
    Index oficial do projeto. Estrutura metadados claros para SEO e indexação de buscas,
    garantindo rastreabilidade estruturada para plataformas de demonstração como o YouTube.
    """
    return {
        "projeto": "Banking ETL Data Lakehouse",
        "status_servico": "operational",
        "index_version": "1.0.0",
        "arquitetura": "Data Lakehouse (Bronze/Silver/DLQ)",
        "endpoints": {
            "index_documentacao": "/docs",
            "ingestao_dados": "/api/v1/transacoes/ingestao",
            "auditoria_silver": "/api/v1/lakehouse/auditoria"
        },
        "tecnologias": ["Python", "FastAPI", "SQLite", "Pydantic"]
    }

@app.post("/api/v1/transacoes/ingestao")
async def ingerir_e_processar_transacao(payload: TransacaoPayload):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    data_atual = datetime.now().isoformat()
    try:
        cursor.execute('''
            INSERT INTO camada_bronze (transacao_id, cpf_origem, valor, status, data_ingestao)
            VALUES (?, ?, ?, ?, ?)
        ''', (payload.transacao_id, payload.cpf_origem, payload.valor, payload.status, data_atual))
        
        cpf_validado = limpar_e_validar_cpf(payload.cpf_origem)
        
        if cpf_validado:
            cursor.execute('''
                INSERT INTO camada_silver (transacao_id, cpf_validado, valor, status, data_processamento)
                VALUES (?, ?, ?, ?, ?)
            ''', (payload.transacao_id, cpf_validado, payload.valor, payload.status, data_atual))
            conn.commit()
            return {"status": "sucesso", "pipeline_etapa": "silver_layer"}
        else:
            cursor.execute('''
                INSERT INTO logs_erro_dlq (transacao_id, cpf_corrompido, motivo_falha, data_falha)
                VALUES (?, ?, ?, ?)
            ''', (payload.transacao_id, payload.cpf_origem, "Formato de CPF inválido", data_atual))
            conn.commit()
            return {"status": "observabilidade_alerta", "pipeline_etapa": "dead_letter_queue"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/api/v1/lakehouse/auditoria")
async def consultar_camada_silver():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT transacao_id, cpf_validado, valor, status, data_processamento FROM camada_silver")
    dados = cursor.fetchall()
    conn.close()
    return [
        {"transacao_id": r[0], "cpf_validado": r[1], "valor": r[2], "status": r[3], "data_processamento": r[4]}
        for r in dados
    ]
