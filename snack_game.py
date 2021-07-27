import pygame
import random
from time import sleep
import os

pygame.init()
pygame.mixer.init()

#colurs 
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pink = (233,210,229)

#Creating screen display
screen_width = 900
screen_hight = 600
gamewindow = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("snack game created by Pratham")
clock = pygame.time.Clock()
font1 = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 60)

back_img = pygame.image.load("audio\Ground.png")
back_img = pygame.transform.scale(back_img, (screen_width, screen_hight))
welcome_img = pygame.image.load("audio\game start.png")
welcome_img = pygame.transform.scale(welcome_img, (screen_width, screen_hight)).convert_alpha()
over_img = pygame.image.load("audio\game over.png")
over_img = pygame.transform.scale(over_img, (screen_width, screen_hight)).convert_alpha()

def text_screen_small(text, color, x, y):
    screen_text = font1.render(text, True, color)
    gamewindow.blit(screen_text, [x,y])

def text_screen_big(text, color, x, y):
    screen_text = font2.render(text, True, color)
    gamewindow.blit(screen_text, [x,y])

def snack(gamewindow, color, snack_list, snack_size):
    for x,y in snack_list:
        pygame.draw.rect(gamewindow, color, [x,y, snack_size, snack_size])


#welcome scrren
def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill(pink)
        gamewindow.blit(welcome_img, (0,0))
        pygame.display.update()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                exit_game = True
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RETURN:
                    pygame.mixer.music.load("audio\starting_music.mp3")
                    pygame.mixer.music.play()
                    game_loop()
                
#game loop
def game_loop():

    #Variables for game
    exit_game = False
    game_over = False
    snack_x = 45
    snack_y = 55
    snack_size = 35
    fps = 40
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_hight/2)
    food_size = 35
    velocity_x = 0 
    velocity_y = 0
    init_velocity = 5
    score = 0
    snack_list = []
    snack_length = 1
    extra_point_x = random.randint(20, screen_width/2)
    extra_point_y = random.randint(20, screen_width/2)
    if (not os.path.exists("Highscore.txt")):
        with open("Highscore.txt", "w") as f:
            f.write("0")
    with open('Highscore.txt', 'r') as f:
        highscore = f.read()

    while not exit_game:

        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(highscore))
            gamewindow.fill(white)
            gamewindow.blit(over_img,(0,0))
            text_screen_big(": "+str(score), black,500,522)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()

                    if event.key == pygame.K_ESCAPE:
                        exit_game = True

        else:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    exit_game = True

                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if events.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if events.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if events.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if events.key == pygame.K_ESCAPE:
                        exit_game = True
                        
            snack_x = snack_x + velocity_x
            snack_y = snack_y + velocity_y

            if abs(snack_x - food_x)<20 and abs(snack_y - food_y)<20:
                pygame.mixer.music.load("audio\\TING.mp3")
                pygame.mixer.music.play()
                score = score + 10
                # print('Your score is {}'.format(score))
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_hight/2)
                fps = fps + 1
                snack_length = snack_length + 5

                if score > int(highscore):
                    highscore = score

            gamewindow.fill(white)
            gamewindow.blit(back_img, (0,0))
            text_screen_small("Score: " + str(score) + " | High score : "+ str(highscore), black, 20, 5)

            head = []
            head.append(snack_x)
            head.append(snack_y)
            snack_list.append(head)
            # print(snack_list)
            if len(snack_list)>snack_length:
                del snack_list[0]

            if head in snack_list[:-1]:
                pygame.mixer.music.load("audio\hit.wav")
                pygame.mixer.music.play()
                sleep(1)                
                game_over = True

            if snack_x < 0 or snack_x > screen_width or snack_y < 0 or snack_y > screen_hight:
                pygame.mixer.music.load("audio\hit.wav")
                pygame.mixer.music.play()
                sleep(1)
                game_over = True

            #making food and snack
            snack(gamewindow, black, snack_list, snack_size)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, food_size, food_size])
            #Extra point
            if score>=100 and (score%100)==0 :
                pygame.mixer.music.load("audio\point.wav")
                pygame.mixer.music.play()

                pygame.draw.rect(gamewindow, red, [extra_point_x, extra_point_y,50,50])
                if abs(snack_x - extra_point_x)<20 and abs(snack_y - extra_point_y)<20:
                    pygame.mixer.music.load("audio\TING.mp3")
                    pygame.mixer.music.play()
                    score = score + 20
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == "__main__":
    
    welcome()
