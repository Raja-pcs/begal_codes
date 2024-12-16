import subprocess
import time
import Adafruit_BBIO.GPIO as GPIO

# GPIO Pins for Ultrasonic Sensor
TRIG_PIN = "P9_27"  # Trigger pin for ultrasonic sensor
ECHO_PIN = "P9_23"  # Echo pin for ultrasonic sensor

# GPIO Setup
GPIO.setup(TRIG_PIN, GPIO.OUT)  # Trigger pin as output
GPIO.setup(ECHO_PIN, GPIO.IN)   # Echo pin as input

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

def measure_distance():
    """
    Measure the distance using the ultrasonic sensor.
    Returns the distance in centimeters.
    """
    # Send a 10µs pulse to trigger
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10µs
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the duration of the echo
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()

    # Calculate distance (duration * speed of sound / 2)
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Speed of sound is 34300 cm/s
    return round(distance, 2)

# List of commands to initialize the OLED
commands = [
    "./oled_bin -n 2 -I 128x64",  # Initialize 128x64 resolution
    "./oled_bin -n 2 -c",         # Clear the display
    "./oled_bin -n 2 -r 0",       # Rotate the display to 0 degrees
]

# Run each command to set up the OLED
for cmd in commands:
    run_command(cmd)

# Main loop to continuously measure distance and update OLED
while True:
    distance = measure_distance()  # Get distance reading
    update_oled_message("Distance:", f"{distance} cm")  # Update OLED with the reading
    time.sleep(1)  # Delay for stability
