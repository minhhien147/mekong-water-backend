# 🌊 Hệ thống Giám sát Mực nước Sông Mekong

Backend service Python để scrape và cung cấp dữ liệu mực nước gần real-time từ Mekong River Commission (MRC).

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [API Endpoints](#api-endpoints)
- [Cấu hình](#cấu-hình)
- [Lưu ý quan trọng](#lưu-ý-quan-trọng)

## ✨ Tính năng

### 1. **Web Scraping từ MRC**
- ✅ Sử dụng Selenium để scrape dữ liệu từ biểu đồ động (Highcharts)
- ✅ Hỗ trợ 5 trạm chính ở ĐBSCL: Cần Thơ, Mỹ Thuận, Vĩnh Long, Tân Châu, Châu Đốc
- ✅ Chạy ở chế độ headless để tự động hóa
- ✅ Xử lý lỗi và fallback data khi không scrape được

### 2. **Xử lý và Phân tích Dữ liệu**
- 📊 Chuyển đổi múi giờ về UTC+7 (Việt Nam)
- 📈 Tính toán đỉnh triều cao/thấp
- 🔮 Dự báo thời gian đỉnh triều tiếp theo
- 📉 Phân tích xu hướng (mực nước đang lên/xuống)
- 📊 Thống kê cơ bản (max, min, mean, std)

### 3. **Hệ thống Cảnh báo**
- 🚨 CRITICAL: Mực nước vượt ngưỡng báo động III (nguy cơ ngập lụt)
- ⚠️ WARNING: Mực nước vượt ngưỡng cảnh báo
- ✅ NORMAL: Mực nước trong giới hạn an toàn

### 4. **Cập nhật Tự động**
- ⏰ Scheduler tự động cập nhật mỗi 1 giờ
- 💾 Lưu dữ liệu vào JSON (latest) và CSV (historical)
- 🔄 Có thể trigger update thủ công qua API

### 5. **REST API**
- 🌐 Flask REST API với CORS support
- 📱 Dễ dàng tích hợp với Flutter app
- 📝 Response format JSON chuẩn
- ❤️ Health check endpoint

## 📁 Cấu trúc dự án

```
backend-python/
├── app.py                  # Flask API server chính
├── mrc_scraper.py         # Module scrape dữ liệu từ MRC
├── data_processor.py      # Module xử lý và phân tích dữ liệu
├── scheduler.py           # Module scheduler tự động cập nhật
├── config.py              # Cấu hình hệ thống
├── requirements.txt       # Dependencies Python
├── .env.example           # File cấu hình mẫu
├── README.md              # Tài liệu này
├── data/                  # Thư mục lưu dữ liệu
│   ├── latest_water_levels.json   # Dữ liệu mới nhất
│   └── historical_data.csv        # Dữ liệu lịch sử
└── logs/                  # Thư mục logs
    ├── api.log
    └── scheduler.log
```

## 🔧 Yêu cầu hệ thống

### Python
- Python 3.8 trở lên

### Chrome/Chromium
- Google Chrome hoặc Chromium browser (để Selenium hoạt động)
- ChromeDriver sẽ được tự động tải bởi `webdriver-manager`

### Thư viện Python
Xem file `requirements.txt` để biết chi tiết. Các thư viện chính:
- `selenium` - Web scraping
- `flask` - REST API
- `pandas` - Data processing
- `APScheduler` - Task scheduling

## 🚀 Cài đặt

### Bước 1: Clone repository (nếu chưa có)
```bash
cd E:\fpt-guard-v2\backend-python
```

### Bước 2: Tạo virtual environment (khuyến nghị)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình (optional)
Copy file `.env.example` thành `.env` và điều chỉnh nếu cần:
```bash
copy .env.example .env
```

## 💻 Sử dụng

### Chạy API Server (Khuyến nghị - Chạy cả API + Scheduler)

```bash
python app.py
```

Server sẽ:
1. ✅ Khởi động scheduler (cập nhật mỗi 1 giờ)
2. ✅ Chạy update ngay lần đầu tiên
3. ✅ Khởi động Flask API tại `http://localhost:5000`

### Chạy Scheduler riêng (Chỉ cập nhật data, không có API)

```bash
python scheduler.py
```

### Test các module riêng lẻ

```bash
# Test scraper
python mrc_scraper.py

# Test data processor
python data_processor.py
```

## 🌐 API Endpoints

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. **GET /** - Thông tin API
```bash
curl http://localhost:5000/
```

#### 2. **GET /api/health** - Health check
```bash
curl http://localhost:5000/api/health
```

#### 3. **GET /api/stations** - Danh sách tất cả các trạm
```bash
curl http://localhost:5000/api/stations
```

Response:
```json
{
  "success": true,
  "data": {
    "can_tho": {
      "station_id": "can_tho",
      "name": "Cần Thơ",
      "name_en": "Can Tho",
      "coordinates": {"lat": 10.0452, "lon": 105.7469},
      "thresholds": {"warning": 1.8, "flood": 2.0}
    },
    ...
  },
  "total": 5
}
```

#### 4. **GET /api/latest** - Dữ liệu mới nhất của tất cả các trạm
```bash
curl http://localhost:5000/api/latest
```

Response:
```json
{
  "success": true,
  "data": {
    "last_updated": "2026-01-09T09:57:00+07:00",
    "stations": {
      "can_tho": {
        "station_id": "can_tho",
        "station_name": "Cần Thơ",
        "current": {
          "water_level": 1.65,
          "timestamp": "2026-01-09T09:55:00+07:00",
          "unit": "m"
        },
        "alert": {
          "level": "NORMAL",
          "message": "✓ Mực nước tại Cần Thơ trong giới hạn an toàn..."
        },
        "forecast": {
          "next_high_tide": {...},
          "next_low_tide": {...}
        },
        "trend": {
          "direction": "rising",
          "direction_vn": "Đang lên"
        },
        ...
      }
    }
  }
}
```

#### 5. **GET /api/stations/{station_id}** - Dữ liệu chi tiết một trạm
```bash
curl http://localhost:5000/api/stations/can_tho
```

#### 6. **GET /api/alerts** - Danh sách cảnh báo hiện tại
```bash
curl http://localhost:5000/api/alerts
```

Response:
```json
{
  "success": true,
  "data": {
    "alerts": [
      {
        "station_id": "can_tho",
        "station_name": "Cần Thơ",
        "alert_level": "CRITICAL",
        "message": "🚨 CẢNH BÁO NGẬP LỤT!...",
        "current_water_level": 2.15
      }
    ],
    "total": 1,
    "has_critical": true
  }
}
```

#### 7. **POST /api/update** - Trigger cập nhật thủ công
```bash
curl -X POST http://localhost:5000/api/update
```

#### 8. **GET /api/status** - Trạng thái hệ thống
```bash
curl http://localhost:5000/api/status
```

#### 9. **GET /api/historical/{station_id}?limit=100** - Dữ liệu lịch sử
```bash
curl http://localhost:5000/api/historical/can_tho?limit=50
```

## ⚙️ Cấu hình

### File `config.py`

Các thông số quan trọng có thể điều chỉnh:

```python
# Cập nhật mỗi bao lâu (giây)
UPDATE_INTERVAL = 3600  # 1 giờ

# Ngưỡng cảnh báo cho từng trạm (mét)
STATIONS = {
    "can_tho": {
        "flood_threshold": 2.0,     # Báo động III
        "warning_threshold": 1.8,    # Cảnh báo
        ...
    }
}

# Selenium headless mode
SELENIUM_CONFIG = {
    "headless": True,  # False để xem browser
    "timeout": 30
}

# Flask API
API_HOST = "0.0.0.0"  # Cho phép truy cập từ mọi IP
API_PORT = 5000
```

## 📝 Lưu ý quan trọng

### 1. Đạo đức Web Scraping
- ✅ Có delay 2 giây giữa các request để tránh overload server MRC
- ✅ Chỉ sử dụng cho mục đích giáo dục, phi thương mại
- ✅ Tôn trọng robots.txt và Terms of Service của MRC

### 2. Dữ liệu mẫu
- Khi không scrape được từ MRC, hệ thống tự động tạo **dữ liệu mẫu** để test
- Dữ liệu mẫu được đánh dấu `"data_source": "sample"`
- Trong production, bạn có thể tắt tính năng này

### 3. Cấu trúc HTML của MRC có thể thay đổi
- Trang MRC có thể cập nhật cấu trúc HTML
- Cần theo dõi và cập nhật selector trong `mrc_scraper.py`
- Hiện tại sử dụng JavaScript để extract từ Highcharts

### 4. Firewall và Ports
- Đảm bảo port 5000 không bị firewall chặn
- Nếu chạy trên server, cấu hình port forwarding

### 5. Performance
- Lần chạy đầu tiên sẽ lâu (tải ChromeDriver)
- Scraping mất ~30-60 giây cho 5 trạm
- Có thể tăng timeout trong config nếu mạng chậm

## 🔄 Tích hợp với Flutter App

### Sử dụng service đã tạo

```dart
import 'package:fpt_guard_v2/services/water_level_service.dart';

// Lấy dữ liệu mới nhất
final data = await WaterLevelService.getLatestData();

// Lấy dữ liệu một trạm
final canThoData = await WaterLevelService.getStationData('can_tho');

// Lấy cảnh báo
final alerts = await WaterLevelService.getAlerts();

// Health check
final isHealthy = await WaterLevelService.healthCheck();
```

### Cập nhật Base URL

Nếu chạy backend trên server khác, cập nhật trong `lib/services/water_level_service.dart`:

```dart
static const String baseUrl = 'http://YOUR_SERVER_IP:5000/api';
```

## 🐛 Troubleshooting

### Lỗi: ChromeDriver không tìm thấy
```bash
pip install --upgrade webdriver-manager
```

### Lỗi: Timeout khi scrape
- Tăng timeout trong `config.py`
- Kiểm tra kết nối internet
- Thử chạy không headless (`headless: False`) để debug

### Lỗi: Port 5000 đã được sử dụng
Thay đổi port trong `config.py`:
```python
API_PORT = 5001  # hoặc port khác
```

### Lỗi: Module not found
```bash
pip install -r requirements.txt --force-reinstall
```

## 📊 Monitoring

### Xem logs
```bash
# API logs
type logs\api.log

# Scheduler logs
type logs\scheduler.log
```

### Kiểm tra dữ liệu
```bash
# Dữ liệu mới nhất
type data\latest_water_levels.json

# Dữ liệu lịch sử
type data\historical_data.csv
```

## 🚢 Deploy lên Server

### Sử dụng Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Sử dụng Docker (Recommended)
```dockerfile
# Dockerfile (tạo file này nếu cần)
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build và run:
```bash
docker build -t mekong-water-api .
docker run -p 5000:5000 mekong-water-api
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs trong thư mục `logs/`
2. Đảm bảo tất cả dependencies đã được cài đặt
3. Kiểm tra Google Chrome đã được cài đặt
4. Thử chạy test các module riêng lẻ

## 📄 License

Dự án này chỉ sử dụng cho mục đích giáo dục và nghiên cứu.

---

**Lưu ý**: Dữ liệu từ MRC là tài sản của Mekong River Commission. Vui lòng sử dụng có trách nhiệm.

