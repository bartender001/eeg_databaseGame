import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
import pygame
import random
import threading
import time

# Function to get prediction
def get_prediction(sample):
    # Load the model
    model = joblib.load('my_model.pkl')  
    
    # Reshape sample if necessary and convert to numpy array
    sample = sample.values.reshape(1, -1)  
    prediction = model.predict(sample)
    
    return prediction

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Load data
data = pd.read_csv('emotions.csv')
X = data.drop('label', axis=1)
Y = data['label']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=123)

# Load images
playerImg = pygame.image.load('spaceship.png')
enemyImg = pygame.image.load('enemy.png')
backgroundImg = pygame.image.load('bg.jpg')  

# Score variable
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Spaceship class to handle independent movement and data reading
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_change = 0
        self.index = 0
        self.alive = True
    
    def move_and_read_data(self):
        while self.alive:
            if self.index < len(y_test):
                sample = x_test.iloc[self.index]  
                prediction = get_prediction(sample)
                
                # Adjust player movement based on prediction
                action = prediction.argmax()  
                
                if action == 0:
                    self.x_change = -20
                elif action == 1:
                    self.x_change = 0
                elif action == 2:
                    self.x_change = 20
                
                self.index += 1

            self.x += self.x_change
            if self.x <= 0:
                self.x = 0
            elif self.x >= 736:
                self.x = 736

            self.x_change = 0
            time.sleep(0.1)  # Adjust the speed of reading data and movement

    def stop(self):
        self.alive = False

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def is_collision(object1_rect, object2_rect):
    return object1_rect.colliderect(object2_rect)

def show_score(x, y):
    score_text = font.render("Collisions: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

running = True

# Create spaceship object and start its movement and data reading in a separate thread
spaceship = Spaceship(370, 480)
spaceship_thread = threading.Thread(target=spaceship.move_and_read_data)
spaceship_thread.start()

enemyX = random.randint(0, 736)
enemyY = 0
enemyY_change = .5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    enemyY += enemyY_change
    if enemyY > 600:
        enemyY = 0
        enemyX = random.randint(0, 736)

    # Get rectangles for collision detection
    player_rect = pygame.Rect(spaceship.x, spaceship.y, playerImg.get_width(), playerImg.get_height())
    enemy_rect = pygame.Rect(enemyX, enemyY, enemyImg.get_width(), enemyImg.get_height())

    # Collision detection between spaceship and enemy
    if is_collision(player_rect, enemy_rect):
        score += 1
        enemyY = 0
        enemyX = random.randint(0, 736)

    screen.blit(backgroundImg, (0, 0))
    player(spaceship.x, spaceship.y)
    enemy(enemyX, enemyY)
    show_score(10, 10)
    pygame.display.update()

pygame.quit()

# Stop the spaceship movement and data reading thread
spaceship.stop()
spaceship_thread.join()
