
"""

Contains the functions needed for routine use of Vortran devices. It so far has been configured solely for a Vortran Stradus laser diode


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
        
    def set_power(self,power):
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
        
        
    def get_power(self):
        """
        

        Returns
        -------
        None.

        """
        print("Get Power")
        
    def set_mode(self,mode):
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
        
    def get_mode(self):
        """
        

        Returns
        -------
        None.

        """
        print("Get Mode")
        
    def send_command(self,command):
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

