
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

import serial
import time

class Vortran:
    
    def __init__(self,port,baudrate=115200,timeout=1):
        """
        Initialize the connection to the Vortran device

        Parameters
        ----------
        port : INT
            Serial port (e.g. 'COM3')
        baudrate : INT, optional
            Communication speed. The default is 115200.
        timeout : FLOAT, optional
            Read timeout in seconds. The default is 1.

        Returns
        -------
        None.

        """
        self.port = f"COM{port}"
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
    
    def connect(self):
        """
        Open the serial connection to the laser

        Returns
        -------
        None.

        """
        try:
            self.connection = serial.Serial(self.port,self.baudrate,timeout=self.timeout)
            print(f"Connected to Vortran device on COM{self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to Vortran device: {e}")
            raise
            
    def disconnect(self):
        """
        Close the serial connection

        Returns
        -------
        None.

        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected from Vortran device")
        
    def activate(self):
        """
        Turn on the laser

        Returns
        -------
        None.

        """
        response = self.sendCommand("L=1")
        print(f"Vortran device ON response: {response}")
        
    def deactivate(self):
        """
        Turn off the laser

        Returns
        -------
        None.

        """
        response = self.sendCommand("L=0")
        print(f"Vortran device OFF response: {response}")
        
    def setPower(self,power):
        """
        Set the laser power

        Parameters
        ----------
        power : INT
            Desired output power as a percentage of maximum

        Returns
        -------
        None.

        """
        if not (0 <= power <= 100):
            raise ValueError("Power percentage must be between 0 and 100")
        response = self.sendCommand(f"P={power}")
        print(f"SetPower response: {response}")
        
    def getPower(self):
        """
        Query the current device output power

        Returns
        -------
        None.

        """
        response = self.sendCommand("P?")
        print(f"Current output power: {response}")
        
    def setMode(self,mode):
        """
        Specify the output type from the Vortran device

        Parameters
        ----------
        mode : STR
            Emission mode of the device ('CW','DIGITAL','ANALOG')

        Returns
        -------
        None.

        """
        mode_map = {
            "CW": "SOUR:AM:STAT OFF",
            "DIGITAL": "SOUR:AM:STAT ON; SOUR:AM:INT DIG",
            "ANALOG": "SOUR:AM:STAT ON; SOURC:AM:INT ANA"
        }
        if mode not in mode_map:
            raise ValueError(f"Invalid mode. Supported modes are: {list(mode_map.keys())}")
        self.sendCommand(mode_map[mode])
        print(f"Vortran device mode set to {mode}")
        
    def getMode(self):
        """
        Query the current output mode of the Vortran device

        Raises
        ------
        Exception
            Unrecognised output mode returned by device. Most likely a use-case that has yet to be accounted for

        Returns
        -------
        STR
            Output mode (CW, DIGITAL, ANALOG)

        """
        response = self.sendCommand("SOUR:AM:STAT?")
        if response == "0":
            return "CW"
        elif response == "1":
            source_type = self.sendCommand("SOUR:AM:INT?")
            return "DIGITAL" if source_type == "DIG" else "ANALOG"
        else:
            raise Exception("Unknown output mode")
        
    def sendCommand(self,command):
        """
        Send a command to the Vortran device and return the response

        Parameters
        ----------
        command : STR
            Command to send to the device. Format must align with Vortran documentation

        Raises
        ------
        ConnectionError
            The device hasn't been connected properly. Check the serial connection '

        Returns
        -------
        response : STR
            The base command return from Vortran devices. Can be interpreted in conjunction with Vortran documentation

        """
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Connection to the Vortran device is not open")
        self.connection.write((command+'\r').encode())
        response = self.connection.readline().decode().strip()
        return response
   
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

