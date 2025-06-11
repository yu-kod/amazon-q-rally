import asyncio
import pygame
import sys
from endless_game import EndlessRallyGame
from config import GameConfig

class WebRallyGameMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Amazon Q Rally - Web Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
    async def run(self):
        """メインゲームループ（Web版）"""
        # 直接エンドレスゲームを開始
        game = EndlessRallyGame(self.screen)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # ゲームの更新と描画
            if not game.run_frame():
                # ゲームが終了した場合、リスタート
                game = EndlessRallyGame(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            # pygbag用の非同期処理
            await asyncio.sleep(0)
        
        pygame.quit()

async def main():
    """Web版メインエントリーポイント"""
    web_game = WebRallyGameMain()
    await web_game.run()

if __name__ == "__main__":
    asyncio.run(main())
