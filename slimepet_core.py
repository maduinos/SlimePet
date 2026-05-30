APP_NAME = "SlimePet"
APP_VERSION = "v0.0.5"


def clamp_position(x, y, max_x, max_y):
    max_x = max(0, int(max_x))
    max_y = max(0, int(max_y))
    return (
        min(max(0, int(x)), max_x),
        min(max(0, int(y)), max_y),
    )
