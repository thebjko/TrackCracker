from django.dispatch import Signal

# save, delete 후 achievement를 다시 계산하기 위한 시그널
# Task 모델 클래스의 save, delete 메서드에서 해당 시그널을 보낸다.
custom_signal = Signal()