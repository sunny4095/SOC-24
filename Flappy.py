import pygame # type: ignore
import random
import numpy as np # type: ignore

# Game Variables 
pygame.init()
WIDTH, HEIGHT = 500,700
GRAVITY = 0.25
BIRD_JUMP = 7
PIPE_GAP = 200
PIPE_VELOCITY = 5
BIRD_WIDTH, BIRD_HEIGHT = 25, 25
PIPE_WIDTH, PIPE_HEIGHT = 50, 800
BACKGROUND_COLOR = (0, 102, 204)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('dejavuserif',60)


# Loading Images
pipe_image = pygame.image.load('pipe.png')
pipe_image = pygame.transform.scale(pipe_image,(PIPE_WIDTH, PIPE_HEIGHT))


# Bird Class
class Bird(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.state = [] #To store different flapping positions of bird
        self.index = 0
        for num in range(1,5) :
            image = pygame.image.load(f'bird{num}.png').convert_alpha()
            image = pygame.transform.scale(image, (BIRD_HEIGHT,BIRD_WIDTH))
            self.state.append(image)
        self.image = self.state[self.index]  
        self.rect = self.image.get_rect()
        self.rect.center = (100,350)
        self.vel = -7
        self.counter = 0

    
    def update(self) :
        self.rect.y += int(self.vel)
        self.vel += GRAVITY
        self.counter += 1
        if self.counter >= 20 :
            self.counter = 0 
            self.index += 1
        if self.index >= 4 :
            self.index = 0 
        self.image = self.state[self.index]

    def jump(self) :
        if pygame.mouse.get_pressed()[0] or jump == True :
            self.vel = -1* BIRD_JUMP
        if self.vel > 10 :
            self.vel = 10
    def draw(self) :
        bird_group.draw(screen)


# Class Pipe
class Pipe(pygame.sprite.Sprite) :
    def __init__(self,x,y,inverted) :
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('pipe.png')
        self.image = pygame.transform.scale(image,(PIPE_WIDTH,PIPE_HEIGHT))
        if inverted == True :
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (x,y - PIPE_GAP)
        else:
            self.rect = self.image.get_rect()
            self.rect.midtop = (x,y)

    def update(self) :
        self.rect.x -= PIPE_VELOCITY
        if self.rect.x <= -20 :
            self.kill()

# setting the bird and pipes
last_pipe = 0          
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)
pipe_group = pygame.sprite.Group()
running = True
Active = True
pass_pipe = False
score = 0

# Detecting collisions 
def check_collision(group_1,group_2) :
    if pygame.sprite.groupcollide(group_1,group_2,False,False) or bird_group.sprites()[0].rect.midtop[1] <=0 or bird_group.sprites()[0].rect.midbottom[1] >= HEIGHT :  
        return False
    else :
        return True
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

#Helper functions
def x_state() :
    return (x - bird_group.sprites()[0].rect.x) // 25

def y_state() :
    return (y - bird_group.sprites()[0].rect.y) // 25

def get_action() :
    if np.random.random() < epsilon :
        if Q_Table[(current_x_state,current_y_state,1)] > Q_Table[(current_x_state,current_y_state,0)] :
            return 1
        elif Q_Table[(current_x_state,current_y_state,1)] < Q_Table[(current_x_state,current_y_state,0)] :
            return 0
        else :
            return 0
    else :
        return 0
    
def terminal_state() :
    if reward == -1000 :
        return True
    else :
        return False
    
def get_reward() :
    i,j = 8,-1
    x = current_x_state
    y = current_y_state
    if check_collision(bird_group,pipe_group) == False :
        return -1000
    elif ((x == 0 or x == 1) and (y == 0 or y==1)) or ((x == 0 or x == 1) and (y == 6 or y == 7)) :
        return 50
    elif (x == 0 or x == 1) and (y == 2 or y == 3 or y == 4 or y == 5) :
        return 100
    elif (x >= 2) and (y == 2 or y == 3 or y == 4 or y == 5) :
        return 10
    elif ((x >= 2) and (y == 0 or y==1)) or ((x >= 2) and (y == 6 or y == 7)) :
        return 1
    while (i <= 27) :
        if ((x >= 2) and y == i) :
            return -10 * i
        i = i + 1
    while (j >= -20) :
        if (x >= 2) and y == j :
            return 10 * j 
        j = j - 1
    

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
Q_Table = {}

# Game Loop
while running :
    current_time = pygame.time.get_ticks() + 1400
    epsilon = 1                  # Can tune in these parameters for controlling the
    discount_factor = 0.8        # exploration and learning rate
    learning_rate = 0.5          
    jump = False
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
                running = False
    if current_time - last_pipe > 1400 and Active :      
        height = random.randint(350,550)                 
        topPipe = Pipe(525,height,False)
        downPipe = Pipe(525,height,True)
        pipe_group.add(topPipe)
        pipe_group.add(downPipe)
        last_pipe = current_time

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
    if pass_pipe == True and len(pipe_group) > 0 :
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score += 1
            pass_pipe = False
    if len(pipe_group) == 2 :
        x = pipe_group.sprites()[0].rect.midright[0]
        y = height

    if len(pipe_group) == 4 :
        x = pipe_group.sprites()[2].rect.midright[0]
        y = height


    screen.fill(BACKGROUND_COLOR)
    text = font.render(f'Score : {str(score)}',True,(0,0,0))
    bird.draw()
    pipe_group.draw(screen)
    if Active :
        bird_group.update()
        pipe_group.update()
    screen.blit(text,(100,30))
    pygame.display.update()
    clock.tick(60)
#-----------------------------------------------
    if current_time > 1600 :
        prev_x_state = current_x_state
        prev_y_state = current_y_state
        if bird_group.sprites()[0].vel <= - 3:
            prev_action_taken = 1
        else :
            prev_action_taken = 0

    current_x_state = x_state()
    current_y_state = y_state()
    if (current_x_state,current_y_state,0) not in Q_Table.keys() :
        Q_Table[(current_x_state,current_y_state,0)] = 0
    if (current_x_state,current_y_state,1) not in Q_Table.keys() :
        Q_Table[(current_x_state,current_y_state,1)] = 0


    reward = get_reward()
    # print(f'{current_x_state},{current_y_state}',{reward}) // for debugging 
    if current_time > 1600 :
        if prev_action_taken == 1 :
            action = 0
        else :
            action = get_action()
    else :
        action = get_action()
# Updating the Q-table based on the reward recieved
    if (current_time > 1600) and ((prev_action_taken == 0 and current_y_state < 8) or (current_y_state >= 8 and prev_action_taken == 1)) :
        old_Q_value = Q_Table[(prev_x_state,prev_y_state,prev_action_taken)]
        temporal_difference = reward + (discount_factor * max(Q_Table[(current_x_state,current_y_state,0)],Q_Table[(current_x_state,current_y_state,1)])) - old_Q_value
        new_Q_value = old_Q_value + (learning_rate * temporal_difference)
        Q_Table[(prev_x_state,prev_y_state,prev_action_taken)] = new_Q_value
    if terminal_state() :
        Active = False
    if action == 1 and not terminal_state() :
        jump = True


#-----------------------------------------------
#-----------------------------------------------------------
    bird.jump()
    Active = check_collision(bird_group,pipe_group)
# resetting the game once the bird dies
    if not Active :

        bird_group.sprites()[0].rect.center = (100,350)
        bird_group.sprites()[0].vel = 0
        score = 0
        pipe_group.empty()
        last_pipe = current_time - 1401
        Active = True


# for x in Q_Table.keys() :
#     print(f'State:{x}   Reward:{Q_Table[x]}')