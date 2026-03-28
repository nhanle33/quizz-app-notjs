# Quiz App: FastAPI & React (Không cần Node.js)

Dự án này là một ứng dụng trắc nghiệm đơn giản, được xây dựng theo kiến trúc Client - Server với mục tiêu nhanh, gọn, dễ cài đặt.

- **Backend**: Viết bằng `Python` sử dụng Framework `FastAPI`.
- **Frontend**: Viết bằng `ReactJS` thông qua CDN trực tiếp trong file HTML (không cần cài Node.js, Webpack hay NPM package). CSS được tách riêng biệt để dễ quản lý.

---

## 📂 Tổ chức mã nguồn
```text
d:\quizz-app-nonodejs
│
├── backend/
│   ├── main.py           # Logic chính của server (Mã nguồn API câu hỏi và chấm điểm)
│   └── requirements.txt  # Danh sách các thư viện Python cần cài đặt
│
└── frontend/
    ├── index.html        # Giao diện chính nhúng React & Babel
    └── style.css         # Các thiết lập màu sắc và thành phần UI (Buttons, typography, layout)
```

---

## 🚀 Hướng dấn khởi động và chạy ứng dụng

### 1. Khởi động Backend
Backend đóng vai trò cung cấp ngân hàng câu hỏi và thực hiện chức năng **chấm điểm** khi bạn nộp bài. Nếu backend không chạy, ứng dụng sẽ không thể lấy được câu hỏi.

1. Bật Command Prompt, PowerShell hoặc Terminal lên.
2. Di chuyển vào thư mục `backend`:
   ```bash
   cd d:\quizz-app-nonodejs\backend
   ```
3. Cài đặt các modules bắt buộc:
   ```bash
   pip install -r requirements.txt
   ```
   *(Đảm bảo máy tính bạn đã cài đặt Python. Nếu chưa có, tải và cài từ [python.org](https://www.python.org/downloads/))*
4. Chạy server:
   ```bash
   uvicorn main:app --reload
   ```
5. Đợi đến khi Terminal thông báo: `Application startup complete` và đang lắng nghe ở cổng `http://127.0.0.1:8000`. Hãy cứ **để nguyên cửa sổ đó** (không tắt đi).

**💡 Mẹo: Thay đổi cổng (port) mặc định?**
Nếu bạn muốn chạy server ở một cổng khác (ví dụ: cổng `8080`), hãy thêm cờ `--port` vào lệnh khởi động:
```bash
uvicorn main:app --reload --port 8080
```
*(Lưu ý quan trọng: Nếu bạn đổi cổng backend, bạn bắt buộc phải mở file `frontend/index.html` (khoảng dòng 22) và cập nhật biến `const API_URL = "http://127.0.0.1:8080";` để frontend có thể kết nối được tới server mới).*

### 2. Mở Frontend (Giao diện tương tác)
Vì dự án cố ý "không dùng Node.js", bạn hoàn toàn có thể chay trực tiếp file trên trình duyệt mà không cần bước `npm start`.

1. Mở File Explorer.
2. Đi vào thư mục: `d:\quizz-app-nonodejs\frontend`
3. Click đúp vào file `index.html` (hoặc nhấp chuột phải chọn **Open With...** -> Google Chrome / Edge).
4. Ngay lập tức, giao diện ứng dụng sẽ hiện ra. Bấm nút **Bắt đầu** để chơi ứng dụng.

---

## 🛠 Cách hoạt động của các chức năng
**Luồng Dữ liệu (Dành cho Developer)**
-  **Lấy câu hỏi (`GET /questions`)**: Frontend gọi API để lấy dãy 5 câu hỏi hiển thị cho người chơi (đáp án thật sự được giấu kĩ tại Server).
-  **Màn hình chơi (Playing State)**: Sử dụng các Hook cơ bản của React (`useState`) lưu trữ lại các Option được bấm (được lưu tại mảng JS trên RAM Browser).
-  **Chấm bài (`POST /submit`)**: Sau khi ấn nút nộp, Frontend gửi Json Array (vd: `[{"question_id": 1, "selected_answer": "JavaScript"}]`). Backend nhận, tính toán số câu chọn đúng, quy chiếu qua số điểm / 10 và gửi trả chi tiết để Frontend in kết quả màn hình ResultScreen.
