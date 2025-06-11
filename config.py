# ゲーム設定
class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # 色定義
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

# 車両設定
class CarConfig:
    # 物理パラメータ（グラベル仕様 - 重量感を追加）
    LATERAL_GRIP = 0.45
    BASE_DECELERATION = 0.04  # 摩擦を弱く（慣性で長く滑る）
    MAX_STEERING_ANGLE = 30
    WHEELBASE = 30
    
    # 車両重量感パラメータ
    VEHICLE_MASS = 1.2  # 車両の慣性質量係数
    
    # ギア設定（ラリーカー仕様 - より現実的な加速度）
    GEAR_RATIOS = {
        1: {"max_speed": 2.8, "base_acceleration": 0.12, "min_speed": 0.0},   # 1速: 加速度を下げる
        2: {"max_speed": 4.5, "base_acceleration": 0.09, "min_speed": 1.8},   # 2速: より段階的に
        3: {"max_speed": 6.5, "base_acceleration": 0.07, "min_speed": 3.2},   # 3速: 重量感を出す
        4: {"max_speed": 8.2, "base_acceleration": 0.055, "min_speed": 5.0},  # 4速: さらに緩やかに
        5: {"max_speed": 9.8, "base_acceleration": 0.045, "min_speed": 6.8},  # 5速: 高速域は時間をかけて
        6: {"max_speed": 11.0, "base_acceleration": 0.035, "min_speed": 8.5}  # 6速: 最高速は徐々に
    }
