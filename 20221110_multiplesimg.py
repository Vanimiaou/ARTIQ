
# -*- coding: utf-8 -*-
"""Rydberg transition. 
@author: Van
"""
from artiq.experiment import *
import numpy as np
import datetime 

ExpSettings=[]



#Laser settings
CoolingRF=108.5*MHz
DetectionRF=106*MHz
RepumpVVA=5.8
CoolingVVA=6.5
#coil
AHcoil=-2.7
BiasX=0.023
BiasY=0.01
BiasZ=0.02
threshold=18
meas_time_load=1*ms
DACScaleFactor=0.05 #Volt/count
scanP=100.0


#SD cooling
Bx_SDcool=0.025
By_SDcool=0.0
Bz_SDcool=0.0
RepumpVVA_SDcool=4.0
CoolingVVA_SDcool=6.0
SDhold=1*ms
SDholdVVA=1.35
SDcoolRF=111*MHz
DDSRampDuration=10*ms
DDSRampStep=101
DDSRampSlope=(SDcoolRF-CoolingRF)/DDSRampStep
DDSRampTimeStep=DDSRampDuration/DDSRampStep

#adiabatic cooling
VVARampDuration=4.5*ms
VVANsteps=42
StartTweezerVVA=4.25
EndTweezerVVA=2.4
VVARampSlope=(EndTweezerVVA-StartTweezerVVA)/VVANsteps
VVARampTimeStep=VVARampDuration/VVANsteps

#uwave
uwave_pulse_time=52*us
uwave_IF=7364.900*kHz #7365.640*kHz#7363.640*kHz
Raman_AOM=107.3649*MHz

drop_time=6*us
twoimgdelay = 150*ms

#OP
D1VVA=9.9
Opt_pump_time=165*us
OPBiasX=-0.64
OPBiasY=-0.13
OPBiasZ=-0.022

#Detection
DetectionRF=105.5*MHz
DetectionVVA=9.9
DetectionVVB=9.9
detection_pulse_time=80*us
meas_time_probe=10*ms
meas_time_probe_second=1.05*ms
Npulse=round(meas_time_probe/detection_pulse_time)


#UV
UV_pulse_time=0.7*us
#SidebandFreq=700*MHz
UVfreq=375.31*MHz#356.5*MHz#348.5*MHz
UVfreqRampDuration=100*ms
UVfreqRampStep=100
UVfreqTimeStep=UVfreqRampDuration/UVfreqRampStep

CorrectingFactor=-0.0008
#scanparam
Nloops=12
Npoints=5

#2ndimg
SecondEndTweezerVVA=2.4
SecondTweezerVVA=9.9
VVARampSlopeSecond=(SecondEndTweezerVVA-SecondTweezerVVA)/VVANsteps
SecondCoolingVVA_SDcool=5.0
SecondSDcoolRF=134*MHz
SecondDDSRampSlope=(SecondSDcoolRF-CoolingRF)/DDSRampStep





ExpSettings.append([' CoolingRF =',CoolingRF])
ExpSettings.append([' DetectionRF =',DetectionRF])
ExpSettings.append([' RepumpVVA =',RepumpVVA])
ExpSettings.append([' CoolingVVA =',CoolingVVA])
ExpSettings.append([' AHcoil = -2.7',AHcoil])
ExpSettings.append([' BiasX =',BiasX])
ExpSettings.append([' BiasY =',BiasY])
ExpSettings.append([' BiasZ =',BiasZ])
ExpSettings.append([' threshold =',threshold])
ExpSettings.append([' meas_time_load =', meas_time_load])

ExpSettings.append([' SDhold =',SDhold])
ExpSettings.append([' SDcoolRF =',SDcoolRF])
ExpSettings.append([' Bx_SDcool =',Bx_SDcool])
ExpSettings.append([' By_SDcool =',By_SDcool])
ExpSettings.append([' Bz_SDcool =',Bz_SDcool])
ExpSettings.append([' DDSRampDuration =',DDSRampDuration])
ExpSettings.append([' DDSRampStep =',DDSRampStep])

ExpSettings.append([' VVARampDuration =',VVARampDuration])
ExpSettings.append([' VVANsteps =',VVANsteps])
ExpSettings.append([' StartTweezerVVA =',StartTweezerVVA])
ExpSettings.append([' EndTweezerVVA =',EndTweezerVVA])
ExpSettings.append([' Bz_SDcool =',Bz_SDcool])
ExpSettings.append([' DDSRampDuration =',DDSRampDuration])
ExpSettings.append([' DDSRampStep =',DDSRampStep])
ExpSettings.append(['Raman_AOM=',Raman_AOM])


ExpSettings.append([' uwave_pulse_time =',uwave_pulse_time])
ExpSettings.append([' uwave_IF =',uwave_IF])

ExpSettings.append([' drop_time =',drop_time])

