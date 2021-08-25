# initialization
import pygame
import random
import os
import time

pygame.init()
clock=pygame.time.Clock()
font=pygame.font.SysFont(None,55)

# backgound music

pygame.mixer.init()
pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play(-1)

# colours
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
blue=(0,0,255)

# game window
screen_w=900
screen_h=600
game_win=pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("snakes by pa")
icon=pygame.image.load('snake.png')
pygame.display.set_icon(icon)
pygame.display.update()

# background
bgimg=pygame.image.load("pic.jpg")
bgimg=pygame.transform.scale(bgimg,(screen_w,screen_h)).convert_alpha()


def text_score(text,color,x,y):
    text_screen=font.render(text,True,color)
    game_win.blit(text_screen,[x,y])

def plot_snake(game_win,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(game_win,color,[x,y,snake_size,snake_size])

def welcome():
    exit_games=False
    while not exit_games:
        game_win.fill(white)
        game_win.blit(bgimg,(0,0))
        text_score("Welcome to snakes by pa",red,200,240)
        text_score("press space to play",red,240,300)
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        selection()
    
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()

def selection():
    exit_games=False
    while not exit_games:
        game_win.fill(white)
        game_win.blit(bgimg,(0,0))
        text_score("for single player press space",red,200,240)
        text_score("for multiplayer press enter",red,220,300)
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        welcome()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        gameloop()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop2()
    
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()



def gameloop():

    # game specific variables

    exit_games=False
    game_over=False
    snake_x=45
    snake_y=55
    velocity_x=0
    velocity_y=0
    snake_size=15
    velocity_init=3
    score=0
    food_x=random.randint(20,screen_w/1.2)
    food_y=random.randint(20,screen_h/1.2)
    fps=60
    snk_list=[]
    snk_len=1
    reset=0

    # high score
    if (not os.path.exists('hscore.txt')):
        with open('hscore.txt','w') as f:
            f.write("0")
    with open('hscore.txt','r') as f:
        hscore=f.read()

    while not exit_games:
        
        if game_over==True:
            with open('hscore.txt','w') as f:
                f.write(str(hscore))
            game_win.fill(black)
            game_win.blit(bgimg,(0,0))
            text_score("game over!!!!!",red,280,200)
            text_score("press enter to continue",red,200,240)
            text_score("score:"+str(score)+"  high score  "+str(hscore),red,210,280)
            text_score("to reset the score press r",red,200,400)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        welcome()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        hscore=0    

        
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        welcome()
                    if event.key==pygame.K_RIGHT:
                        velocity_x=velocity_init
                        velocity_y=0
                    if event.key==pygame.K_DOWN:
                        velocity_y=velocity_init
                        velocity_x=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-velocity_init
                        velocity_y=0
                    if event.key==pygame.K_UP:
                        velocity_y=-velocity_init
                        velocity_x=0

            snake_x+=velocity_x
            snake_y+=velocity_y
            if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
                pygame.mixer.music.load("beep.mp3")
                pygame.mixer.music.play()
                score+=10
                snk_len+=5
                velocity_init+=0.3
                food_x=random.randint(20,screen_w/1.2)
                food_y=random.randint(20,screen_h/1.2)
                time.sleep(0.2)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                if score>int(hscore):
                    hscore=score

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_len:
                del snk_list[0]

            if snake_x>screen_w or snake_x<0 or snake_y>screen_h or snake_y<0:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True
            if head in snk_list[:-1]:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True

            game_win.fill(white)
            game_win.blit(bgimg,(0,0))
            text_score("score:"+str(score)+"  high score  "+str(hscore),red,10,10)
            plot_snake(game_win,black,snk_list,snake_size)
            pygame.draw.rect(game_win,red,[food_x,food_y,snake_size,snake_size])
        
        
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()

def gameloop2():

    # game specific variables

    exit_games=False
    game_over=False
    snake1_x=45
    snake1_y=55
    snake2_x=45
    snake2_y=105
    velocity1_x=0
    velocity1_y=0
    velocity2_x=0
    velocity2_y=0
    snake_size=15
    velocity_init1=3
    velocity_init2=3
    score1=0
    score2=0
    food_x=random.randint(20,screen_w/1.2)
    food_y=random.randint(20,screen_h/1.2)
    fps=60
    snk_list1=[]
    snk_len1=1
    snk_list2=[]
    snk_len2=1
    reset=0

    # high score
    if (not os.path.exists('hscore.txt')):
        with open('hscore.txt','w') as f:
            f.write("0")
    with open('hscore.txt','r') as f:
        hscore=f.read()

    while not exit_games:
        
        if game_over==True:
            with open('hscore.txt','w') as f:
                f.write(str(hscore))
            game_win.fill(black)
            game_win.blit(bgimg,(0,0))
            text_score("game over!!!!!",red,280,200)
            text_score("press enter to continue",red,200,240)
            text_score("player1:"+str(score1)+"  player2:"+str(score2)+"  high score  "+str(hscore),red,210,280)
            text_score("to reset the score press r",red,200,400)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        welcome()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop2()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        hscore=0    

        
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_games=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        welcome()
                    if event.key==pygame.K_RIGHT:
                        velocity1_x=velocity_init1
                        velocity1_y=0
                    if event.key==pygame.K_DOWN:
                        velocity1_y=velocity_init1
                        velocity1_x=0
                    if event.key==pygame.K_LEFT:
                        velocity1_x=-velocity_init1
                        velocity1_y=0
                    if event.key==pygame.K_UP:
                        velocity1_y=-velocity_init1
                        velocity1_x=0
                    if event.key==pygame.K_d:
                        velocity2_x=velocity_init2
                        velocity2_y=0
                    if event.key==pygame.K_s:
                        velocity2_y=velocity_init2
                        velocity2_x=0
                    if event.key==pygame.K_a:
                        velocity2_x=-velocity_init2
                        velocity2_y=0
                    if event.key==pygame.K_w:
                        velocity2_y=-velocity_init2
                        velocity2_x=0

            snake1_x+=velocity1_x
            snake1_y+=velocity1_y
            snake2_x+=velocity2_x
            snake2_y+=velocity2_y
            if abs(snake1_x-food_x)<10 and abs(snake1_y-food_y)<10:
                pygame.mixer.music.load("beep.mp3")
                pygame.mixer.music.play()
                score1+=10
                snk_len1+=5
                velocity_init1+=0.3
                food_x=random.randint(20,screen_w/1.2)
                food_y=random.randint(20,screen_h/1.2)
                time.sleep(0.2)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                if score1>int(hscore):
                    hscore=score1
            if abs(snake2_x-food_x)<10 and abs(snake2_y-food_y)<10:
                pygame.mixer.music.load("beep.mp3")
                pygame.mixer.music.play()
                score2+=10
                snk_len2+=5
                velocity_init2+=0.3
                food_x=random.randint(20,screen_w/1.2)
                food_y=random.randint(20,screen_h/1.2)
                time.sleep(0.2)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                if score2>int(hscore):
                    hscore=score2

            head1=[]
            head1.append(snake1_x)
            head1.append(snake1_y)
            snk_list1.append(head1)
            head2=[]
            head2.append(snake2_x)
            head2.append(snake2_y)
            snk_list2.append(head2)

            if len(snk_list1)>snk_len1:
                del snk_list1[0]
            if len(snk_list2)>snk_len2:
                del snk_list2[0]

            if snake1_x>screen_w or snake1_x<0 or snake1_y>screen_h or snake1_y<0:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True
            if head1 in snk_list1[:-1]:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True
            if snake2_x>screen_w or snake2_x<0 or snake2_y>screen_h or snake2_y<0:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True
            if head2 in snk_list2[:-1]:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                time.sleep(0.5)
                pygame.mixer.music.load("audio.mp3")
                pygame.mixer.music.play()
                game_over=True

            game_win.fill(white)
            game_win.blit(bgimg,(0,0))
            text_score("player1:"+str(score1)+"  player2:"+str(score2)+"  high score  "+str(hscore),red,10,10)
            plot_snake(game_win,black,snk_list1,snake_size)
            plot_snake(game_win,blue,snk_list2,snake_size)
            pygame.draw.rect(game_win,red,[food_x,food_y,snake_size,snake_size])
        
        
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()

welcome()