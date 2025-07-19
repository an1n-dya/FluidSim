# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Simulation settings
SIM_RESOLUTION = 128
SCALE = SCREEN_WIDTH // SIM_RESOLUTION
DT = 0.1
DIFFUSION = 0.0001
VISCOSITY = 0.0000001
VORTICITY = 1.0  # Strength of vorticity confinement

# Visual settings
SHADING = True
COLORFUL = True
BLOOM = True
BLOOM_INTENSITY = 0.8
BLOOM_THRESHOLD = 0.6
SUNRAYS = True
SUNRAYS_WEIGHT = 0.9
BACKGROUND_COLOR = (0, 0, 0)
BACKGROUND_IMAGE = None # Path to image file or None

# Interaction settings
RANDOM_SPLATS = False
SPLAT_FREQUENCY = 10 # Lower is more frequent

# Audio settings
AUDIO_VISUALIZER = False

def update_settings_from_ui(values):
    global DIFFUSION, VISCOSITY, VORTICITY, BLOOM_INTENSITY, BLOOM_THRESHOLD, SUNRAYS_WEIGHT
    global SHADING, COLORFUL, BLOOM, SUNRAYS, RANDOM_SPLATS
    DIFFUSION = values['density']
    VISCOSITY = values['velocity']
    VORTICITY = values['vorticity']
    BLOOM_INTENSITY = values['bloom_intensity']
    BLOOM_THRESHOLD = values['bloom_threshold']
    SUNRAYS_WEIGHT = values['sunrays_weight']
    SHADING = values['shading']
    COLORFUL = values['colorful']
    BLOOM = values['bloom']
    SUNRAYS = values['sunrays']
    RANDOM_SPLATS = values['random_splats']
