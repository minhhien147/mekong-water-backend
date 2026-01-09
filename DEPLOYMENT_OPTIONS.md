# 🚀 Các Phương án Deploy Backend cho APK

## ❓ Vấn đề

Khi bạn build APK và cài trên thiết bị khác, **backend Python PHẢI chạy thủ công** vì:
- APK chỉ chứa Flutter app
- Backend Python là service riêng biệt
- APK cần kết nối tới backend qua network

---

## ✅ GIẢI PHÁP

### Option 1: Deploy lên Cloud (KHUYẾN NGHỊ) ⭐

**Ưu điểm:**
- ✅ Backend tự động chạy 24/7
- ✅ Không cần máy tính của bạn
- ✅ Thiết bị nào cũng truy cập được
- ✅ Có domain/IP cố định

**Các nền tảng:**

#### A. Heroku (Miễn phí tier)
```bash
# 1. Cài Heroku CLI
# 2. Login
heroku login

# 3. Tạo app
cd backend-python
heroku create mekong-water-api

# 4. Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# 5. Backend tự động chạy tại: https://mekong-water-api.herokuapp.com
```

#### B. Railway.app (Dễ dùng)
```bash
# 1. Đăng ký tại railway.app
# 2. Tạo project mới
# 3. Connect GitHub repo
# 4. Deploy tự động
# 5. Backend chạy tại: https://your-app.railway.app
```

#### C. Render.com (Miễn phí)
```bash
# 1. Đăng ký tại render.com
# 2. Tạo Web Service
# 3. Connect GitHub
# 4. Build command: pip install -r requirements.txt
# 5. Start command: python app.py
```

#### D. PythonAnywhere (Miễn phí)
```bash
# 1. Đăng ký tại pythonanywhere.com
# 2. Upload code
# 3. Cấu hình WSGI
# 4. Backend chạy tại: your-username.pythonanywhere.com
```

**Sau khi deploy, cập nhật baseUrl trong Flutter:**
```dart
// lib/services/water_level_service.dart
static const String baseUrl = 'https://your-backend-url.com/api';
```

---

### Option 2: Chạy trên Server riêng

**Ưu điểm:**
- ✅ Full control
- ✅ Performance tốt
- ✅ Không giới hạn

**Cách làm:**
```bash
# 1. Mua VPS (DigitalOcean, AWS EC2, etc.)
# 2. SSH vào server
# 3. Cài Python, dependencies
# 4. Chạy với systemd service (tự động khởi động)
# 5. Cấu hình firewall
```

**Tạo systemd service (Linux):**
```bash
# /etc/systemd/system/mekong-water.service
[Unit]
Description=Mekong Water Level API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/backend-python
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable mekong-water
sudo systemctl start mekong-water
```

---

### Option 3: Chạy trên máy tính + Share IP

**Ưu điểm:**
- ✅ Không tốn tiền
- ✅ Dễ test

**Nhược điểm:**
- ❌ Phải bật máy tính 24/7
- ❌ IP có thể thay đổi
- ❌ Cần cấu hình router/firewall

**Cách làm:**

1. **Lấy IP máy tính:**
```bash
# Windows
ipconfig
# Tìm IPv4 Address, ví dụ: 192.168.1.100

# Linux/Mac
ifconfig
# Tìm inet, ví dụ: 192.168.1.100
```

2. **Cấu hình backend chạy trên tất cả IP:**
```python
# backend-python/config.py
API_HOST = "0.0.0.0"  # Đã có sẵn
API_PORT = 5000
```

3. **Cấu hình Windows Firewall:**
```powershell
# Mở port 5000
New-NetFirewallRule -DisplayName "Mekong Water API" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

4. **Cập nhật Flutter app:**
```dart
// lib/services/water_level_service.dart
static const String baseUrl = 'http://192.168.1.100:5000/api';
// Thay 192.168.1.100 bằng IP máy tính của bạn
```

5. **Đảm bảo thiết bị và máy tính cùng WiFi**

---

### Option 4: Sử dụng ngrok (Temporary, cho test)

**Ưu điểm:**
- ✅ Nhanh, dễ setup
- ✅ Có HTTPS

**Nhược điểm:**
- ❌ URL thay đổi mỗi lần chạy
- ❌ Giới hạn requests (free tier)

**Cách làm:**
```bash
# 1. Cài ngrok
# 2. Chạy backend
python app.py

# 3. Terminal khác, chạy ngrok
ngrok http 5000

# 4. Lấy URL từ ngrok (ví dụ: https://abc123.ngrok.io)
# 5. Cập nhật Flutter:
static const String baseUrl = 'https://abc123.ngrok.io/api';
```

---

## 📱 CẬP NHẬT FLUTTER APP

Sau khi deploy backend, cập nhật baseUrl:

```dart
// lib/services/water_level_service.dart

// Option 1: Cloud (Production)
static const String baseUrl = 'https://your-backend-url.com/api';

// Option 2: Local network (Development)
static const String baseUrl = 'http://192.168.1.100:5000/api';

// Option 3: Android emulator
static const String baseUrl = 'http://10.0.2.2:5000/api';

// Option 4: iOS simulator
static const String baseUrl = 'http://localhost:5000/api';
```

**Hoặc dùng environment variable:**
```dart
// lib/services/water_level_service.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

static String get baseUrl {
  return dotenv.env['API_BASE_URL'] ?? 'http://10.0.2.2:5000/api';
}
```

```env
# .env
API_BASE_URL=https://your-backend-url.com/api
```

---

## 🎯 KHUYẾN NGHỊ

### Cho Production:
1. **Deploy lên Heroku/Railway** (miễn phí, dễ)
2. **Hoặc mua VPS** (nếu cần performance cao)

### Cho Development/Test:
1. **Chạy local + ngrok** (nhanh)
2. **Hoặc chạy local + share IP** (nếu cùng WiFi)

---

## 📝 CHECKLIST DEPLOY

- [ ] Deploy backend lên cloud
- [ ] Test API endpoint: `curl https://your-backend.com/api/health`
- [ ] Cập nhật baseUrl trong Flutter
- [ ] Build APK: `flutter build apk --release`
- [ ] Test APK trên thiết bị thật
- [ ] Kiểm tra kết nối backend

---

## 🐛 TROUBLESHOOTING

### APK không kết nối được backend?

1. **Kiểm tra backend đang chạy:**
```bash
curl https://your-backend.com/api/health
```

2. **Kiểm tra baseUrl trong code:**
```dart
print(WaterLevelService.baseUrl);
```

3. **Kiểm tra network permissions:**
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET"/>
```

4. **Kiểm tra CORS trên backend:**
```python
# backend-python/app.py
CORS(app)  # Đã có sẵn
```

---

## 💡 TIP

**Để dễ quản lý, tạo file config:**

```dart
// lib/config/app_config.dart
class AppConfig {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://your-backend-url.com/api',
  );
}
```

Build với custom URL:
```bash
flutter build apk --dart-define=API_BASE_URL=https://your-backend.com/api
```

---

**Chọn phương án phù hợp với nhu cầu của bạn!** 🚀

