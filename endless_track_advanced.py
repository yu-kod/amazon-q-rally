import pygame
import random
import math
from config import GameConfig
from advanced_track_generator import AdvancedTrackChunk

class EndlessTrackConfig:
    TILE_SIZE = 16
    CHUNK_HEIGHT = 20  # チャンクの高さ（タイル数）
    TRACK_WIDTH_MIN = 4  # 最小トラック幅
    TRACK_WIDTH_MAX = 8  # 最大トラック幅
    DIFFICULTY_INCREASE_RATE = 0.0008  # 難易度上昇率を少し下げる
    
    # タイルタイプ
    GRASS = 0
    GRAVEL = 1
    DIRT = 2
    TARMAC = 3
    TREE = 4
    ROCK = 5
    WATER = 6
    MUD = 7
    
    # 色パレット
    COLORS = {
        GRASS: (34, 139, 34),
        GRAVEL: (139, 119, 101),
        DIRT: (160, 82, 45),
        TARMAC: (64, 64, 64),
        TREE: (0, 100, 0),
        ROCK: (105, 105, 105),
        WATER: (0, 100, 200),
        MUD: (101, 67, 33)
    }

class AdvancedEndlessPixelTrack:
    def __init__(self):
        self.chunks = []
        # カメラの初期位置を車の位置に合わせる
        self.camera_y = GameConfig.SCREEN_HEIGHT - 100 - GameConfig.SCREEN_HEIGHT // 2
        self.distance_traveled = 0
        self.difficulty = 0.0
        self.tile_surfaces = {}
        
        # 初期チャンクを生成
        self._generate_initial_chunks()
    
    def _generate_initial_chunks(self):
        """初期チャンクを生成（シンプルに）"""
        chunks_needed = 20
        
        prev_center = None
        # 車の位置をタイル座標で計算
        car_tile_y = (GameConfig.SCREEN_HEIGHT - 100) // EndlessTrackConfig.TILE_SIZE
        
        for i in range(chunks_needed):
            # 車の位置から上下にチャンクを配置（タイル座標で）
            y_offset = car_tile_y - (chunks_needed // 2 - i) * EndlessTrackConfig.CHUNK_HEIGHT
            chunk = AdvancedTrackChunk(y_offset, 0.1, prev_center)  # 初期難易度を低く
            self.chunks.append(chunk)
            prev_center = chunk.get_last_center()
    
    def update(self, car_y_position):
        """トラックの更新（カメラ追従とチャンク生成）"""
        # カメラ位置を更新（車を画面中央に表示）
        self.camera_y = car_y_position - GameConfig.SCREEN_HEIGHT // 2
        
        # 進行距離を更新
        initial_car_y = GameConfig.SCREEN_HEIGHT - 100
        self.distance_traveled = max(0, (initial_car_y - car_y_position) / 10)
        
        # 難易度を更新
        self.difficulty = min(1.0, self.distance_traveled * EndlessTrackConfig.DIFFICULTY_INCREASE_RATE)
        
        # 新しいチャンクが必要かチェック
        self._check_and_generate_chunks()
        
        # 古いチャンクを削除
        self._cleanup_old_chunks()
    
    def _check_and_generate_chunks(self):
        """新しいチャンクの生成が必要かチェック（高度な生成システム使用）"""
        if not self.chunks:
            return
        
        # 最後のチャンクの位置
        last_chunk = self.chunks[-1]
        last_chunk_top = last_chunk.y_offset * EndlessTrackConfig.TILE_SIZE
        
        # カメラの上端
        camera_top = self.camera_y - 400  # 十分なバッファ
        
        # 新しいチャンクが必要な場合
        while last_chunk_top > camera_top:
            new_y_offset = last_chunk.y_offset - last_chunk.height  # 上方向に生成
            prev_center = last_chunk.track_center_line[0] if last_chunk.track_center_line else None
            new_chunk = AdvancedTrackChunk(new_y_offset, self.difficulty, prev_center)
            self.chunks.append(new_chunk)
            last_chunk = new_chunk
            last_chunk_top = last_chunk.y_offset * EndlessTrackConfig.TILE_SIZE
    
    def _cleanup_old_chunks(self):
        """画面外の古いチャンクを削除"""
        camera_bottom = self.camera_y + GameConfig.SCREEN_HEIGHT + 400  # バッファ
        
        self.chunks = [chunk for chunk in self.chunks 
                      if chunk.y_offset * EndlessTrackConfig.TILE_SIZE < camera_bottom]
    
    def _get_tile_surface(self, tile_type, x, y):
        """タイル表面をキャッシュして取得"""
        # 固定パターンでキャッシュ（位置に依存しない）
        pattern_id = (x + y) % 8  # 8パターンのバリエーション
        key = (tile_type, pattern_id)
        if key not in self.tile_surfaces:
            random.seed(tile_type * 1000 + pattern_id)  # 固定シード
            surface = self._create_tile_surface(tile_type)
            self.tile_surfaces[key] = surface
            random.seed()
        return self.tile_surfaces[key]
    
    def _create_tile_surface(self, tile_type):
        """タイル表面を作成"""
        surface = pygame.Surface((EndlessTrackConfig.TILE_SIZE, EndlessTrackConfig.TILE_SIZE))
        base_color = EndlessTrackConfig.COLORS[tile_type]
        
        if tile_type == EndlessTrackConfig.TARMAC:
            # アスファルトの描画
            surface.fill((60, 60, 60))  # ダークグレー
            # アスファルトのテクスチャ
            for _ in range(4):
                x = random.randint(0, 15)
                y = random.randint(0, 15)
                color = random.randint(55, 65)
                surface.set_at((x, y), (color, color, color))
        
        elif tile_type == EndlessTrackConfig.GRAVEL:
            # グラベル（砂利）の描画
            surface.fill((139, 119, 101))  # ベージュ
            # 砂利のテクスチャ
            for _ in range(12):
                x = random.randint(0, 15)
                y = random.randint(0, 15)
                if random.random() < 0.5:
                    lighter = (min(255, base_color[0]+20), min(255, base_color[1]+20), min(255, base_color[2]+20))
                else:
                    lighter = (max(0, base_color[0]-20), max(0, base_color[1]-20), max(0, base_color[2]-20))
                surface.set_at((x, y), lighter)
        
        elif tile_type == EndlessTrackConfig.DIRT:
            # ダート（土）の描画
            surface.fill((160, 82, 45))  # 茶色
            # 土のテクスチャ
            for _ in range(10):
                x = random.randint(0, 15)
                y = random.randint(0, 15)
                darker = (max(0, base_color[0]-25), max(0, base_color[1]-25), max(0, base_color[2]-25))
                surface.set_at((x, y), darker)
        
        elif tile_type == EndlessTrackConfig.GRASS:
            # 草の描画
            surface.fill(base_color)
            for _ in range(8):
                x = random.randint(0, 15)
                y = random.randint(0, 15)
                darker = (max(0, base_color[0]-20), max(0, base_color[1]-20), max(0, base_color[2]-20))
                surface.set_at((x, y), darker)
        
        elif tile_type == EndlessTrackConfig.TREE:
            # 木の描画
            surface.fill((34, 139, 34))  # 草地背景
            trunk_color = (101, 67, 33)
            leaf_color = (0, 100, 0)
            
            # 幹
            for y in range(10, 16):
                for x in range(6, 10):
                    surface.set_at((x, y), trunk_color)
            
            # 葉
            for y in range(2, 12):
                for x in range(2, 14):
                    if (x-8)**2 + (y-7)**2 <= 25:
                        surface.set_at((x, y), leaf_color)
        
        elif tile_type == EndlessTrackConfig.ROCK:
            # 岩の描画
            surface.fill((34, 139, 34))  # 草地背景
            rock_color = (105, 105, 105)
            
            # 岩
            for y in range(4, 12):
                for x in range(4, 12):
                    if (x-8)**2 + (y-8)**2 <= 16:
                        surface.set_at((x, y), rock_color)
        
        else:
            surface.fill(base_color)
        
        return surface
    
    def draw(self, screen):
        """エンドレストラックの描画（タイルベースに戻す）"""
        # 画面に表示される範囲を計算
        start_tile_y = int(self.camera_y // EndlessTrackConfig.TILE_SIZE)
        end_tile_y = int((self.camera_y + GameConfig.SCREEN_HEIGHT) // EndlessTrackConfig.TILE_SIZE) + 1
        
        tiles_per_row = GameConfig.SCREEN_WIDTH // EndlessTrackConfig.TILE_SIZE
        
        for tile_y in range(start_tile_y, end_tile_y):
            for tile_x in range(tiles_per_row):
                # ワールド座標でのタイル取得
                tile_type = self.get_tile_at_world_pos(tile_x, tile_y)
                
                # 画面座標での描画位置
                screen_x = tile_x * EndlessTrackConfig.TILE_SIZE
                screen_y = tile_y * EndlessTrackConfig.TILE_SIZE - self.camera_y
                
                # 画面内にある場合のみ描画
                if -EndlessTrackConfig.TILE_SIZE <= screen_y <= GameConfig.SCREEN_HEIGHT:
                    tile_surface = self._get_tile_surface(tile_type, tile_x, tile_y)
                    screen.blit(tile_surface, (screen_x, screen_y))
    
    def get_tile_at_world_pos(self, tile_x, tile_y):
        """ワールド座標でのタイル取得"""
        # タイル座標で直接比較
        for chunk in self.chunks:
            if chunk.y_offset <= tile_y < chunk.y_offset + chunk.height:
                return chunk.get_tile_at(tile_x, tile_y)
        
        return EndlessTrackConfig.GRASS
    
    def get_surface_at_position(self, pos):
        """指定位置での路面タイプを取得"""
        tile_x = int(pos[0] // EndlessTrackConfig.TILE_SIZE)
        tile_y = int(pos[1] // EndlessTrackConfig.TILE_SIZE)
        
        tile_type = self.get_tile_at_world_pos(tile_x, tile_y)
        
        # タイルタイプを路面タイプに変換
        if tile_type == EndlessTrackConfig.GRAVEL:
            return "gravel"
        elif tile_type == EndlessTrackConfig.DIRT:
            return "dirt"
        elif tile_type == EndlessTrackConfig.TARMAC:
            return "tarmac"
        elif tile_type == EndlessTrackConfig.MUD:
            return "mud"
        else:
            return "gravel"
    
    def is_on_track(self, pos):
        """指定位置がトラック上にあるかチェック"""
        tile_x = int(pos[0] // EndlessTrackConfig.TILE_SIZE)
        tile_y = int(pos[1] // EndlessTrackConfig.TILE_SIZE)
        
        tile_type = self.get_tile_at_world_pos(tile_x, tile_y)
        return tile_type in [EndlessTrackConfig.GRAVEL, EndlessTrackConfig.DIRT, 
                           EndlessTrackConfig.TARMAC, EndlessTrackConfig.MUD]
    
    def get_distance_traveled(self):
        """進行距離を取得"""
        return self.distance_traveled
    
    def get_difficulty(self):
        """現在の難易度を取得"""
        return self.difficulty
