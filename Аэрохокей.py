import pygame
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
import random

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Аэрохоккей")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать в Аэрохоккей!")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        start_button = QPushButton("Начать игру")
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)
        history_info = QLabel("Второй игрок управляет клавишами W и S.\nПервый игрок управляет стрелками вверх и вниз.")
        layout.addWidget(history_info)
        history_button = QPushButton("История игр")
        history_button.clicked.connect(self.show_history)
        layout.addWidget(history_button)

        self.setLayout(layout)

    def start_game(self):

        pygame.init()
        # Инициализация mixer
        pygame.mixer.init()
        # Загрузка музыки
        pygame.mixer.music.load("81cebf7e45fdef7.mp3")  # Укажите путь к вашему музыкальному файлу
        pygame.mixer.music.set_volume(0.5)  # Установка громкости (от 0.0 до 1.0)
        pygame.mixer.music.play(-1)
        # Задание параметров игры
        width, height = 800, 400
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Аэрохоккей")

        # Цвета
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)

        # Параметры игры
        paddle_width, paddle_height = 10, 100
        puck_radius = 15
        goal_limit = 10

        def game_loop():
            player1_score = 0
            player2_score = 0

            # Позиции
            player1_pos = [30, height // 2 - paddle_height // 2]
            player2_pos = [width - 30 - paddle_width, height // 2 - paddle_height // 2]
            puck_pos = [width // 2, height // 2]
            puck_speed = [5, 5]

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Управление игроками
                keys = pygame.key.get_pressed()

                # Игрок 1
                if keys[pygame.K_w] and player1_pos[1] > 0:
                    player1_pos[1] -= 5
                if keys[pygame.K_s] and player1_pos[1] < height - paddle_height:
                    player1_pos[1] += 5

                # Игрок 2
                if keys[pygame.K_UP] and player2_pos[1] > 0:
                    player2_pos[1] -= 5
                if keys[pygame.K_DOWN] and player2_pos[1] < height - paddle_height:
                    player2_pos[1] += 5

                # Движение шайбы
                puck_pos[0] += puck_speed[0]
                puck_pos[1] += puck_speed[1]

                # Проверка столкновений с границами
                if puck_pos[1] <= 0 or puck_pos[1] >= height:
                    puck_speed[1] = -puck_speed[1]

                # Проверка столкновений с игроками
                if (player1_pos[0] < puck_pos[0] < player1_pos[0] + paddle_width and
                        player1_pos[1] < puck_pos[1] < player1_pos[1] + paddle_height):
                    puck_speed[0] = -puck_speed[0]

                if (player2_pos[0] < puck_pos[0] < player2_pos[0] + paddle_width and
                        player2_pos[1] < puck_pos[1] < player2_pos[1] + paddle_height):
                    puck_speed[0] = -puck_speed[0]

                # Проверка на голы
                if puck_pos[0] <= 0:  # Ворота игрока 2
                    player2_score += 1
                    puck_pos = [width // 2, height // 2]
                    puck_speed = [5, 5]
                if puck_pos[0] >= width:  # Ворота игрока 1
                    player1_score += 1
                    puck_pos = [width // 2, height // 2]
                    puck_speed = [-5, 5]

                # Проверка счёта и завершение игры
                if player1_score == goal_limit or player2_score == goal_limit:
                    show_winner(player1_score, player2_score)
                    break

                # Отрисовка
                screen.fill(WHITE)

                pygame.draw.rect(screen, BLUE, (player1_pos[0], player1_pos[1], paddle_width, paddle_height))
                pygame.draw.rect(screen, RED, (player2_pos[0], player2_pos[1], paddle_width, paddle_height))
                pygame.draw.circle(screen, BLACK, (int(puck_pos[0]), int(puck_pos[1])), puck_radius)

                # Отображение счета
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"{player1_score} - {player2_score}", True, BLACK)
                screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

                pygame.display.flip()
                pygame.time.delay(30)

        def show_winner(player1_score, player2_score):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill(WHITE)
                for i in range(10000):
                    screen.fill(pygame.Color('green'),
                                (random.random() * width,
                                 random.random() * height, 1, 2))
                font = pygame.font.Font(None, 72)
                if player1_score > player2_score:
                    winner_text = font.render("Игрок 1 Победил!", True, BLUE)
                else:
                    winner_text = font.render("Игрок 2 Победил!", True, RED)

                screen.blit(winner_text,
                            (width // 2 - winner_text.get_width() // 2,
                             height // 2 - winner_text.get_height() // 2 - 20))

                # Кнопки

                restart_text = font.render("Нажмите R для перезапуска", True, BLACK)
                exit_text = font.render("Нажмите Q для выхода", True, BLACK)
                screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))
                screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 70))

                pygame.display.flip()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    if player1_score > player2_score:
                        with open('history.txt', 'w', encoding="utf8") as sa:
                            sa.write(f'Игрок 1, {player1_score}-{player2_score}')
                    else:
                        with open('history.txt', 'w', encoding="utf8") as sa:
                            sa.write(f'Игрок 2, {player1_score}-{player2_score}')
                    game_loop()
                if keys[pygame.K_q]:
                    if player1_score > player2_score:
                        with open('history.txt', 'w', encoding="utf8") as sa:
                            sa.write(f'Игрок 1, {player1_score}-{player2_score}')
                    else:
                        with open('history.txt', 'w', encoding="utf8") as sa:
                            sa.write(f'Игрок 2, {player1_score}-{player2_score}')
                    pygame.quit()
                    sys.exit()

        game_loop()

    def show_history(self):
        self.res = results()
        self.res.show()

class results(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 200)
        with open('history.txt', 'r', encoding="utf8") as csvfile:
            reader = csvfile.readlines()
            csvfile.close()
        with open('history.txt', 'w', encoding="utf8") as e:
            for i in reader:
                e.write(i)
            e.close()
        reader = [i.split(',') for i in reader]
        self.tableWidget = QTableWidget(2, 2, self)
        self.tableWidget.setHorizontalHeaderLabels(['Победитель', 'Результат'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(reader):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elem.strip()))
        self.tableWidget.resizeColumnsToContents()

app = QApplication(sys.argv)
window = StartWindow()
window.show()
sys.exit(app.exec())
