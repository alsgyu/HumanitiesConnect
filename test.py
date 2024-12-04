from transformers import pipeline

# Hugging Face에 업로드된 모델 경로
model_name = "alsgyu/sentiment-analysis-fine-tuned-model"

# 모델과 토크나이저를 Hugging Face에서 로드
analyzer = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)

# 테스트 문장
sample_text = "오늘은 제 생일이었어요!"

# 감정 분석
result = analyzer(sample_text)

# 결과 출력
print(f"Input: {sample_text}\nAnalysis Result: {result}")
