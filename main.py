import pygame
import sys
from config import GameConfig
from endless_game import EndlessRallyGame

class RallyGameMain:
    """ラリーゲームのメインクラス"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Amazon Q Rally - Endless Mode")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
    def show_title_screen(self):
        """タイトル画面の表示"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    # 何かキーが押されたらゲーム開始
                    return True
            
            # 背景
            self.screen.fill((20, 20, 40))  # 濃い青
            
            # タイトル
            title_text = self.font_large.render("Amazon Q Rally", True, GameConfig.WHITE)
            title_rect = title_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)
            
            # サブタイトル
            subtitle_text = self.font_medium.render("Endless Mode", True, GameConfig.YELLOW)
            subtitle_rect = subtitle_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, 220))
            self.screen.blit(subtitle_text, subtitle_rect)
            
            # 操作説明
            controls = [
                "Controls:",
                "↑/W: Accelerate",
                "↓/S: Brake/Reverse",
                "←→: Steering",
                "Q: Shift Up",
                "E: Shift Down",
                "",
                "Press any key to start!"
            ]
            
            start_y = 300
            for i, control in enumerate(controls):
                if control == "Press any key to start!":
                    # 点滅効果
                    alpha = int(127 + 127 * abs(pygame.time.get_ticks() % 2000 - 1000) / 1000)
                    color = (*GameConfig.YELLOW, alpha)
                    text_surface = self.font_medium.render(control, True, GameConfig.YELLOW)
                else:
                    text_surface = self.font_small.render(control, True, GameConfig.WHITE)
                
                text_rect = text_surface.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, start_y + i * 30))
                self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def run(self):
        """メインループ"""
        while True:
            # タイトル画面
            if not self.show_title_screen():
                break  # ウィンドウを閉じた場合は終了
            
            # ゲーム開始
            game = EndlessRallyGame()
            continue_to_menu = game.run()
            
            # ゲームの戻り値に応じて処理
            if not continue_to_menu:
                break  # アプリケーション終了
            
            # continue_to_menu が True の場合は再びタイトル画面に戻る
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point for the game"""
    main_game = RallyGameMain()
    main_game.run()

if __name__ == "__main__":
    main()
