import time
import RPi.GPIO as GPIO
import requests
from Sensor import get_flow_value, distance
from chlorineAI import predict_solenoid_opening_time

RELAY_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def open_solenoid_valve(open_time_seconds: float) -> None:
    print(f"Opening solenoid valve for {open_time_seconds} seconds.")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(open_time_seconds)
    GPIO.output(RELAY_PIN, GPIO.LOW)

def get_ph_level() -> float:
    try:
        response = requests.get('http://127.0.0.1:5000/PH_level')
        if response.status_code == 200:
            data = response.json()
            ph_level = float(data)  # Ensure that the response is properly converted to a float
            print("pH Level:", ph_level)
            return ph_level
        else:
            print("Failed to get pH level:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

def solenoid() -> None:
    timer_duration = 300
    timer_start = time.time()
    rain_detected = False
    initial_water_level = None  # Variable to store the initial water level

    try:
        while True:
            # Check if rainwater is pouring (using flowrate sensor)
            try:
                if get_flow_value() > 1:
                    rain_detected = True
                    timer_start = time.time()  # Reset timer
                    print("Rainwater detected. Timer reset.")

                    # Store the initial water level when rain is detected for the first time
                    if initial_water_level is None:
                        initial_water_level = distance()
                        print(f"Initial water level stored: {initial_water_level} liters")
            except Exception as e:
                print("Error reading flow value:", e)

            # If rain detected and timer expired, perform AI prediction and open solenoid valve
            if rain_detected and time.time() - timer_start >= timer_duration:
                print("Timer expired. Performing AI prediction.")

                # Read sensor data
                try:
                    current_water_level = distance()
                except Exception as e:
                    print("Error reading water level:", e)
                    current_water_level = None

                ph_level = get_ph_level()

                if current_water_level is not None and ph_level is not None:
                    # Calculate the difference in water levels
                    water_level_difference = current_water_level - initial_water_level

                    # Perform AI prediction for solenoid opening time based on water level difference
                    water_level_difference, ph_level, predicted_time = predict_solenoid_opening_time(
                        water_level_difference, ph_level)
                    print(f'Water Level Difference: {water_level_difference} L')
                    print(f'pH Level: {ph_level}')
                    print(f'Predicted Solenoid Opening Time: {predicted_time} seconds')

                    # Open solenoid valve for the predicted time
                    open_solenoid_valve(predicted_time)

                    # Reset rain detection and timer
                    rain_detected = False
                    timer_start = time.time()
                    print("Process Complete.")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up GPIO...")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    solenoid()
