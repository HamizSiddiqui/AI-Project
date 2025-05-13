import pygame
import numpy as np
import random
import sys
import copy

GRID_SIZE = 8
CELL_SIZE = 80
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
SCORE_PANEL_HEIGHT = 100

# Modern soothing color palette
WHITE = (245, 245, 245)
BLACK = (40, 40, 40)
NAVY_BLUE = (30, 60, 120)
AI_COLOR = (30, 30, 30)
FIRE_COLOR = (255, 69, 58)
EARTH_COLOR = (60, 179, 113)
WATER_COLOR = (30, 144, 255)
AIR_COLOR = (255, 255, 102)
NEUTRAL_COLOR = (200, 200, 200)
START_TILE_COLOR = (147, 112, 219)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (120, 255, 120)

nature_types = ["Earth", "Water", "Air", "Fire", None]

nature_colors = {
    "Earth": EARTH_COLOR,
    "Water": WATER_COLOR,
    "Air": AIR_COLOR,
    "Fire": FIRE_COLOR,
    None: NEUTRAL_COLOR
}

nature_labels = {
    "Earth": "🌍",
    "Water": "💧",
    "Air": "🌬️",
    "Fire": "🔥",
    None: "⬜"
}

nature_points = {
    "Water": 3,
    "Air": 5,
    "Fire": -5,
    "Earth": -3,
    None: 1
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + SCORE_PANEL_HEIGHT))
pygame.display.set_caption("Nature Wars")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 48)
emoji_small_font = pygame.font.SysFont("Segoe UI Emoji", 18)  # Added for rules screen

class NatureWars:
    def __init__(self):
        self.board = np.full((GRID_SIZE, GRID_SIZE), None)
        self.nature_board = self.generate_biased_board()
        self.board[0, 0] = "Player"
        self.board[GRID_SIZE - 1, GRID_SIZE - 1] = "AI"
        self.current_turn = "Player"
        self.scores = {"Player": 0, "AI": 0}

    def generate_biased_board(self):
        board = np.random.choice(nature_types, size=(GRID_SIZE, GRID_SIZE), p=[0.25, 0.2, 0.15, 0.25, 0.15])
        for i in range(2):
            for j in range(2):
                if random.random() < 0.7:
                    board[i, j] = random.choice(["Earth", "Fire"])
        for i in range(6, 8):
            for j in range(6, 8):
                if random.random() < 0.7:
                    board[i, j] = random.choice(["Air", "Water"])
        return board

    def get_valid_moves(self, player):
        moves = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.board[x, y] == player:
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.board[nx, ny] is None:
                            moves.append((x, y, nx, ny))
        return moves

    def make_move(self, move, player):
        _, _, nx, ny = move
        self.board[nx, ny] = player
        tile_type = self.nature_board[nx, ny]
        self.scores[player] += nature_points[tile_type]

    def positive_tiles_left(self):
        return np.any(np.isin(self.nature_board, ["Water", "Air"]))

    def is_game_over(self):
        if self.scores["Player"] >= 35 or self.scores["AI"] >= 35:
            return True
        if not self.positive_tiles_left():
            return True
        if np.all(self.board != None):
            return True
        if not self.get_valid_moves("Player") and not self.get_valid_moves("AI"):
            return True
        return False

    def evaluate_board(self):
        ai_score = self.scores["AI"]
        player_score = self.scores["Player"]
        ai_moves = len(self.get_valid_moves("AI"))
        player_moves = len(self.get_valid_moves("Player"))
        high_value_control = 0
        trap_bonus = 0

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.board[x, y] == "AI" and self.nature_board[x, y] in ["Water", "Air"]:
                    high_value_control += 10
                if self.board[x, y] == "Player" and self.nature_board[x, y] in ["Water", "Air"]:
                    high_value_control -= 10

        if player_moves <= 2:
            trap_bonus += 15

        return (
            (ai_score - player_score) * 5 +
            (ai_moves - player_moves) * 3 +
            high_value_control +
            trap_bonus
        )

def move_priority(move, game):
    _, _, nx, ny = move
    tile_type = game.nature_board[nx, ny]
    if tile_type == "Air":
        return 1
    elif tile_type == "Water":
        return 2
    elif tile_type == None:
        return 3
    elif tile_type == "Earth":
        return 4
    elif tile_type == "Fire":
        return 5
    return 6

