# LangChain 기반 감정 분석 및 인문학적 대화 시스템

## 프로젝트 개요
이 프로젝트는 **LangChain** 오픈소스를 기반으로, 감정 분석 기능과 인문학적 통찰을 결합하여 공감 중심의 대화형 AI 시스템을 구현한 것입니다. 세밀한 감정 분석을 위해 Hugging Face 모델을 파인튜닝하였으며, 이를 통해 사용자의 감정을 보다 정확히 분석할 수 있습니다. 또한, 인문학적 자료와 통찰을 활용해 정신 건강 관리에 도움을 줄 수 있는 대화를 제공합니다.

인문학은 철학, 문학, 예술 등의 자료를 통해 감정을 이해하므로써, 마음의 안정을 찾는 데 기여할 수 있습니다. 이러한 인문학적 접근을 기반으로, 사용자와 더욱 깊은 공감을 이끌어내는 것을 목표로 합니다.

#### 프로젝트 주제 선정 배경 및 소개
[LangChain 기반 감정 분석 및 인문학적 대화 프로젝트 소개.pdf](https://github.com/user-attachments/files/18011253/LangChain.pdf)

---

## 주요 기능

### 1. 세밀한 감정 분석
Hugging Face의 Fine-tuned 모델을 활용하여 사용자의 감정을 세밀하게 분석합니다. 사용자 텍스트의 맥락을 고려해 감정을 분류하며, 파인튜닝 과정을 통해 한국어 텍스트 분석에 최적화된 성능을 발휘합니다.

### 2. 인문학적 자료 추천
분석된 감정에 따라 문학, 예술, 음악 등 다양한 인문학적 자료를 추천합니다. 이 자료는 사용자에게 위로와 통찰을 제공하며, 정신 건강 관리에 도움을 줄 수 있도록 설계되었습니다.

### 3. 공감 기반 대화 생성
LangChain을 기반으로 사용자의 입력에 따라 공감 중심의 대화를 생성합니다. 대화의 맥락을 유지하며, 친근하지만 진지한 어조로 응답을 제공합니다.

### 4. RAG (Retrieval-Augmented Generation) 시스템 확장
Pinecone 기반 문서 검색과 LangChain의 히스토리 관리 기능을 활용하여, 사용자의 질문에 적합한 정보를 검색하고 응답합니다. 

---

## 설치 및 실행 방법

### 요구 사항
- Python >= 3.8
- Hugging Face Transformers
- LangChain 및 관련 라이브러리
- Pinecone 계정 및 API 키
- OpenAI API 키

### 설치 과정
1. **프로젝트 클론**
   ```bash
   git clone [저장소 URL]
   cd [저장소 이름]
2. 필요 라이브러리 설치
   pip install -r requirements.txt
3. 환경 변수 설정
   PINECONE_API_KEY=your_pinecone_key
   OPENAI_API_KEY=your_openai_key
4. 프로그램 실행
   python main.py

## 세부 기술 설명

### Hugging Face 모델 파인튜닝
이 프로젝트에서는 Hugging Face의 Transformers 라이브러리를 사용해 감정 분석 모델을 파인튜닝했습니다.

- 데이터: 한국어 텍스트 기반의 감정 데이터셋을 수집하고 전처리하여 학습 데이터를 구성하였습니다.
- 모델: distilbert-base-multilingual-cased와 같은 멀티링구얼 모델을 초기화하여 세밀한 감정 분류를 위한 파인튜닝을 진행하였습니다.
- 파인튜닝 과정: 사용자 텍스트를 5가지 이상의 감정(예: 행복, 슬픔, 분노 등)으로 분류할 수 있도록 학습했으며, 이를 통해 보다 개인화된 분석이 가능하게 되었습니다.
### LangChain 기반 RAG 시스템
LangChain의 Retrieval-Augmented Generation(RAG) 시스템을 확장하여 사용자 입력을 이해하고 맥락에 맞는 정보를 제공합니다. Pinecone 기반 검색을 통해 빠르고 정확한 결과를 도출하며, 이를 대화 응답에 반영합니다.

### 인문학적 자료 추천
감정 분석 결과에 따라 추천되는 자료는 철학, 문학, 예술, 음악 등 다양한 인문학적 콘텐츠로 구성됩니다. 이러한 자료는 사용자의 감정을 이해하고 스스로 마음의 안정을 찾을 수 있는 계기를 제공합니다.

## 프로젝트 구조
```
프로젝트 디렉토리 구조
├── .vscode/                     # Visual Studio Code 설정 디렉토리
├── for_you/                     # 메인 프로젝트 디렉토리
│   ├── __pycache__/             # 파이썬 캐시 디렉토리
│   ├── .devcontainer/           # Dev Container 설정 디렉토리
│   ├── venv/                    # 가상 환경 디렉토리
│   ├── .gitignore               # Git 제외 파일 설정
│   ├── .python-version          # 파이썬 버전 관리 파일
│   ├── config.py                # 
│   ├── for_streamlit.ipynb      # Streamlit 관련 Jupyter 노트북
│   ├── foryou.code-workspace    # VSCode 워크스페이스 설정
│   ├── humanities.pdf           # 인문학 관련 PDF 자료(2024 세계 인문학 포럼 자료)
│   ├── llm.py                   # LangChain 기반 주요 기능
│   ├── main.py                  # 메인 실행 파일
│   ├── README.md                # 프로젝트 설명 파일
│   ├── requirements.txt         # 프로젝트 의존성 파일
│   ├── test.py                  # 파인튜닝한 허깅페이스 모델의 성능 평가 파일
│   ├── Untitled-1.ipynb         # 기본 설정을 위한 Jupyter 노트북
│   ├── upload_hf.py             # 학습 완료 후 Hugging Face 모델 업로드 스크립트
├── .env                         # 환경 변수 설정 파일
├── ai_image.jpg                 # AI 프로필 이미지
├── inmoon.docx                  # Pinecone 데이터 적재 파일
├── user.jpg                     # 사용자 프로필 이미지

```
## 사용된 오픈소스 및 라이브러리
### LangChain
출처: [LangChain GitHub](https://github.com/langchain-ai/langchain)

주요 사용 기능: 대화 히스토리 관리, 문서 검색, RAG 시스템
### Hugging Face Transformers
출처: [Hugging Face GitHub](https://github.com/huggingface/transformers)

주요 사용 기능: 감정 분석 모델 로드 및 실행
### Pinecone
출처: https://www.pinecone.io/

주요 사용 기능: 고속 문서 검색 및 텍스트 임베딩
### OpenAI API
출처: [OpenAI API](https://platform.openai.com/docs/overview)

## Hugging Face 모델 파인튜닝 및 업로드

### 데이터셋 준비

이 프로젝트는 AI 허브에서 제공하는 **한국어 감정 데이터셋**을 기반으로 Hugging Face 모델을 파인튜닝하였습니다.  
- **데이터셋 출처**: [AI 허브 한국어 감정 데이터셋](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71603)
- **데이터 구성**: 다양한 감정(예: 행복, 슬픔, 분노 등)과 관련된 한국어 텍스트가 포함되어 있으며, 감정 레이블이 사전 정의되어 있습니다.
- **전처리 과정**: 텍스트 정규화 및 레이블 인코딩을 통해 모델 학습에 적합한 형태로 데이터셋을 준비하였습니다.

---

### 모델 파인튜닝

한국어 자연어 처리에 특화된 Hugging Face의 **beomi/KcBERT-base** 모델을 선택하여 감정 분석 모델로 파인튜닝을 진행했습니다.

- **모델 출처**: [beomi/KcBERT-base](https://huggingface.co/beomi/KcBERT-base)
- **프레임워크**: Hugging Face Transformers
- **학습 환경**: 
  - GPU 환경에서 학습
  - 학습률, 배치 크기 등 하이퍼파라미터 최적화
- **학습 목표**: 감정 분석을 위한 다중 분류 문제 해결
  - 레이블: 행복, 슬픔, 분노, 두려움, 중립 등  

#### 학습 코드 (요약)

### Hugging Face 허브 업로드
파인튜닝된 모델은 Hugging Face 허브에 업로드하여 로컬 환경 설정 없이 누구나 쉽게 사용할 수 있도록 하였습니다.

모델 업로드 경로: https://huggingface.co/alsgyu/sentiment-analysis-fine-tuned-model/tree/main

### 모델 활용의 이점

접근성: Hugging Face 허브에 업로드되어 로컬 환경 없이 간편하게 사용 가능합니다.
한국어 감정 분석 특화: AI 허브 데이터셋과 KcBERT 모델로 학습하여 한국어 텍스트에 높은 성능 보장합니다.
확장 가능성: 다양한 응용 프로그램 및 서비스에 손쉽게 통합 가능합니다.

### 참고 자료

Hugging Face 허브: https://huggingface.co
AI 허브 데이터셋: https://www.aihub.or.kr

## Pinecone 데이터 적재
이 프로젝트에서는 Pinecone을 활용하여 인문학 자료를 효율적으로 사용할 수 있는 시스템을 구축하였습니다. 주요 철학적 관점과 자료를 임베딩하여 사용자의 감정에 필요한 인문학 자료를 신속하게 제공할 수 있도록 설계되었습니다.

### 적재된 주요 자료
- 스토아학파 주요 철학
- 실존주의 주요 철학
- 세계인문학포럼 자료

## 보안 및 개인정보 보호
이 프로젝트는 보안과 개인정보 보호를 중요하게 고려하여 설계되었습니다.

- 최신 보안 패치가 적용된 라이브러리를 사용합니다.
- API 키는 .env 파일을 통해 안전하게 관리됩니다.
- 사용자 입력 데이터는 대화 세션 동안만 유지되며 외부에 저장되지 않습니다.

## 기여 및 문의
오픈소스 커뮤니티와의 협력을 환영합니다!
Pull Request: 새로운 기능 추가나 버그 수정을 제안해 주세요.

## 프로젝트의 목적

기술적 도구와 인문학적 접근을 결합하여 사용자에게 감정적, 정신적 도움 제공을 목표로 합니다. 
이를 통해 인문학이 우리의 정신 건강에 긍정적인 영향을 미칠 수 있음을 증명하고자 합니다.

