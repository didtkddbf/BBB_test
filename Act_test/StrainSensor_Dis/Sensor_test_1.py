import time
from time import sleep
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP2
from Adafruit_AMG88xx import Adafruit_AMG88xx

myEncoder = RotaryEncoder(eQEP2)
myEncoder.enable()
sensor = Adafruit_AMG88xx(address=0x69, busnum=2)

ADC.setup()
analogPin="P9_40"

Act = 'P8_13'
Act_dirA = 'P8_14'
Act_dirB = 'P8_15'
Fan = 'P8_9'

#Fann = 'P8_15'

GPIO.setup(Act_dirA, GPIO.OUT)
GPIO.setup(Act_dirB, GPIO.OUT)
GPIO.setup(Fan, GPIO.OUT)
#GPIO.setup(Act, GPIO.OUT)

PWM.start(Act, 0, 1000)

GPIO.output(Act_dirA, GPIO.HIGH)
#GPIO.output(Act, GPIO.LOW)
GPIO.output(Act_dirB, GPIO.LOW)
GPIO.output(Fan, GPIO.HIGH)
#GPIO.output(Fann, GPIO.HIGH)


f = raw_input('file name : ')
filename = f + '.txt'
tdata = open(filename, 'a+')

tdata.write("Test start,start,start,start,start\n")
a=0
R = 0
global pwm
pwm = 20

#main function
while a!=4:
    a = int(input('act=1, cool=2, cycle=3, stop=4, zero=5, PWMset=6 '))

    if a==1:
        c = int(input('heating time(s) : '))
        b = c*10+1
        tdata.write("Cal_Disp(mm),Temperature('c),Resistance(ohm),Time(s) \n")
        for count in range(1,b):
            PWM.set_duty_cycle(Act, pwm)
            distance = myEncoder.position * 0.02
            temp = max(sensor.readPixels())
#            Vr=ADC.read(analogPin)
#            R=10000*Vr/(1.8-Vr)
            print("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            tdata.write("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            time.sleep(0.1)
        PWM.set_duty_cycle(Act, 0)
        for count in range(b,b+1):
            distance = myEncoder.position * 0.02
            temp = max(sensor.readPixels())
#            Vr=ADC.read(analogPin)
#            R=10000*Vr/(1.8-Vr)
            print("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            tdata.write("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            time.sleep(0.1)

    elif a==2:
        c = int(input('cooling time(s) : '))
        b = c*5+1
        GPIO.output(Fan, GPIO.LOW)
        tdata.write("Cal_Disp, mm, Sen_Disp, mm, Temperature, 'c, Time, s \n")
        for count in range(1,b):
            distance = myEncoder.position * 0.02
            temp = max(sensor.readPixels())
            GPIO.output(Fan, GPIO.LOW)
            Vr=ADC.read(analogPin)
            R=99.00*Vr/(1.8-Vr)
            print("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            tdata.write("%.2f,%d,%d,%.1f\n" % (distance, temp, R, count * 0.1))
            time.sleep(0.1)
        GPIO.output(Fan, GPIO.HIGH)

    elif a==3:
        ht = int(input('High disp : '))
        ct = int(input('Low disp : '))
        cy = int(input('cycle number : '))
        tdata.write("Cal_Disp(mm),Temperature('c),Resistance(Ohm),Time(s),Cycle(n) \n")
        distance = 0.00
        count = 0.00
        temp = 0.00
        R = 0.00
        for cycle in range(1, cy):
            while distance < ht:
                PWM.set_duty_cycle(Act, pwm)
                distance = -myEncoder.position * 0.02
                temp = max(sensor.readPixels())
                Vr = ADC.read(analogPin)
                R = 99.00 * Vr / (1.80 - Vr)
                count = count+1
                print("%.2f,%.2f,%.2f,%.1f,%d" % (distance, temp, R, count * 1, cycle))
                tdata.write("%.2f,%.2f,%.2f,%.1f,%d\n" % (distance, temp, R, count * 1, cycle))
                time.sleep(0.1)
            PWM.set_duty_cycle(Act, 0)
            while distance > ct:
                GPIO.output(Fan, GPIO.LOW)
                distance = -myEncoder.position * 0.02
                temp = max(sensor.readPixels())
                Vr = ADC.read(analogPin)
                R = 99.00* Vr / (1.8 - Vr)
                count = count+1
                print("%.2f,%.2f,%.2f,%.1f,%d" % (distance, temp, R, count * 1, cycle))
                tdata.write("%.2f,%.2f,%.2f,%.1f,%d\n" % (distance, temp, R, count * 1, cycle))
                time.sleep(0.1)
            GPIO.output(Fan, GPIO.HIGH)
            PWM.set_duty_cycle(Act, 0)
    elif a==5:
        myEncoder.zero()
    elif a==6:
        pwm = int(input('PWM value(1~100) : '))
    elif a==7:
        print(pwm)


PWM.stop("P8_13")
PWM.cleanup()
GPIO.cleanup()
tdata.close()

