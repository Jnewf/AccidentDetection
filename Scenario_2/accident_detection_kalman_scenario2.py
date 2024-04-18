import os
import sys
import numpy as np
import logging
from kalman_filter_scenario2 import kalman_filter_predict
from constant_speed_model_scenario2 import constant_speed_predict

# Logging setup for data collection
logging.basicConfig(filename='simulation_data_kalman_scenario2.log', level=logging.INFO, format='%(asctime)s:%(message)s')

# Constants for detection thresholds and parameters
LEADER_DETECT_DIST = 10  # Distance in meters to check for a leading vehicle
COLLISION_WARN_GAP = 5  # Gap in meters below which a collision warning is issued
COLLISION_WARN_SPEED_DIFF = 2  # Minimum speed difference in m/s to consider a collision warning
SIDE_SWIPE_THRESHOLD = 3  # Lateral distance in meters to check for potential side-swipe collision
TIME_DELTA = 1.0  # Time delta in seconds for prediction

# Ensure SUMO_HOME is set for access to SUMO libraries
if 'SUMO_HOME' not in os.environ:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
sys.path.append(tools)

import traci  # Importing the SUMO TraCI library to interact with the simulation

def detect_collisions(vehicle_ids):
    """
    Detects potential collisions based on vehicle positions, speeds, and headings.
    Logs collision and warning events and highlights vehicles involved.
    """
    for veh_id in vehicle_ids:
        try:
            pos = traci.vehicle.getPosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
            initial_state = np.array([pos[0], speed])
            initial_covariance = np.eye(2)
            predicted_state_kf, _ = kalman_filter_predict(veh_id, initial_state, initial_covariance, TIME_DELTA)
            predicted_pos_kf = predicted_state_kf[0]

            # Rear-end collision detection
            leader_info = traci.vehicle.getLeader(veh_id, LEADER_DETECT_DIST)
            if leader_info:
                leader_id, leader_gap = leader_info
                leader_pos = traci.vehicle.getPosition(leader_id)
                leader_speed = traci.vehicle.getSpeed(leader_id)
                leader_initial_state = np.array([leader_pos[0], leader_speed])
                leader_predicted_state_kf, _ = kalman_filter_predict(leader_id, leader_initial_state, initial_covariance, TIME_DELTA)
                predicted_gap = leader_predicted_state_kf[0] - predicted_pos_kf

                if predicted_gap < COLLISION_WARN_GAP:
                    logging.warning(f"Rear-end collision warning: {leader_id} leading {veh_id}")
                    traci.vehicle.setColor(veh_id, (255, 0, 0, 255))
                    traci.vehicle.setColor(leader_id, (255, 255, 0, 255))

            # Side-swipe collision detection
            for other_id in vehicle_ids:
                if other_id != veh_id:
                    other_pos = traci.vehicle.getPosition(other_id)
                    other_speed = traci.vehicle.getSpeed(other_id)
                    other_initial_state = np.array([other_pos[0], other_speed])
                    other_predicted_state_kf, _ = kalman_filter_predict(other_id, other_initial_state, initial_covariance, TIME_DELTA)
                    lateral_dist = np.abs(pos[0] - other_pos[0])
                    predicted_lateral_dist = np.abs(predicted_pos_kf - other_predicted_state_kf[0])

                    if predicted_lateral_dist < SIDE_SWIPE_THRESHOLD:
                        if lateral_dist < SIDE_SWIPE_THRESHOLD:
                            logging.warning(f"Side-swipe collision warning: {veh_id} and {other_id}")
                            traci.vehicle.setColor(veh_id, (0, 0, 255, 255))

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
        "--collision-output", "collision_log_kalman_scenario2.txt"
    ]

    traci.start(sumoCmd)

    while traci.simulation.getTime() <= 199.60:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        detect_collisions(vehicle_ids)

    traci.close()

if __name__ == "__main__":
    run()