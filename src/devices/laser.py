
"""

Contains the functions needed for routine use of Vortran devices. It so far has been configured solely for a Vortran Stradus laser diode. The example test code should perform the following routine:
- Connect
- Activate
- Set mode to continuous wave and return confirmation of mode
- Set power to 50 mW and return confirmation of power
- Wait 5 seconds
- Return power to 0mW and return confirmation
- Deactivate
- Disconnect
- 

"""

import time

class Vortran:
    
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        print("Init")
    
    def connect(self):
        """
        

        Returns
        -------
        None.

        """
        print("Connect")
        
    def disconnect(self):
        """
        

        Returns
        -------
        None.

        """
        print("Disconnect")
        
    def activate(self):
        """
        

        Returns
        -------
        None.

        """
        print("Activate")
        
    def deactivate(self):
        """
        

        Returns
        -------
        None.

        """
        print("Deactivate")
        
    def setPower(self,power):
        """
        

        Parameters
        ----------
        power : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print("Set Power")
        
    def getPower(self):
        """
        

        Returns
        -------
        None.

        """
        print("Get Power")
        
    def setMode(self,mode):
        """
        

        Parameters
        ----------
        mode : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print("Set Mode")
        
    def getMode(self):
        """
        

        Returns
        -------
        None.

        """
        print("Get Mode")
        
    def sendCommand(self,command):
        """
        

        Parameters
        ----------
        command : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print("Send Command")
   
        
"""
Example usage.
"""
if __name__ == "__main__":
    laser = Vortran()
    try:
        laser.connect()
        laser.activate()
        laser.set_mode("CW")
        laser.get_mode()
        laser.set_power(50)
        laser.get_power()
        time.sleep(5)
        laser.set_power(0)
        laser.get_power()
        laser.deactivate()
    finally:
        laser.disconnect()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

