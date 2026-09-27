# ml_model.py
import os
import joblib
import pandas as pd

# 모델 경로 정의
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "xgboost_model.pkl")

# 메모리 효율성을 위한 모델 객체 글로벌 캐싱
_MODEL = None
_FEATURE_NAMES = None


def _load_model():
    """모델 파일이 로드되어 있지 않다면 최초 1회 로드합니다."""
    global _MODEL, _FEATURE_NAMES
    if _MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"모델 파일이 존재하지 않습니다: '{MODEL_PATH}'\n먼저 train_model.py를 실행하여 모델을 생성하세요."
            )
        
        saved_data = joblib.load(MODEL_PATH)
        if isinstance(saved_data, dict):
            _MODEL = saved_data["model"]
            _FEATURE_NAMES = saved_data.get("feature_names", None)
        else:
            _MODEL = saved_data
            _FEATURE_NAMES = getattr(_MODEL, "feature_names_in_", None)


def predict(features: dict) -> dict:
    """
    Feature를 전달받아 XGBoost 모델 기반으로 피싱 확률을 계산하고 분류 결과를 반환합니다.

    [입력형식]
    {
        "url_length": 30,
        "keyword_count": 1
    }

    [출력형식]
    {
        "prediction": "phishing",  # "safe", "suspicious", "phishing"
        "probability": 0.85
    }
    """
    _load_model()

    # 입력 피처를 DataFrame으로 변환
    input_df = pd.DataFrame([features])

    # 학습할 때 사용한 피처와 맞추고 누락된 피처는 0으로 보완
    if _FEATURE_NAMES is not None:
        for feat in _FEATURE_NAMES:
            if feat not in input_df.columns:
                input_df[feat] = 0
        input_df = input_df[_FEATURE_NAMES]

    # 피싱(Class 1) 예측 확률 계산
    probabilities = _MODEL.predict_proba(input_df)[0]
    phishing_prob = float(probabilities[1])  # 피싱 확률 추출

    # 3단계 위험도 분류 임계값 (Threshold) 기준
    # - prob < 0.35 : 정상 URL (safe)
    # - 0.35 <= prob < 0.70 : 피싱 의심 URL (suspicious)
    # - prob >= 0.70 : 악성 URL (phishing)
    if phishing_prob >= 0.70:
        prediction_status = "phishing"      # 악성 URL
    elif phishing_prob >= 0.35:
        prediction_status = "suspicious"    # 피싱 의심 URL
    else:
        prediction_status = "safe"          # 정상 URL

    return {
        "prediction": prediction_status,
        "probability": round(phishing_prob, 2)
    }


# 단체 테스트 실행 코드
if __name__ == "__main__":
    # 테스트 케이스 1: 정상 URL 피처
    input_safe = {
        "url_length": 25,
        "keyword_count": 0,
        "dot_count": 1,
        "has_ip": 0,
        "num_subdomains": 0
    }

    # 테스트 케이스 2: 요청하신 예시 입력
    input_example = {
        "url_length": 30,
        "keyword_count": 1
    }

    # 테스트 케이스 3: 악성 URL 피처
    input_phishing = {
        "url_length": 130,
        "keyword_count": 3,
        "dot_count": 4,
        "has_ip": 1,
        "num_subdomains": 2
    }

    print("=== 예측 실행 테스트 ===")
    print("1. 정상 URL 예시:", predict(input_safe))
    print("2. 사용자 입력 예시:", predict(input_example))
    print("3. 악성 URL 예시:", predict(input_phishing))
