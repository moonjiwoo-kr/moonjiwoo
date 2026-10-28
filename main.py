# ==========================================
# [파트 4] 제어 및 메인 루프 모듈
# ==========================================
def control_relay(is_occupied, relay_pin=22):
    """
    AI 판단 결과에 따라 릴레이 모듈을 구동하여 외부 기기(조명 등)를 제어합니다.
    """
    if is_occupied == 1:
        GPIO.output(relay_pin, GPIO.HIGH)
        print("[제어] 사람 감지 -> 💡 조명 ON")
    else:
        GPIO.output(relay_pin, GPIO.LOW)
        print("[제어] 빈 방 -> 🌑 조명 OFF")

def main():
    # 초기 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.IN)                 # PIR 핀
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) # 릴레이 핀
    
    # AI 모델 로드
    try:
        ai_model = joblib.load('ai_model.pkl')
        print("AI 모델 로드 완료.")
    except Exception as e:
        print(f"AI 모델 로드 실패: {e}")
        return

    # 레이더 시리얼 포트 연결
    try:
        radar_serial = serial.Serial('/dev/serial0', 256000, timeout=1)
    except:
        radar_serial = None

    print("🚀 실시간 재실 감지 메인 루프 시작")
    try:
        while True:
            # 1. 센서 데이터 수신 파트
            pir, motion, still = read_sensors(radar_serial)
            
            # 2. 데이터 전처리 파트
            features = extract_features(pir, motion, still)
            
            # 3. AI 추론(판단) 파트
            is_occupied = predict_occupancy(ai_model, features)
            
            # 4. 제어 파트
            control_relay(is_occupied)
            
            time.sleep(1) # 1초 주기 반복
            
    except KeyboardInterrupt:
        print("\n시스템 종료 중...")
    finally:
        GPIO.cleanup()
        if radar_serial and radar_serial.is_open:
            radar_serial.close()

if __name__ == "__main__":
    main()