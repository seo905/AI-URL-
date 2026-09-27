# 🛡️ AI 기반 피싱 URL 탐지 및 위험 분석 시스템

URL의 정적 특성(Feature)을 기반으로 XGBoost 모델을 통해 피싱 확률을 계산하고, 위험도(정상 / 피싱 의심 / 악성)를 분류하는 머신러닝 모듈입니다.
파이썬 버전 3.10.x 이상으로 실행

---

## 1. 터미널 실행 방법 (Quick Start)

### Step 1. 가상환경 생성 및 활성화
```bash
# 가상환경 생성 (최초 1회)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS / Linux)
source venv/bin/activate

* 패키지 설치 및 업데이트
python -m pip install --upgrade pip
```
### Step 2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

### Step 3. XGBoost 모델 학습 및 .pkl 저장
```bash
python train_model.py
실행 시 model/xgboost_model.pkl 경로에 학습된 모델 파일이 생성됩니다.
```

### Step 4. 예측 모듈 테스트 실행
```bash
python ml_model.py
샘플 데이터를 통한 정상, 의심, 악성 URL 예측 결과가 터미널에 출력됩니다.
```

## 2. 프로젝트 디렉토리 구조
```bash
phishing-url-detection/
├── model/
│   └── xgboost_model.pkl   # 학습 완료된 XGBoost 모델 파일
├── train_model.py          # 데이터셋 준비 및 모델 학습/저장 스크립트
├── ml_model.py             # 피처를 받아 피싱 확률 및 위험도를 반환하는 모듈
└── requirements.txt       # 프로젝트 의존성 라이브러리 목록
```

## 3. 주요 모듈 및 예측 함수 사용법
```bash
ml_model.predict(features)
입력받은 피처(dict)를 기반으로 피싱 확률 및 예측 결과를 반환합니다.

입력 예시 (Input)
from ml_model import predict

features = {
    "url_length": 30,
    "keyword_count": 1
}

result = predict(features)
print(result)

출력 예시 (Output)
{
    "prediction": "phishing",
    "probability": 0.85
}
```
