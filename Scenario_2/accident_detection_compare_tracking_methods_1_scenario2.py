import os
import sys
import numpy as np
import logging
from kalman_filter_scenario2 import kalman_filter_predict
from constant_speed_model_scenario2 import constant_speed_predict

# Setup logging
logging.basicConfig(filename='simulation_data_tracking_methods_scenario2.log', level=logging.INFO, format='%(asctime)s:%(message)s')

# Constants for detection thresholds and parameters
LEADER_DETECT_DIST = 10  # Distance in meters to check for a leading vehicle
COLLISION_WARN_GAP = 5  # Gap in meters below which a collision warning is issued
COLLISION_WARN_SPEED_DIFF = 2  # Speed difference in m/s to consider a collision warning
SIDE_SWIPE_THRESHOLD = 3  # Lateral distance in meters for side-swipe collision detection
TIME_DELTA = 1.0  # Time delta in seconds for prediction

# Ensure SUMO_HOME is set for access to SUMO libraries
if 'SUMO_HOME' not in os.environ:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
sys.path.append(tools)

import traci

def detect_collisions(vehicle_ids):
    for veh_id in vehicle_ids:
        try:
            pos = traci.vehicle.getPosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)

	    # Initialize state and covariance
            initial_state = np.array([pos[0], speed])
            initial_covariance = np.eye(2)

            # Predict future position using both models
            cs_prediction = constant_speed_predict(veh_id, TIME_DELTA)
            kf_prediction, _ = kalman_filter_predict(veh_id, initial_state, initial_covariance, TIME_DELTA)

            # Advanced collision detection logic
            # ...

        except Exception as e:
            logging.error(f"Error processing vehicle {veh_id}: {str(e)}")

def run():
    """
    Main function to run the simulation, detect collisions, and log data for machine learning.
    """
    sumoCmd = [
        "sumo-gui",
        "-c", "cross.sumocfg",
        "--collision.action", "warn",
        "--collision.mingap-factor", "2",
        "--collision-output", "collision_log_compare_scenario2.txt"
    ]

    traci.start(sumoCmd)

    while traci.simulation.getTime() <= 199.60:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        detect_collisions(vehicle_ids)

    traci.close()

if __name__ == "__main__":
    run()