def minimax(game, depth, alpha, beta, is_maximizing):
    if depth == 0 or game.is_game_over():
        return game.evaluate_board(), None

    moves = game.get_valid_moves("AI" if is_maximizing else "Player")
    if not moves:
        return game.evaluate_board(), None

    moves.sort(key=lambda move: move_priority(move, game))

    best_move = None
    if is_maximizing:
        max_eval = -float('inf')
        for move in moves:
            temp_game = copy.deepcopy(game)
            temp_game.make_move(move, "AI")
            temp_game.current_turn = "Player"
            eval_score, _ = minimax(temp_game, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            temp_game = copy.deepcopy(game)
            temp_game.make_move(move, "Player")
            temp_game.current_turn = "AI"
            eval_score, _ = minimax(temp_game, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def draw_board(game):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) == (0, 0) or (x, y) == (GRID_SIZE - 1, GRID_SIZE - 1):
                color = START_TILE_COLOR
            else:
                nature = game.nature_board[x, y]
                color = nature_colors[nature]
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            nature = game.nature_board[x, y]
            label = emoji_font.render(nature_labels[nature], True, BLACK)
            screen.blit(label, (y * CELL_SIZE + CELL_SIZE//2 - label.get_width()//2, x * CELL_SIZE + CELL_SIZE//2 - label.get_height()//2))

            owner = game.board[x, y]
            if owner == "Player":
                icon = emoji_font.render("🧑‍🌾", True, NAVY_BLUE)
                screen.blit(icon, (y * CELL_SIZE + 5, x * CELL_SIZE + 5))
            elif owner == "AI":
                icon = emoji_font.render("🤖", True, AI_COLOR)
                screen.blit(icon, (y * CELL_SIZE + 5, x * CELL_SIZE + 5))

def draw_scores(game):
    pygame.draw.rect(screen, WHITE, (0, SCREEN_SIZE, SCREEN_SIZE, SCORE_PANEL_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, SCREEN_SIZE), (SCREEN_SIZE, SCREEN_SIZE), 3)

    player_score_text = font.render(f" Player: {game.scores['Player']}", True, NAVY_BLUE)
    ai_score_text = font.render(f" AI: {game.scores['AI']}", True, BLACK)

    screen.blit(player_score_text, (20, SCREEN_SIZE + 30))
    screen.blit(ai_score_text, (SCREEN_SIZE - ai_score_text.get_width() - 20, SCREEN_SIZE + 30))

def show_rules():
    showing = True
    while showing:
        screen.fill((230, 255, 240))  # Soothing greenish background

        # Draw bordered box for rules
        rules_rect = pygame.Rect(60, 40, SCREEN_SIZE - 120, SCREEN_SIZE - 100)
        pygame.draw.rect(screen, WHITE, rules_rect, border_radius=20)
        pygame.draw.rect(screen, BLACK, rules_rect, 3, border_radius=20)

        # Title
        title_font = pygame.font.Font(None, 50)
        title = title_font.render(" Welcome to Royal Virus ! ", True, NAVY_BLUE)
        screen.blit(title, (SCREEN_SIZE // 2 - title.get_width() // 2, 60))

        # Rules text
        rules = [
            "🎯 Objective: Reach 35 points or control high-value tiles.",
            "",
            "🔹 Movement:",
            "   --> Move to adjacent tiles (up/down/left/right).",
            "",
            "🔸 Tile Types & Points:",
            "   💧 Water: +3 points",
            "   🌬️ Air: +5 points",
            "   🌍 Earth: -3 points",
            "   🔥 Fire: -5 points",
            "   ⬜ Neutral: +1 point",
            "",
            "🧠 Tip: High-value tiles (💧, 🌬️) are key to winning!",
        ]

        for idx, line in enumerate(rules):
            rule_text = emoji_small_font.render(line, True, BLACK)
            screen.blit(rule_text, (rules_rect.left + 30, 130 + idx * 30))

        # Continue button
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE - 80, 200, 50)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR, button_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, button_rect, 3, border_radius=12)

        button_text = font.render("Continue", True, BLACK)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                showing = False

def show_winner(game):
    WINNER_GREEN = (34, 139, 34)
    BACKGROUND_COLOR = (220, 255, 230)

    winner_font = pygame.font.Font(None, 72)
    medium_font = pygame.font.Font(None, 42)

    player_score = game.scores["Player"]
    ai_score = game.scores["AI"]

    if player_score > ai_score:
        winner_text_str = "Player Wins!"
        winner_color = WINNER_GREEN
        winner_score_text = f"Player Score: {player_score}"
        runner_score_text = f"AI Score: {ai_score}"
    elif player_score < ai_score:
        winner_text_str = "AI Wins!"
        winner_color = WINNER_GREEN
        winner_score_text = f"AI Score: {ai_score}"
        runner_score_text = f"Player Score: {player_score}"
    else:
        winner_text_str = "It's a Tie!"
        winner_color = BLACK
        winner_score_text = f"Player Score: {player_score}"
        runner_score_text = f"AI Score: {ai_score}"

    # Show screen until user closes
    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False

        screen.fill(BACKGROUND_COLOR)

        if not game.positive_tiles_left():
            top_text = medium_font.render("Positive tiles ended!", True, BLACK)
            screen.blit(top_text, (SCREEN_SIZE//2 - top_text.get_width()//2, SCREEN_SIZE//2 - 160))

        winner_text = winner_font.render(winner_text_str, True, winner_color)
        screen.blit(winner_text, (SCREEN_SIZE//2 - winner_text.get_width()//2, SCREEN_SIZE//2 - 80))

        winner_score_rendered = medium_font.render(winner_score_text, True, winner_color)
        runner_score_rendered = medium_font.render(runner_score_text, True, NAVY_BLUE)

        screen.blit(winner_score_rendered, (SCREEN_SIZE//2 - winner_score_rendered.get_width()//2, SCREEN_SIZE//2 + 10))
        screen.blit(runner_score_rendered, (SCREEN_SIZE//2 - runner_score_rendered.get_width()//2, SCREEN_SIZE//2 + 60))

        pygame.display.flip()




def main():
    show_rules()
    game = NatureWars()
    clock = pygame.time.Clock()
    running = True

    while running:
        if game.is_game_over():
            show_winner(game)
            running = False
            break

        if game.current_turn == "Player":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if my < SCREEN_SIZE:
                        x, y = my // CELL_SIZE, mx // CELL_SIZE
                        moves = game.get_valid_moves("Player")
                        for move in moves:
                            if move[2] == x and move[3] == y:
                                game.make_move(move, "Player")
                                game.current_turn = "AI"
                                break
        else:
            _, best_move = minimax(game, 5, -float('inf'), float('inf'), True)
            if best_move:
                game.make_move(best_move, "AI")
            game.current_turn = "Player"

        screen.fill(WHITE)
        draw_board(game)
        draw_scores(game)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
