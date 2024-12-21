"""

Interaction with the Agilent33220A function generator
*Needs written in a format that allows integration with Scimitar.
 Not yet with the class structure consistant with other devices.
"""

import pyvisa

# Create a resource manager
rm = pyvisa.ResourceManager()

# List all connected instruments
print(rm.list_resources())

# Connect to the signal generator (update the resource name as necessary)
sig_gen = rm.open_resource('USB0::0x0957::0x0407::MY43004556::INSTR')

# Example Waveform 1
freq = 17.17    # Signal Frequency
vAmp = 100      # Signal Amplitude [mV]
vTyp = 'VPP'    # Peak to Peak (alternatively RMS)
vOff = 0        # DC Offset [mV]
wave = "SQU"    # Waveform

sig_gen.write(f'FUNC {wave}')          
sig_gen.write(f'FREQ {freq}')         
sig_gen.write(f'VOLT:UNIT {vTyp}')
sig_gen.write(f'VOLT:OFFS {vOff/1000}') 
sig_gen.write(f'VOLT {vAmp/1000}')        

# Make triggerable with TTL
sig_gen.write('BURST:STAT ON')  # Activates when triggered
sig_gen.write('BURST:MODE GAT') # Helps with triggering on and off
sig_gen.write('BURST:NCYC INF') # Continues until un-triggered
sig_gen.write('TRIG:SOUR EXT')  # Accepts triggers from external source

# Close the connection
sig_gen.close()


# Useful functions
# *RST - Reset the instrument to default settings
# *OPC - Query if the operation is complete

# FUNC SIN   - Sine wave
# FUNC SQU   - Square wave
# FUNC RAMP  - Ramp wave
# FUNC:RAMP:SYM <value> - Set ramp symmetry (0-100)
# FUNC PULSE - Pulse wave
# FUNC NOIS  - Noise
# FUNC DC    - DC output
# FUNC?      - Query function type

# FREQ <value> - Set frequency
# FREQ?        - Query frequency

# VOLT <value>   - Set amplitude
# VOLT?          - Query amplitude
# VOLT:UNIT VPP  - Set voltage units to peak-to-peak
# VOLT:UNIT VRMS - Set voltage units to RMS
# VOLT:UNIT?     - Query voltage units
# VOLT:OFFS <value> - Set DC offset
# VOLT:OFFS?        - Query the voltage offset

# PULS:WIDT <value> - Set pulse width
# PULS:WIDT?        - Query pulse width
# PULS:TRAN <value> - Set pulse rise/fall time
# PULS:TRAN?        - Query the pulse transition time
# PULS:DCYC <value> - Pulse duty cycle percentage
# PULS:DCYC?        - Query the pulse duty cycle
# PULS:PER <value>  - Set pulse period
# PULS:PER?         - Query the current pulse period

# AM:STAT ON/OFF    - Enable/Disable Amplitude modulation
# AM:DEPTH <value>  - Set AM depth percentage

# FM: STAT ON/OFF   - Enable/Disable Frequency modulation
# FM:DEV <value>    - Set FM deviation

# PM:STAT ON/OFF    - Enable/Disable Phase modulation
# PM:DEVI <value>   - Set PM deviation

# OUTPUT ON   - Enable output
# OUTPUT OFF  - Disable output
# OUTPUT?     - Query output state

# TRIG:SOUR IMM - Set trigger source to immediate
# TRIG:SOUR BUS - Set trigger source to software (bus) trigger
# TRIG:SOUR EXT - Set trigger source to external
# TRIG:DEL <value> - Set trigger delay
# TRIG:SLOP POS - Set trigger slope to positive
# TRIG:SLOP NEG - Set trigger slope to negative

# BURST:STAT ON   - Enable burst mode
# BURST:STAT OFF  - Disable burst mode
# BURST:NCYC <value> - Set number of cycles per trigger
# BURST:MODE TRIG - Set burst mode to triggered
# BURST:MODE GAT  - Set burst mode to gated
# BURST:PHAS <value> - Set burst phase

# DISP:TEXT "<message>" - Display a custom message on the screen
# DISP:TEXT:CLE         - Clear custom message from the display

# SYST:BEEP - Generate a beep sound
