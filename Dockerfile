# ใช้ Python Image ที่มีขนาดเล็กและปลอดภัย
FROM python:3.9-slim-buster

# กำหนด Working Directory ใน Container
WORKDIR /app

# ป้องกันไม่ให้ Python เขียนไฟล์ .pyc และให้ Output แสดงผลทันที (Real-time log)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอก Code ทั้งหมดเข้า Container
COPY . .

# ใช้ Gunicorn แทน Flask Development Server เพื่อความปลอดภัยและประสิทธิภาพ (Production ready)
RUN pip install gunicorn

# สั่งรันแอป โดยใช้ Port 5000 (หรือตามที่ Vercel/Cloud กำหนด)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]