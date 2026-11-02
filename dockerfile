# Usa uma imagem oficial leve do Python corporativo
FROM python:3.11-slim

# Define o diretório interno de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código do seu repositório para dentro do contêiner
COPY main.py .
COPY test_pipeline.py .
COPY analise_auditoria.py .

# Instala as dependências de alta performance que validamos antes
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Expõe a porta padrão que a API do FastAPI utiliza
EXPOSE 8000

# Comando padrão para iniciar o servidor assíncrono ao subir o contêiner
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
