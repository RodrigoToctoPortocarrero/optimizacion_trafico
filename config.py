# config.py - VERSIÓN CON PARÁMETROS OPTIMIZADOS
class Config:
    # ==================== VENTANA ====================
    WINDOW_TITLE     = "Sistema de Optimización de Tráfico con Algoritmo Genético"
    WINDOW_WIDTH     = 1350
    WINDOW_HEIGHT    = 800
    COLOR_BG         = "#0f1620"
    UPDATE_INTERVAL  = 16

    # ==================== TODOS LOS COLORES DE LA GUI ====================
    COLOR_PRIMARY           = "#1e2a38"
    COLOR_SECONDARY         = "#16202c"
    COLOR_PANEL             = "#16202c"
    COLOR_ACCENT            = "#00bcd4"
    COLOR_SUCCESS           = "#2ecc71"
    COLOR_DANGER            = "#e74c3c"
    COLOR_INFO              = "#3498db"
    COLOR_WARNING           = "#f39c12"
    COLOR_LIGHT             = "#ecf0f1"
    COLOR_DARK              = "#2c3e50"
    COLOR_TEXT              = "#ecf0f1"
    COLOR_TEXT_DARK         = "#bdc3c7"
    COLOR_TEXT_SECONDARY    = "#95a5a6"
    COLOR_BUTTON_HOVER      = "#34495e"
    COLOR_HEADER            = "#1abc9c"
    CANVAS_BG               = "#1a1a2e"

    # ==================== CANVAS ====================
    CANVAS_WIDTH     = 1100
    CANVAS_HEIGHT    = 650
    FPS              = 60
    BACKGROUND_COLOR = "#1a1a2e"

    # ==================== COLORES SIMULACIÓN ====================
    ROAD_COLOR            = "#2c3e50"
    ROAD_LINE_COLOR       = "#ffeb3b"
    VEHICLE_COLOR_MOVING  = "#3498db"
    VEHICLE_COLOR_WAITING = "#e74c3c"
    LIGHT_GREEN           = "#00ff00"
    LIGHT_RED             = "#ff0000"
    LIGHT_OFF             = "#555555"

    # ==================== VELOCIDADES ====================
    VEHICLE_SPEED_MIN = 1.4
    VEHICLE_SPEED_MAX = 3.2

    # ==================== CARRETERAS ====================
    LANES = [
        (0, 200, 1100, 200, "horizontal"),
        (1100, 200, 0, 200, "horizontal"),
        (0, 450, 1100, 450, "horizontal"),
        (1100, 450, 0, 450, "horizontal"),
        (250, 0, 250, 650, "vertical"),
        (250, 650, 250, 0, "vertical"),
        (550, 0, 550, 650, "vertical"),
        (550, 650, 550, 0, "vertical"),
        (850, 0, 850, 650, "vertical"),
        (850, 650, 850, 0, "vertical"),
    ]

    # ==================== INTERSECCIONES ====================
    INTERSECTIONS = [
        {"id": 0, "x": 250, "y": 200},
        {"id": 1, "x": 550, "y": 200},
        {"id": 2, "x": 850, "y": 200},
        {"id": 3, "x": 250, "y": 450},
        {"id": 4, "x": 550, "y": 450},
        {"id": 5, "x": 850, "y": 450},
    ]

    # ==================== ALGORITMO GENÉTICO ====================
    # ==================== ALGORITMO GENÉTICO ====================
    GA_POPULATION_SIZE = 120     # Población más grande para más diversidad
    GA_GENERATIONS     = 120     # Generaciones equilibradas
    GA_MUTATION_RATE   = 0.22    # Tasa de mutación óptima
    GA_CROSSOVER_RATE  = 0.82    # Alta tasa de cruce
    GA_MIN_GREEN_TIME  = 25      # Límites realistas
    GA_MAX_GREEN_TIME  = 50
    GA_CYCLE_TIME      = 60