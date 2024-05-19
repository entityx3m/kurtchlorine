import time
from phsensor import read_ph_level
from test_water_level import water_distance
from test_flow_rate import water_flow
from chlorineAI import predict_solenoid_opening_time


def open_solenoid_valve(open_time_seconds):
    print(f"Opening solenoid valve for {open_time_seconds} seconds.")


def main():
    timer_duration = 3
    timer_start = time.time()
    rain_detected = False
    initial_water_level = None  # Variable to store the initial water level

    while True:
        # Check if rainwater is pouring (using flowrate sensor)
        if water_flow() > 0.5:
            rain_detected = True
            timer_start = time.time()  # Reset timer
            print("Rainwater detected. Timer reset.")

            # Store the initial water level when rain is detected for the first time
            if initial_water_level is None:
                initial_water_level = water_distance()
                print(f"Initial water level stored: {initial_water_level} liters")

        # If rain detected and timer expired, perform AI prediction and open solenoid valve
        if rain_detected and time.time() - timer_start >= timer_duration:
            print("Timer expired. Performing AI prediction.")

            # Read sensor data
            current_water_level = water_distance()
            ph_level = read_ph_level()

            # Calculate the difference in water levels
            water_level_difference = current_water_level - initial_water_level

            # Perform AI prediction for solenoid opening time based on water level difference
            water_level_difference, ph_level, predicted_time = predict_solenoid_opening_time(water_level_difference,
                                                                                             ph_level)
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


if __name__ == "__main__":
    main()
