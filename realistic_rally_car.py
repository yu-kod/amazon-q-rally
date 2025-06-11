import pygame
import math
from config import GameConfig, CarConfig
from realistic_car import RealisticCarRenderer, CarSoundSystem

class RealisticRallyCar(pygame.sprite.Sprite):
    def __init__(self, track=None):
        super().__init__()
        self.track = track
        self._setup_graphics()
        self._setup_physics()
        self._setup_transmission()
        self._setup_sound()
        
    def _setup_graphics(self):
        """グラフィック関連の初期化（リアルな車）"""
        self.car_renderer = RealisticCarRenderer()
        self.original_image = self.car_renderer.create_car_surface()
        self.drift_effect_surface = self.car_renderer.create_drift_effect_surface()
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        # 車を道の上の適切な位置に配置
        self.rect.center = (GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT * 0.8)
        self.original_rect = self.original_image.get_rect()
        
        # ドリフト状態
        self.is_drifting = False
        self.drift_intensity = 0.0
        
    def _setup_physics(self):
        """物理パラメータの初期化"""
        self.direction = 90  # 上向き（90度 - rotate(-90)で上向きベクトルになる）
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.steering_angle = 0
        
    def _setup_transmission(self):
        """トランスミッション関連の初期化"""
        self.current_gear = 1
        self.max_gear = 6
        self.shift_up_pressed = False
        self.shift_down_pressed = False
        
    def _setup_sound(self):
        """サウンドシステムの初期化"""
        self.sound_system = CarSoundSystem()
        self.last_gear = self.current_gear
        
    def set_track(self, track):
        """トラックを設定"""
        self.track = track
        
    def get_speed_kmh(self):
        """現在の速度をkm/hで取得"""
        speed_pixels_per_frame = self.velocity.length()
        speed_kmh = speed_pixels_per_frame * 0.1 * 60 * 3.6
        return speed_kmh
    
    def get_rpm(self):
        """現在のRPMを取得"""
        speed = self.velocity.length()
        gear = self.current_gear
        
        if speed < 0.1:
            return 800  # アイドリング
        
        # ギア比に基づくRPM計算
        gear_settings = CarConfig.GEAR_RATIOS[gear]
        max_speed_for_gear = gear_settings["max_speed"]
        
        # 速度比からRPMを計算
        speed_ratio = min(1.0, speed / max_speed_for_gear)
        
        # RPM範囲を計算
        min_rpm_for_gear = 800 + (gear - 1) * 500
        max_rpm_for_gear = min(8000, min_rpm_for_gear + 3000)
        
        rpm = min_rpm_for_gear + (max_rpm_for_gear - min_rpm_for_gear) * speed_ratio
        
        # アクセル入力による微調整
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            rpm += 200  # アクセル時のRPM上昇
        
        return min(8000, rpm)
    
    def shift_up(self):
        """シフトアップ"""
        if self.current_gear < self.max_gear:
            self.current_gear += 1
            self.sound_system.play_gear_sound()
    
    def shift_down(self):
        """シフトダウン"""
        if self.current_gear > 1:
            self.current_gear -= 1
            self.sound_system.play_gear_sound()
    
    def get_torque_efficiency(self):
        """現在のトルク効率を取得"""
        current_speed = self.velocity.length()
        min_efficient_speed = CarConfig.GEAR_RATIOS[self.current_gear]["min_speed"]
        
        if min_efficient_speed > 0 and current_speed < min_efficient_speed:
            return max(0.15, current_speed / min_efficient_speed)
        else:
            return 1.0
    
    def _get_surface_grip_modifier(self):
        """現在の路面に応じたグリップ修正値を取得"""
        if not self.track:
            return 1.0
        
        surface_type = self.track.get_surface_at_position(self.position)
        
        # 路面タイプ別のグリップ係数
        grip_modifiers = {
            "gravel": 0.8,   # グラベル：少し滑りやすい
            "dirt": 0.7,     # ダート：滑りやすい
            "tarmac": 1.2,   # ターマック：グリップ良好
            "mud": 0.5,      # 泥：非常に滑りやすい
        }
        
        return grip_modifiers.get(surface_type, 1.0)
    
    def _get_surface_friction_modifier(self):
        """現在の路面に応じた摩擦修正値を取得"""
        if not self.track:
            return 1.0
        
        surface_type = self.track.get_surface_at_position(self.position)
        
        # 路面タイプ別の摩擦係数
        friction_modifiers = {
            "gravel": 0.9,   # グラベル：少し摩擦が少ない
            "dirt": 0.7,     # ダート：摩擦が少ない（滑りやすい）
            "tarmac": 1.3,   # ターマック：摩擦が大きい
            "mud": 0.4,      # 泥：摩擦が非常に少ない
        }
        
        return friction_modifiers.get(surface_type, 1.0)
    
    def _calculate_acceleration(self, keys):
        """加速度の計算（重量感を考慮）"""
        gear_settings = CarConfig.GEAR_RATIOS[self.current_gear]
        base_acceleration = gear_settings["base_acceleration"]
        torque_efficiency = self.get_torque_efficiency()
        actual_acceleration = base_acceleration * torque_efficiency
        
        # トルクスリップの計算（重い車両では少し緩和）
        torque_slip_factor = 1.0
        if actual_acceleration > 0.08:  # 閾値を下げる
            slip_intensity = (actual_acceleration - 0.08) * 1.2  # スリップ強度を調整
            torque_slip_factor = 0.9 - slip_intensity
            torque_slip_factor = max(0.7, torque_slip_factor)  # 最低70%は伝達
        
        return actual_acceleration * torque_slip_factor
    
    def _handle_input(self, keys):
        """入力処理"""
        # パドルシフト
        if keys[pygame.K_q] and not self.shift_up_pressed:
            self.shift_up()
            self.shift_up_pressed = True
        elif not keys[pygame.K_q]:
            self.shift_up_pressed = False
            
        if keys[pygame.K_e] and not self.shift_down_pressed:
            self.shift_down()
            self.shift_down_pressed = True
        elif not keys[pygame.K_e]:
            self.shift_down_pressed = False
        
        # ステアリング
        if keys[pygame.K_LEFT]:
            self.steering_angle = min(self.steering_angle + 2, CarConfig.MAX_STEERING_ANGLE)
        elif keys[pygame.K_RIGHT]:
            self.steering_angle = max(self.steering_angle - 2, -CarConfig.MAX_STEERING_ANGLE)
        else:
            if abs(self.steering_angle) > 1:
                self.steering_angle *= 0.9
            else:
                self.steering_angle = 0
    
    def _apply_acceleration(self, keys):
        """加速・減速の適用（重量感を考慮）"""
        current_speed = self.velocity.length()
        max_speed = CarConfig.GEAR_RATIOS[self.current_gear]["max_speed"]
        forward_vector = pygame.math.Vector2(1, 0).rotate(-self.direction)
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if current_speed < max_speed:
                acceleration = self._calculate_acceleration(keys)
                # 重量感を考慮した加速度適用
                acceleration_force = acceleration / CarConfig.VEHICLE_MASS
                self.velocity += forward_vector * acceleration_force
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if current_speed < CarConfig.GEAR_RATIOS[1]["max_speed"] * 0.5:
                brake_force = CarConfig.GEAR_RATIOS[1]["base_acceleration"] * 0.6 / CarConfig.VEHICLE_MASS
                self.velocity -= forward_vector * brake_force
    
    def _apply_friction(self, keys):
        """摩擦の適用（重量感と路面タイプを考慮した段階的減速）"""
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            if self.velocity.length() > 0:
                current_speed = self.velocity.length()
                
                # 路面タイプによる摩擦修正
                surface_friction_modifier = self._get_surface_friction_modifier()
                
                # 段階的な摩擦力（速度に応じて変化）
                base_friction = CarConfig.BASE_DECELERATION * surface_friction_modifier
                air_resistance = current_speed * 0.008  # 空気抵抗を弱く
                rolling_resistance = 0.02 * surface_friction_modifier  # 転がり抵抗も路面依存
                
                total_friction = base_friction + air_resistance + rolling_resistance
                
                # 重量感を考慮した摩擦適用
                friction_force = total_friction / CarConfig.VEHICLE_MASS
                friction = self.velocity.normalize() * friction_force
                
                if self.velocity.length() > friction_force:
                    self.velocity -= friction
                else:
                    # 完全停止の閾値を上げる（より自然な停止）
                    if self.velocity.length() < 0.05:
                        self.velocity = pygame.math.Vector2(0, 0)
                    else:
                        self.velocity *= 0.95  # 徐々に減速
    
    def _apply_vehicle_physics(self):
        """車両物理の適用（路面タイプを考慮）"""
        current_speed = self.velocity.length()
        if current_speed > 0.1:
            # 路面グリップ修正値を取得
            grip_modifier = self._get_surface_grip_modifier()
            
            # スリップ角の計算
            velocity_angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
            slip_angle = self.direction - velocity_angle
            while slip_angle > 180:
                slip_angle -= 360
            while slip_angle < -180:
                slip_angle += 360
            
            # ドリフト判定
            self.drift_intensity = abs(slip_angle) / 30.0  # 0-1の範囲
            self.is_drifting = self.drift_intensity > 0.3
            
            # スキール音の再生
            if self.is_drifting and current_speed > 1.0:
                self.sound_system.play_skid_sound(self.drift_intensity)
            
            # 横方向の力（グラベル仕様 + 路面タイプ考慮）
            lateral_grip = CarConfig.LATERAL_GRIP * grip_modifier
            lateral_force = slip_angle * lateral_grip * 0.015
            lateral_vector = pygame.math.Vector2(0, 1).rotate(-self.direction)
            self.velocity -= lateral_vector * lateral_force
            
            # ステアリングによる方向変更
            if abs(self.steering_angle) > 0.5:
                forward_vector = pygame.math.Vector2(1, 0).rotate(-self.direction)
                is_forward = self.velocity.dot(forward_vector) > 0
                
                steering_rad = math.radians(self.steering_angle)
                if abs(steering_rad) > 0.001:
                    turning_radius = CarConfig.WHEELBASE / math.tan(abs(steering_rad))
                    angular_velocity = current_speed / turning_radius
                    
                    # 路面グリップによる旋回性能調整
                    angular_velocity *= grip_modifier
                    
                    if not is_forward:
                        angular_velocity = -angular_velocity
                    if self.steering_angle < 0:
                        angular_velocity = -angular_velocity
                    
                    self.direction += math.degrees(angular_velocity)
                    self.direction = self.direction % 360
    
    def _update_graphics(self):
        """グラフィックの更新"""
        # 車の描画は上向きなので、物理の角度から90度引く
        display_angle = self.direction - 90
        rotated_image = pygame.transform.rotate(self.original_image, display_angle)
        temp_rect = rotated_image.get_rect()
        max_size = int((self.original_rect.width**2 + self.original_rect.height**2)**0.5) + 2
        self.image = pygame.Surface((max_size, max_size), pygame.SRCALPHA)
        self.image.blit(rotated_image, ((max_size - temp_rect.width) // 2, (max_size - temp_rect.height) // 2))
        
        # ドリフトエフェクトの追加
        if self.is_drifting and self.drift_intensity > 0.5:
            drift_effect = pygame.transform.rotate(self.drift_effect_surface, display_angle)
            drift_rect = drift_effect.get_rect()
            self.image.blit(drift_effect, ((max_size - drift_rect.width) // 2, (max_size - drift_rect.height) // 2), 
                          special_flags=pygame.BLEND_ALPHA_SDL2)
        
        self.rect = self.image.get_rect(center=self.position)
    
    def _update_sound(self, keys):
        """サウンドの更新"""
        rpm = self.get_rpm()
        throttle_input = 1.0 if (keys[pygame.K_UP] or keys[pygame.K_w]) else 0.0
        current_speed = self.velocity.length()
        
        # エンジン音の更新（速度を渡す）
        self.sound_system.update_engine_sound(rpm, throttle_input, current_speed)
        
        # ギア変更音
        if self.current_gear != self.last_gear:
            self.sound_system.play_gear_sound()
            self.last_gear = self.current_gear
    
    def update_for_endless_mode(self):
        """エンドレスモード用の更新処理"""
        keys = pygame.key.get_pressed()
        
        self._handle_input(keys)
        self._apply_acceleration(keys)
        self._apply_friction(keys)
        self._apply_vehicle_physics()
        self._update_sound(keys)
        
        # 最大速度制限
        max_speed = CarConfig.GEAR_RATIOS[self.current_gear]["max_speed"]
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed
        
        # 位置更新
        self.position += self.velocity
        
        # 横方向の境界制限のみ（縦方向は自由）
        self.position.x = max(20, min(self.position.x, GameConfig.SCREEN_WIDTH - 20))
        
        # 車が下に行きすぎないように制限（上方向への移動を促進）
        if self.position.y > GameConfig.SCREEN_HEIGHT - 50:
            self.position.y = GameConfig.SCREEN_HEIGHT - 50
        
        self.rect.center = self.position
        
        self._update_graphics()
        
        # トラックから外れた場合の処理
        if self.track and not self.track.is_on_track(self.position):
            # トラック外では速度を大幅に減少
            self.velocity *= 0.95
    
    def update(self):
        """通常の更新処理"""
        keys = pygame.key.get_pressed()
        
        self._handle_input(keys)
        self._apply_acceleration(keys)
        self._apply_friction(keys)
        self._apply_vehicle_physics()
        self._update_sound(keys)
        
        # 最大速度制限
        max_speed = CarConfig.GEAR_RATIOS[self.current_gear]["max_speed"]
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed
        
        # 位置更新
        self.position += self.velocity
        
        # 画面境界制限
        self.position.x = max(20, min(self.position.x, GameConfig.SCREEN_WIDTH - 20))
        self.position.y = max(20, min(self.position.y, GameConfig.SCREEN_HEIGHT - 20))
        self.rect.center = self.position
        
        self._update_graphics()
        
        # トラックから外れた場合の処理
        if self.track and not self.track.is_on_track(self.position):
            # トラック外では速度を大幅に減少
            self.velocity *= 0.95
