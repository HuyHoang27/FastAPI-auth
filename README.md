# FastAPI Text-to-Speech và Speech-to-Text API

Dự án này cung cấp hai API cho chuyển đổi văn bản thành giọng nói (text-to-speech) và chuyển đổi giọng nói thành văn bản (speech-to-text), cùng với xác thực sử dụng JWT.

## Cài Đặt

1. Tạo môi trường ảo và cài đặt các gói cần thiết từ `requirements.txt`:

    ```bash
    pipenv install
    ```

2. Kích hoạt môi trường ảo và chạy lệnh sau:
    ```bash
    pipenv shell
    ```
    ```bash
    pip install openai
    ```
3. Cài đặt các thư viện bổ sung (nếu có) bằng cách thêm chúng vào `requirements.txt` và chạy lệnh:

    ```bash
    pipenv install -r requirements.txt
    ```
    Kiểm tra các thư viện có trong environment chạy lệnh:
    ```bash
    pip list
    ```
4. Thoát khỏi môi trường ảo khi bạn đã hoàn thành:

    ```bash
    exit
    ```

## Chạy FastAPI
1. Cài đặt các tham số của mô hình trong file .env
2. Chạy dự án FastAPI bằng lệnh sau:

```bash
uvicorn main:app --reload
