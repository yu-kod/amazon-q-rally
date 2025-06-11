import pygame
import sys
from config import GameConfig
from realistic_rally_car import RealisticRallyCar
from ui import GameUI
from endless_track_advanced import AdvancedEndlessPixelTrack  # 元に戻す
from death_line import DeathLine, DeathLineUI
from tachometer import Tachometer

class EndlessRallyGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Endless Rally Game - Realistic Edition")
        self.clock = pygame.time.Clock()
        
        # 高度なエンドレストラック作成
        self.track = AdvancedEndlessPixelTrack()
        
        # リアルな車両作成
        self.car = RealisticRallyCar(self.track)
        # 車を画面の下部に配置
        self.car.position = pygame.math.Vector2(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT - 100)
        self.car.rect.center = self.car.position
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.car)
        
        # デスライン作成
        self.death_line = DeathLine()
        self.death_line.reset(self.car.position)
        
        # タコメーター作成（左下に配置）
        self.tachometer = Tachometer(120, GameConfig.SCREEN_HEIGHT - 120)
        
        self.ui = EndlessGameUI()
        self.death_line_ui = DeathLineUI()
        
        # ゲーム状態
        self.game_over = False
        self.game_over_reason = ""
        self.best_distance = 0
    
    def run(self):
        """メインゲームループ"""
        running = True
        quit_to_menu = False
        
        while running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit_to_menu = False  # アプリケーション終了
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self._restart_game()
                    elif event.key == pygame.K_m and self.game_over:
                        running = False
                        quit_to_menu = True  # メニューに戻る
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        quit_to_menu = True  # メニューに戻る
            
            if not self.game_over:
                # 更新
                self.car.update_for_endless_mode()
                
                # トラック更新（カメラ追従）
                self.track.update(self.car.position.y)
                
                # デスライン更新
                self.death_line.update(self.car.position, self.track.get_distance_traveled())
                
                # ゲームオーバー判定
                self._check_game_over()
            
            # 描画
            # 背景をクリア
            self.screen.fill((34, 139, 34))  # 草の色で背景を塗りつぶし
            
            # カメラオフセットを適用してトラックを描画
            camera_offset = pygame.math.Vector2(0, self.track.camera_y)
            
            # トラックを描画
            self.track.draw(self.screen)
            
            # デスラインを描画
            self.death_line.draw(self.screen, self.track.camera_y)
            
            # 車両を画面座標で描画
            car_screen_pos = self.car.position - camera_offset
            self.car.rect.center = car_screen_pos
            self.all_sprites.draw(self.screen)
            
            # UI描画
            self.ui.draw_endless_hud(self.screen, self.car, self.track, self.game_over, self.best_distance, self.game_over_reason)
            self.death_line_ui.draw_death_line_info(self.screen, self.death_line, self.car.position)
            
            # タコメーター描画
            self.tachometer.draw(self.screen, self.car)
            
            pygame.display.flip()
            self.clock.tick(GameConfig.FPS)
        
        # 戻り値でメニューに戻るかアプリ終了かを判断
        return quit_to_menu
    
    def _check_game_over(self):
        """ゲームオーバー判定"""
        # デスラインとの衝突チェック
        if self.death_line.check_collision(self.car.position):
            self.game_over_reason = "Caught by Death Line!"
            self._game_over()
            return
        
        # トラックから大きく外れた場合
        if not self.track.is_on_track(self.car.position):
            # 少し猶予を与える
            if hasattr(self, 'off_track_timer'):
                self.off_track_timer += 1
                if self.off_track_timer > 120:  # 2秒間トラック外（短縮）
                    self.game_over_reason = "Off Track Too Long!"
                    self._game_over()
            else:
                self.off_track_timer = 0
        else:
            self.off_track_timer = 0
        
        # 速度が極端に遅くなった場合（スタック判定）
        if self.car.velocity.length() < 0.1:
            if hasattr(self, 'stuck_timer'):
                self.stuck_timer += 1
                if self.stuck_timer > 180:  # 3秒間停止（短縮）
                    self.game_over_reason = "Vehicle Stuck!"
                    self._game_over()
            else:
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0
    
    def _game_over(self):
        """ゲームオーバー処理"""
        self.game_over = True
        distance = self.track.get_distance_traveled()
        if distance > self.best_distance:
            self.best_distance = distance
    
    def _restart_game(self):
        """ゲーム再開"""
        self.game_over = False
        self.game_over_reason = ""
        self.off_track_timer = 0
        self.stuck_timer = 0
        
        # 高度なトラックをリセット
        self.track = AdvancedEndlessPixelTrack()
        
        # リアルな車両をリセット
        self.car = RealisticRallyCar(self.track)
        self.car.position = pygame.math.Vector2(GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT - 100)
        self.car.velocity = pygame.math.Vector2(0, 0)
        self.car.direction = 90  # 上向きに設定
        self.car.current_gear = 1
        self.car.rect.center = self.car.position
        
        # スプライトグループを更新
        self.all_sprites.empty()
        self.all_sprites.add(self.car)
        
        # デスラインをリセット
        self.death_line.reset(self.car.position)
        self.death_line.reset(self.car.position)

