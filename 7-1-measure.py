
import RPi.GPIO as GPIO
import time
from matplotlib import pyplot

GPIO.setmode(GPIO.BCM)

leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac  = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

comp = 14
troyka = 13

GPIO.setup(troyka, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)

def GetBin(volt_value):
    return [int (elem) for elem in bin(volt_value)[2:].zfill(8)]

def adc():
    value = 128
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 128

    value += 64
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 64

    value += 32
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 32


    value += 16
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 16

    value += 8
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 8

    value += 4
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 4

    value += 2
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 2

    value += 1
    GPIO.output(dac, GetBin(value))
    time.sleep(0.005)
    if (GPIO.input(comp)):
        value -= 1

    return value

data_value = []
All_time = 0
try:
    volt = 0
    NumOfExperiment = 0

    GPIO.output(troyka, 1)
    Begin = time.time()
    while volt < 207:
        volt = adc()
        print(volt)
        data_value.append(volt) 
        NumOfExperiment += 1
        GPIO.output(leds, GetBin(volt))
        time.sleep(0.01)
    print('gadost')
    GPIO.output(troyka, 0)

    while volt > (166):
        volt = adc()
        print(volt)
        data_value.append(volt)
        NumOfExperiment += 1
        GPIO.output(leds, GetBin(volt))
        All_time = time.time()
        All_time -= Begin
        time.sleep(0.01)
    
    with open("data.txt", 'w') as f:
        for value in data_value:
            f.write(str(value) + '\n')

    with open("settings.txt", 'w') as f:
        f.write(str(NumOfExperiment / All_time) + '\n')

    print("Общее время эксперимента: {}".format(All_time))
    print("Период: {}".format(All_time / NumOfExperiment))
    print("Средняя частота дискретизации: {}".format(NumOfExperiment / All_time))
    print("Шаг квантования: {}".format(3.3/255))

    y = [i / 255 * 3.3 for i in data_value]
    x = [i * All_time / NumOfExperiment for i in range(NumOfExperiment)]

    pyplot.plot(x, y)
    pyplot.show()

finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
