import pygame
import math
from config import GameConfig, CarConfig

class Tachometer:
    """リアルなタコメーター"""
    
    def __init__(self, center_x, center_y, radius=80):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.inner_radius = radius - 15
        
        # RPM設定
        self.max_rpm = 8000
        self.redline_rpm = 7000
        self.idle_rpm = 800
        
        # 角度設定（下から時計回りに240度）
        self.start_angle = 240  # 開始角度
        self.sweep_angle = 240  # 全体の角度範囲
        
        # フォント
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # 色定義
        self.needle_color = (255, 255, 255)
        self.redline_color = (255, 100, 100)
        self.normal_color = (100, 255, 100)
        self.background_color = (30, 30, 30)
        self.text_color = (255, 255, 255)
    
    def calculate_rpm(self, car):
        """車の状態からRPMを計算"""
        speed = car.velocity.length()
        gear = car.current_gear
        
        if speed < 0.1:
            return self.idle_rpm
        
        # ギア比に基づくRPM計算
        gear_settings = CarConfig.GEAR_RATIOS[gear]
        max_speed_for_gear = gear_settings["max_speed"]
        
        # 速度比からRPMを計算
        speed_ratio = min(1.0, speed / max_speed_for_gear)
        
        # RPM範囲を計算
        min_rpm_for_gear = self.idle_rpm + (gear - 1) * 500
        max_rpm_for_gear = min(self.max_rpm, min_rpm_for_gear + 3000)
        
        rpm = min_rpm_for_gear + (max_rpm_for_gear - min_rpm_for_gear) * speed_ratio
        
        # アクセル入力による微調整
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            rpm += 200  # アクセル時のRPM上昇
        
        return min(self.max_rpm, rpm)
    
    def draw(self, screen, car):
        """タコメーターの描画"""
        current_rpm = self.calculate_rpm(car)
        speed_kmh = car.get_speed_kmh()
        
        # 背景円
        pygame.draw.circle(screen, self.background_color, 
                         (self.center_x, self.center_y), self.radius)
        pygame.draw.circle(screen, (60, 60, 60), 
                         (self.center_x, self.center_y), self.radius, 3)
        
        # RPM目盛りを描画
        self._draw_rpm_scale(screen)
        
        # RPMゾーンを描画
        self._draw_rpm_zones(screen)
        
        # 針を描画
        self._draw_needle(screen, current_rpm)
        
        # 中央の速度表示
        self._draw_speed_display(screen, speed_kmh)
        
        # ギア表示
        self._draw_gear_display(screen, car.current_gear)
        
        # RPM数値表示
        self._draw_rpm_display(screen, current_rpm)
    
    def _draw_rpm_scale(self, screen):
        """RPM目盛りの描画"""
        for rpm in range(0, self.max_rpm + 1000, 1000):
            angle_deg = self._rpm_to_angle(rpm)
            angle_rad = math.radians(angle_deg)
            
            # 大きな目盛り
            start_x = self.center_x + (self.radius - 20) * math.cos(angle_rad)
            start_y = self.center_y + (self.radius - 20) * math.sin(angle_rad)
            end_x = self.center_x + (self.radius - 5) * math.cos(angle_rad)
            end_y = self.center_y + (self.radius - 5) * math.sin(angle_rad)
            
            color = self.redline_color if rpm >= self.redline_rpm else (200, 200, 200)
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)
            
            # 数値表示
            if rpm % 2000 == 0:
                text = self.font_small.render(str(rpm // 1000), True, color)
                text_x = self.center_x + (self.radius - 35) * math.cos(angle_rad) - text.get_width() // 2
                text_y = self.center_y + (self.radius - 35) * math.sin(angle_rad) - text.get_height() // 2
                screen.blit(text, (text_x, text_y))
        
        # 小さな目盛り
        for rpm in range(0, self.max_rpm + 500, 500):
            if rpm % 1000 != 0:  # 大きな目盛りと重複しない
                angle_deg = self._rpm_to_angle(rpm)
                angle_rad = math.radians(angle_deg)
                
                start_x = self.center_x + (self.radius - 15) * math.cos(angle_rad)
                start_y = self.center_y + (self.radius - 15) * math.sin(angle_rad)
                end_x = self.center_x + (self.radius - 5) * math.cos(angle_rad)
                end_y = self.center_y + (self.radius - 5) * math.sin(angle_rad)
                
                color = self.redline_color if rpm >= self.redline_rpm else (150, 150, 150)
                pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 1)
    
    def _draw_rpm_zones(self, screen):
        """RPMゾーンの描画"""
        # レッドゾーン
        redline_start_angle = self._rpm_to_angle(self.redline_rpm)
        redline_end_angle = self._rpm_to_angle(self.max_rpm)
        
        # レッドゾーンの弧を描画
        for angle in range(int(redline_start_angle), int(redline_end_angle) + 1, 2):
            angle_rad = math.radians(angle)
            x = self.center_x + (self.radius - 10) * math.cos(angle_rad)
            y = self.center_y + (self.radius - 10) * math.sin(angle_rad)
            pygame.draw.circle(screen, self.redline_color, (int(x), int(y)), 2)
    
    def _draw_needle(self, screen, rpm):
        """針の描画"""
        angle_deg = self._rpm_to_angle(rpm)
        angle_rad = math.radians(angle_deg)
        
        # 針の先端
        needle_end_x = self.center_x + (self.radius - 25) * math.cos(angle_rad)
        needle_end_y = self.center_y + (self.radius - 25) * math.sin(angle_rad)
        
        # 針の基部
        base_angle_rad = angle_rad + math.pi
        needle_base_x = self.center_x + 15 * math.cos(base_angle_rad)
        needle_base_y = self.center_y + 15 * math.sin(base_angle_rad)
        
        # 針を描画
        pygame.draw.line(screen, self.needle_color, 
                        (needle_base_x, needle_base_y), (needle_end_x, needle_end_y), 3)
        
        # 中央のピン
        pygame.draw.circle(screen, self.needle_color, 
                         (self.center_x, self.center_y), 8)
        pygame.draw.circle(screen, self.background_color, 
                         (self.center_x, self.center_y), 5)
    
    def _draw_speed_display(self, screen, speed_kmh):
        """中央の速度表示"""
        speed_text = self.font_large.render(f"{speed_kmh:.0f}", True, self.text_color)
        speed_rect = speed_text.get_rect(center=(self.center_x, self.center_y - 10))
        screen.blit(speed_text, speed_rect)
        
        # km/h表示
        unit_text = self.font_small.render("km/h", True, self.text_color)
        unit_rect = unit_text.get_rect(center=(self.center_x, self.center_y + 15))
        screen.blit(unit_text, unit_rect)
    
    def _draw_gear_display(self, screen, gear):
        """ギア表示"""
        gear_text = self.font_medium.render(f"G{gear}", True, self.text_color)
        gear_rect = gear_text.get_rect(center=(self.center_x - 50, self.center_y + 40))
        screen.blit(gear_text, gear_rect)
    
    def _draw_rpm_display(self, screen, rpm):
        """RPM数値表示"""
        rpm_text = self.font_small.render(f"{rpm:.0f} RPM", True, self.text_color)
        rpm_rect = rpm_text.get_rect(center=(self.center_x + 50, self.center_y + 40))
        screen.blit(rpm_text, rpm_rect)
    
    def _rpm_to_angle(self, rpm):
        """RPMを角度に変換"""
        rpm_ratio = rpm / self.max_rpm
        angle = self.start_angle + (self.sweep_angle * rpm_ratio)
        return angle
    
    def is_in_redline(self, rpm):
        """レッドラインかどうか判定"""
        return rpm >= self.redline_rpm
