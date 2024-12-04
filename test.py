from transformers import pipeline

# 로컬 디렉토리 경로
model_path = "D:/wow/fine_tuned_model/fine_tuned_model"  # 실제 경로로 변경
analyzer = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

# 테스트
label_mapping = {
    "LABEL_0": "부정",
    "LABEL_1": "중립",
    "LABEL_2": "긍정"
}

result = analyzer("오늘은 좀 우중충 하네요")
human_readable_result = {
    "감정": label_mapping[result[0]['label']],
    "확률": result[0]['score']
}
print(human_readable_result)