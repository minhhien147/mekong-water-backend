"""
Flask API cho hệ thống giám sát mực nước sông Mekong
Flask REST API for Mekong River Water Level Monitoring
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
import pytz

from scheduler import DataUpdateScheduler
from mrc_scraper import MRCWaterLevelScraper
from data_processor import WaterLevelProcessor
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{config.LOGS_DIR}/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS cho Flutter app

# Khởi tạo scheduler
scheduler = DataUpdateScheduler()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """
    Endpoint trang chủ - thông tin API
    """
    return jsonify({
        "name": "Mekong River Water Level Monitoring API",
        "version": "1.0.0",
        "description": "API cung cấp dữ liệu mực nước sông Mekong gần real-time từ MRC",
        "endpoints": {
            "/": "Thông tin API",
            "/api/stations": "Danh sách tất cả các trạm",
            "/api/stations/<station_id>": "Dữ liệu chi tiết của một trạm",
            "/api/latest": "Dữ liệu mới nhất của tất cả các trạm",
            "/api/alerts": "Danh sách cảnh báo hiện tại",
            "/api/update": "Trigger cập nhật dữ liệu thủ công (POST)",
            "/api/status": "Trạng thái của scheduler và hệ thống",
            "/api/health": "Health check"
        },
        "documentation": "https://github.com/your-repo/mekong-water-level",
        "contact": "your-email@example.com"
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(pytz.timezone(config.TIMEZONE)).isoformat(),
        "scheduler_running": scheduler.is_running
    })


@app.route('/api/stations', methods=['GET'])
def get_all_stations():
    """
    Lấy thông tin tất cả các trạm (không bao gồm dữ liệu chi tiết)
    """
    try:
        stations_info = {}
        for station_id, info in config.STATIONS.items():
            stations_info[station_id] = {
                "station_id": station_id,
                "name": info['name'],
                "name_en": info['name_en'],
                "coordinates": info['coordinates'],
                "thresholds": {
                    "warning": info['warning_threshold'],
                    "flood": info['flood_threshold']
                }
            }
        
        return jsonify({
            "success": True,
            "data": stations_info,
            "total": len(stations_info)
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách trạm: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    """
    Lấy dữ liệu mới nhất của tất cả các trạm
    """
    try:
        # Đọc từ file JSON
        if not os.path.exists(config.LATEST_DATA_FILE):
            return jsonify({
                "success": False,
                "error": "Chưa có dữ liệu. Vui lòng đợi lần cập nhật đầu tiên."
            }), 404
        
        with open(config.LATEST_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            "success": True,
            "data": data
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu mới nhất: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/stations/<station_id>', methods=['GET'])
def get_station_data(station_id):
    """
    Lấy dữ liệu chi tiết của một trạm cụ thể
    """
    try:
        if station_id not in config.STATIONS:
            return jsonify({
                "success": False,
                "error": f"Không tìm thấy trạm với ID: {station_id}"
            }), 404
        
        # Đọc từ file JSON
        if not os.path.exists(config.LATEST_DATA_FILE):
            return jsonify({
                "success": False,
                "error": "Chưa có dữ liệu. Vui lòng đợi lần cập nhật đầu tiên."
            }), 404
        
        with open(config.LATEST_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        station_data = data['stations'].get(station_id)
        
        if not station_data:
            return jsonify({
                "success": False,
                "error": f"Không có dữ liệu cho trạm {station_id}"
            }), 404
        
        return jsonify({
            "success": True,
            "data": station_data
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu trạm {station_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """
    Lấy danh sách các cảnh báo hiện tại (chỉ trạm có mực nước cao)
    """
    try:
        if not os.path.exists(config.LATEST_DATA_FILE):
            return jsonify({
                "success": False,
                "error": "Chưa có dữ liệu"
            }), 404
        
        with open(config.LATEST_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        alerts = []
        
        for station_id, station_data in data['stations'].items():
            alert = station_data.get('alert', {})
            if alert.get('level') in ['WARNING', 'CRITICAL']:
                alerts.append({
                    "station_id": station_id,
                    "station_name": station_data['station_name'],
                    "alert_level": alert['level'],
                    "message": alert['message'],
                    "current_water_level": station_data['current']['water_level'],
                    "timestamp": station_data['current']['timestamp']
                })
        
        return jsonify({
            "success": True,
            "data": {
                "alerts": alerts,
                "total": len(alerts),
                "has_critical": any(a['alert_level'] == 'CRITICAL' for a in alerts)
            }
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách cảnh báo: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/update', methods=['POST'])
def trigger_update():
    """
    Trigger cập nhật dữ liệu thủ công
    """
    try:
        logger.info("Nhận request cập nhật dữ liệu thủ công")
        
        success = scheduler.update_data()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Cập nhật dữ liệu thành công",
                "timestamp": datetime.now(pytz.timezone(config.TIMEZONE)).isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "Cập nhật dữ liệu thất bại"
            }), 500
        
    except Exception as e:
        logger.error(f"Lỗi khi trigger update: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Lấy trạng thái của scheduler và hệ thống
    """
    try:
        status = scheduler.get_status()
        
        # Thêm thông tin file
        data_file_exists = os.path.exists(config.LATEST_DATA_FILE)
        data_file_size = os.path.getsize(config.LATEST_DATA_FILE) if data_file_exists else 0
        
        last_update = None
        if data_file_exists:
            with open(config.LATEST_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                last_update = data.get('last_updated')
        
        status.update({
            "data_file_exists": data_file_exists,
            "data_file_size_bytes": data_file_size,
            "last_update": last_update,
            "current_time": datetime.now(pytz.timezone(config.TIMEZONE)).isoformat()
        })
        
        return jsonify({
            "success": True,
            "data": status
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy status: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/historical/<station_id>', methods=['GET'])
def get_historical_data(station_id):
    """
    Lấy dữ liệu lịch sử của một trạm (từ CSV)
    
    Query params:
    - limit: số lượng bản ghi tối đa (default: 100)
    """
    try:
        if station_id not in config.STATIONS:
            return jsonify({
                "success": False,
                "error": f"Không tìm thấy trạm với ID: {station_id}"
            }), 404
        
        if not os.path.exists(config.HISTORICAL_DATA_FILE):
            return jsonify({
                "success": False,
                "error": "Chưa có dữ liệu lịch sử"
            }), 404
        
        # Đọc CSV
        import pandas as pd
        df = pd.read_csv(config.HISTORICAL_DATA_FILE)
        
        # Filter theo station_id
        df_station = df[df['station_id'] == station_id]
        
        # Limit
        limit = int(request.args.get('limit', 100))
        df_station = df_station.tail(limit)
        
        # Convert to dict
        records = df_station.to_dict('records')
        
        return jsonify({
            "success": True,
            "data": {
                "station_id": station_id,
                "records": records,
                "total": len(records)
            }
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu lịch sử: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint không tồn tại"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Lỗi server"
    }), 500


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Khởi động Flask app và scheduler
    """
    logger.info("="*70)
    logger.info("MEKONG RIVER WATER LEVEL MONITORING - API SERVER")
    logger.info("="*70)
    
    # Tạo thư mục nếu chưa có
    Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
    
    # Khởi động scheduler
    logger.info("\nKhởi động scheduler...")
    scheduler.start(immediate=True)
    
    # Lấy port từ environment variable (cho cloud platforms) hoặc dùng config
    port = int(os.environ.get('PORT', config.API_PORT))
    host = os.environ.get('HOST', config.API_HOST)
    
    # Khởi động Flask app
    logger.info(f"\nKhởi động Flask API server...")
    logger.info(f"  → Host: {host}")
    logger.info(f"  → Port: {port}")
    logger.info(f"  → API URL: http://localhost:{port}")
    logger.info(f"  → Debug mode: {config.API_DEBUG}")
    logger.info(f"\n{'='*70}\n")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=config.API_DEBUG,
            use_reloader=False  # Tắt reloader để tránh chạy scheduler 2 lần
        )
    except KeyboardInterrupt:
        logger.info("\n\nNhận được tín hiệu dừng...")
        scheduler.stop()
        logger.info("API server đã dừng. Tạm biệt!")


if __name__ == '__main__':
    main()

