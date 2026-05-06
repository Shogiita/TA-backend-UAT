# Menggunakan image Python yang ringan
FROM python:3.11-slim

# Menentukan direktori kerja di dalam container
WORKDIR /workspace

# Menyalin file requirements dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode sumber ke dalam container
COPY . .

# Mengekspos port 8080 sesuai standar Cloud Run
EXPOSE 8080

# Menjalankan server FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]