FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN npx prisma generate
EXPOSE 8000
CMD ["bash", "-lc", "npx prisma migrate deploy && gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --access-logfile - --error-logfile -"]
