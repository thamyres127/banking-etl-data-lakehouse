import csv
import random
from datetime import datetime

def gerar_massa_dados_bancarios(filename="transacoes_legado.csv", qtd_registros=100):
    """
    Gera um arquivo CSV simulando um lote de dados brutos e corrompidos de um sistema legado.
    Contém CPFs válidos, CPFs desformatados e CPFs completamente inválidos para testar a DLQ.
    """
    cpfs_base = ["12345678900", "98765432199", "45678912311", "32165498722"]
    formatos_sujos = [
        lambda c: f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}", # Formato correto com pontos
        lambda c: c,                                    # Apenas números
        lambda c: f"  {c[:3]} {c[3:6]} {c[6:9]} {c[9:]} ", # Com espaços extras
        lambda c: "CPF_CORROMPIDO_INVALIDO",             # Falha crítica de string
        lambda c: f"{c}/11"                             # Formato misturado com barra
    ]
    
    status_opcoes = ["COMPLETED", "PENDING", "FAILED"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Cabeçalho do arquivo bruto (Camada Bronze)
        writer.writerow(["transacao_id", "cpf_origem", "valor", "status"])
        
        for i in range(1, qtd_registros + 1):
            txn_id = f"TXN-LEGACY-{1000 + i}"
            cpf_escolhido = random.choice(cpfs_base)
            formatador = random.choice(formatos_sujos)
            cpf_final = formatador(cpf_escolhido)
            valor = round(random.uniform(10.0, 5000.0), 2)
            status = random.choice(status_opcoes)
            
            writer.writerow([txn_id, cpf_final, valor, status])
            
    print(f"[{datetime.now()}] Sucesso! Arquivo '{filename}' gerado com {qtd_registros} transações simuladas.")

if __name__ == "__main__":
    gerar_massa_dados_bancarios()
