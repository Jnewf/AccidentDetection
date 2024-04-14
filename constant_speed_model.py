import traci

def constant_speed_predict(vehicle_id, time_delta):
    """
    Predicts the future position of a vehicle using the constant speed
    model and real-time data from SUMO via TraCI.

    Args:
        vehicle_id (str): The ID of the vehicle in the SUMO simulation.
        time_delta (float): The time interval for prediction in seconds.

    Returns:
        float: The predicted future position of the vehicle along the X-axis.
    """
    initial_position = traci.vehicle.getPosition(vehicle_id)[0]  # X-axis position
    initial_speed = traci.vehicle.getSpeed(vehicle_id)
    future_position = initial_position + (initial_speed * time_delta)
    return future_position
