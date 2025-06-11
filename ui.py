import pygame
from config import GameConfig

class GameUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_hud(self, screen, car):
        """HUDの描画"""
        speed_kmh = car.get_speed_kmh()
        gear = car.current_gear
        torque_eff = car.get_torque_efficiency()
        
        # 速度表示
        speed_text = self.font.render(f"Speed: {speed_kmh:.1f} km/h", True, GameConfig.WHITE)
        screen.blit(speed_text, (10, 10))
        
        # ギア表示（トルク効率に応じて色変更）
        gear_color = GameConfig.GREEN if torque_eff > 0.8 else (GameConfig.RED if torque_eff < 0.5 else GameConfig.WHITE)
        gear_text = self.font.render(f"Gear: {gear}", True, gear_color)
        screen.blit(gear_text, (10, 50))
        
        # トルク効率表示
        torque_text = self.small_font.render(f"Torque: {torque_eff*100:.0f}%", True, gear_color)
        screen.blit(torque_text, (10, 85))
    
    def draw_stage_controls(self, screen):
        """ステージ選択モード用操作説明の描画"""
        controls_text = [
            "Controls:",
            "↑/W: Accelerate",
            "↓/S: Brake",
            "←→: Steering",
            "Q: Shift Up",
            "E: Shift Down",
            "",
            "Pixel Tracks:",
            "1: Oval Track",
            "2: Winding Track", 
            "3: Random Track",
            "",
            "Vector Tracks:",
            "4: Basic Track",
            "5: Winding Track",
            "6: Random Track",
            "",
            "ESC: Back to Menu"
        ]
        
        for i, text in enumerate(controls_text):
            control_surface = self.small_font.render(text, True, GameConfig.WHITE)
            screen.blit(control_surface, (GameConfig.SCREEN_WIDTH - 200, 10 + i * 16))
    
    def draw_track_info(self, screen, track_type):
        """トラック情報の描画"""
        track_info = f"Track: {track_type.capitalize()}"
        track_text = self.small_font.render(track_info, True, GameConfig.WHITE)
        screen.blit(track_text, (10, 120))
