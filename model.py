# ==========================================
# [파트 3] 인공지능 추론(판단) 모듈
# ==========================================
def predict_occupancy(model, features):
    """
    학습된 AI 모델(.pkl)을 활용하여 전처리된 특징 데이터로부터 재실 여부(0 또는 1)를 판단합니다.
    """
    if features[1] == 0.0 and features[2] == 0.0:
        return 0  # 초기 데이터 부족 시 빈 방 처리
        
    input_data = np.array(features).reshape(1, -1)
    prediction = model.predict(input_data)
    
    return int(prediction[0])