FROM python:3.11-slim

WORKDIR /app

# Step 1: Copy ONLY requirements
COPY requirements.txt .

# Step 2: Install dependencies (cached if requirements.txt unchanged)
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Now copy your code
COPY . .

ENV PYTHONPATH="/app/src"


EXPOSE 8000

# This is the key change:
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "/app/src"]