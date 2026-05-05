# ใช้ Python แบบ slim เพื่อลดขนาด Image
FROM python:3.9-slim

# ตั้งค่า Working Directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt เข้าไปก่อนเพื่อทำ Layer Caching
# (สร้างไฟล์ requirements.txt ด้วยนะครับ)
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้า Container
COPY . .

# กำหนด Port (Vercel หรือ Cloud Platform มักใช้ 8080 หรือ 5000)
EXPOSE 5000

# ใช้ Gunicorn แทน app.run() เพื่อความเสถียรใน Production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
