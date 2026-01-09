# 🚀 BẮT ĐẦU DEPLOY - Đọc file này trước!

## 📋 TÓM TẮT

Bạn có **3 phương án** để deploy backend lên cloud:

1. **Railway** ⭐ (Khuyến nghị - Dễ nhất)
2. **Render** (Dễ nhưng có sleep)
3. **Heroku** (Ổn định nhưng cần CLI)

---

## ⚡ QUICK START - Railway (5 phút)

### Bước 1: Tạo GitHub repo

```bash
cd E:\fpt-guard-v2\backend-python

# Khởi tạo git (nếu chưa có)
git init
git add .
git commit -m "Ready for deployment"

# Tạo repo trên GitHub (vào https://github.com/new)
# Sau đó:
git remote add origin https://github.com/YOUR_USERNAME/mekong-backend.git
git branch -M main
git push -u origin main
```

### Bước 2: Deploy trên Railway

1. Vào https://railway.app
2. Đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repo `mekong-backend`
5. Railway tự động deploy! ⚡

### Bước 3: Lấy URL

1. Vào tab "Settings"
2. Click "Generate Domain"
3. Copy URL (ví dụ: `https://mekong-backend-production.up.railway.app`)

### Bước 4: Cập nhật Flutter

```dart
// lib/services/water_level_service.dart
static const String baseUrl = 'https://mekong-backend-production.up.railway.app/api';
```

### Bước 5: Test

```bash
curl https://mekong-backend-production.up.railway.app/api/health
```

---

## 📚 HƯỚNG DẪN CHI TIẾT

- **Railway**: Xem `DEPLOY_TO_RAILWAY.md`
- **Render**: Xem `DEPLOY_TO_RENDER.md`
- **Tất cả**: Xem `QUICK_DEPLOY_GUIDE.md`
- **Tổng quan**: Xem `DEPLOYMENT_OPTIONS.md`

---

## ✅ FILES ĐÃ SẴN SÀNG

Các file cần thiết đã được tạo:

- ✅ `Procfile` - Cho Railway/Heroku
- ✅ `runtime.txt` - Python version
- ✅ `.railwayignore` - Ignore files
- ✅ `requirements.txt` - Dependencies
- ✅ `app.py` - Đã cập nhật hỗ trợ PORT env

---

## 🎯 KHUYẾN NGHỊ

**Cho lần đầu deploy:**
→ Dùng **Railway** (dễ nhất, free tier tốt)

**Sau khi deploy xong:**
1. Test API endpoint
2. Cập nhật baseUrl trong Flutter
3. Build APK: `flutter build apk --release`
4. Test APK trên thiết bị

---

## 🐛 VẤN ĐỀ THƯỜNG GẶP

### Selenium không chạy trên cloud?

**Vấn đề:** Cloud platforms không hỗ trợ Chrome headless tốt.

**Giải pháp:**
1. Dùng dữ liệu mẫu (đã có sẵn)
2. Hoặc dùng Selenium Grid
3. Hoặc chuyển sang API khác (NOAA, Stormglass)

### App sleep sau 15 phút (Render)?

**Giải pháp:**
- Dùng Railway (không sleep)
- Hoặc setup keep-alive script

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Xem logs trong dashboard
2. Kiểm tra `Procfile` đúng format
3. Kiểm tra `requirements.txt` đầy đủ
4. Test local trước khi deploy

---

**Bắt đầu với Railway - Dễ nhất! 🚂✨**