ExpSettings.append([' D1VVA =',D1VVA])
ExpSettings.append([' Opt_pump_time =',Opt_pump_time])
ExpSettings.append([' OPBiasX =',OPBiasX])
ExpSettings.append([' OPBiasY =',OPBiasY])
ExpSettings.append([' OPBiasZ =',OPBiasZ])
ExpSettings.append([' DetectionVVA =',DetectionVVA])
ExpSettings.append([' DetectionVVB =',DetectionVVB])
ExpSettings.append([' DetectionRF =',DetectionRF])
ExpSettings.append(['detection_pulse_time',detection_pulse_time])
ExpSettings.append([' meas_time_probe =',meas_time_probe])


ExpSettings.append([' Nloops =',Nloops])
ExpSettings.append([' Npoints =',Npoints])
current_time=datetime.datetime.now()
FileName='SettingLogs\{0}{1:0=2d}{2:0=2d}_{3:0=2d}{4:0=2d}_SettingLog.csv'.format(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute)
np.savetxt(FileName,ExpSettings, delimiter=",", fmt='%s')


class Main(EnvExperiment):
    """
    """
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0") #Counts detection
        self.setattr_device("zotino0") 
        self.setattr_device("urukul0_ch0") #cooling and detection detuning
        self.setattr_device("urukul0_ch3") 
        self.setattr_device("urukul0_ch1") #9.2GHZ RF SSB mod
        self.setattr_device("urukul0_ch2") #9.2GHZ RF SSB mod
        self.setattr_device("ttl4") #cooling
        self.setattr_device("ttl5") #repump
        self.setattr_device("ttl6") #detection
        self.setattr_device("ttl7") #D1
        self.setattr_device("ttl8") #tweezer AOD
        self.setattr_device("ttl9") #tweezer common AOM
        self.setattr_device("ttl10") #detection 2
        self.setattr_device("ttl11") #raman
        self.setattr_device("ttl12") #raman 107
        self.setattr_device("ttl13") #UV aom
        self.setattr_device("ttl14") #osc trigger
        self.setattr_device("ttl16") #EMCCDned
        self.setattr_device("ttl17") #Shutter
        self.setattr_device("ttl18") #Microwave
        self.setattr_device("ttl19") #Microwave unused channel
        self.setattr_device("sampler0")
    @kernel
    def run(self): 
        self.core.reset()
        self.ttl4.off() #Cooling ON
        self.ttl5.off() #Repump ON
        self.ttl6.on() #Detection OFF
        self.ttl7.on() #D1 OFF
        self.ttl8.off() #AOD Tweezer ON AOD
        self.ttl9.off() #AOM Tweezer ON common
        self.ttl10.on() #Detection 2 OFF
        self.ttl11.off() #AOM Raman on        
        self.ttl13.on() #AOM UV off
        self.ttl14.off() #osc trigger
        self.ttl16.off() #EMCCD off
        self.ttl17.off() #SRS shutter closed
        self.ttl18.on() #Microwave off
        self.ttl19.on() #Microwave unused channel off
        self.core.break_realtime()
        self.sampler0.init()
        self.zotino0.init(blind=False)
        self.urukul0_ch0.set_att(0*dB)
        self.urukul0_ch0.init()
        self.urukul0_ch3.set_att(0*dB)
        self.urukul0_ch3.init()
        self.urukul0_ch1.set_att(0*dB)
        self.urukul0_ch1.init()
        self.urukul0_ch2.set_att(0*dB)
        self.urukul0_ch2.init()
        delay(1*ms)
        self.urukul0_ch0.sw.on()
        self.urukul0_ch0.set(CoolingRF)
        self.urukul0_ch1.sw.on()
        self.urukul0_ch1.set(uwave_IF,0.0,1.0) #IF SSB. microwave freq = 9.2GHz - IF
        self.urukul0_ch2.sw.on()
        self.urukul0_ch2.set(Raman_AOM, 0.0, 1.0) 
        self.urukul0_ch3.sw.on()
        self.urukul0_ch3.set(UVfreq, 0.0, 1.0) #-40*0.5*MHz
        self.zotino0.write_dac(0, AHcoil) #AH coil
        self.zotino0.write_dac(1, BiasX) #X coil
        self.zotino0.write_dac(2, BiasY) #Y coil
        self.zotino0.write_dac(3, BiasZ) #Z coil
        self.zotino0.write_dac(4, CoolingVVA) #Cooling VVA
        self.zotino0.write_dac(5, RepumpVVA) #Repump VVA
        self.zotino0.write_dac(6, DetectionVVA) #Detection VVA
        self.zotino0.write_dac(7, D1VVA) #D1 VVA
        self.zotino0.write_dac(9, StartTweezerVVA) #Tweezer VVA
        self.zotino0.write_dac(10, DetectionVVB) #Detection2 VVA
        self.zotino0.write_dac(11, 9.9) #Raman 100
        self.zotino0.write_dac(12, 9.9) #Raman 107
        self.zotino0.write_dac(13, 9.9) #UV AOM
        self.zotino0.write_dac(24, 0.0)
        self.zotino0.load()  
        self.sampler0.set_gain_mu(0,0)
        self.sampler0.set_gain_mu(1,0)
        delay(1000*ms)
        
        #StartUVFreq=UVfreq-(Npoints-1)*0.5*0.1*MHz
        #
        #     ********************SET UP SCAN****************
        #
        """for p in range(12):
            for j in range(5):
                DetectionRF=(101+j*0.5)*MHz
                for m in range(12):
                    detVVA=1.8+m*0.1
                    self.zotino0.write_dac(6, DetectionVVA) #Detection VVA
                    self.zotino0.write_dac(10, DetectionVVB) #Detection2 VVA
                    self.zotino0.load()
                    for j in range(25): #   ********range == # repetitions ********************SET # OF REPETITIONS FOR EACH POINT HERE******
                        print(DetectionRF,',',detVVA)
                        delay(10*ms)"""
        """for p in range(40):
            for m in range(21):
                tweezerVVA=3.5+m*0.25   
                self.zotino0.write_dac(9, tweezerVVA)
                self.zotino0.load()  
                delay(1*ms)"""
        for j in range(300): #   ********range == # repetitions ********************SET # OF REPETITIONS FOR EACH POINT HERE******
            #print(tweezerVVA)
            #3delay(10*ms)
            count_load=self.ttl0.count(self.ttl0.gate_rising(meas_time_load))#   
            while count_load<threshold:
                delay(1*ms)
                count_load=self.ttl0.count(self.ttl0.gate_rising(meas_time_load))
            #
            #     ********************BEGIN EXPERIMENT****************
            #
            delay(1*ms) #                      
            self.ttl4.on() #Cooling OFF
            self.ttl14.on() # OSCILLOSCOPE TRIGGER ON
            delay(1000*us)
            self.zotino0.write_dac(0, 0.0) #  AH coil OFF
            self.zotino0.write_dac(5, 9.9) #Increase Repump VVA for SD cool and OP
            self.zotino0.write_dac(1, Bx_SDcool)
            self.zotino0.write_dac(2, By_SDcool)
            self.zotino0.write_dac(5, RepumpVVA_SDcool) #Increase Repump VVA for SD cool and OP
            self.zotino0.write_dac(4, CoolingVVA_SDcool) #Increase Repump VVA for SD cool and OP
            self.zotino0.load()
            delay(100*us)
            #
            #     ********************SD COOL****************
            #
            self.ttl4.off() #Cooling ON
            for n in range(DDSRampStep):
                self.urukul0_ch0.set(CoolingRF+DDSRampSlope*(n+1))
                delay(DDSRampTimeStep)
            delay(SDhold)
            self.zotino0.write_dac(4, SDholdVVA) 
            #self.ttl4.on() #Cooling OFF
            self.ttl5.on() #repump OFF
            delay(200*us)# best practice to ensure cooling turns off before repump and atom is in F=4
            
            #
            #     ********************PREPARE FOR DETECTION****************
            #
            #self.urukul0_ch0.set(DetectionRF)
            delay(100*us)
            self.zotino0.write_dac(9, 9.9) # SUDDEN INCREASE IN TWEEZERS
            self.zotino0.write_dac(1, BiasX) #X coil
            self.zotino0.write_dac(2, BiasY) #Y coil
            self.zotino0.write_dac(3, BiasZ) #Z coil
            self.zotino0.write_dac(5, RepumpVVA) #Repump VVA
            self.zotino0.load()
            delay(3*ms)
            for i in range(50):
                #
                #     ********************DETECT****************
                #
                self.ttl5.off()
                self.ttl17.on()
                delay(3*ms) # Repump ON
                self.ttl16.on()
                with parallel:
                    self.ttl6.off()
                    with sequential:
                        delay(0.5*us)
                        self.ttl10.off()
                delay(meas_time_probe)
                with parallel:
                    self.ttl6.on()
                    with sequential:
                        delay(0.5*us)
                        self.ttl10.on()
                delay(1*us)
                self.ttl16.off()
                self.ttl17.off()
                delay(10*ms)
            #
            #     ********************RELOAD TRAP****************
            #
            self.ttl4.off() #Cooling On
            self.ttl5.off() #Repump On
            self.zotino0.write_dac(9, StartTweezerVVA) # AH coil ON
            self.zotino0.write_dac(4, CoolingVVA) #Cooling VVA
            self.zotino0.write_dac(0, AHcoil) # AH coil ON
            self.zotino0.write_dac(1, BiasX) #X coil
            self.zotino0.write_dac(2, BiasY) #Y coil
            self.zotino0.write_dac(3, BiasZ) #Z coil
            self.zotino0.load()
            delay(1*ms)
            self.urukul0_ch0.set(CoolingRF)
            delay(1*ms)
            #
            #     ********************OUTPUT DATA****************
            #
            #print(meas_time_probe) # PRINT COUNT VALUE
            #delay(50*ms)
            #self.zotino0.write_dac(24, DACScaleFactor*float(count_i)) #OUTPUT COUNT TO DAC
            #self.zotino0.load()
            #delay(1*ms)"""
                    
  
