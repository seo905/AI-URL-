# train_model.py
import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

def train_and_save_model():
    # 1. 모델 저장 디렉토리 생성
    os.makedirs("model", exist_ok=True)
    model_path = os.path.join("model", "xgboost_model.pkl")

    # 2. 샘플 데이터셋 준비 (가상 피처 생성)
    np.random.seed(42)
    n_samples = 1000

    url_length = np.random.randint(10, 150, n_samples)
    keyword_count = np.random.randint(0, 5, n_samples)
    dot_count = np.random.randint(1, 6, n_samples)
    has_ip = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])
    num_subdomains = np.random.randint(0, 4, n_samples)

    # 피싱 확률에 가중치를 두어 라벨 생성
    score = (url_length > 60)*2.0 + keyword_count*1.5 + dot_count*1.0 + has_ip*3.0 + num_subdomains*1.2
    prob = 1 / (1 + np.exp(-(score - 6)))
    y = (prob > 0.5).astype(int)

    X = pd.DataFrame({
        "url_length": url_length,
        "keyword_count": keyword_count,
        "dot_count": dot_count,
        "has_ip": has_ip,
        "num_subdomains": num_subdomains
    })

    # 3. XGBoost 모델 학습
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    model.fit(X, y)

    # 4. 모델 및 피처 정보 딕셔너리로 저장
    save_data = {
        "model": model,
        "feature_names": list(X.columns)
    }
    
    joblib.dump(save_data, model_path)
    print(f"✅ 모델 학습 완료! '{model_path}' 저장 성공")

if __name__ == "__main__":
    train_and_save_model()