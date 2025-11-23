```
# Start:
docker compose up --build -d

# Dừng containers
docker compose stop

# Khởi động lại
docker compose restart

# Xóa containers
docker compose down

# Xóa containers và volumes
docker compose down -v

# Xem logs của một service cụ thể
docker compose logs backend
docker compose logs db

# Vào shell của container
docker compose exec backend bash

# Rebuild một service cụ thể
docker compose up --build backend

# Chạy lệnh trong container
docker compose exec backend python test.py

# Thêm data học bổng
docker compose exec backend python test.py
```