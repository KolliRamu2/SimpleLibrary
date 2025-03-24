# builder stage 
FROM python:3.11-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# runner stage
FROM python:3.11-alpine AS runner
ENV  DATABASE_URL=postgresql://user:password@localhost:5432/library
USER nobody
COPY --chown=nobody --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=nobody --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --chown=nobody /api/models.py /db/main.py /app
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

