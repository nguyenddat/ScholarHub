import os
import json

from core.config import settings
from ai.WebScraper.WebScraper import LLMsWebScraper

resp = LLMsWebScraper.scrape(
    num_pages = 10
)

with open(os.path.join(settings.BASE_DIR, "artifacts", "WebScrape", "data1.json"), "w", encoding = "utf-8") as file:
    json.dump(resp, file, ensure_ascii = False)
import json
from datetime import datetime
import os
import uuid

# Đường dẫn tới file JSON và file kết quả
json_file_path = os.path.join(os.getcwd(), "backend", "artifacts", "WebScrape", "data.json")
output_file_path = "insert_scholarships.txt"

# Tải dữ liệu từ file JSON
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Danh sách các cột cần insert
columns = [
    "id", "title", "provider", "type", "funding_level", "degree_level", "region",
    "country", "major", "deadline", "description", "original_url", "language", "posted_at"
]

def escape(value):
    if value is None:
        return "NULL"
    # Đảm bảo chuỗi được escape đúng cách
    value = str(value)
    value = value.replace("'", "''")  # Đảm bảo không có dấu ' trong chuỗi
    value = value.replace("\\", "\\\\")  # Escape dấu backlash nếu có
    return f"'{value}'"

# Sinh câu lệnh INSERT
values_list = []
for item in data:
    # Tạo giá trị UUID cho id
    values = [escape(str(uuid.uuid4()))]
    
    # Lấy giá trị cho các cột, bỏ qua cột 'posted_at' và xử lý giá trị mặc định nếu thiếu
    values.extend([escape(item.get(col, '')) for col in columns[1:-1]])  # sử dụng '' nếu giá trị không có
    values.append(f"'{datetime.utcnow().isoformat(sep=' ', timespec='seconds')}'")  # thêm giá trị cho 'posted_at'
    
    # Thêm giá trị vào danh sách
    values_list.append(f"({', '.join(values)})")

# Tạo câu lệnh INSERT chung
insert_statement = f"INSERT INTO scholarships ({', '.join(columns)}) VALUES \n{',\n'.join(values_list)};"

# Ghi ra file txt
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(insert_statement)

print(f"✅ Đã ghi lệnh INSERT chung vào '{output_file_path}'")