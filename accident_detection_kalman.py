import os
import sys
import numpy as np
import logging
from kalman_filter import kalman_filter_predict
from constant_speed_model import constant_speed_predict

# Logging setup for data collection
logging.basicConfig(filename='simulation_data_kalman.log', level=logging.INFO, format='%(asctime)s:%(message)s')

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
    Highlights vehicles involved in potential collisions.
    """
    for veh_id in vehicle_ids:
        try:
            pos = traci.vehicle.getPosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
            heading = traci.vehicle.getAngle(veh_id)

            # Predict future position using constant speed model or Kalman filter
            predicted_pos_cs = constant_speed_predict(veh_id, TIME_DELTA)
            predicted_state_kf, _ = kalman_filter_predict(veh_id, np.eye(2), TIME_DELTA)
            predicted_pos_kf = predicted_state_kf[0]

            # Choose which prediction to use (e.g., based on previous accuracy analysis)
            # For now, let's use the Kalman Filter prediction as an example
            predicted_pos = predicted_pos_kf

            # Rear-end collision detection based on predicted positions
            leader_info = traci.vehicle.getLeader(veh_id, LEADER_DETECT_DIST)
            if leader_info:
                leader_id, leader_gap = leader_info
                leader_predicted_state_kf, _ = kalman_filter_predict(leader_id, np.eye(2), TIME_DELTA)
                leader_predicted_pos = leader_predicted_state_kf[0]

                # Check if the predicted gap is smaller than the warning threshold
                predicted_gap = leader_predicted_pos - predicted_pos
                if predicted_gap < COLLISION_WARN_GAP:
                    logging.warning(f"Rear-end collision warning: {leader_id} leading {veh_id}")
                    traci.vehicle.setColor(veh_id, (255, 0, 0, 255))  # Following vehicle in red
                    traci.vehicle.setColor(leader_id, (255, 255, 0, 255))  # Leading vehicle in yellow

            # Side-swipe collision detection based on predicted lateral distances
            for other_id in vehicle_ids:
                if other_id != veh_id:
                    other_predicted_state_kf, _ = kalman_filter_predict(other_id, np.eye(2), TIME_DELTA)
                    other_predicted_pos = other_predicted_state_kf[0]
                    lateral_dist = np.abs(predicted_pos - other_predicted_pos)  # Assuming simple lateral distance calculation

                    if lateral_dist < SIDE_SWIPE_THRESHOLD:
                        logging.warning(f"Side-swipe collision warning: {veh_id} and {other_id}")
                        traci.vehicle.setColor(veh_id, (0, 0, 255, 255))  # Vehicle in blue

        except Exception as e:
            logging.error(f"Error processing vehicle {veh_id}: {str(e)}")

def run():
    """
    Main function to run the simulation, detect collisions, and log data for machine learning.
    """
    traci.start(["sumo-gui", "-c", "accident.sumocfg"])
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        detect_collisions(vehicle_ids)
    traci.close()

if __name__ == "__main__":
    run()
