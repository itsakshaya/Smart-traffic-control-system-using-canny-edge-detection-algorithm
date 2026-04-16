def get_signal_timing(density: float):

    if density < 15:
        return {
            "level": "Low",
            "green_time": 20,
            "message": "Light traffic"
        }

    elif density < 35:
        return {
            "level": "Medium",
            "green_time": 40,
            "message": "Moderate traffic"
        }

    else:
        return {
            "level": "High",
            "green_time": 60,
            "message": "Heavy traffic"
        }