import RPi.GPIO as GPIO
import time
import math
def decimal2binary(value):
    return [int(bit) for bit in format(value, 'b').zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(leds, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = 1)

def adc():
    result_bin = [0 for i in range(8)]
    #volums = [0, 1, 3, 7, 15, 31, 63, 127, 255]


    result = 0

    for i in range(8):
        result_bin[i] = 1
        GPIO.output(dac, result_bin)
        time.sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val == 0:
            result += 2**(7-i)
        else:
            result_bin[i] = 0
    
    index = 0
    for i in range(math.ceil((result/256)*8)):
        index += 2**i
    return index#volums[math.ceil((result/256)*8)]
    
try:
    while True:
        var = adc()
        #print(var)
        GPIO.output(leds, decimal2binary(var))
        #voltage = var*3.3/256
        #print(f"Voltage: {voltage: .4}V")

  
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
