from snake_game import SnakeGame
import pygame

if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print("Final Score", score)

    pygame.quit()