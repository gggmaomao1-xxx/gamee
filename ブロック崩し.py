import pygame
import sys

# --- 1. 初期設定 ---
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ピンポンゲーム - 完成版")
clock = pygame.time.Clock()

# フォントの設定（PCに入っている標準フォントを使用）
font = pygame.font.SysFont("msgothic", 30) # 日本語が出ない場合は "arial" などに変えてみてね
large_font = pygame.font.SysFont("msgothic", 80)

# 色の定義
WHITE = (255, 255, 255)
BLUE  = (50, 150, 255)
RED   = (255, 80, 80)
BLACK = (0, 0, 0)

def reset_game():
    """ゲームの状態をリセットする関数"""
    return {
        "paddle": pygame.Rect(250, 370, 100, 15), # 板の場所
        "ball": pygame.Rect(300, 200, 15, 15),    # ボールの場所
        "ball_speed": [5, 5],                     # ボールの速度 [x, y]
        "lives": 3,                               # ライフ
        "game_over": False                        # ゲーム終了フラグ
    }

# ゲームデータの初期化
g = reset_game()

# --- 2. メインループ ---
while True:
    # イベント処理（閉じるボタンやキー入力）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # ゲームオーバー時に 'R' キーでリトライ
        if g["game_over"] and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                g = reset_game()

    if not g["game_over"]:
        # --- 3. ゲーム中の動く処理 ---
        
        # 板の移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and g["paddle"].left > 0:
            g["paddle"].x -= 8
        if keys[pygame.K_RIGHT] and g["paddle"].right < WIDTH:
            g["paddle"].x += 8

        # ボールの移動
        g["ball"].x += g["ball_speed"][0]
        g["ball"].y += g["ball_speed"][1]

        # 横壁での跳ね返り
        if g["ball"].left <= 0 or g["ball"].right >= WIDTH:
            g["ball_speed"][0] *= -1
        
        # 天井での跳ね返り
        if g["ball"].top <= 0:
            g["ball_speed"][1] *= -1

        # 板（自分）での跳ね返り
        if g["ball"].colliderect(g["paddle"]):
            g["ball_speed"][1] *= -1
            g["ball"].bottom = g["paddle"].top # 重なり防止

        # 落下判定
        if g["ball"].bottom >= HEIGHT:
            g["lives"] -= 1
            if g["lives"] <= 0:
                g["game_over"] = True
            else:
                # ライフが残っていれば真ん中から再開
                g["ball"].center = (WIDTH // 2, HEIGHT // 2)
                g["ball_speed"][1] *= -1 # 上向きに飛ばす

    # --- 4. 描画処理 ---
    screen.fill(BLACK) # 画面を真っ黒にする

    if not g["game_over"]:
        # ゲーム中の表示
        pygame.draw.rect(screen, BLUE, g["paddle"])  # 板を描く
        pygame.draw.ellipse(screen, RED, g["ball"])   # ボールを描く
        
        # ライフの表示
        life_text = font.render(f"LIFE: {g['lives']}", True, WHITE)
        screen.blit(life_text, (20, 20))
    else:
        # ゲームオーバー画面の表示
        over_text = large_font.render("GAME OVER", True, RED)
        retry_text = font.render("Press 'R' to Restart", True, WHITE)
        
        # 画面の真ん中に配置
        screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 60))
        screen.blit(retry_text, (WIDTH // 2 - 130, HEIGHT // 2 + 40))

    pygame.display.flip() # 画面を更新
    clock.tick(60)        # 1秒間に60コマで動かす
