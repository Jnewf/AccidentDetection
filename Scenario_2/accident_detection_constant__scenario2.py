import os
import sys
import numpy as np
import logging
from constant_speed_model_scenario2 import constant_speed_predict

# Logging setup for data collection
logging.basicConfig(filename='simulation_data_constant_scenario2.log', level=logging.INFO, format='%(asctime)s:%(message)s')

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
            predicted_pos = constant_speed_predict(veh_id, TIME_DELTA)

            # Rear-end collision detection
            leader_info = traci.vehicle.getLeader(veh_id, LEADER_DETECT_DIST)
            if leader_info:
                leader_id, leader_gap = leader_info
                leader_predicted_pos = constant_speed_predict(leader_id, TIME_DELTA)
                predicted_gap = leader_gap - (leader_predicted_pos - predicted_pos)
                
                if predicted_gap < COLLISION_WARN_GAP:
                    logging.warning(f"Rear-end collision warning: {leader_id} leading {veh_id}")
                    traci.vehicle.setColor(veh_id, (255, 0, 0, 255))  # Following vehicle in red
                    traci.vehicle.setColor(leader_id, (255, 255, 0, 255))  # Leading vehicle in yellow

            # Side-swipe collision detection
            for other_id in vehicle_ids:
                if other_id != veh_id:
                    other_pos = traci.vehicle.getPosition(other_id)
                    other_predicted_pos = constant_speed_predict(other_id, TIME_DELTA)
                    lateral_dist = np.abs(pos[0] - other_pos[0])
                    predicted_lateral_dist = np.abs(predicted_pos - other_predicted_pos)

                    if predicted_lateral_dist < SIDE_SWIPE_THRESHOLD:
                        if lateral_dist < SIDE_SWIPE_THRESHOLD:
                            logging.warning(f"Side-swipe collision warning: {veh_id} and {other_id}")
                            traci.vehicle.setColor(veh_id, (0, 0, 255, 255))  # Vehicle in blue

        except Exception as e:
            logging.error(f"Error processing vehicle {veh_id}: {str(e)}")

def run():
    """
    Main function to run the simulation, detect collisions, and log data for machine learning.
    """
    sumoCmd = [
        "sumo-gui",  # or "sumo" for non-GUI mode
        "-c", "cross.sumocfg",
        "--collision.action", "warn",  # Action taken on collision
        "--collision.mingap-factor", "2",  # Collision min gap factor
        # "--collision-output", "collision_log_scenario2.txt"  # Collision log output file
    ]

    traci.start(sumoCmd)

    while traci.simulation.getTime() <= 199.60:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        detect_collisions(vehicle_ids)

    traci.close()

if __name__ == "__main__":
    run()
