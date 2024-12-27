import cv2
import mediapipe as mp
import pygame
import sys
import json
import random
import time

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Khởi tạo đồng hồ FPS
clock = pygame.time.Clock()

# Cài đặt màn hình
WIDTH, HEIGHT = 650, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Đỡ Bóng Phá Gạch")

# Tải hình nền
manhinhcho = pygame.image.load("manhinhcho.jpg")  # Thay đổi đường dẫn nếu cần
manhinhcho = pygame.transform.scale(manhinhcho, (WIDTH, HEIGHT))
manhinhlv = pygame.image.load("manhinhlv.jpg")  # Thay đổi đường dẫn nếu cần
manhinhlv = pygame.transform.scale(manhinhlv, (WIDTH, HEIGHT))
manhinhchoi = pygame.image.load("manhinhchoi.jpg")  # Thay đổi đường dẫn nếu cần
manhinhchoi = pygame.transform.scale(manhinhchoi, (WIDTH, HEIGHT))
manhinhwin = pygame.image.load("manhinhwin.jpg")  # Thay đổi đường dẫn nếu cần
manhinhwin = pygame.transform.scale(manhinhwin, (WIDTH, HEIGHT))
manhinhlose = pygame.image.load("manhinhlose.jpg")  # Thay đổi đường dẫn nếu cần
manhinhlose = pygame.transform.scale(manhinhlose, (WIDTH, HEIGHT))
# Màn hình nền cho từng cấp độ
background_easy = pygame.image.load("background_easy.jpg")  # Dễ
background_easy = pygame.transform.scale(background_easy, (WIDTH, HEIGHT))
background_medium = pygame.image.load("background_medium.jpg")  # Trung bình
background_medium = pygame.transform.scale(background_medium, (WIDTH, HEIGHT))
background_hard = pygame.image.load("background_hard.jpg")  # Khó
background_hard = pygame.transform.scale(background_hard, (WIDTH, HEIGHT))
# Tải hình ảnh các đối tượng
brick_img = pygame.image.load("brick.png")  # Hình ảnh gạch
brick_img = pygame.transform.scale(brick_img, (WIDTH // 8 - 5, 30))  
obstacle_img = pygame.image.load("obstacle.png")  # Hình ảnh chướng ngại vật
obstacle_img = pygame.transform.scale(obstacle_img, (50, 20))  
ball_img = pygame.image.load("ball.png")  # Hình ảnh bóng
ball_img = pygame.transform.scale(ball_img, (25, 25))
paddle_img = pygame.image.load("paddle.png")  # Hình ảnh thanh đỡ
paddle_img = pygame.transform.scale(paddle_img, (100, 20)) 
# Tải hình ảnh các powerup
big_ball_img = pygame.image.load("big_ball.png")
extra_life_img = pygame.image.load("extra_life.png")
big_paddle_img = pygame.image.load("big_paddle.png")
add_brick_img = pygame.image.load("add_brick.png")
big_ball_img = pygame.transform.scale(big_ball_img, (30, 30))
extra_life_img = pygame.transform.scale(extra_life_img, (30, 30))
big_paddle_img = pygame.transform.scale(big_paddle_img, (30, 30))
add_brick_img = pygame.transform.scale(add_brick_img, (30, 30))

# Tải các file âm thanh
brickHitSound = pygame.mixer.Sound("bullet.wav")
bounceSound = pygame.mixer.Sound("hitGameSound.wav")
bounceSound.set_volume(.5)  
effectSound1 = pygame.mixer.Sound("âm thanh khi bóng rơi ra màn hình.mp3")
effectSound2 = pygame.mixer.Sound("âm thanh khi bóng to lên.mp3")
effectSound3 = pygame.mixer.Sound("âm thanh ăn vật phẩm.mp3")
game_over_sound = pygame.mixer.Sound("âm thanh thua trò chơi.mp3")  
win_sound = pygame.mixer.Sound("winning-218995.mp3")  
# Tải nhạc nền
background_music = 'nhạc nền.mp3'  # Đường dẫn tới tệp nhạc nền

# Phát nhạc nền (lặp lại vô hạn)
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(loops=-1, start=0.0)
# Điều chỉnh âm lượng nhạc nền (từ 0.0 đến 1.0)
pygame.mixer.music.set_volume(0.3)  # 30% âm lượng
# Tạm dừng nhạc nền
pygame.mixer.music.pause()
# Tiếp tục nhạc nền
pygame.mixer.music.unpause()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (225, 225, 0)


# Font chữ
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 20)
# Font tùy chỉnh (thay 'custom_font.ttf' bằng tên file font của bạn)
font = pygame.font.Font("custom_font.ttf", 80)  # Font tiêu đề chính
font.set_bold(True)  # Đặt font đậm
small_font = pygame.font.Font("custom_font.ttf", 20)  # Font nhỏ hơn cho các văn bản khác
small_font.set_bold(True)  # Đặt font đậm

# File lưu điểm cao
high_score_file = "high_score.json"
# Đọc điểm cao
def load_high_score():  
    try:
        with open(high_score_file, "r") as f:
            return json.load(f).get("high_score", 0)
    except FileNotFoundError:
        return 0
# Lưu điểm cao
def save_high_score(score):
    try:
        with open(high_score_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"high_score": 0}
    
    # Cập nhật điểm cao nếu điểm mới cao hơn  
    if score > data["high_score"]:
        data["high_score"] = score
    
    # Lưu lại file JSON với điểm cao mới
    with open(high_score_file, "w") as f:
        json.dump(data, f)
        
# Màn hình bắt đầu
def show_start_screen():
    win.blit(manhinhcho, (0, 0))  # Vẽ hình nền lên màn hình
   
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
# Màn hình chọn cấp độ
def show_level_selection():
    win.blit(manhinhlv, (0, 0))  # Vẽ hình nền lên màn hình
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
# Vẽ màn hình cho từng level
def draw_level_background(level):
    if level == "easy":
        win.blit(background_easy, (0, 0))
    elif level == "medium":
        win.blit(background_medium, (0, 0))
    elif level == "hard":
        win.blit(background_hard, (0, 0))
# Tạo gạch với vị trí căn giữa
def create_bricks(rows, cols, brick_width, brick_height):
    bricks = []
    # Tính toán khoảng cách giữa các viên gạch để căn giữa
    total_width = cols * brick_width
    start_x = (WIDTH - total_width) // 2  # Tính toán vị trí bắt đầu để căn giữa

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * brick_width
            y = row * brick_height
            bricks.append(pygame.Rect(x, y, brick_width - 5, brick_height - 5))
    return bricks
# Tạo vật phẩm
def spawn_powerup(x, y):
    powerup_type = random.choice(["big_ball", "extra_life", "big_paddle", "add_brick"])
    if powerup_type == "big_ball":
        img = big_ball_img
    elif powerup_type == "extra_life":
        img = extra_life_img
    elif powerup_type == "big_paddle":
        img = big_paddle_img
    elif powerup_type == "add_brick":
        img = add_brick_img
    return {"type": powerup_type, "rect": pygame.Rect(x, y, 30, 30), "img": img}
# Xử lý va chạm vật phẩm
def handle_powerup_collision(powerup, ball_radius, paddle_width, lives, bricks):
    global ball_img, paddle_img  # Thêm dòng này để sửa đổi ball_img và paddle_img
    if powerup["type"] == "big_ball":
        ball_radius += 5
        # Tăng kích thước bóng
        ball_img = pygame.transform.scale(ball_img, (ball_radius * 2, ball_radius * 2))  # Điều chỉnh kích thước bóng
    elif powerup["type"] == "extra_life":
        lives += 1
    elif powerup["type"] == "big_paddle":
        paddle_width += 50
        # Tăng kích thước thanh đỡ
        paddle_img = pygame.transform.scale(paddle_img, (paddle_width, 20))  # Điều chỉnh kích thước thanh đỡ        
    elif powerup["type"] == "add_brick":
        new_bricks = create_bricks(1, 5, WIDTH // 8, 30)
        bricks.extend(new_bricks)
        
    return ball_radius, paddle_width, lives

# Tạo chướng ngại vật
def create_obstacles(count):
    obstacles = []
    for _ in range(count):
        obs_x = random.randint(0, WIDTH - 50)
        obs_y = random.randint(50, HEIGHT // 2)
        obstacles.append(pygame.Rect(obs_x, obs_y, 50, 20))
    return obstacles
# Hiển thị màn hình chiến thắng
def show_win_screen(score, high_score):
    win.blit(manhinhwin, (0, 0))  # Vẽ hình nền lên màn hình
    offset = 50  # Căn dòng màn hình
    # Vẽ điểm số 
    score_text = small_font.render(f"{score}", True, YELLOW)  
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2 + 100, HEIGHT // 4 + offset)) 
    # Vẽ điểm cao 
    high_score_text = small_font.render(f"{high_score}", True, YELLOW)  
    win.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2 + 100, HEIGHT // 4 + 2 * offset))  
    pygame.display.update()   
    # Đợi người chơi bấm phím để lựa chọn hành động  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_r:  # Nhấn R để khởi động lại trò chơi  
                    return "restart"  
                if event.key == pygame.K_m:  # Nhấn M để quay lại màn hình chính  
                    return "main_menu"  
                if event.key == pygame.K_q:  # Nhấn Q để thoát trò chơi  
                    pygame.quit()  
                    sys.exit()
# Hiển thị màn hình kết thúc 
def show_game_over_screen(score, high_score):  
    win.blit(manhinhlose, (0, 0))  # Vẽ hình nền lên màn hình  
    offset = 50  # Khoảng cách giữa các dòng văn bản  
    # Vẽ điểm số 
    score_text = small_font.render(f"{score}", True, RED)  
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2 + 100, HEIGHT // 4 + offset)) 
    # Vẽ điểm cao 
    high_score_text = small_font.render(f"{high_score}", True, RED)  
    win.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2 + 100, HEIGHT // 4 + 2 * offset))  
    pygame.display.update()  # Cập nhật màn hình để hiển thị  
      
    # Đợi người chơi bấm phím để lựa chọn hành động  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_r:  # Nhấn R để khởi động lại trò chơi  
                    return "restart"  
                if event.key == pygame.K_m:  # Nhấn M để quay lại màn hình chính  
                    return "main_menu"  
                if event.key == pygame.K_q:  # Nhấn Q để thoát trò chơi  
                    pygame.quit()  
                    sys.exit()
# Tạm dừng trò chơi
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Nhấn P để tiếp tục
                    paused = False
                if event.key == pygame.K_q:  # Nhấn Q để thoát
                    pygame.quit()
                    sys.exit()
# Vòng lặp chính
def game_loop(level):
    global high_score
    # Cấu hình cấp độ
    ball_speed = [3, 3] if level == "easy" else [5, 5] if level == "medium" else [7, 7]
    obstacle_count = 3 if level == "easy" else 5 if level == "medium" else 7
    paddle_width = 100
    paddle_height = 10
    paddle_pos = [WIDTH // 2 - paddle_width // 2, HEIGHT - 50]
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_radius = 10
    lives = 3
    bricks = create_bricks(3, 5, WIDTH // 8, 30)
    powerups = [] 

    # Thanh đỡ và bóng
    paddle_width = 100
    paddle_height = 20
    paddle_pos = [WIDTH // 2 - paddle_width // 2, HEIGHT - 50]
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_radius = 10

    # Tạo gạch và chướng ngại vật
    bricks = create_bricks(4, 6, WIDTH // 8, 30)
    obstacles = create_obstacles(obstacle_count)

    score = 0

    # MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Lỗi mở camera! Vui lòng kiểm tra kết nối.")
        pygame.quit()
        sys.exit()
    running = True 
       
    while running:
        draw_level_background(level)  # Vẽ màn hình nền theo cấp độ
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                paddle_pos[0] = int(hand_x * WIDTH) - paddle_width // 2
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        cv2.imshow("Webcam - Hand Tracking", frame)      
        
        # Va chạm với gạch
        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
        for brick in bricks[:]:
            if ball_rect.colliderect(brick):
                bricks.remove(brick)  # Xóa gạch khi va chạm
                ball_speed[1] = -ball_speed[1]  # Đổi hướng bóng
                score += 10  # Cộng điểm khi phá gạch
                brickHitSound.play()
                break  # Thoát vòng lặp sau khi phá một viên gạch
        # Kiểm tra nếu không còn gạch nào
        if not bricks:
            win_sound.play()
            choice = show_win_screen(score, high_score)  # Hiển thị màn hình chiến thắng
            if choice == "restart":
              game_loop(level)  # Gọi lại trò chơi
            elif choice == "main_menu":
              show_start_screen()
            level = show_level_selection()
            game_loop(level)
            return  # Thoát khỏi hàm game_loop

        # Cập nhật bóng
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]
        if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
            bounceSound.play()
            ball_speed[0] = -ball_speed[0]
        if ball_pos[1] <= ball_radius:
            bounceSound.play()
            ball_speed[1] = -ball_speed[1]
        if ball_pos[1] >= HEIGHT:
            lives -= 1
            if lives <= 0:
                running = False
            else:
                ball_pos = [WIDTH // 2, HEIGHT // 2]
    # Cập nhật thanh đỡ
        if paddle_pos[1] <= ball_pos[1] + ball_radius <= paddle_pos[1] + paddle_height and paddle_pos[0] <= ball_pos[0] <= paddle_pos[0] + paddle_width:
            ball_speed[1] = -ball_speed[1]
            effectSound2.play()
        paddle_pos[0] = max(0, min(WIDTH - paddle_width, paddle_pos[0]))
    # Cập nhật gạch
        for brick in bricks[:]:
            if brick.collidepoint(ball_pos[0], ball_pos[1] - ball_radius):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                if random.random() < 0.7:
                    powerups.append(spawn_powerup(brick.x, brick.y))   
    
        for powerup in powerups[:]:
            powerup["rect"].y += 3
            if powerup["rect"].colliderect(pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height)):
                ball_radius, paddle_width, lives = handle_powerup_collision(powerup, ball_radius, paddle_width, lives, bricks)
                effectSound3.play()
                powerups.remove(powerup)

            elif powerup["rect"].y > HEIGHT:
                powerups.remove(powerup)
       
        # Va chạm với chướng ngại vật
        for obstacle in obstacles[:]:
            if obstacle.collidepoint(ball_pos[0], ball_pos[1] - ball_radius):
                obstacles.remove(obstacle)
                ball_speed[1] = -ball_speed[1]
                score -= 10  # Trừ 10 điểm khi bóng chạm chướng ngại vật
        
        # Vẽ lại các đối tượng trên màn hình        
        for brick in bricks:
            win.blit(brick_img, (brick.x, brick.y))
        for obstacle in obstacles:
            win.blit(obstacle_img, (obstacle.x, obstacle.y))
        win.blit(ball_img, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))
        win.blit(paddle_img, (paddle_pos[0], paddle_pos[1]))
        for powerup in powerups:
            win.blit(powerup["img"], powerup["rect"])       

       # Vẽ giá trị của lives 
        lives_text = small_font.render(f"{lives}", True, WHITE)
        win.blit(lives_text, (100, 5))  
        # Vẽ giá trị của score 
        score_text = small_font.render(f"{score}", True, WHITE)
        win.blit(score_text, (100, 30))  
        pygame.display.update()   

                # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Nhấn P để tạm dừng
                    pause_game()

    # Sau khi game kết thúc, gọi màn hình kết thúc và xử lý lựa chọn người chơi
    if len(bricks) == 0:  # Khi người chơi phá hết gạch
        choice = show_win_screen(score, high_score)
    else:
        choice = show_game_over_screen(score, high_score)
    if choice == "restart":
        game_loop(level)  # Gọi lại hàm game_loop để khởi động lại trò chơi
    elif choice == "main_menu":
        show_start_screen()  # Quay lại màn hình chính
        level = show_level_selection()  # Chọn lại cấp độ
        game_loop(level)  # Bắt đầu trò chơi lại
    # Điều khiển tốc độ khung hình (60 FPS)
        clock.tick(60)
    # Dứng nhạc khi trò chơi kết thúc
    pygame.mixer.music.stop()
       
# Bắt đầu trò chơi
high_score = load_high_score()
show_start_screen()
level = show_level_selection()
game_loop(level)