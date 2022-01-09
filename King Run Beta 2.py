#Patrick May, Ethan Kramer
#final Project for CS 110
#December 7 2020

import pgzrun
import pygame
import random
import sys
from itertools import cycle

#key values for the running pygame
TITLE = "King Run"
WIDTH = 600
HEIGHT = 500
display = pygame.display.set_mode((WIDTH, HEIGHT))

#game actor to keep track of certain global parts of the game
game = Actor('tile000')
game.state = [0, 1, 2, 3] #title, game, credits, quit
game.current_state = game.state[0]
game.is_playing = False
game.death_played = False

#colors used in the game
white = (255,255,255)
black = (0,0,0)
blue = (0,150,250)
LightBlue = (0,200,255)
color = (200,75,75)

#king should be a ~95x35 hitbox rectangle
#main character
king = Actor('tile000')
king.pos = (125,330)
king.walk = ['run000','run000','run000','run001','run001','run001','run002','run002','run002','run003','run003','run003','run004','run004','run004','run005','run005','run005','run006','run006','run006','run007','run007','run007']
king.walk_cycle = cycle(king.walk)
king.idle = ['tile000','tile000','tile000','tile001','tile001','tile001','tile001','tile002','tile002','tile002','tile002','tile003','tile003','tile003','tile004','tile004','tile004','tile005','tile005','tile005','tile005','tile006','tile006','tile006','tile006','tile007','tile007','tile007']
king.idle_cycle = cycle(king.idle)
king.vy = 0
king.score = 0
king.dead = False
king.jumping = False

#making a hitbox shadow for the king
king_shadow = Actor('shadow')
king_shadow.center = king.center
king_shadow.bottom = king.bottom

#background panes
background = Actor('parallax_2')
background2 = Actor('parallax_2')
background.topleft = 0,0
background2.topleft = 2*background.x-20, 0
static_back = Actor('parallax_2')
static_back.topleft=0,0

#obstacles
ground_block = Actor('scaled_rock') 
air_block = Actor('bat_1')
air_block.fly = ('bat_1') 
ground_block.exists = False
air_block.exists = False


#key values defining INITIAL VALUES for parts of the game
BACK_SPEED = 5
GRAVITY = 0.4
JUMP_POWER = 10
DIFFICULTY = 1

#setting game values from unchangeable start values
game.game_speed = BACK_SPEED
game.game_difficulty = DIFFICULTY

#accessory text functions
def textObjects(words, font):
    surface = font.render(words, True, white)
    
    return surface, surface.get_rect()

def black_text_objects(words, font):
    surface = font.render(words, True, black)
    return surface, surface.get_rect()

