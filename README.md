# eOffice Draft Helper

Trợ lý soạn thảo văn bản AI cho hệ thống eOffice. Giao diện side-by-side: bên trái xem trước dự thảo, bên phải chat với AI để tạo và chỉnh sửa văn bản hành chính.

## Kiến trúc

```
eoffice-draft-helper/
├── backend/              # FastAPI + SSE streaming + Redis session
├── frontend/             # React + TypeScript + Tailwind CSS
├── docs/                 # Tài liệu hướng dẫn
├── docker-compose.yml    # Deploy tất cả services
└── .gitignore
```

## Yêu cầu

- Docker 24+ và Docker Compose v2+
- VNPT LLM API key

## Khởi chạy nhanh

```bash
# 1. Cấu hình
cd backend && cp .env.example .env   # Sửa VNPT_API_KEY

# 2. Deploy (Docker)
docker compose up -d

# 3. Phát triển frontend local
cd frontend && npm install && npm run dev

# 4. Truy cập
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/health
```

## Tài liệu

- [Hướng dẫn triển khai](docs/deployment-guide.md) - Docker deploy, phát triển local
- [Hướng dẫn tích hợp](docs/integration-guide.md) - Nhúng vào web app khác (iframe)
- [API Reference](docs/api-reference.md) - Chi tiết các endpoint backend

## License

Internal use - eOffice project.
