# 🚀 Hướng dẫn Nhanh - Mekong Water Level API

## Chạy Backend trong 3 bước

### Bước 1: Cài đặt Dependencies
```bash
cd backend-python
pip install -r requirements.txt
```

### Bước 2: Chạy API Server
```bash
python app.py
```

### Bước 3: Test API
Mở browser và truy cập: http://localhost:5000

## 🧪 Test nhanh các API

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

### 2. Lấy dữ liệu mới nhất
```bash
curl http://localhost:5000/api/latest
```

### 3. Lấy dữ liệu trạm Cần Thơ
```bash
curl http://localhost:5000/api/stations/can_tho
```

### 4. Lấy cảnh báo
```bash
curl http://localhost:5000/api/alerts
```

## 📱 Sử dụng trong Flutter

```dart
import 'package:fpt_guard_v2/services/water_level_service.dart';

// Trong hàm async
final data = await WaterLevelService.getLatestData();
print('Dữ liệu: $data');
```

## ⚙️ Cấu hình nhanh

### Thay đổi port (nếu port 5000 bị chiếm)
Sửa trong `config.py`:
```python
API_PORT = 5001  # Đổi sang port khác
```

### Thay đổi tần suất cập nhật
Sửa trong `config.py`:
```python
UPDATE_INTERVAL = 1800  # 30 phút (tính bằng giây)
```

### Tắt chế độ headless (để xem browser khi debug)
Sửa trong `config.py`:
```python
SELENIUM_CONFIG = {
    "headless": False,  # Đổi thành False
    ...
}
```

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError
```bash
pip install -r requirements.txt --force-reinstall
```

### Lỗi: ChromeDriver
- Đảm bảo đã cài Google Chrome
- Chạy lại: `pip install webdriver-manager --upgrade`

### Lỗi: Port đã được sử dụng
- Đổi port trong `config.py`
- Hoặc tắt ứng dụng đang dùng port 5000

## 📖 Tài liệu đầy đủ
Xem file `README.md` để biết chi tiết đầy đủ.

## 🎯 Các ID trạm có sẵn
- `can_tho` - Cần Thơ
- `my_thuan` - Mỹ Thuận
- `vinh_long` - Vĩnh Long
- `tan_chau` - Tân Châu
- `chau_doc` - Châu Đốc

---
✨ **Tip**: Lần chạy đầu tiên sẽ mất ~1-2 phút để scrape dữ liệu. Hãy kiên nhẫn!

