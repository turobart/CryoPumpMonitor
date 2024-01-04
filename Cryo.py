#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import serial
import time
from datetime import datetime


def log_cryo_data():
    ser = serial.Serial('/dev/ttyS0', 9600,
                        parity=serial.PARITY_NONE, 
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
     
    comm='T\r' # command for the T readout
    encodec_command=comm.encode()

    now_date = ''
    while(True):
        now_is=datetime.now()
        now_date=now_is.strftime("%m%d%y")
        current_time = str(now_is.time().strftime("%H:%M:%S"))
        ser.write(encodec_command)
        time.sleep(2)
        if ser.in_waiting>0:
            try:
                raw_data=ser.read(ser.in_waiting).strip()[2:]
            except:
                continue
            data = ''
            # fix answer encoding
            for ch in raw_data:
                if(ch == '\xb0'):
                    ch = '0'
                elif(ch == '\xb1'):
                    ch = '1'
                elif(ch == '\xb2'):
                    ch = '2'
                elif(ch == '\xb3'):
                    ch = '3'
                elif(ch == '\xb4'):
                    ch = '4'
                elif(ch == '\xb5'):
                    ch = '5'
                elif(ch == '\xb6'):
                    ch = '6'
                elif(ch == '\xb7'):
                    ch = '7'
                elif(ch == '\xb8'):
                    ch = '8'
                elif(ch == '\xb9'):
                    ch = '9'    
                elif (ch == '\xae'):
                    ch = '.'
                elif(ch == '\x8d'):
                    ch = ''
                elif(ch == 'T'):
                    ch = ''
                elif(ch == '\x22'):
                    ch = ''
                elif(ch == '\xd4'):
                    ch = ''
                elif(ch == '\x0d'):
                    break
                data += ch
            
            if len(data)<3: continue
            print(current_time, data)
                    
            with open(now_date+'.txt','a') as f:
                full_log = current_time + "\t" + data
                f.write(full_log)
                f.write('\n')
        time.sleep(28)

log_cryo_data()