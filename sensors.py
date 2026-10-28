import time
import numpy as np
import RPi.GPIO as GPIO
import serial
import joblib
from collections import deque

# ==========================================
# [파트 1] 센서 데이터 수신 모듈
# ==========================================
def read_sensors(radar_serial, pir_pin=17):
    """
    라즈베리파이 GPIO 및 UART 통신을 통해 센서의 원시 데이터(Raw Data)를 읽어옵니다.
    """
    # 1. PIR 센서 읽기
    pir_val = GPIO.input(pir_pin)
    
    # 2. 레이더 센서 읽기 (예시 파싱)
    radar_motion_val = 0
    radar_still_val = 0
    if radar_serial and radar_serial.in_waiting > 0:
        try:
            line = radar_serial.readline().decode('utf-8').strip()
            parts = line.split(',')
            if len(parts) == 2:
                radar_motion_val = int(parts[0])
                radar_still_val = int(parts[1])
        except Exception as e:
            print(f"[수신 오류] {e}")
            
    return pir_val, radar_motion_val, radar_still_val