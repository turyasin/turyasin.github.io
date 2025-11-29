FROM python:3.11-slim

WORKDIR /app

# Copy the entire backend directory contents to /app
COPY backend/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
