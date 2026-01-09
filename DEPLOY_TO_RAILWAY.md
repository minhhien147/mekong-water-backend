# 🚂 Deploy Backend lên Railway.app (Miễn phí)

Railway là nền tảng dễ nhất để deploy Python backend!

## 📋 Yêu cầu

- GitHub account (miễn phí)
- Railway account (miễn phí tại https://railway.app)

---

## 🚀 BƯỚC 1: Chuẩn bị Code

### 1.1. Tạo file `Procfile` (cho Railway biết cách chạy app)

```bash
cd backend-python
```

Tạo file `Procfile`:
```
web: python app.py
```

### 1.2. Tạo file `runtime.txt` (chỉ định Python version)

```
python-3.11.0
```

### 1.3. Tạo file `.railwayignore` (giống .gitignore)

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
*.log
data/
logs/
```

---

## 🚀 BƯỚC 2: Push code lên GitHub

### 2.1. Khởi tạo Git (nếu chưa có)

```bash
cd E:\fpt-guard-v2\backend-python
git init
git add .
git commit -m "Initial commit - Mekong Water Level API"
```

### 2.2. Tạo repo trên GitHub

1. Vào https://github.com/new
2. Tạo repo mới (ví dụ: `mekong-water-backend`)
3. **KHÔNG** check "Initialize with README"

### 2.3. Push code

```bash
git remote add origin https://github.com/YOUR_USERNAME/mekong-water-backend.git
git branch -M main
git push -u origin main
```

---

## 🚀 BƯỚC 3: Deploy lên Railway

### 3.1. Đăng ký Railway

1. Vào https://railway.app
2. Click "Start a New Project"
3. Đăng nhập bằng GitHub

### 3.2. Tạo Project mới

1. Click "New Project"
2. Chọn "Deploy from GitHub repo"
3. Chọn repo `mekong-water-backend`
4. Railway tự động detect Python và deploy!

### 3.3. Cấu hình Environment Variables (nếu cần)

1. Vào tab "Variables"
2. Thêm các biến nếu cần:
   ```
   API_PORT=5000
   API_HOST=0.0.0.0
   ```

### 3.4. Lấy URL

1. Vào tab "Settings"
2. Click "Generate Domain"
3. Copy URL (ví dụ: `https://mekong-water-backend-production.up.railway.app`)

---

## 🚀 BƯỚC 4: Cập nhật Flutter App

### 4.1. Cập nhật baseUrl

```dart
// lib/services/water_level_service.dart
static const String baseUrl = 'https://mekong-water-backend-production.up.railway.app/api';
```

### 4.2. Test kết nối

```bash
curl https://mekong-water-backend-production.up.railway.app/api/health
```

---

## ✅ HOÀN TẤT!

Backend giờ đã chạy 24/7 trên Railway!

**Lưu ý:**
- Railway free tier có giới hạn usage
- Nếu hết free tier, có thể upgrade hoặc chuyển sang Render.com

---

## 🔄 Update Code

Mỗi khi push code mới lên GitHub:
```bash
git add .
git commit -m "Update code"
git push
```

Railway tự động deploy lại!

---

## 🐛 Troubleshooting

### Lỗi: Build failed

- Kiểm tra `Procfile` đúng format
- Kiểm tra `requirements.txt` có đầy đủ
- Xem logs trong Railway dashboard

### Lỗi: App không start

- Kiểm tra port: Railway tự động set `PORT` env variable
- Cập nhật `app.py` để dùng `os.environ.get('PORT', 5000)`

### Lỗi: Selenium không chạy

- Railway không hỗ trợ Chrome headless tốt
- Có thể cần dùng Selenium Grid hoặc chuyển sang API khác

---

**Railway là cách dễ nhất! 🚂✨**

