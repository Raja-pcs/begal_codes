import subprocess
import time
import Adafruit_BBIO.GPIO as GPIO

# Setup GPIO for LDR sensor (digital pin)
LDR_PIN = "P9_15"  # Digital input pin
GPIO.setup(LDR_PIN, GPIO.IN)  # Set the pin as input

def run_command(command):
    """
    Run a shell command and print its output or error.
    """
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {e.stderr}")

def update_oled_message(line_1, line_2=""):
    """
    Clear the OLED display and update with messages on the first and second rows.
    """
    # Clear the display first
    run_command("./oled_bin -n 2 -c")
    
    # Update the first line with the message
    run_command(f"./oled_bin -n 2 -x 1 -y 1 -l \"{line_1}\"")
    
    # Update the second line if a second message is provided
    if line_2:
        run_command(f"./oled_bin -n 2 -x 1 -y 2 -l \"{line_2}\"")
    else:
        # If no second message, clear the second line
        run_command("./oled_bin -n 2 -x 1 -y 2 -l \"\"")

def read_ldr_state():
    """
    Read the digital value from the LDR sensor (using a comparator).
    """
    return GPIO.input(LDR_PIN)  # Returns 1 (HIGH) or 0 (LOW)

# List of commands to initialize the OLED
commands = [
    "./oled_bin -n 2 -I 128x64",  # Initialize 128x64 resolution
    "./oled_bin -n 2 -c",         # Clear the display
    "./oled_bin -n 2 -r 0",       # Rotate the display to 0 degrees
]

# Run each command to set up the OLED
for cmd in commands:
    run_command(cmd)

# Main loop to read LDR and update OLED dynamically
while True:
    ldr_state = read_ldr_state()  # Read the current state of the LDR
    print(f"LDR State: {'Light Detected' if ldr_state else 'Light Not Detected'}")

    # If light is detected (HIGH signal), display "Light Detected" and "Light On"
    if ldr_state:
        update_oled_message("Light Detected", "Light On")  # First line: "Light Detected", Second line: "Light On"
    else:
        update_oled_message("Light Not Detected", "Light Off")  # First line: "Light Not Detected", Second line: "Light Off"

    time.sleep(1)  # Delay for 1 second before checking the state again
