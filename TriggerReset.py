###############################################################################
"""
Reset the Digital Outputs from the USB6349 to 0V. Note that digital control of the SLS205 refers to the shutter, and so to instill a dark state requires a True status for that device
"""
###############################################################################
import nidaqmx as ni
from nidaqmx.constants import LineGrouping as LG
###############################################################################
class NI:
    def __init__(self,deviceList):
        PO = ni.Task('Digital Output') 
        self.PO = PO
        self.deviceList = deviceList
    __init__.__doc__ = "Create an instance of the NI DAQ which contains a PO task. The PO task is responsible for digitally triggering other devices (spectrometer, signal generator, etc.). Device list contains name and boolean status"
    ###########################################################################
    def __enter__(self):
        return self
    __enter__.__doc__ = "Context manager"
    ###########################################################################  
    def __exit__(self, exc_type, exc_value, traceback):
        ni.Task.close(self.PO)
    __exit__.__doc__ = "Close the task(s) to free up the DAQ."
    ###########################################################################
    def configure(self):
        activePO = []
        for i in range(len(self.deviceList)):
            self.PO.do_channels.add_do_chan(
                'Dev1/port0/line'+str(i), 
                line_grouping=LG.CHAN_PER_LINE
                )
            if self.deviceList[i][1] == True:
                activePO.append(True)
            elif self.deviceList[i][1] == False:
                activePO.append(False)
        return self
    configure.__doc__ = "Create a digital output channel with a line for every port on the DAQ. Iterate through every device and extract its boolean status value to determine whether it should be armed or not. "
    ###########################################################################
    def trigger(self):
        self.PO.write(self.activePO)
    trigger.__doc__ = "Writes to the digital output channel according to the arming characteristics provided through configure()"
###############################################################################
    

###############################################################################   
if __name__ == "__main__":
    
    # Define the boolean state of each of the PO lines
    deviceList = []
    deviceList.append(['Laser',             False]) 
    deviceList.append(['Signal Generator',  False])
    deviceList.append(['Xe',                not False])
    deviceList.append(['Spectrometer',      False])
    deviceList.append(['',                  False])
    deviceList.append(['',                  False])
    deviceList.append(['',                  False])
    deviceList.append(['',                  False])
        
    # Create the DAQ task and pass the device list (with name and boolean)
    exp = NI(deviceList)
    with exp as obj:
        obj.configure()
        obj.trigger()
###############################################################################
