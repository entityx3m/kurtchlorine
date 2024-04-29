import time
import RPi.GPIO as GPIO
from dht11 import read_dht11_sensor_data
from Sensor import distance, get_flow_value
from chlorineAI import predict_solenoid_opening_time

RELAY_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)


def open_solenoid_valve(open_time_seconds):

    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(open_time_seconds)
    GPIO.output(RELAY_PIN, GPIO.LOW)


def main():
    global last_water_level
    timer_duration = 5 * 60
    timer_start = time.time()
    rain_detected = False

    while True:
        # Check if rainwater is pouring (using flowrate sensor)
        if get_flow_value() > 0:
            rain_detected = True
            timer_start = time.time()  # Reset timer
            print("Rainwater detected. Timer reset.")

        # If rain detected and timer expired, perform AI prediction and open solenoid valve
        if rain_detected and time.time() - timer_start >= timer_duration:
            print("Timer expired. Performing AI prediction.")

            # Read sensor data
            water_level = distance()
            temperature, humidity = read_dht11_sensor_data()

            # Calculate the difference in water level since last recording
            water_level_difference = water_level - last_water_level
            last_water_level = water_level  # Update last recorded water level

            # Perform AI prediction for solenoid opening time based on water level difference
            predicted_time = predict_solenoid_opening_time(water_level_difference, temperature, humidity)
            print(f"Predicted Solenoid Opening Time: {predicted_time} seconds")

            # Open solenoid valve for the predicted time
            open_solenoid_valve(predicted_time)

            # Reset rain detection and timer
            rain_detected = False
            timer_start = time.time()
            print("Solenoid valve opened.")

        time.sleep(1)


if __name__ == "__main__":
    main()
