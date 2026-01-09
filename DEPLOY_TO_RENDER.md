# 🎨 Deploy Backend lên Render.com (Miễn phí)

Render.com là nền tảng tốt cho Python apps!

## 📋 Yêu cầu

- GitHub account
- Render account (miễn phí tại https://render.com)

---

## 🚀 BƯỚC 1: Chuẩn bị Code

### 1.1. Tạo file `render.yaml` (optional, để tự động deploy)

```yaml
services:
  - type: web
    name: mekong-water-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: API_PORT
        value: 5000
      - key: API_HOST
        value: 0.0.0.0
```

### 1.2. Đảm bảo có `requirements.txt`

Đã có sẵn! ✅

---

## 🚀 BƯỚC 2: Push code lên GitHub

(Tương tự như Railway)

```bash
cd E:\fpt-guard-v2\backend-python
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mekong-water-backend.git
git push -u origin main
```

---

## 🚀 BƯỚC 3: Deploy lên Render

### 3.1. Đăng ký Render

1. Vào https://render.com
2. Click "Get Started for Free"
3. Đăng nhập bằng GitHub

### 3.2. Tạo Web Service

1. Dashboard → "New +" → "Web Service"
2. Connect GitHub repo `mekong-water-backend`
3. Cấu hình:
   - **Name**: `mekong-water-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

### 3.3. Environment Variables

Trong "Environment" tab, thêm:
```
API_PORT=5000
API_HOST=0.0.0.0
```

### 3.4. Deploy

1. Click "Create Web Service"
2. Render tự động build và deploy
3. Đợi 5-10 phút
4. Lấy URL (ví dụ: `https://mekong-water-api.onrender.com`)

---

## 🚀 BƯỚC 4: Cập nhật Flutter

```dart
// lib/services/water_level_service.dart
static const String baseUrl = 'https://mekong-water-api.onrender.com/api';
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Render Free Tier:

- **Sleep sau 15 phút không dùng** → Lần request đầu sẽ chậm (~30s)
- **Giới hạn 750 giờ/tháng**
- **Không phù hợp cho production**

### Giải pháp:

1. **Dùng Render Paid** ($7/tháng) - Không sleep
2. **Hoặc dùng Railway** - Tốt hơn cho free tier
3. **Hoặc setup cron job** để ping mỗi 10 phút (giữ app không sleep)

---

## 🔄 Keep-Alive Script

Tạo file `keep_alive.py` để ping app mỗi 10 phút:

```python
import requests
import time
import schedule

def ping_app():
    try:
        response = requests.get('https://mekong-water-api.onrender.com/api/health', timeout=10)
        print(f"✅ Pinged: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Chạy mỗi 10 phút
schedule.every(10).minutes.do(ping_app)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Chạy trên máy tính hoặc VPS khác.

---

## ✅ HOÀN TẤT!

Backend đã deploy lên Render!

**Tip:** Render tốt cho test, nhưng Railway tốt hơn cho production (free tier).

---

**Render.com - Dễ dùng nhưng có giới hạn! 🎨**

