APP_NAME = "SlimePet"
APP_VERSION = "v0.0.4"


def clamp_position(x, y, max_x, max_y):
    return (
        min(max(0, int(x)), int(max_x)),
        min(max(0, int(y)), int(max_y)),
    )
