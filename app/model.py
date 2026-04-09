from transformers import pipeline
import torch
import yaml

class SentimentModel:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        model_path = config["model_path"]
        print(f"Đang load model: {model_path} ...")
        
        self.classifier = pipeline(
            "sentiment-analysis",
            model=model_path,
            device=0 if torch.cuda.is_available() else -1
        )
        print("✅ Model loaded successfully!")

    def predict(self, text: str):
        if not text or len(text.strip()) == 0:
            raise ValueError("Text không được để trống")
        
        result = self.classifier(text)[0]
        # result ví dụ: {'label': '5 stars', 'score': 0.98}
        stars = int(result["label"].split()[0])
        
        return {
            "sentiment": result["label"],
            "score": round(float(result["score"]), 4),
            "stars": stars
        }