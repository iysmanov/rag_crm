FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx tesseract-ocr && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"] 