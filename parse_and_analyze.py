import xml.etree.ElementTree as ET
import logging

def parse_collision_log(filename):
    """
    Parses the collision log XML to extract collision events.
    Args:
    filename (str): Path to the XML file containing collision data.
    Returns:
    list: A list of dictionaries, each representing a collision event.
    """
    collisions = []
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        for collision in root.findall('.//collision'):
            collisions.append({
                "time": float(collision.get("time")),
                "collider": collision.get("collider"),
                "victim": collision.get("victim"),
                "colliderSpeed": float(collision.get("colliderSpeed")),
                "victimSpeed": float(collision.get("victimSpeed"))
            })
    except ET.ParseError as e:
        logging.error(f"Error parsing the collision log file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return collisions

def parse_simulation_log(filename):
    """
    Parses the simulation log to extract warnings about potential collisions.
    Args:
    filename (str): Path to the log file containing simulation data.
    Returns:
    list: A list of dictionaries, each containing information about a warning.
    """
    warnings = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if "collision warning" in line:
                    time, message = line.strip().split(":", 1)
                    warnings.append({"time": time.strip(), "warning_info": message.strip()})
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except Exception as e:
        logging.error(f"Error reading the simulation log file: {e}")
    return warnings

def analyze_algorithm(collisions, warnings):
    """
    Analyzes the effectiveness of the collision detection algorithm.
    Args:
    collisions (list): List of actual collisions parsed from the collision log.
    warnings (list): List of warnings generated by the simulation.
    """
    detected_collisions = 0
    for collision in collisions:
        for warning in warnings:
            if collision['collider'] in warning['warning_info'] and collision['victim'] in warning['warning_info']:
                detected_collisions += 1
                break
    total_collisions = len(collisions)
    precision = detected_collisions / total_collisions if total_collisions > 0 else 0
    print(f"Detected Collisions: {detected_collisions}")
    print(f"Total Collisions: {total_collisions}")
    print(f"Precision: {precision:.2f}")

if __name__ == "__main__":
    collisions = parse_collision_log('collision_log.txt')
    kalman_warnings = parse_simulation_log('simulation_data_kalman.log')
    constant_warnings = parse_simulation_log('simulation_data_constant.log')

    print("Kalman Filter Analysis:")
    analyze_algorithm(collisions, kalman_warnings)

    print("\nConstant Speed Model Analysis:")
    analyze_algorithm(collisions, constant_warnings)
