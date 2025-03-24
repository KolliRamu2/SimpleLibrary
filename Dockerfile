# Stage:1 Build Stage 
FROM python:3.11-alpine AS builder
# Set environment variables to avoid Python writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#Install runtime dependencies, including PostgreSQL client libraries
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev postgresql-dev
# Choose Workdir
WORKDIR /app
# Copy the requiremens.txt to install dependencies
COPY requirements.txt .
# Install the application dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Stage:2 Run Stage
FROM python:3.11-alpine AS runner
# Set environment variables to avoid Python writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# set enviornment variable connection string to connect with database
ENV  DATABASE_URL=postgresql://user:password@localhost:5432/library
USER nobody
# Install runtime dependencies, including PostgreSQL client libraries
RUN apk add --no-cache libpq
# Copy installed dependencies from the builder stage
COPY --chown=nobody --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=nobody --from=builder /usr/local/bin /usr/local/bin
# Copy the application source code to the working directory
COPY --chown=nobody . /app
WORKDIR /app
# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

