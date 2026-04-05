%%writefile sentiment-api/README.md
# Sentiment Analysis API

**Sinh viên:** THANG  
**Môn:** Tư duy Tính toán - Bài thực hành 1

## Mô hình sử dụng
- **Tên mô hình:** nlptown/bert-base-multilingual-uncased-sentiment  
- **Link:** https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment

## Chức năng
API phân tích cảm xúc văn bản (1-5 sao), hỗ trợ tiếng Việt.

## Hướng dẫn chạy

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000