class EndlessGameUI(GameUI):
    def __init__(self):
        super().__init__()
    
    def draw_endless_hud(self, screen, car, track, game_over, best_distance, game_over_reason=""):
        """エンドレスモード用HUD"""
        # 基本的な車両情報
        speed_kmh = car.get_speed_kmh()
        gear = car.current_gear
        torque_eff = car.get_torque_efficiency()
        
        # 速度表示
        speed_text = self.font.render(f"Speed: {speed_kmh:.1f} km/h", True, GameConfig.WHITE)
        screen.blit(speed_text, (10, 10))
        
        # ギア表示
        gear_color = GameConfig.GREEN if torque_eff > 0.8 else (GameConfig.RED if torque_eff < 0.5 else GameConfig.WHITE)
        gear_text = self.font.render(f"Gear: {gear}", True, gear_color)
        screen.blit(gear_text, (10, 50))
        
        # 進行距離
        distance = track.get_distance_traveled()
        distance_text = self.font.render(f"Distance: {distance:.0f}m", True, GameConfig.WHITE)
        screen.blit(distance_text, (10, 90))
        
        # 難易度
        difficulty = track.get_difficulty()
        difficulty_text = self.small_font.render(f"Difficulty: {difficulty*100:.1f}%", True, GameConfig.WHITE)
        screen.blit(difficulty_text, (10, 130))
        
        # 路面タイプ
        surface_type = track.get_surface_at_position(car.position)
        surface_text = self.small_font.render(f"Surface: {surface_type.capitalize()}", True, GameConfig.WHITE)
        screen.blit(surface_text, (10, 150))
        
        # ベスト記録
        if best_distance > 0:
            best_text = self.small_font.render(f"Best: {best_distance:.0f}m", True, GameConfig.YELLOW)
            screen.blit(best_text, (10, 170))
        
        # 操作説明
        controls_text = [
            "Controls:",
            "↑/W: Accelerate",
            "↓/S: Brake",
            "←→: Steering",
            "Q: Shift Up",
            "E: Shift Down"
        ]
        
        if game_over:
            controls_text.extend([
                "",
                "GAME OVER!",
                game_over_reason,
                "R: Restart",
                "M: Menu",
                "ESC: Menu"
            ])
        
        for i, text in enumerate(controls_text):
            if text == "GAME OVER!":
                color = GameConfig.RED
            elif text == game_over_reason:
                color = GameConfig.YELLOW
            else:
                color = GameConfig.WHITE
            control_surface = self.small_font.render(text, True, color)
            screen.blit(control_surface, (GameConfig.SCREEN_WIDTH - 200, 10 + i * 20))
        
        # 進行方向インジケーター
        self._draw_progress_indicator(screen, car, track)
    
    def _draw_progress_indicator(self, screen, car, track):
        """進行状況インジケーター"""
        # 画面右側に進行バー
        bar_x = GameConfig.SCREEN_WIDTH - 30
        bar_y = 50
        bar_height = 200
        bar_width = 10
        
        # バー背景
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # 現在位置（車の位置を基準）
        progress = min(1.0, track.get_difficulty())
        fill_height = int(bar_height * progress)
        
        # 難易度に応じて色を変更
        if progress < 0.3:
            color = GameConfig.GREEN
        elif progress < 0.7:
            color = (255, 255, 0)  # 黄色
        else:
            color = GameConfig.RED
        
        pygame.draw.rect(screen, color, (bar_x, bar_y + bar_height - fill_height, bar_width, fill_height))
        
        # ラベル
        progress_text = self.small_font.render("Progress", True, GameConfig.WHITE)
        screen.blit(progress_text, (bar_x - 35, bar_y - 20))

if __name__ == "__main__":
    game = EndlessRallyGame()
    game.run()
