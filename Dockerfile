# img python
FROM python:3.11-slim

# dir
WORKDIR /app

# copia arquivos pra dentro da img
COPY . .

# dependências do requirements.txt instalada
RUN pip install --no-cache-dir -r requirements.txt

# mostra a porta que o flask usa
EXPOSE 5000

# cmd que roda o app
CMD ["python", "main.py"]
