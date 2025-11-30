# Configuración global de la aplicación
class Config:
    # Ventana
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    WINDOW_TITLE = "🚦 Sistema de Optimización de Tráfico con AG"
    
    # Canvas de simulación
    CANVAS_WIDTH = 1100
    CANVAS_HEIGHT = 650
    CANVAS_BG = "#2c3e50"
    
    # Carreteras
    ROAD_COLOR = "#34495e"
    ROAD_LINE_COLOR = "#f39c12"
    ROAD_WIDTH = 50
    LANE_WIDTH = 25
    
    # Intersecciones (Grid 3x2)
    INTERSECTIONS = [
        {"id": 0, "x": 250, "y": 200, "label": "I0"},
        {"id": 1, "x": 550, "y": 200, "label": "I1"},
        {"id": 2, "x": 850, "y": 200, "label": "I2"},
        {"id": 3, "x": 250, "y": 450, "label": "I3"},
        {"id": 4, "x": 550, "y": 450, "label": "I4"},
        {"id": 5, "x": 850, "y": 450, "label": "I5"},
    ]
    
    # Carriles (cada carretera tiene 2 carriles)
    # Formato: (x1, y1, x2, y2, dirección)
    LANES = [
        # Horizontales superiores
        (0, 188, 1100, 188, "horizontal"),    # Carril superior de la fila 1
        (0, 212, 1100, 212, "horizontal"),    # Carril inferior de la fila 1
        
        # Horizontales inferiores
        (0, 438, 1100, 438, "horizontal"),    # Carril superior de la fila 2
        (0, 462, 1100, 462, "horizontal"),    # Carril inferior de la fila 2
        
        # Verticales izquierdos
        (238, 0, 238, 650, "vertical"),       # Carril izquierdo columna 1
        (262, 0, 262, 650, "vertical"),       # Carril derecho columna 1
        
        # Verticales medios
        (538, 0, 538, 650, "vertical"),       # Carril izquierdo columna 2
        (562, 0, 562, 650, "vertical"),       # Carril derecho columna 2
        
        # Verticales derechos
        (838, 0, 838, 650, "vertical"),       # Carril izquierdo columna 3
        (862, 0, 862, 650, "vertical"),       # Carril derecho columna 3
    ]
    
    # Vehículos
    VEHICLE_SIZE = 8
    VEHICLE_COLOR_MOVING = "#3498db"
    VEHICLE_COLOR_WAITING = "#e74c3c"
    VEHICLE_SPEED_MIN = 2.0
    VEHICLE_SPEED_MAX = 3.5
    VEHICLE_SPAWN_INTERVAL = 0.3  # segundos
    
    # Semáforos
    LIGHT_SIZE = 35
    LIGHT_BG = "#f4d03f"
    LIGHT_GREEN = "#00ff00"
    LIGHT_RED = "#ff0000"
    LIGHT_YELLOW = "#ffff00"
    LIGHT_OFF = "#2c2c2c"
    
    # Algoritmo Genético
    GA_POPULATION_SIZE = 40
    GA_GENERATIONS = 100
    GA_MUTATION_RATE = 0.15
    GA_CROSSOVER_RATE = 0.8
    GA_MIN_GREEN_TIME = 15
    GA_MAX_GREEN_TIME = 60
    GA_CYCLE_TIME = 90
    
    # Animación
    FPS = 60
    UPDATE_INTERVAL = 16  # milisegundos (1000/60)
    
    # Colores de la interfaz
    COLOR_BG = "#1a1a2e"
    COLOR_PANEL = "#16213e"
    COLOR_PRIMARY = "#3498db"
    COLOR_SUCCESS = "#2ecc71"
    COLOR_DANGER = "#e74c3c"
    COLOR_WARNING = "#f39c12"
    COLOR_TEXT = "#ecf0f1"
    COLOR_TEXT_SECONDARY = "#bdc3c7"