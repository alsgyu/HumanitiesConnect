# 마음의 길잡이: 감정 분석과 인문학적 공감을 통한 AI 솔루션
---
## 프로젝트 개요
이 프로젝트는 **LangChain** 오픈소스를 기반으로, 감정 분석 기능과 인문학적 통찰을 결합하여 공감 중심의 대화형 AI 시스템을 구현한 것입니다. 세밀한 감정 분석을 위해 Hugging Face 모델을 파인튜닝하였으며, 이를 통해 사용자의 감정을 보다 정확히 분석할 수 있습니다. 또한, 인문학적 자료와 통찰을 활용해 정신 건강 관리에 도움을 줄 수 있는 대화를 제공합니다. 또한 Pinecone의 벡터 데이터베이스를 자료 적재에 활용함으로써, 인문학적 자료에 대한 고속 검색이 가능하며, 이를 통해 사용자에게 적합한 자료와 통찰을 실시간으로 제공합니다.

#### 프로젝트 주제선정 배경 및 소개
- [alsgyu chat_humanity.pdf](https://github.com/user-attachments/files/18023472/alsgyu.chat_humanity.pdf)
<br/>

이 프로젝트는 오픈소스를 기반으로 시작되었고, Streamlit을 기반으로 사용자 인터페이스가 설계되었습니다.<br/>

**오픈소스 출처** : https://github.com/jasonkang14/streamlit-korean-income-tax-rag<br/>
**활용 내용**: LangChain 및 Pinecone 기반 검색 시스템을 활용하였습니다.

---
## 프로젝트의 목적

기술적 도구를 인문학적 접근과 결합하여 사용자에게 정신적 도움 제공을 제공하고자 하였습니다. 
이를 통해 인문학이 우리의 정신 건강에 긍정적인 영향을 미칠 수 있음을 보여주고 싶습니다.

---

## 주요 기능

### 1. 세밀한 감정 분석
Hugging Face의 한국어 모델을 파인튜닝한 후 활용하여 사용자의 감정을 더욱 세밀히 분석합니다. 사용자 텍스트의 맥락을 고려해 감정을 분류하여, 한국어 텍스트에 더욱 세밀하게 감정을 분석할 수 있도록 합니다.

### 2. 인문학적 자료 추천
분석된 감정에 따라 문학, 예술, 음악 등 다양한 인문학적 자료를 추천합니다. 이 자료는 사용자에게 위로와 통찰을 제공하며, 정신 건강 관리에 도움을 줄 수 있도록 설계되었습니다.

### 3. 공감 기반 대화 생성
LangChain을 기반으로 사용자의 입력에 따라 공감 중심의 대화를 생성합니다. 대화의 맥락을 유지하며, 친근하지만 진지한 어조로 응답을 제공합니다.

### 4. RAG 시스템 확장
LangChain의 Retrieval-Augmented Generation 시스템을 확장하여 Few-Shot Prompting을 활용, Pinecone 기반 검색과 맥락 학습을 결합합니다. 이를 통해 사용자의 입력을 이해하고 학습에 기반한 유사한 맥락에서 더욱 적절한 정보를 생성합니다.  

---
## 활용된 오프소스 라이브러리
이 프로젝트는 여러 오픈소스 라이브러리를 활용함으로써 개발할 수 있었습니다.

### Hugging FaceTransformers
한국어 감정 분석 모델을 파인튜닝하고 감정 상태를 분석하기 위해 사용되었습니다.
### LangChain
대화 흐름 설계와 Retrieval-Augmented Generation 시스템의 확장을 통해 공감 기반의 대화를 생성할 수 있었습니다.
### Pinecone
대규모 벡터 데이터베이스를 사용하여 인문학 자료를 검색하고 적합한 자료를 찾아 사용자에게 추천할 수 있었습니다.
### OpenAI API
OpenAI를 활용하여 대화의 자연스러움과 응답의 품질을 개선하였습니다.
### Streamlit
사용자 친화적인 UI/UX를 제공하면서 간결하고 직관적인 웹 인터페이스를 구현할 수 있었습니다.

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
   git clone https://github.com/alsgyu/HumanitiesConnect.git
   cd HumanitiesConnect
2. 가상환경 생성과 사용
   ```bash
   python -m venv venv
   venv\Scripts\activate

4. 필요 라이브러리 설치
   ```bash
   pip install -r requirements.txt
5. 환경 변수 설정
   ```bash
   PINECONE_API_KEY=your_pinecone_key
   OPENAI_API_KEY=your_openai_key
6. 프로그램 실행
   ```bash
   streamlit run main.py
   
### Streamlit을 활용한 배포
화면 확대 비율을 90%로 맞춰주시면 더욱 깔끔하게 이용하실 수 있습니다.
- https://alsgyu-humanitiesconnect.streamlit.app/

현재 pinecone과 streamlit간의 연동 오류가 있어 원활한 실행이 되지 않습니다. 계속해서 수정해나가겠습니다.

### 프로젝트 구조
```
프로젝트 주요 디렉토리 구조           
├── for_you/                     # 메인 프로젝트 디렉토리
│   ├── venv/                    # 가상 환경 디렉토리
│   ├── config.py                # 구체적이고 문맥적인 답변을 위한 Few-Shot Prompting
│   ├── llm.py                   # LangChain 기반 주요 기능
│   ├── main.py                  # 메인 실행 파일
│   ├── README.md                # 프로젝트 설명 파일
│   ├── requirements.txt         # 프로젝트 의존성 파일
│   ├── test.py                  # 파인튜닝한 허깅페이스 모델의 성능 평가 파일
├── .env                         # 환경 변수 설정 파일
├── inmoon.docx                  # Pinecone 데이터 적재 파일
```
---
## 세부 준비 과정

### 감정 분석을 위한 데이터셋 준비

이 프로젝트는 AI 허브에서 제공하는 한국어 감정 데이터셋을 기반으로 Hugging Face 모델을 파인튜닝하였습니다.  
- 데이터셋 출처: [AI 허브 한국어 감정 데이터셋](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71603)
- 데이터 구성: 다양한 상황에서 감정과 관련된 한국어 텍스트가 포함되어 있으며, 감정 레이블이 정의되어 있습니다.
- 전처리 과정: 텍스트 정규화 및 레이블 인코딩을 통해 모델 학습에 적합한 형태로 데이터셋을 준비하였습니다.


### 모델 파인튜닝

한국어 자연어 처리에 특화된 Hugging Face의 **beomi/KcBERT-base** 모델을 선택하여 감정 분석 모델로 파인튜닝을 진행하였습니다.

- 모델 출처: [beomi/KcBERT-base](https://huggingface.co/beomi/KcBERT-base)
- 프레임워크: Hugging Face Transformers
- 학습 목표: 감정 분석을 위한 한국어 텍스트 감정 분류


### 학습 코드
주피터 노트북을 이용한 학습코드 https://github.com/alsgyu/finetunning_huggingface


### Hugging Face 허브 업로드
파인튜닝된 모델은 Hugging Face 허브에 업로드하여 로컬 환경 설정 없이 간편히 사용할 수 있도록 하였습니다.<br/>
업로드 경로: https://huggingface.co/alsgyu/sentiment-analysis-fine-tuned-model/tree/main


### Pinecone의 데이터 적재
Pinecone을 활용하여 인문학 자료를 효율적으로 사용할 수 있는 시스템을 구축하였습니다. 주요 철학적 관점과 자료를 임베딩하여 사용자의 감정에 필요한 인문학 자료를 신속하게 제공할 수 있도록 설계되었습니다.
- 스토아학파 주요 철학: 내적 평온과 윤리적 삶을 강조  
- 실존주의 주요 철학: 개인의 자유와 책임, 존재의 의미에 대한 탐구  
- 세계인문학포럼 자료: 현대 사회 문제 해결을 위한 인문학적 통찰
<br/>

---
## 보안 및 개인정보 보호
보안과 개인정보 보호를 고려하여 설계되었습니다.

- 최신 보안 패치가 적용된 라이브러리를 사용합니다.
- API 키는 .env 파일을 통해 안전하게 관리됩니다.
- 사용자 입력 데이터는 대화 세션 동안만 유지되며 외부에 저장되지 않습니다.

---

## 프로젝트 기여
이 프로젝트는 MIT License를 따르며, 누구나 자유롭게 사용, 수정, 배포할 수 있습니다. 프로젝트의 발전을 위해 여러분의 기여를 언제나 환영합니다!<br/>
새로운 아이디어나 개선했으면 하는 부분이 있다면 GitHub Issues를 통해 알려주시거나, Pull Request를 보내주세요. 감사합니다.

---

