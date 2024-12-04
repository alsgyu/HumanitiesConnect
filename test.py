from transformers import pipeline

# Hugging Face에 업로드된 모델 경로
model_name = "alsgyu/sentiment-analysis-fine-tuned-model"

# 모델과 토크나이저를 Hugging Face에서 로드
analyzer = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)

# 테스트 문장
sample_text = "오늘은 제 생일이었어요!"

# 감정 분석
result = analyzer(sample_text)

label_mapping = {
    "LABEL_0": "부정",
    "LABEL_1": "중립",
    "LABEL_2": "긍정"
}

result_label = label_mapping[result[0]['label']]
print(f"Input: {sample_text}\nAnalysis Result: {result_label} (Score: {result[0]['score']:.2f})")
