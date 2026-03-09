# eOffice Draft Helper

Trợ lý soạn thảo văn bản AI cho hệ thống eOffice. Giao diện side-by-side: bên trái xem trước dự thảo, bên phải chat với AI để tạo và chỉnh sửa văn bản hành chính.

## Kiến trúc

```
eoffice-draft-helper/
├── backend/          # FastAPI + SSE streaming + Redis session
├── frontend/         # React + TypeScript + Tailwind CSS
└── docs/             # Tài liệu hướng dẫn
```

## Yêu cầu hệ thống

- **Backend**: Python 3.11+, Redis 7+
- **Frontend**: Node.js 20+
- **LLM**: VNPT LLM API key (OpenAI-compatible endpoint)

## Khởi chạy nhanh

```bash
# 1. Backend
cd backend
cp .env.example .env        # Sửa VNPT_API_KEY
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# 2. Frontend
cd frontend
npm install
npm run dev                  # http://localhost:3000
```

## Tài liệu

- [Hướng dẫn triển khai](docs/huong-dan-trien-khai.md) - Cài đặt, cấu hình, deploy production
- [Hướng dẫn vận hành](docs/huong-dan-van-hanh.md) - Giám sát, xử lý sự cố, bảo trì
- [Hướng dẫn nhúng](docs/huong-dan-nhung.md) - Tích hợp vào web app khác (iframe / library)
- [API Reference](docs/api-reference.md) - Chi tiết các endpoint backend

## License

Internal use - eOffice project.
