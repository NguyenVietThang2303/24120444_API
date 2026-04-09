from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
from typing import Dict

app = FastAPI(
    title="Multilingual Sentiment Analysis API",
    description="API phân tích cảm xúc (1-5 sao) sử dụng model nlptown/bert-base-multilingual-uncased-sentiment",
    version="1.0"
)

# Load model một lần khi khởi động
classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=0  # dùng GPU nếu có, bỏ nếu chạy CPU
)

class TextInput(BaseModel):
    text: str

@app.get("/")
async def root():
    return {
        "message": "Chào mừng đến với Multilingual Sentiment Analysis API!",
        "model": "nlptown/bert-base-multilingual-uncased-sentiment",
        "description": "Phân tích cảm xúc review sản phẩm (1-5 sao), hỗ trợ 6 ngôn ngữ.",
        "endpoints": {
            "/health": "Kiểm tra trạng thái",
            "/predict": "POST text → trả về 1-5 sao"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
async def predict(input_data: TextInput):
    if not input_data.text or len(input_data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text không được để trống")
    
    try:
        result = classifier(input_data.text)[0]
        # result ví dụ: {'label': '5 stars', 'score': 0.987}
        
        return {
            "input_text": input_data.text,
            "sentiment": result["label"],
            "score": round(float(result["score"]), 4),
            "stars": int(result["label"].split()[0])  # 5 stars → 5
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi suy luận: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)