from math import floor

# ------------- DIMENSIONS -------------
# Field dimensions in game units
FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
GOAL_SPAN = 240
CHAMBER_SIZE = 30  # on both size - eg: 30 = 30mm x 30mm

# Objects sizes in game units
PUCK_RADIUS = 32
STRIKER_RADIUS = 50

# Limits
YLIMIT = 230
XLIMIT = 65
STRIKER_AREA_WIDTH = 446
CORNER_SAFEGUARD_X = XLIMIT + STRIKER_RADIUS * 2
CORNER_SAFEGUARD_Y = STRIKER_RADIUS + PUCK_RADIUS * 2
GOAL_CORNER_SAFEGUARD_X = 0  # STRIKER_RADIUS + PUCK_RADIUS*1.5
GOAL_CORNER_SAFEGUARD_Y = 0  # STRIKER_RADIUS + PUCK_RADIUS*1.5

# -------------- STRATEGY --------------
DEFENSE_LINE = STRIKER_RADIUS + PUCK_RADIUS
STOPPING_LINE = 200
CLOSE_DISTANCE = PUCK_RADIUS  # what is considered to be "close enough"

# -------------- MOTORS --------------
# Striker limitations
MAX_ACCELERATION = 30000
MAX_DECELERATION = 100000
MAX_SPEED = 3000
KP_GAIN = MAX_DECELERATION / (MAX_SPEED * 2)

# -------------- Data collector --------------
CLIP_LENGTH = 5  # seconds
CLIP_BEFORE_AFTER_RATIO = 8 / 10  # cant be zero
CLIP_FRAMERATE = 15