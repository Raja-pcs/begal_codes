
import subprocess
import time
import Adafruit_BBIO.GPIO as GPIO

# GPIO Pins for switches and LEDs
SWITCH1_PIN = "P9_30"  # Digital input for switch 1
SWITCH2_PIN = "P9_41"  # Digital input for switch 2
LED1_PIN = "P9_18"  # Digital output for LED 1
LED2_PIN = "P9_16"  # Digital output for LED 2

# GPIO Setup
GPIO.setup(SWITCH1_PIN, GPIO.IN)  # Switch 1 input
GPIO.setup(SWITCH2_PIN, GPIO.IN)  # Switch 2 input
GPIO.setup(LED1_PIN, GPIO.OUT)    # LED 1 output
GPIO.setup(LED2_PIN, GPIO.OUT)    # LED 2 output

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

# List of commands to initialize the OLED
commands = [
    "./oled_bin -n 2 -I 128x64",  # Initialize 128x64 resolution
    "./oled_bin -n 2 -c",         # Clear the display
    "./oled_bin -n 2 -r 0",       # Rotate the display to 0 degrees
]

# Run each command to set up the OLED
for cmd in commands:
    run_command(cmd)

# Main loop to control LEDs and update OLED dynamically
switch1_last_state = 0  # Track the last state of switch 1
switch2_last_state = 0  # Track the last state of switch 2

while True:
    switch1_state = GPIO.input(SWITCH1_PIN)  # Read the state of switch 1
    switch2_state = GPIO.input(SWITCH2_PIN)  # Read the state of switch 2

    # Handle Switch 1
    if switch1_state == 1 and switch1_last_state == 0:  # Switch 1 pressed
        GPIO.output(LED1_PIN, GPIO.HIGH)  # Turn on LED 1
        update_oled_message("LED1: ON")
    elif switch1_state == 0 and switch1_last_state == 1:  # Switch 1 released
        GPIO.output(LED1_PIN, GPIO.LOW)  # Turn off LED 1
        update_oled_message("")  # Clear OLED

    # Handle Switch 2
    if switch2_state == 1 and switch2_last_state == 0:  # Switch 2 pressed
        GPIO.output(LED2_PIN, GPIO.HIGH)  # Turn on LED 2
        update_oled_message("LED2: ON")
    elif switch2_state == 0 and switch2_last_state == 1:  # Switch 2 released
        GPIO.output(LED2_PIN, GPIO.LOW)  # Turn off LED 2
        update_oled_message("")  # Clear OLED

    # Update last states
    switch1_last_state = switch1_state
    switch2_last_state = switch2_state

    time.sleep(0.1)  # Delay for debounce and CPU efficiency
