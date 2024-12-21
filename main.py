
"""

The principal Scimitar control script

"""

import numpy as np
import os
import datetime
import time
import random
import scipy

from playsound import playsound

class scan:
    def __init__(self, **kwargs):  
        for key, value in kwargs.items():
            setattr(self,key,value)
    __init__.__doc__ = "The scan class is passed a list of devices that become attributes of the class. This allows each of the devices to be referred to and operated on regardless of what those devices are as long as there exists a separate class that can be accessed to control them. Within the Scimitar package there is a class dedicated to each device / type of device that the user may wish to integrate into their experiment"       
    def __enter__(self):
        for attr_name in dir(self):   
            if not attr_name.startswith("__"):   
                attr = getattr(self, attr_name)
                if hasattr(attr, '__enter__'):
                    attr.__enter__()
        return self
    __enter__.__doc__ = "Look through all of the devices passed as attributes of the scan class during the __init__() method and call their respective __enter__() methods. This is a simpler way of incorporating the context manager without having to explicitly engage it for each device, particularly when those devices are likely to change regularly depending on the nature of the experiment described."
    def __exit__(self,exc_type,exc_value,traceback):
        for attr_name in dir(self):   
            if not attr_name.startswith("__"):   
                attr = getattr(self, attr_name)
                if hasattr(attr, '__exit__'):
                    attr.__exit__(None,None,None)
    __exit__.__doc__ = "Look through all of the devices passed as attributes of the scan class and call their respective __exit__() methods. This allows all of the experiment devices to be configured and terminate connections to those devices properly should the script crash unexpectedly. It means that no remnaants of previous experiments are left to block the new connections to be made within subsequent experiments."
    def activeMeasurement(self,database):
        activeDevices = []
        for device in deviceList:
            if device.name == "Photodiode1" or device.name == "Photodiode2":
                activeDevices.append(device)
        print("LSPR Impedmimetry Commenced...")
        data2 = scan.daqMeasure(activeDevices,deviceList)
        database.append(data2)
        return activeDevices
    activeMeasurement.__doc__ = "The measurement phase during excitation with voltage and monochromatic light. Recordings are taken from both the reference and measurement photodiodes. The devices used for measurement are returned"
    
    def readDevices(self,devicesToRead,params):
        Daq = devices.USB6349(devicesToRead,
                              deviceList,
                              SPC = int(params['AIintTime']*params['FS']),
                              FS = params['FS'],
                              duration = params['AIduration'])   
        with Daq as obj:
            obj.configure()
            data = obj.readDaq()  
        return data
    
    
    
    def daqMeasure(self,activeDevices,deviceList):
        Daq = devices.USB6349(activeDevices,
                              deviceList,
                              SPC = int(AIintTime*FS),
                              FS = FS,
                              duration = AIduration) 
        
        with Daq as obj:
            obj.configure()
            data = obj.readDaq()      
        return data  
    daqMeasure.__doc__ = "Create the Daq object given the device list which includes all connected devices whether active or not, configure the necessary tasks, and read from the AI devices specified in activeDevices. Only use this method call when there are AI devices contained within the device list"
    def daqTrigger(self,devicesToActivate,deviceList):
        # Daq = devices.USB6349(devicesToActivate,
        #                       deviceList,
        #                       SPC = int(AIintTime*FS),
        #                       FS = FS,
        #                       duration = AIduration)
        Daq = devices.USB6349(devicesToActivate,
                              deviceList)
        with Daq as obj:
            obj.configure()
            obj.trigger()
    daqTrigger.__doc__ = "CCreate the Daq object given the device list which includes all connected devices whether active or not, configure the necessary tasks, and trigger the PO devices in the task. Only use this method call when there are PO devices contained within the activeDevices"
    def getPos(self):
        pos = []
        for attr_name in dir(self):
            if not attr_name.startswith("__"):           
                attr = getattr(self, attr_name)
                if hasattr(attr, 'getPos'):
                    pos.append(attr.getPos())
        return pos
    getPos.__doc__ = "From the list of devices defined in the experiment description, the getPos() method is called for all devices which have one. Under normal circumstances this only applies to stage-type devices but allows the 3-dimensional position of the sample to be controlled directly rather than addressing each stage individually (i.e. specify [X,Y,Z] and the appropriate device will populate the corresponding axis position)"
    def lamp(self):
        activeDevices = []
        
        scan.daqTrigger(activeDevices,deviceList)
        time.sleep(0.1)
        if not activeDevices:
            for device in deviceList:
                if device.name == "SLS205":
                    activeDevices.append(device)
        return activeDevices
    lamp.__doc__ = "Set the triggerable devices such that only the lamp is active. This exists as a standalone step so that illumination can be guaranteed before the onset of measurement by either spectrometer or photodiode(s). We reset the active device list to reflect the fact that the lamp behaves contrary to the other triggerable devices in the list"
    def laser(self):
        activeDevices = []
        for device in deviceList:
            if device.name == "Vortran" or device.name == "SLS205":
                activeDevices.append(device)
        scan.daqTrigger(activeDevices.deviceList)
        time.sleep(0.1)
        activeDevices = []
        for device in deviceList:
            if device.name == "Vortran":
                activeDevices.append(device)
        return activeDevices
        
    def laserSigGen(self):
        activeDevices = []
        for device in deviceList:
            if device.name == "Vortran" or device.name == "Tektronix" or device.name == "SLS205":  
                activeDevices.append(device)
        scan.daqTrigger(activeDevices,deviceList)
        time.sleep(0.1)
        activeDevices = []
        for device in deviceList:
            if device.name == "Vortran" or device.name == "Tektronix":  
                activeDevices.append(device)
        return activeDevices
    laserSigGen.__doc__ = "The triggering step for what might be considered the active phase of the measurement. The laser and signal generator are both set as active while all other triggerable devices are disengaged. We re-write the active device list to reflect the fact that the lamp behaves contrary to the other devices in the list"
    
    def activateDevices(self,devicesToActivate):
        Daq = devices.USB6349(devicesToActivate,
                              deviceList)
        with Daq as obj:
            obj.configure()
            obj.trigger()
        
    def playTune(self):
        home = os.getcwd()
        root = 'C:\\Users\\ezxfn1\\OneDrive - The University of Nottingham\\Optimise\\B06\\Audio'
        t0 = datetime.datetime.now()
        date = str(t0)
        date.find('-')
        month = date[5:7]
        path = root+'\\'+month
        os.chdir(path)
        mp3files = os.listdir()
        rand = random.randrange(1,len(mp3files))
        path = root+'\\'+month+'\\Soundbite'+str(rand)+'.mp3'
        playsound(path)
        os.chdir(home)
    playTune.__doc__ = "Alerts the user to the completion of a scan by playing a seasonal soundbite"
    def readSpectrum(self,activeDevices,deviceList):
        Daq = devices.USB6349(activeDevices,
                              deviceList,
                              SPC = int(specIntTime*FS),
                              FS = FS,
                              duration = specDuration)  
        with Daq as obj:
            obj.configure()
            [spectra,wavelengths,daqData] = Spectro.measure(obj)
        return spectra,wavelengths,daqData
    readSpectrum.__doc__ = "To be called in conjunction with AI devices (i.e. the internal photodiode of the Lamp and/or the photodiodes located throughout the system. This method call allows synchronous acquisition of data from both the spectrometer and DAQ where either act in isolation leads to asynchrony" 

        
        
        
    def reference(self,database,spectrabase):
        activeDevices = []
        for device in deviceList:
            if device.name == "Photodiode1" or device.name == "Photodiode2" or device.name == "Lamp":
                activeDevices.append(device)
        print("Referencing Commenced...")
        [spectra,wavelengths,data1] = scan.readSpectrum(activeDevices,deviceList)
        spectrabase.append(spectra)
        database.append(data1)
        return activeDevices
    reference.__doc__ = "The current definition of reference where we record from the spectrometer, reference and measurement photodiodes, and the lamp's internal photodiode while the lamp is active. The devices used for measurement are returned"
    def routine1(self,database2):
        self.triggerReset() # Sample not illuminated and no recordings taken
        self.stageStep() # Move the stage to the next (or first) location
        devicesToActivate = ['Vortran','Tektronix']
        self.activateDevices(devicesToActivate)
        
        mPODev = self.laserSigGen() # Switch to laser illumination and Sig.Gen.
        mAIDev = self.activeMeasurement(database2) # Record from both diodes
        return mPODev,mAIDev
    routine1.__doc__ = "Navigate to the next sample position and perform synchronous laser illumination, signal generator triggering and acquisition from both measurement and reference diodes"
    def routine2(self,database1,database2,spectrabase1):
        self.triggerReset() # Sample not illuminated and no recordings taken
        self.stageStep() # Move the stage to the next (or first) location
        rPODev = self.lamp() # Illuminate with the lamp
        rAIDev = self.reference(database1,spectrabase1)
        self.triggerReset() # Sample not illuminated and no recordings taken
        mPODev = self.laserSigGen() # Switch to laser illumination and Sig.Gen.
        mAIDev = self.activeMeasurement(database2) # Record from both diodes
        return rPODev,rAIDev,mPODev,mAIDev
    routine2.__doc__ = "Similar to routine 1 but with the addition of a referencing step. Navigate to the next sample position, illuminate with the lamp and record spectra and reference data from the appropriate diode simultaneously before then performing snchronous laser illumination, signal generator triggering, and acquisition from both measurement and reference diodes."   
    def routine3(self,database1,database2):
        self.triggerReset() # Sample not illuminated and no recordings taken
        self.stageStep() # Move the stage to the next (or first) location
        rPODev = self.laser()
        rAIDev = self.measure(database1)
    def setPos(self,**kwargs):
        for attr_name in dir(self):
            if not attr_name.startswith("__"):           
                attr = getattr(self, attr_name)
                if hasattr(attr, 'setPos'):
                    attr.setPos(**kwargs)
    setPos.__doc__ = "From the list of devices defined in the experiment description, the setPos() method is called for all devices which have one. Under normal circumstances this only applies to stage-type devices but allows the 3-dimensional position of the sample to be controlled with directly rather than addressing each stage individually (i.e. specify [X,Y,Z] and the appropriate device will navigate to the location corresponding to its axis of translation."             
    def stageStep(self):
        scan.setPos(targetX = pListX[i],
                    targetY = pListY[j],
                    targetZ = pListZ[k])
        time.sleep(0.1)
        [posXY,posZ] = scan.getPos()
        print(f"Stage Position: [{posXY[0]:.3f}, {posXY[1]:.3f}, {posZ:.3f}]")
        time.sleep(0.1)
    stageStep.__doc__ = "Move the stage to the next position along the scan trajectory and print the new location to the terminal. This last part is useful as there is no other way to determine stage position without stopping the script since the Zaber and PI devices can't be accessed while the script is running"
    def triggerReset(self):
        for device in deviceList:
            if device.name == "SLS205":
                activeDevices = [device]
        scan.daqTrigger(activeDevices,deviceList)
        time.sleep(0.1)
        print("Triggers Reset...")  
    triggerReset.__doc__ = "All triggerable devices are returned to their OFF state with the exception of the SLS205 lamp shutter where we define its state as ON such that the light from the lamp is in essence OFF"  
