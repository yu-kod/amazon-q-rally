import pygame
import random
import math
from config import GameConfig

class AdvancedTrackChunk:
    """高度なトラックチャンク"""
    
    def __init__(self, y_offset, difficulty=1.0, prev_center=None):
        self.y_offset = y_offset
        self.height = 20  # チャンクの高さ
        self.width = GameConfig.SCREEN_WIDTH
        self.difficulty = difficulty
        
        # トラックの中心線を生成
        self.track_center_line = []
        self.track_width = []
        self.surface_types = []  # 路面タイプを追加
        
        # 前のチャンクの中心から開始
        if prev_center is None:
            start_center = self.width // 2
        else:
            start_center = prev_center
        
        # ラリーらしいトラック生成
        self._generate_rally_track(start_center)
    
    def _generate_rally_track(self, start_center):
        """ラリーらしいトラックを生成"""
        current_center = start_center
        
        # セクションタイプを決定（ストレート、カーブ、ヘアピン）
        section_types = ['straight', 'curve', 'hairpin', 'chicane', 'elevation']
        section_type = random.choice(section_types)
        
        # セクション固有のパラメータ
        curve_direction = 1 if random.random() > 0.5 else -1
        elevation_phase = random.uniform(0, math.pi * 2)
        
        for i in range(self.height):
            # セクションに応じたカーブ生成
            if section_type == 'straight':
                curve_amount = random.uniform(-0.8, 0.8)  # 緩やかな直線
            elif section_type == 'curve':
                # 一方向への連続カーブ
                curve_intensity = 1 + self.difficulty
                curve_amount = curve_direction * random.uniform(1, 2 * curve_intensity)
            elif section_type == 'hairpin':
                # 急カーブ（ヘアピン）
                curve_amount = random.uniform(-5, 5) * (1 + self.difficulty)
            elif section_type == 'chicane':
                # S字カーブ
                curve_amount = math.sin(i * 0.8) * 3 + random.uniform(-1, 1)
            elif section_type == 'elevation':
                # 高低差を模した蛇行
                curve_amount = math.sin(i * 0.3 + elevation_phase) * 2 + random.uniform(-1, 1)
            
            current_center += curve_amount
            
            # 画面内に収める（より狭い範囲で）
            min_center = 60
            max_center = self.width - 60
            current_center = max(min_center, min(max_center, current_center))
            
            self.track_center_line.append(current_center)
            
            # ラリーらしいトラック幅（セクションに応じて変化）
            if section_type == 'hairpin':
                base_width = random.uniform(70, 90)  # ヘアピンは狭い
            elif section_type == 'straight':
                base_width = random.uniform(100, 130)  # ストレートは広め
            else:
                base_width = random.uniform(80, 110)  # 通常
            
            width_variation = random.uniform(-15, 15)
            track_width = max(50, base_width + width_variation)
            self.track_width.append(track_width)
            
            # 路面タイプをセクションに応じて決定
            surface_type = self._determine_surface_type_by_section(section_type, i)
            self.surface_types.append(surface_type)
    
    def _determine_surface_type_by_section(self, section_type, position):
        """セクションタイプに応じて路面タイプを決定"""
        rand = random.random()
        
        if section_type == 'straight':
            # ストレートはアスファルトが多い
            if rand < 0.6:
                return 3  # TARMAC
            elif rand < 0.8:
                return 1  # GRAVEL
            else:
                return 2  # DIRT
        elif section_type == 'hairpin':
            # ヘアピンはグラベルが多い（滑りやすい）
            if rand < 0.5:
                return 1  # GRAVEL
            elif rand < 0.7:
                return 2  # DIRT
            else:
                return 3  # TARMAC
        elif section_type == 'elevation':
            # 高低差セクションはダートが多い
            if rand < 0.5:
                return 2  # DIRT
            elif rand < 0.7:
                return 1  # GRAVEL
            else:
                return 3  # TARMAC
        else:
            # その他はバランス良く
            if rand < 0.35:
                return 3  # TARMAC
            elif rand < 0.65:
                return 1  # GRAVEL
            else:
                return 2  # DIRT
    
    def get_last_center(self):
        """最後の中心位置を取得"""
        return self.track_center_line[-1] if self.track_center_line else self.width // 2
    
    def is_on_track(self, x, y):
        """指定位置がトラック上かどうか判定"""
        # ワールド座標をチャンク内座標に変換
        local_y = y - self.y_offset
        if local_y < 0 or local_y >= self.height:
            return False
        
        row = int(local_y)
        if row < 0 or row >= len(self.track_center_line):
            return False
        
        center = self.track_center_line[row]
        width = self.track_width[row]
        
        return abs(x - center) <= width / 2
    
    def get_surface_at_position(self, x, y):
        """指定位置の路面タイプを取得"""
        if not self.is_on_track(x, y):
            return "grass"
        
        # 簡単な路面タイプ判定
        row = int(y - self.y_offset)
        if row < 0 or row >= len(self.track_center_line):
            return "grass"
        
        center = self.track_center_line[row]
        distance_from_center = abs(x - center)
        width = self.track_width[row]
        
        if distance_from_center < width * 0.3:
            return "tarmac"  # 中央はターマック
        elif distance_from_center < width * 0.4:
            return "gravel"  # 端はグラベル
        else:
            return "dirt"    # さらに端はダート
    
    def get_tile_at(self, tile_x, tile_y):
        """指定タイル位置のタイルタイプを取得"""
        # このチャンクの範囲内かチェック
        if tile_y < self.y_offset or tile_y >= self.y_offset + self.height:
            return 0  # GRASS
        
        # チャンク内の相対位置
        local_y = int(tile_y - self.y_offset)
        if local_y < 0 or local_y >= len(self.track_center_line):
            return 0  # GRASS
        
        center = self.track_center_line[local_y]
        width = self.track_width[local_y]
        
        # タイル座標をワールド座標に変換してトラック判定
        world_x = tile_x * 16  # TILE_SIZE = 16
        
        # トラック上かどうか判定
        if abs(world_x - center) <= width / 2:
            # トラック上の場合、路面タイプを返す
            if local_y < len(self.surface_types):
                return self.surface_types[local_y]
            else:
                return 3  # TARMAC（デフォルト）
        else:
            # トラック外は全て草にする（木や岩を削除）
            return 0  # GRASS
    
    def draw(self, screen, camera_y):
        """チャンクを描画"""
        for i in range(self.height):
            world_y = self.y_offset + i
            screen_y = world_y - camera_y
            
            # 画面外なら描画しない
            if screen_y < -50 or screen_y > GameConfig.SCREEN_HEIGHT + 50:
                continue
            
            center = self.track_center_line[i]
            width = self.track_width[i]
            
            # トラック描画（より太く、より見やすく）
            track_rect = pygame.Rect(
                int(center - width // 2), int(screen_y),
                int(width), 4  # 高さを4ピクセルに増加
            )
            pygame.draw.rect(screen, (60, 60, 60), track_rect)  # ダークグレー
            
            # トラックの端を描画
            left_edge = pygame.Rect(
                int(center - width // 2 - 2), int(screen_y),
                2, 4
            )
            right_edge = pygame.Rect(
                int(center + width // 2), int(screen_y),
                2, 4
            )
            pygame.draw.rect(screen, (100, 100, 100), left_edge)
            pygame.draw.rect(screen, (100, 100, 100), right_edge)
            
            # 中央線（より見やすく）
            if i % 6 == 0:  # 点線効果を調整
                center_line_rect = pygame.Rect(int(center - 1), int(screen_y), 2, 4)
                pygame.draw.rect(screen, (255, 255, 255), center_line_rect)
