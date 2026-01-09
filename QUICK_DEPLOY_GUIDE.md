# ⚡ Hướng dẫn Deploy Nhanh - 3 Phương án

## 🎯 Chọn phương án phù hợp

| Nền tảng | Độ khó | Free Tier | Sleep? | Tốt cho |
|----------|--------|-----------|--------|---------|
| **Railway** | ⭐ Dễ | ✅ Tốt | ❌ Không | Production |
| **Render** | ⭐ Dễ | ⚠️ Có giới hạn | ✅ Có (15 phút) | Test/Dev |
| **Heroku** | ⭐⭐ Trung bình | ⚠️ Giới hạn | ✅ Có | Production |

---

## 🚂 PHƯƠNG ÁN 1: Railway (KHUYẾN NGHỊ) ⭐

### ✅ Ưu điểm:
- Dễ nhất
- Free tier tốt
- Không sleep
- Auto-deploy từ GitHub

### 📝 Các bước:

1. **Tạo file `Procfile`:**
```
web: python app.py
```

2. **Push lên GitHub:**
```bash
cd backend-python
git init
git add .
git commit -m "Deploy to Railway"
git remote add origin https://github.com/YOUR_USERNAME/mekong-backend.git
git push -u origin main
```

3. **Deploy trên Railway:**
   - Vào https://railway.app
   - New Project → Deploy from GitHub
   - Chọn repo → Done!

4. **Lấy URL và cập nhật Flutter:**
```dart
static const String baseUrl = 'https://your-app.railway.app/api';
```

**⏱️ Thời gian: ~10 phút**

---

## 🎨 PHƯƠNG ÁN 2: Render.com

### ✅ Ưu điểm:
- Dễ setup
- Free tier

### ⚠️ Nhược điểm:
- Sleep sau 15 phút
- Lần request đầu chậm

### 📝 Các bước:

1. **Push lên GitHub** (giống Railway)

2. **Deploy trên Render:**
   - Vào https://render.com
   - New → Web Service
   - Connect GitHub repo
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`

3. **Cập nhật Flutter:**
```dart
static const String baseUrl = 'https://your-app.onrender.com/api';
```

**⏱️ Thời gian: ~15 phút**

---

## 🟣 PHƯƠNG ÁN 3: Heroku

### ✅ Ưu điểm:
- Ổn định
- Nhiều add-ons

### ⚠️ Nhược điểm:
- Cần Heroku CLI
- Free tier giới hạn

### 📝 Các bước:

1. **Cài Heroku CLI:**
   - Download: https://devcenter.heroku.com/articles/heroku-cli

2. **Tạo file `Procfile`:**
```
web: python app.py
```

3. **Login và deploy:**
```bash
heroku login
cd backend-python
heroku create mekong-water-api
git push heroku main
```

4. **Cập nhật Flutter:**
```dart
static const String baseUrl = 'https://mekong-water-api.herokuapp.com/api';
```

**⏱️ Thời gian: ~20 phút**

---

## 🔧 CHUẨN BỊ CODE (Cho tất cả)

### File cần có:

1. **`Procfile`** (cho Railway/Heroku):
```
web: python app.py
```

2. **`runtime.txt`** (optional):
```
python-3.11.0
```

3. **`.gitignore`** (đã có):
```
__pycache__/
*.pyc
venv/
data/
logs/
.env
```

4. **`requirements.txt`** (đã có) ✅

---

## 📱 CẬP NHẬT FLUTTER

Sau khi deploy, cập nhật:

```dart
// lib/services/water_level_service.dart

// Railway
static const String baseUrl = 'https://your-app.railway.app/api';

// Render
static const String baseUrl = 'https://your-app.onrender.com/api';

// Heroku
static const String baseUrl = 'https://your-app.herokuapp.com/api';
```

---

## ✅ CHECKLIST

- [ ] Tạo `Procfile`
- [ ] Push code lên GitHub
- [ ] Deploy lên cloud platform
- [ ] Test API: `curl https://your-app.com/api/health`
- [ ] Cập nhật baseUrl trong Flutter
- [ ] Build APK: `flutter build apk --release`
- [ ] Test APK trên thiết bị

---

## 🎯 KHUYẾN NGHỊ

**Cho Production:**
→ **Railway** (dễ nhất, free tier tốt)

**Cho Test/Development:**
→ **Render** (nhanh, nhưng có sleep)

**Cho Enterprise:**
→ **Heroku** hoặc **AWS**

---

## 🐛 TROUBLESHOOTING

### Build failed?

- Kiểm tra `requirements.txt` đầy đủ
- Kiểm tra Python version
- Xem logs trong dashboard

### App không start?

- Kiểm tra `Procfile` đúng format
- Kiểm tra port (dùng env variable `PORT`)
- Xem logs

### Selenium không chạy?

- Cloud platforms không hỗ trợ Chrome tốt
- Cần dùng Selenium Grid hoặc API khác

---

## 💡 TIP: Dùng Environment Variable

Thay vì hardcode URL, dùng env:

```dart
// lib/services/water_level_service.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

static String get baseUrl {
  return dotenv.env['API_BASE_URL'] ?? 
         'http://10.0.2.2:5000/api'; // fallback
}
```

```env
# .env
API_BASE_URL=https://your-app.railway.app/api
```

Build APK:
```bash
flutter build apk --release --dart-define=API_BASE_URL=https://your-app.railway.app/api
```

---

**Chọn Railway cho dễ nhất! 🚂✨**