"""
###############################################################################
"""
if __name__ == '__main__':
    
    import devices
    
    """ List devices connected to the DAQ [Channel, Family, Name] """
    devA0 = devices.AODevice(0, "", "")
    devA1 = devices.AODevice(1, "", "")
    devA2 = devices.AODevice(2, "", "")
    devA3 = devices.AODevice(3, "", "")
    devB0 = devices.AIDevice(0, "Photodiode", "PhotodiodeT")
    devB1 = devices.AIDevice(1, "Photodiode", "PhotodiodeR")
    devB2 = devices.AIDevice(2, "Photodiode", "Lamp")
    devB3 = devices.AIDevice(3, "Photodiode", "PhotodiodeOther")
    devB4 = devices.AIDevice(4, "Accessory", "SignalGenerator")
    devB5 = devices.AIDevice(5, "", "")
    devB6 = devices.AIDevice(6, "", "")
    devB7 = devices.AIDevice(7, "", "")
    devC0 = devices.PODevice(0, "Source", "Vortran")
    devC1 = devices.PODevice(1, "Accessory", "Tektronix")
    devC2 = devices.PODevice(2, "Source", "SLS205")
    devC3 = devices.PODevice(3, "Spectrometer", "CCS200")
    devC4 = devices.PODevice(4, "", "")
    devC5 = devices.PODevice(5, "", "")
    devC6 = devices.PODevice(6, "", "")
    devC7 = devices.PODevice(7, "", "")
    
    deviceList = [devA0, devA1, devA2, devA3,
                  devB0, devB1, devB2, devB3, devB4, devB5, devB6, devB7,
                  devC0, devC1, devC2, devC3, devC4, devC5, devC6, devC7]

    """ Define the stage parameters """
    originX = 239751 # Encoder steps
    originY = 447035 # Encoder steps
    originZ = 3.8795 # mm
    locsX = 1 # No. points in the scan [X]
    locsY = 1 # No. points in the scan [Y]
    locsZ = 1 # No. points in the scan [Z]
    ssX = 16 # Stepsize in encoder units [X]
    ssY = 0 # Stepsize in encoder units [Y]
    ssZ = 0 # Stepsize in encoder units [Z]

    pListX = np.linspace(originX, originX+(locsX-1)*ssX, locsX)
    pListY = np.linspace(originY, originY+(locsY-1)*ssY, locsY)
    pListZ = np.linspace(originZ, originZ+(locsZ-1)*ssZ, locsZ)

    """ Define the spectrometer parameters """
    specIntTime = 1.0  # Duration of a single spectrometer acquisition [s]
    noSpectra = 10 # Number of spectra to acquire at any point
    specDuration = noSpectra*specIntTime  # Duration of the spectrometry phase
    specMode = "Continuous"  # Spectrometer acquisition mode

    """ Initialise the devices in the scan """
  
    ZStage = devices.E873(model = "E-873",
                          serial = "121007658",
                          origin = [originZ])
    
    XYStage = devices.ASR(channel = 8,
                          origin = [originX,originY])
    
    Spectro = devices.CCS200(ID =  b"USB0::0x1313::0x8089::M00928154::RAW",
                              mode = specMode,
                              intTime = 0.1, 
                              duration = specDuration*100)
    
    # How many measurements steps at each location
    
    
    dataVariables = {}
    root_name = "data"
    noMeasurements = 2
    dataVariables[f"{root_name}{noMeasurements}"] = []
    
    data1, database1 = [],[] # Reference Measurements
    data2, database2 = [],[] # Active Measurements
    spectrabase1 = []        # Spectrometer data
    
    tmp1 = []
    tmp2 = []
    
    """
    #####################################
    State which devices are actually used in the scan and when
    """
    with scan(
            # XYStage = XYStage,
            # ZStage = ZStage
            # Spectro = Spectro
              ) as scan:
        
        total = len(pListZ)*len(pListY)*len(pListX)
        pMap = []
        
        for k in range(len(pListZ)):
            for j in range(len(pListY)):
                for i in range(len(pListX)):
                
                    """
                    ####################################
                    Experiment description
                    ####################################
                    """
                    
                    start = time.time()
                    iteration = len(pListY)*len(pListX)*k+len(pListX)*j+i+1
                    pMap.append([pListX[i],pListY[j],pListZ[k]])
                    
                    # MOVE STAGE
                    # scan.stageStep()
                    
                    # # RESET TRIGGERS
                    # scan.triggerReset()
                    
                    # # DEVICE TRIGGERING
                    # devicesToActivate = []
                    # transientDevicesPO1 = ['Vortran']
                    # for device in transientDevicesPO1:
                    #     for dev in deviceList:
                    #         if dev.family == "PO" and dev.name == device:
                    #             devicesToActivate.append(dev)
                    # scan.activateDevices(devicesToActivate)
                    
                    # DEVICE RECORDING 1
                    FS = 100000                      # AI device sampling rate
                    AIintTime = 0.1                  # Duration of a single measurement
                    AIduration = AIintTime*1       # Total duration recording at each location
                    
                    params1 = {'FS':FS,
                              'AIintTime':AIintTime,
                              'AIduration':AIduration}
                    
                    transientDevicesAI1 = ['Photodiode1','Photodiode2']
       
                    devicesToRead = []
                    for device in transientDevicesAI1:
                        for dev in deviceList:
                            if dev.family == "AI" and dev.name == device:
                                devicesToRead.append(dev)
                    tmp = scan.readDevices(devicesToRead,params1)
                    data1.append(tmp)
                    
                    
                    # # DEVICE TRIGGERING
                    # devicesToActivate = []
                    # transientDevicesPO2 = ['Vortran','Tektronix']
                    # for device in transientDevicesPO2:
                    #     for dev in deviceList:
                    #         if dev.family == "PO" and dev.name == device:
                    #             devicesToActivate.append(dev)
                    # scan.activateDevices(devicesToActivate)
                    
                    
                    # # DEVICE RECORDING 2
                    # FS = 100000                     # AI device sampling rate
                    # AIintTime = 0.1                  # Duration of a single measurement
                    # AIduration = AIintTime*1       # Total duration recording at each location
                    
                    # params2 = {'FS':FS,
                    #           'AIintTime':AIintTime,
                    #           'AIduration':AIduration}
                    
                    # transientDevicesAI2 = ['Photodiode1','Photodiode2']
                    
                    # devicesToRead = []
                    # for device in transientDevicesAI2:
                    #     for dev in deviceList:
                    #         if dev.family == "AI" and dev.name == device:
                    #             devicesToRead.append(dev)
                    # tmp = scan.readDevices(devicesToRead,params2)
                    # data2.append(tmp)
                    
                    # # DEVICE RECORDING
                    # FS = 1000                      # AI device sampling rate
                    # AIintTime = 1                  # Duration of a single measurement
                    # AIduration = AIintTime*1       # Total duration recording at each location
                    # devicesToRead = []
                    # transientDevices = ['Photodiode1','Photodiode2']
                    # for device in transientDevices:
                    #     for dev in deviceList:
                    #         if dev.family == "AI" and dev.name == device:
                    #             devicesToRead.append(dev)
                    # tmp2 = scan.readDevices(devicesToRead,FS,AIintTime,AIduration,tmp2)
                    
                    
                    
                    
                    
                    
                    
                    # ROUTINES
                    # mPODev,mAIDev = scan.routine1(database2)
                    # rPODev,rAIDev,mPODev,mAIDev = scan.routine2(database1,database2,spectrabase1)
                    
                    print(f"{iteration} of {total}: {iteration/total*100:.2f} Complete")
                    print(f"Last Acquisition Cycle Duration: {(time.time() - start):.2f} seconds")
                    
        # RESET - Reset all triggerable devices (Lamp shutter ON)
        scan.triggerReset()
        # FINISHED
        scan.playTune()
        
    print("Scan Complete. Have a Nice Day")
    
    # # ROUTINE 1
    # db2reshaped = []
    # db2 = np.array(database2)
    # for i in range(np.shape(db2)[1]):
    #     reshaped_array = db2[:,i,:]
    #     db2reshaped.append(reshaped_array)
    # mdict = {
    #           'PosMap':pMap,
    #           'Stage1_DevicesAI':mAIDev,
    #           'Stage1_DevicesPO':mPODev,
    #           'AISamplingRate':FS
    #         }
              
    mdict = {
            'PosMap':pMap,
            'Params1':params1,
            # 'Params2':params2,
            'Data1':data1,
            # 'Data2':data2,
            'AIDevices1':transientDevicesAI1,
            # 'AIDevices2':transientDevicesAI2,
            # 'PODevices1':transientDevicesPO1
            # 'PODevices2':transientDevicesPO2
            }
    # }
    # for i, item in enumerate(db2reshaped):
    #     key_name = f'Stage1_{mAIDev[i].name}'  # Create dynamic variable names
    #     mdict[key_name] = item
    filename = f"Scimitar_{time.time():.0f}.mat"
    scipy.io.savemat(
        filename,
        mdict, 
        appendmat=True, 
        format='5', 
        long_field_names=False, 
        do_compression=False, 
        oned_as='row')  
    
    # # # ROUTINE 2
    # # db1reshaped = []
    # # db1 = np.array(database1)
    # # for i in range(np.shape(db1)[1]):
    # #     reshaped_array = db1[:,i,:]
    # #     db1reshaped.append(reshaped_array)
    # # db2reshaped = []
    # # db2 = np.array(database2)
    # # for i in range(np.shape(db2)[1]):
    # #     reshaped_array = db2[:,i,:]
    # #     db2reshaped.append(reshaped_array)
    # # mdict = {
    # #           'PosMap':pMap,
    # #           'Stage1_DevicesAI':rAIDev,
    # #           'Stage1_DevicesPO':rPODev,
    # #           'Stage2_DevicesAI':mAIDev,
    # #           'Stage2_DevicesPO':mPODev,
    # #           'AISamplingRate':FS,
    # #           'Stage1_Spectra':spectrabase1,
    # # }
    # # for i, item in enumerate(db1reshaped):
    # #     key_name = f'Stage1_{rAIDev[i].name}'  # Create dynamic variable names
    # #     mdict[key_name] = item    
    # # for i, item in enumerate(db2reshaped):
    # #     key_name = f'Stage2_{mAIDev[i].name}'  # Create dynamic variable names
    # #     mdict[key_name] = item
    # # filename = f"Scimitar_{time.time():.0f}.mat"
    # # scipy.io.savemat(
    # #     filename,
    # #     mdict, 
    # #     appendmat=True, 
    # #     format='5', 
    # #     long_field_names=False, 
    # #     do_compression=False, 
    # #     oned_as='row')   
    
