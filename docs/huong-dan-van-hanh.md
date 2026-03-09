# Hướng dẫn Vận hành

## Mục lục

1. [Kiểm tra sức khoẻ hệ thống](#kiểm-tra-sức-khoẻ-hệ-thống)
2. [Quản lý dịch vụ](#quản-lý-dịch-vụ)
3. [Giám sát logs](#giám-sát-logs)
4. [Xử lý sự cố](#xử-lý-sự-cố)
5. [Bảo trì định kỳ](#bảo-trì-định-kỳ)

---

## Kiểm tra sức khoẻ hệ thống

### Backend health check

```bash
# Kiểm tra nhanh
curl http://localhost:8000/

# Kiểm tra chi tiết (bao gồm trạng thái LLM)
curl http://localhost:8000/health
```

Response kỳ vọng:
```json
{
  "status": "healthy",
  "llm_configured": true,
  "model": "llm-medium-v4"
}
```

### Redis health check

```bash
redis-cli ping
# → PONG

# Kiểm tra số session đang active
redis-cli keys "draft:session:*" | wc -l
```

### Frontend health check

Truy cập `http://localhost:3000` — nếu trang load được là OK.

## Quản lý dịch vụ

### Docker Compose

```bash
# Xem trạng thái
docker compose ps

# Restart một dịch vụ
docker compose restart backend

# Xem logs
docker compose logs -f backend

# Dừng tất cả
docker compose down

# Khởi động lại
docker compose up -d
```

### Systemd (không Docker)

Tạo `/etc/systemd/system/eoffice-draft-backend.service`:

```ini
[Unit]
Description=eOffice Draft Helper Backend
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/eoffice-draft-helper/backend
Environment=PATH=/var/www/eoffice-draft-helper/backend/.venv/bin
ExecStart=/var/www/eoffice-draft-helper/backend/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable eoffice-draft-backend
sudo systemctl start eoffice-draft-backend
sudo systemctl status eoffice-draft-backend
```

## Giám sát logs

### Backend logs

```bash
# Docker
docker compose logs -f --tail=100 backend

# Systemd
journalctl -u eoffice-draft-backend -f --since "1 hour ago"
```

### Các log quan trọng cần theo dõi

| Log pattern | Ý nghĩa | Hành động |
|---|---|---|
| `LLM streaming error` | LLM API lỗi | Kiểm tra API key, kết nối mạng |
| `Session not found` | Session hết hạn | Bình thường nếu TTL đã qua |
| `VNPT_API_KEY is required` | Thiếu cấu hình | Kiểm tra file .env |
| `Connection refused redis` | Redis chết | Restart Redis |

## Xử lý sự cố

### 1. LLM không phản hồi

**Triệu chứng**: Frontend hiện "Đang tạo..." nhưng không có nội dung.

**Kiểm tra**:
```bash
# Test LLM trực tiếp
curl -X POST http://localhost:8000/draft/generate \
  -H "Content-Type: application/json" \
  -d '{"file_content": "Test document content"}'
```

**Nguyên nhân phổ biến**:
- API key hết hạn/sai → Cập nhật `VNPT_API_KEY` trong `.env`
- Network firewall chặn outbound → Mở port 443 đến `assistant-stream.vnpt.vn`
- Model không tồn tại → Kiểm tra `VNPT_MODEL` trong `.env`

### 2. Redis mất kết nối

**Triệu chứng**: Lỗi 500 khi gọi API, log hiện "Connection refused".

**Khắc phục**:
```bash
# Kiểm tra Redis
redis-cli ping

# Restart Redis
sudo systemctl restart redis
# hoặc
docker compose restart redis
```

### 3. Frontend không kết nối được backend

**Triệu chứng**: Network tab hiện lỗi CORS hoặc 502/504.

**Kiểm tra**:
- Nginx proxy config có `proxy_buffering off` chưa
- Backend đang chạy: `curl http://localhost:8000/health`
- CORS_ORIGINS trong `.env` có chứa domain frontend không

### 4. SSE streaming không hoạt động (nội dung hiện cùng lúc)

**Nguyên nhân**: Proxy server buffer response.

**Khắc phục**: Đảm bảo Nginx config có:
```nginx
proxy_buffering off;
proxy_cache off;
proxy_http_version 1.1;
proxy_set_header Connection '';
```

## Bảo trì định kỳ

### Hàng ngày
- Kiểm tra `/health` endpoint

### Hàng tuần
- Xem log có error pattern bất thường
- Kiểm tra Redis memory usage: `redis-cli info memory`

### Hàng tháng
- Cập nhật dependencies: `pip install --upgrade -r requirements.txt`
- Kiểm tra SSL certificate expiry
- Review và dọn Redis sessions nếu cần: `redis-cli keys "draft:session:*" | wc -l`