def text(words):
    text = ptgame.font.Font('freesandsbold.ttf',35)
    word_surface, word_box = textObjects(words, text)
    word_box.center = ((WIDTH // 2), (HEIGHT // 2))
    display.blit(word_surface, word_box)
    
    pygame.display.update(20)

#buttons used in the title screen to change game state
def button(message, x, y, w, h, inactive, active):
    mouse = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, active,(x,y,w,h))
        
        #CHECKING PLAY BUTTON
        if press[0] == 1 and 200 > mouse[0] > 100 and 275 > mouse[1] > 225:
            game.current_state = game.state[1]
        
        #checking credit button
        elif press[0] == 1 and 350 > mouse[0] > 250 and 350 > mouse[1] > 300:
            game.current_state = game.state[2]
        
        #checking quit button
        elif press[0] == 1 and 500 > mouse[0] > 400 and 275 > mouse[1] > 225:
            game.current_state = game.state[3]
    
            
    else:
        pygame.draw.rect(display, inactive,(x,y,w,h))
    
    text = pygame.font.Font('freesansbold.ttf',20)
    word_surface, word_box = textObjects(message, text)
    word_box.center = ((x+(w/2)), (y+(h/2)))
    display.blit(word_surface, word_box)

#draws the title screen for the game
def game_title():
    
   
    text = pygame.font.Font('freesansbold.ttf',30)
    word_surface, word_box = textObjects("King Run", text)
    word_box.center = ((WIDTH // 2), (HEIGHT // 2))
    display.blit(word_surface, word_box)
        
    button('Play',100,225,100,50, blue, LightBlue)
    button('Quit',400,225,100,50, blue, LightBlue)
    button('About',250,300,100,50, blue, LightBlue)
        
    
#runs the different states of the game
def draw():
    if game.current_state == 0:
        screen.clear()
        static_back.draw()
        king.draw()
        game_title()
        
    elif game.current_state == 1:
        screen.clear()
        background.draw()
        background2.draw()
        air_block.draw()
        ground_block.draw()
        king.draw()
        tutorial()
        score()
        sound()
        
    elif game.current_state == 2:
        screen.clear()
        static_back.draw()
        king.draw()
        about()
    
    elif game.current_state == 3:
        Quit()

#displays the score of the king at the bottom left as well as printing out text on death
def score():
    
    text = pygame.font.Font('freesansbold.ttf',18)
 
    word_surface, word_box = textObjects("Score: "+str(king.score), text)
    word_box.center = (50, 475)
    display.blit(word_surface, word_box)
    
    #displaying death text only seems to work in a function that is called with update
    #death text, and reminding player to press "r" to respawn
    if king.dead:
        text = pygame.font.Font('freesansbold.ttf',45)
        word_surface, word_box = textObjects("YOU DIED", text)
        word_box.center = ((WIDTH // 2), (HEIGHT // 3))
        display.blit(word_surface, word_box)
        word_surface, word_box = textObjects("YOUR SCORE: "+str(king.score), text)
        word_box.center = ((WIDTH // 2), (HEIGHT // 2))
        display.blit(word_surface, word_box)
        word_surface, word_box = textObjects("Press R to Respawn", text)
        word_box.center = ((WIDTH // 2), 2*(HEIGHT // 3))
        display.blit(word_surface, word_box)

#update function, updates differently depending on the current game state
def update(dt):
    if game.current_state ==1:   
        move_background()
        update_king()
        update_obstacles()
    
    elif game.current_state ==0:
        idle_king()
        
    elif game.current_state ==2:
        idle_king()
        draw()
    
    check_keys(dt)

#reminder text for parts of the gameplay loop
def tutorial():
    text = pygame.font.Font('freesansbold.ttf',14)
    if king.score<30:
        word_surface, word_box = textObjects("Press 'Space' to Jump", text)
        word_box.topleft = (50, 280)
        display.blit(word_surface, word_box)
        
     
    word_surface, word_box = textObjects("Press 'Esc' to return to the main menu", text)
    word_box.topleft = (10, 10)
    display.blit(word_surface, word_box)   
    
        
#accessory method to cycle through the king's idle frames
def idle_king():
    king.image = next(king.idle_cycle)
    
#main function to update king's vertical movement physics and run his animations, also checks for enemy collisions
def update_king():
    
    uy = king.vy
    #gravity accelerting downwards
    king.vy +=GRAVITY
    king.y += king.vy
    king_shadow.y = king.y
    
    
    #resetting if king is on the "floor"
    if(king.pos>=(125, 330)):
        king.vy = 0
        king.bottom = 450
        king_shadow.bottom = king.bottom
        king.jumping = False
   
    #checking for obstacle collision    
    if king_shadow.colliderect(ground_block) or king_shadow.colliderect(air_block): 
        king.dead = True
        
    
    #setting jump animations based on the king's velocity
    if not king.dead:
        if 0>king.vy>-5:
            king.image = "jump000"
        elif king.vy<-4:
            king.image = "jump001"
        elif 0<king.vy<5:
            king.image = "fall00"
        elif king.vy>4:
            king.image = "fall01"
        elif king.vy ==0:
            king_run()
    
    #starts death process
    if king.dead:
        death()
    
    #moving two background actors in conjunction as "tiles"
def move_background():
    
    background.x-=game.game_speed
    background2.x-=game.game_speed
    
    if background.topright<(0,0):
        background.topleft = WIDTH, 0
    elif background2.topright<(0,0):
        background2.topleft = WIDTH, 0
    
    #every 100 points, the game increases its speed slightly
    if game.game_difficulty <((king.score/100)+1) and king.score%100==0:
        game.game_difficulty+=1
        game.game_speed+=1.5
        
    
    
    #spawning a rock enemy on the ground
def create_ground():       
    spawn_offset = random.randrange(500, 1000, 1)
    ground_block.topleft=(spawn_offset, 380)
    ground_block.exists = True


#spawns a flying enemy to collide into in the air
def create_air():
    spawn_offset = random.randrange(500, 1000, 1)
    
    air_block.topleft=(spawn_offset, 200) 
    air_block.exists = True


#moves both obstacle actors as well as does cleanup when they reach off the left side of the screen
def update_obstacles():
    #sometimes the ground and air obstacles spawn too close together making an impossible obstacle
    #this checkes and moves the air obstacle out of the way further back making it a possible jump
    if ground_block.x-150<air_block.x<ground_block.x+150:
        air_block.x=ground_block.x+200*game.game_difficulty
    
    #moving the blocks
    ground_block.right-=game.game_speed
    air_block.right -= game.game_speed

    
    
    if ground_block.right < 0:
        king.score+=10
        ground_block.exists = False
    
    if air_block.right < 0:
        king.score+=10
        air_block.exists = False
        
    if not ground_block.exists:
        create_ground()
        
    if not air_block.exists:
        create_air()
        
   
def check_keys(dt):
    if keyboard.space and not king.jumping and not king.dead:
        king.vy=-1*JUMP_POWER
        sounds.jump_11.play()
        king.jumping = True
    
    if keyboard.escape:
        game.current_state =0
    
    if keyboard.r and king.dead:
        reborn()    


#resets the gameplay loop to play again
def reborn():
    king.dead = False
    king.score = 0
    game.game_speed=BACK_SPEED
    game.game_difficulty = 1
    game.death_played = False
    create_ground()
    create_air()


#automatic king run animation
def king_run():
    king.image = next(king.walk_cycle)


#starts the music loop
def sound():
    if not game.is_playing:
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.load('Yellow-Forest.wav')
        pygame.mixer.music.play(-1)
        game.is_playing = True


def death():
    king.image="death007"
    #death sound effect, checked to make sure it is not played multiple times
    if not game.death_played:
        sounds.king_death.play()
        game.death_played = True
    game.game_speed = 0
    
    
#prints out text for the about page    
def about():
    us = "Developed by Patrick May & Ethan Kramer"
    effects = "Sound Effects: dklon"
    sounds = "Soundtrack: patrickdearteaga.com"
    enemies = "Enemies: bevoiliin.com"
    king = "King Spritepack: Luiz Melo (luizmelo.itch.io)"
    back = "Background: Parallax Forest by ansimuz"
    
    #pasting all the different attribution to the sources used
    word_surface, word_box = textObjects("CREDITS", pygame.font.Font('freesansbold.ttf',30))
    word_box.center = ((WIDTH // 2), 25)
    display.blit(word_surface, word_box)
    
    
    text = pygame.font.Font('freesansbold.ttf',24)
    #developers
    word_surface, word_box = textObjects(us, text)
    word_box.topleft = (20, 460)
    display.blit(word_surface, word_box)
    
    #effects
    word_surface, word_box = textObjects(effects, text)
    word_box.topleft = (20, 170)
    display.blit(word_surface, word_box)
    
    #music
    word_surface, word_box = textObjects(sounds, text)
    word_box.topleft = (20, 200)
    display.blit(word_surface, word_box)
    
    #enemies
    word_surface, word_box = textObjects(enemies, text)
    word_box.topleft = (20, 230)
    display.blit(word_surface, word_box)
    
    #king
    word_surface, word_box = textObjects(king, text)
    word_box.topleft = (20, 260)
    display.blit(word_surface, word_box)
    
    #background
    word_surface, word_box = textObjects(back, text)
    word_box.topleft = (20, 290)
    display.blit(word_surface, word_box)
       
#quits out
def Quit():
    sys.exit()

#starts everything
game_title()
pgzrun.go()