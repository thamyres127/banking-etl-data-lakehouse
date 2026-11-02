import sqlite3
from datetime import datetime

DB_NAME = "lakehouse.db"

def rodar_relatorios_auditoria():
    """
    Executa queries analíticas simulando as consultas que um time de auditoria,
    compliance ou engenharia de dados faria no Lakehouse bancário.
    """
    print(f"[{datetime.now()}] Iniciando extração de relatórios analíticos de dados...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Query 1: Volumetria geral por camada do Lakehouse
        print("\n=== 1. VOLUMETRIA DE DADOS POR CAMADA ===")
        cursor.execute("SELECT COUNT(*) FROM camada_bronze")
        total_bronze = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM camada_silver")
        total_silver = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM logs_erro_dlq")
        total_dlq = cursor.fetchone()[0]
        
        print(f"Total de registros originais (Bronze): {total_bronze}")
        print(f"Total de registros limpos e aprovados (Silver): {total_silver}")
        print(f"Total de anomalias isoladas (Dead Letter Queue): {total_dlq}")
        
        # Query 2: Métrica de Qualidade de Dados (Data Quality Score)
        print("\n=== 2. ÍNDICE DE QUALIDADE DE DADOS DO LEGADO ===")
        if total_bronze > 0:
            taxa_sucesso = (total_silver / total_bronze) * 100
            taxa_erro = (total_dlq / total_bronze) * 100
            print(f"Aproveitamento dos dados legados: {taxa_sucesso:.2f}%")
            print(f"Taxa de corrupção/Erros de layout: {taxa_erro:.2f}%")
        else:
            print("Nenhum dado processado na base para calcular indicadores.")
            
        # Query 3: Amostra analítica da Camada Silver para inspeção
        print("\n=== 3. AMOSTRA DE AUDITORIA (CAMADA SILVER) ===")
        cursor.execute("SELECT transacao_id, cpf_validado, valor, status FROM camada_silver LIMIT 5")
        rows_silver = cursor.fetchall()
        for row in rows_silver:
            print(f"ID: {row[0]} | CPF Higienizado: {row[1]} | Valor: R${row[2]:.2f} | Status: {row[3]}")
            
    except sqlite3.OperationalError:
        print("\n[AVISO] As tabelas do banco ainda não foram povoadas ou criadas.")
        print("Certifique-se de executar o arquivo 'main.py' ou 'processador_batch.py' antes para gerar a base local.")
    finally:
        conn.close()

if __name__ == "__main__":
    rodar_relatorios_auditoria()
