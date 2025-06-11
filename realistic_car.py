import pygame
import math
from config import GameConfig

class RealisticCarRenderer:
    """リアルな車の描画"""
    
    def __init__(self):
        self.car_width = 16  # 上向きなので幅と高さを入れ替え
        self.car_height = 32
        
        # 色定義
        self.body_color = (200, 50, 50)  # 赤いボディ
        self.window_color = (100, 150, 200)  # 青いウィンドウ
        self.tire_color = (40, 40, 40)  # 黒いタイヤ
        self.rim_color = (180, 180, 180)  # シルバーのリム
        self.headlight_color = (255, 255, 200)  # ヘッドライト
        self.taillight_color = (255, 100, 100)  # テールライト
        self.detail_color = (150, 150, 150)  # 詳細部分
    
    def create_car_surface(self):
        """リアルな車のサーフェスを作成（上向き）"""
        surface = pygame.Surface((self.car_width, self.car_height), pygame.SRCALPHA)
        
        # 車体の影（立体感）
        shadow_rect = pygame.Rect(1, 1, self.car_width - 2, self.car_height - 2)
        pygame.draw.ellipse(surface, (0, 0, 0, 100), shadow_rect)
        
        # メインボディ
        body_rect = pygame.Rect(2, 2, self.car_width - 4, self.car_height - 4)
        pygame.draw.ellipse(surface, self.body_color, body_rect)
        
        # ボディのハイライト
        highlight_rect = pygame.Rect(3, 3, self.car_width - 6, self.car_height - 8)
        pygame.draw.ellipse(surface, (min(255, self.body_color[0] + 50), 
                                    min(255, self.body_color[1] + 50), 
                                    min(255, self.body_color[2] + 50)), highlight_rect)
        
        # ウィンドウ（フロント - 上部）
        front_window = pygame.Rect(4, 2, self.car_width - 8, 6)
        pygame.draw.ellipse(surface, self.window_color, front_window)
        
        # ウィンドウ（リア - 下部）
        rear_window = pygame.Rect(4, self.car_height - 8, self.car_width - 8, 6)
        pygame.draw.ellipse(surface, self.window_color, rear_window)
        
        # ヘッドライト（上部）
        pygame.draw.circle(surface, self.headlight_color, 
                         (4, 3), 2)
        pygame.draw.circle(surface, self.headlight_color, 
                         (self.car_width - 4, 3), 2)
        
        # テールライト（下部）
        pygame.draw.circle(surface, self.taillight_color, 
                         (4, self.car_height - 3), 1)
        pygame.draw.circle(surface, self.taillight_color, 
                         (self.car_width - 4, self.car_height - 3), 1)
        
        # タイヤ（上向き配置）
        self._draw_tire(surface, 1, 6)  # 左前
        self._draw_tire(surface, self.car_width - 3, 6)  # 右前
        self._draw_tire(surface, 1, self.car_height - 8)  # 左後
        self._draw_tire(surface, self.car_width - 3, self.car_height - 8)  # 右後
        
        # ドアライン
        pygame.draw.line(surface, self.detail_color, 
                        (2, 8), (self.car_width - 2, 8), 1)
        pygame.draw.line(surface, self.detail_color, 
                        (2, self.car_height - 10), (self.car_width - 2, self.car_height - 10), 1)
        
        # ルーフライン
        pygame.draw.line(surface, self.detail_color, 
                        (self.car_width // 2, 8), (self.car_width // 2, self.car_height - 8), 1)
        
        return surface
    
    def _draw_tire(self, surface, x, y):
        """タイヤの描画"""
        # タイヤ本体
        pygame.draw.circle(surface, self.tire_color, (x, y), 3)
        # リム
        pygame.draw.circle(surface, self.rim_color, (x, y), 2)
        pygame.draw.circle(surface, self.tire_color, (x, y), 1)
    
    def create_drift_effect_surface(self):
        """ドリフト時のエフェクト用サーフェス"""
        surface = pygame.Surface((40, 20), pygame.SRCALPHA)
        
        # タイヤ痕
        for i in range(3):
            alpha = 150 - i * 50
            color = (100, 100, 100, alpha)
            pygame.draw.line(surface, color[:3], 
                           (5 + i * 2, 15), (35 + i * 2, 15), 2)
            pygame.draw.line(surface, color[:3], 
                           (5 + i * 2, 5), (35 + i * 2, 5), 2)
        
        return surface

class CarSoundSystem:
    """車のサウンドシステム"""
    
    def __init__(self):
        self.sounds_enabled = True
        self.engine_sounds = {}  # RPMレベル別のエンジン音
        self.skid_sound = None
        self.gear_sound = None
        self.current_engine_channel = None
        
        # サウンドの初期化を試行
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._create_procedural_sounds()
        except pygame.error:
            print("Warning: Could not initialize sound system")
            self.sounds_enabled = False
    
    def _create_procedural_sounds(self):
        """プロシージャルサウンドの生成"""
        if not self.sounds_enabled:
            return
        
        try:
            # エンジン音の生成（簡易版）
            self._generate_engine_sound()
            # スキール音の生成
            self._generate_skid_sound()
            # ギア音の生成
            self._generate_gear_sound()
        except Exception as e:
            print(f"Warning: Could not generate sounds: {e}")
            self.sounds_enabled = False
    
    def _generate_engine_sound(self):
        """RPMレベル別のエンジン音を生成"""
        import numpy as np
        
        try:
            # 複数のRPMレベル用のエンジン音を生成
            rpm_levels = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
            
            for rpm in rpm_levels:
                duration = 0.5  # 短めのループ
                sample_rate = 22050
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # RPMに応じた基本周波数を計算
                base_freq = 30 + (rpm / 8000) * 150  # 30Hz～180Hz
                
                # 複数の周波数を重ねてエンジン音を作成
                wave1 = np.sin(2 * np.pi * base_freq * t) * 0.4
                wave2 = np.sin(2 * np.pi * base_freq * 2 * t) * 0.2  # 2倍音
                wave3 = np.sin(2 * np.pi * base_freq * 3 * t) * 0.1  # 3倍音
                
                # RPMが高いほどノイズを追加（排気音の表現）
                noise_intensity = 0.05 + (rpm / 8000) * 0.15
                noise = np.random.normal(0, noise_intensity, len(t))
                
                engine_wave = (wave1 + wave2 + wave3 + noise) * 0.3
                
                # ステレオ化
                stereo_wave = np.zeros((len(engine_wave), 2), dtype=np.float32)
                stereo_wave[:, 0] = engine_wave
                stereo_wave[:, 1] = engine_wave
                
                # pygame用に変換
                sound_array = (stereo_wave * 32767).astype(np.int16)
                
                if not sound_array.flags['C_CONTIGUOUS']:
                    sound_array = np.ascontiguousarray(sound_array)
                
                self.engine_sounds[rpm] = pygame.sndarray.make_sound(sound_array)
            
        except Exception as e:
            print(f"Warning: Could not generate engine sounds: {e}")
            self.engine_sounds = {}
    
    def _generate_skid_sound(self):
        """スキール音の生成"""
        try:
            import numpy as np
            
            duration = 0.5
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # 高周波のノイズでスキール音を作成
            frequency = 2000
            wave = np.sin(2 * np.pi * frequency * t) * 0.5
            noise = np.random.normal(0, 0.3, len(t))
            
            skid_wave = (wave + noise) * 0.4
            
            # ステレオ化（C-contiguousにする）
            stereo_wave = np.zeros((len(skid_wave), 2), dtype=np.float32)
            stereo_wave[:, 0] = skid_wave
            stereo_wave[:, 1] = skid_wave
            
            # pygame用に変換（16bit整数に変換）
            sound_array = (stereo_wave * 32767).astype(np.int16)
            
            # C-contiguousであることを確認
            if not sound_array.flags['C_CONTIGUOUS']:
                sound_array = np.ascontiguousarray(sound_array)
            
            self.skid_sound = pygame.sndarray.make_sound(sound_array)
            
        except Exception as e:
            print(f"Warning: Could not generate skid sound: {e}")
            self.skid_sound = None
    
    def _generate_gear_sound(self):
        """ギア音の生成"""
        try:
            import numpy as np
            
            duration = 0.2
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # クリック音（短いパルス）
            frequency = 1000
            envelope = np.exp(-t * 10)  # 減衰エンベロープ
            wave = np.sin(2 * np.pi * frequency * t) * envelope * 0.3
            
            # ステレオ化（C-contiguousにする）
            stereo_wave = np.zeros((len(wave), 2), dtype=np.float32)
            stereo_wave[:, 0] = wave
            stereo_wave[:, 1] = wave
            
            # pygame用に変換（16bit整数に変換）
            sound_array = (stereo_wave * 32767).astype(np.int16)
            
            # C-contiguousであることを確認
            if not sound_array.flags['C_CONTIGUOUS']:
                sound_array = np.ascontiguousarray(sound_array)
            
            self.gear_sound = pygame.sndarray.make_sound(sound_array)
            
        except Exception as e:
            print(f"Warning: Could not generate gear sound: {e}")
            self.gear_sound = None
            frequency = 1000
            wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 10)
            
            stereo_wave = np.array([wave, wave]).T
            gear_wave_int = (stereo_wave * 32767).astype(np.int16)
            
            self.gear_sound = pygame.sndarray.make_sound(gear_wave_int)
            
        except Exception as e:
            print(f"Warning: Could not generate gear sound: {e}")
    
    def play_engine_sound(self, rpm, volume=0.5, pitch_factor=1.0):
        """RPMに応じたエンジン音の再生"""
        if not self.sounds_enabled or not self.engine_sounds:
            return
        
        try:
            # RPMに最も近いエンジン音を選択
            rpm_levels = list(self.engine_sounds.keys())
            closest_rpm = min(rpm_levels, key=lambda x: abs(x - rpm))
            selected_sound = self.engine_sounds[closest_rpm]
            
            # 音量を調整
            adjusted_volume = min(0.4, volume)  # さらに音量を下げる
            
            # 現在のエンジン音チャンネルを管理
            if self.current_engine_channel is None or not self.current_engine_channel.get_busy():
                self.current_engine_channel = pygame.mixer.Channel(0)
                self.current_engine_channel.play(selected_sound, loops=-1)
            
            # 音量を更新
            self.current_engine_channel.set_volume(adjusted_volume)
                
        except Exception as e:
            print(f"Warning: Could not play engine sound: {e}")
    
    def play_skid_sound(self, intensity=1.0):
        """スキール音の再生（音量を下げる）"""
        if not self.sounds_enabled or not self.skid_sound:
            return
        
        try:
            # スキール音の音量を大幅に下げる
            volume = min(0.3, intensity * 0.2)  # 最大音量を0.3に制限
            self.skid_sound.set_volume(volume)
            
            # 頻繁に再生されないように制限
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(self.skid_sound)
        except Exception as e:
            print(f"Warning: Could not play skid sound: {e}")
    
    def play_gear_sound(self):
        """ギア音の再生"""
        if not self.sounds_enabled or not self.gear_sound:
            return
        
        try:
            self.gear_sound.set_volume(0.6)
            self.gear_sound.play()
        except Exception as e:
            print(f"Warning: Could not play gear sound: {e}")
    
    def stop_engine_sound(self):
        """エンジン音の停止"""
        if self.sounds_enabled:
            if self.current_engine_channel:
                self.current_engine_channel.stop()
            pygame.mixer.stop()
    
    def update_engine_sound(self, rpm, throttle_input, speed=0):
        """エンジン音の更新（RPMに応じた音程変化）"""
        if not self.sounds_enabled:
            return
        
        # RPMに基づく基本音量
        base_volume = 0.15 + (rpm / 8000) * 0.25
        
        # スロットル入力による音量追加
        throttle_volume = throttle_input * 0.15
        
        # 最終音量
        total_volume = min(0.4, base_volume + throttle_volume)
        
        # RPMに応じたエンジン音を再生
        self.play_engine_sound(rpm, total_volume)
