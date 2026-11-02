import numpy as np
from collections import deque

# ==========================================
# [파트 2] 데이터 전처리 모듈
# ==========================================
# 시계열 특징 추출을 위한 버퍼 (최근 5초치 데이터 저장)
buffer_size = 5
radar_motion_buffer = deque(maxlen=buffer_size)
radar_still_buffer = deque(maxlen=buffer_size)

def extract_features(pir_val, motion_val, still_val):
    """
    수신된 원시 데이터를 버퍼에 누적하고, 머신러닝 학습에 필요한 통계적 특징(평균, 표준편차)을 추출합니다.
    """
    radar_motion_buffer.append(motion_val)
    radar_still_buffer.append(still_val)
    
    # 버퍼가 아직 채워지지 않은 초기 상태
    if len(radar_motion_buffer) < buffer_size:
        return [pir_val, 0.0, 0.0, 0.0, 0.0]
    
    motion_mean = np.mean(radar_motion_buffer)
    motion_std = np.std(radar_motion_buffer)
    still_mean = np.mean(radar_still_buffer)
    still_std = np.std(radar_still_buffer)
    
    # 모델 입력 형태로 반환 [PIR, 동적평균, 동적표준편차, 정적평균, 정적표준편차]
    return [pir_val, motion_mean, motion_std, still_mean, still_std]