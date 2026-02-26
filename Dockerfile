# 1. Use a lightweight Python version
FROM python:3.11-slim

# 2. Set the directory inside the container
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the model folder and the API code
COPY ./model_final ./model_final
COPY app.py .

# 5. Open the port FastAPI runs on
EXPOSE 8000

# 6. Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]