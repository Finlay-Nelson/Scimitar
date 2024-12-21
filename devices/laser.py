"""

Control of the Vortran Stradus660

"""

import serial
import time

class VortranStradus:
    def __init__(self, port, baudrate=115200, timeout=1):
        """
        Initialize the connection to the Vortran Stradus laser.
        :param port: Serial port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux).
        :param baudrate: Communication speed (default: 115200).
        :param timeout: Read timeout in seconds (default: 1).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """Open the serial connection to the laser."""
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Wait for the connection to stabilize
            print(f"Connected to Vortran Stradus on {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to Vortran Stradus: {e}")
            raise

    def send_command(self, command):
        """Send a command to the laser and return the response."""
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Connection to the laser is not open.")
        self.connection.write((command + '\r').encode())  # Commands end with a carriage return
        time.sleep(0.1)
        response = self.connection.readline().decode().strip()
        return response

    def turn_on(self):
        """Turn on the laser."""
        response = self.send_command("L=1")
        print(f"Laser On Response: {response}")

    def turn_off(self):
        """Turn off the laser."""
        response = self.send_command("L=0")
        print(f"Laser Off Response: {response}")

    def set_power(self, power_percentage):
        """
        Set the laser power.
        :param power_percentage: Desired power as a percentage (e.g., 50 for 50%).
        """
        if not (0 <= power_percentage <= 100):
            raise ValueError("Power percentage must be between 0 and 100.")
        response = self.send_command(f"P={power_percentage}")
        print(f"Set Power Response: {response}")

    def get_power(self):
        """Query the current laser power."""
        response = self.send_command("P?")
        print(f"Current Power: {response}")
        return response
    
    def set_mode(self, mode):
        """
        Set the laser's operating mode.
        :param mode: Mode to set ('CW', 'DIGITAL', 'ANALOG', etc.).
        """
        mode_map = {
            "CW": "SOUR:AM:STAT OFF",
            "DIGITAL": "SOUR:AM:STAT ON; SOUR:AM:INT DIG",
            "ANALOG": "SOUR:AM:STAT ON; SOUR:AM:INT ANA",
        }
        if mode not in mode_map:
            raise ValueError(f"Invalid mode. Supported modes are: {list(mode_map.keys())}")
        self.send_command(mode_map[mode])
        print(f"Laser mode set to {mode}.")
        
    def get_mode(self):
        """
        Query the current operating mode of the laser.
        :return: The current mode ('CW', 'DIGITAL', 'ANALOG').
        """
        response = self.send_command("SOUR:AM:STAT?")
        if response == "0":
            return "CW"
        elif response == "1":
            source_type = self.send_command("SOUR:AM:INT?")
            return "DIGITAL" if source_type == "DIG" else "ANALOG"
        else:
            raise Exception("Unknown mode response.")

    def disconnect(self):
        """Close the serial connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected from Vortran Stradus laser.")

# Example usage
if __name__ == "__main__":
    laser = VortranStradus(port="COM3")  # Replace 'COM3' with the actual port
    try:
        laser.connect()
        laser.turn_on()
        laser.set_power(50)  # Set power to 50%
        time.sleep(5)        # Keep laser on for 5 seconds
        laser.get_power()
        laser.turn_off()
    finally:
        laser.disconnect()
