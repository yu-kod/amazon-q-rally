import pygame
import math
from config import GameConfig

class DeathLine:
    """後ろから迫ってくるゲームオーバーライン"""
    
    def __init__(self):
        self.y_position = 0  # ラインの現在位置
        self.base_speed = 0.5  # 基本速度（ピクセル/フレーム）
        self.acceleration = 0.001  # 時間経過による加速
        self.current_speed = self.base_speed
        self.warning_distance = 150  # 警告を出す距離
        self.danger_distance = 80   # 危険警告を出す距離
        
        # 視覚効果用
        self.pulse_timer = 0
        self.warning_alpha = 0
        
    def update(self, car_position, distance_traveled):
        """デスラインの更新"""
        # 進行距離に応じて速度を調整
        difficulty_multiplier = 1 + (distance_traveled * 0.0001)
        self.current_speed = self.base_speed * difficulty_multiplier
        
        # ラインを上方向に移動（車を追いかける）
        self.y_position -= self.current_speed
        
        # 車との距離を維持（あまり離れすぎないように）
        car_y = car_position.y
        max_distance = 400  # 最大距離
        
        if car_y - self.y_position > max_distance:
            # 車が遠すぎる場合、少し追いつく
            self.y_position = car_y - max_distance
        
        # 視覚効果の更新（点滅なし）
        self.pulse_timer += 0.1
        distance_to_car = car_y - self.y_position
        
        if distance_to_car < self.danger_distance:
            # 危険状態：固定の警告表示
            self.warning_alpha = 100
        elif distance_to_car < self.warning_distance:
            # 警告状態：薄い警告表示
            self.warning_alpha = 50
        else:
            # 安全状態
            self.warning_alpha = 0
    
    def draw(self, screen, camera_y):
        """デスラインの描画"""
        # 画面座標でのライン位置
        screen_y = self.y_position - camera_y
        
        # ラインが画面内にある場合のみ描画
        if -50 <= screen_y <= GameConfig.SCREEN_HEIGHT + 50:
            # メインのデスライン（赤い線）
            pygame.draw.line(screen, (255, 0, 0), 
                           (0, screen_y), (GameConfig.SCREEN_WIDTH, screen_y), 4)
            
            # ライン上の装飾（危険マーク）
            for x in range(0, GameConfig.SCREEN_WIDTH, 40):
                # 三角形の危険マーク
                points = [
                    (x + 20, screen_y - 8),
                    (x + 15, screen_y + 8),
                    (x + 25, screen_y + 8)
                ]
                pygame.draw.polygon(screen, (255, 255, 0), points)
                pygame.draw.polygon(screen, (255, 0, 0), points, 2)
        
        # 警告エフェクトの描画
        if self.warning_alpha > 0:
            self._draw_warning_effects(screen)
    
    def _draw_warning_effects(self, screen):
        """警告エフェクトの描画（目に優しいバージョン）"""
        if self.warning_alpha <= 0:
            return
        
        # 画面端に静的な警告バーを表示
        edge_width = 8
        warning_color = (255, 100, 100) if self.warning_alpha > 75 else (255, 200, 100)
        
        # 左右の端
        pygame.draw.rect(screen, warning_color, 
                        (0, 0, edge_width, GameConfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, warning_color, 
                        (GameConfig.SCREEN_WIDTH - edge_width, 0, edge_width, GameConfig.SCREEN_HEIGHT))
        
        # 上下の端（薄く）
        top_bottom_alpha = self.warning_alpha // 2
        if top_bottom_alpha > 0:
            warning_surface = pygame.Surface((GameConfig.SCREEN_WIDTH, edge_width))
            warning_surface.set_alpha(top_bottom_alpha)
            warning_surface.fill(warning_color)
            
            screen.blit(warning_surface, (0, 0))  # 上端
            screen.blit(warning_surface, (0, GameConfig.SCREEN_HEIGHT - edge_width))  # 下端
    
    def check_collision(self, car_position):
        """車との衝突判定"""
        return car_position.y >= self.y_position
    
    def get_distance_to_car(self, car_position):
        """車との距離を取得（正の値で表示）"""
        distance = car_position.y - self.y_position
        return max(0, distance)  # 負の値を防ぐ
    
    def get_warning_level(self, car_position):
        """警告レベルを取得"""
        distance = self.get_distance_to_car(car_position)
        
        if distance < self.danger_distance:
            return "DANGER"
        elif distance < self.warning_distance:
            return "WARNING"
        else:
            return "SAFE"
    
    def reset(self, car_position):
        """デスラインをリセット"""
        self.y_position = car_position.y + 300  # 車の後ろに配置
        self.current_speed = self.base_speed
        self.pulse_timer = 0
        self.warning_alpha = 0

class DeathLineUI:
    """デスライン関連のUI表示"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.last_distance_ratio = 1.0  # 滑らかなアニメーション用
    
    def draw_death_line_info(self, screen, death_line, car_position):
        """デスライン情報の表示"""
        distance = death_line.get_distance_to_car(car_position)
        warning_level = death_line.get_warning_level(car_position)
        
        # 距離表示
        distance_text = self.small_font.render(f"Death Line: {distance:.0f}m", True, GameConfig.WHITE)
        screen.blit(distance_text, (10, 190))
        
        # 警告レベル表示（点滅なし）
        if warning_level == "DANGER":
            color = (255, 100, 100)  # 明るい赤
            message = "DANGER! SPEED UP!"
        elif warning_level == "WARNING":
            color = (255, 200, 100)  # オレンジ
            message = "WARNING! Death Line Approaching!"
        else:
            color = GameConfig.GREEN
            message = "Safe Distance"
        
        warning_text = self.small_font.render(message, True, color)
        screen.blit(warning_text, (10, 210))
        
        # 距離バー
        self._draw_distance_bar(screen, distance, death_line.warning_distance)
    
    def _draw_distance_bar(self, screen, current_distance, max_distance):
        """距離バーの描画（滑らかなアニメーション）"""
        bar_x = GameConfig.SCREEN_WIDTH - 50
        bar_y = 50
        bar_width = 20
        bar_height = 200
        
        # バー背景
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # 距離に応じたバーの色と高さ（滑らかに変化）
        target_ratio = min(1.0, current_distance / max_distance)
        
        # 滑らかなアニメーション
        self.last_distance_ratio += (target_ratio - self.last_distance_ratio) * 0.1
        distance_ratio = self.last_distance_ratio
        
        fill_height = int(bar_height * distance_ratio)
        
        # グラデーション効果
        if distance_ratio < 0.3:
            color = (255, 100, 100)  # 明るい赤
        elif distance_ratio < 0.6:
            # 赤からオレンジへのグラデーション
            t = (distance_ratio - 0.3) / 0.3
            color = (255, int(100 + 100 * t), 100)
        else:
            # オレンジから緑へのグラデーション
            t = (distance_ratio - 0.6) / 0.4
            color = (int(255 - 255 * t), int(200 + 55 * t), int(100 + 155 * t))
        
        # バーを下から上に向かって描画
        pygame.draw.rect(screen, color, 
                        (bar_x, bar_y + bar_height - fill_height, bar_width, fill_height))
        
        # バー枠
        pygame.draw.rect(screen, GameConfig.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # ラベル
        label_text = self.small_font.render("Distance", True, GameConfig.WHITE)
        screen.blit(label_text, (bar_x - 30, bar_y - 25))
        
        # 危険ゾーンマーカー
        danger_line_y = bar_y + bar_height - int(bar_height * 0.3)
        pygame.draw.line(screen, (255, 255, 255), 
                        (bar_x - 5, danger_line_y), (bar_x + bar_width + 5, danger_line_y), 2)
