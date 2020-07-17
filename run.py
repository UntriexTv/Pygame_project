import pygame, pickle, threading, time, os, pathlib, tkinter
import loading
import Gui_functions
from functools import partial
map_chosing = False
menu_running = True
settings_running = False

settings = open("set.txt", "r")                                             #Open file with settings variables
settings.readline()
height = int(settings.readline().replace("height ", ""))                    #Reads and define height of canvas from set.txt
width = int(settings.readline().replace("width ", ""))                      #Reads and define width of canvas form set.txt
delay = int(settings.readline().replace("delay_between_frames_ms ", ""))    #Reads and define delay between frames from set.txt
vel = int(settings.readline().replace("speed ", ""))                        #Reads and define velocity of player from set.txt
debug_enable = int(settings.readline().replace("debug_tool ", ""))          #Enables or disables debug (set.txt)
nothing_special = settings.readline()                                       #Reads one special character that i cant write there
settings.close()                                                            #Closes file with settoings (set.txt)
pygame.init()                                                               #initialization of pygame module
win = pygame.display.set_mode((width, height))                              #defines window of game with width and height
pygame.display.set_caption("Pygame")                                        #sets caption of window


def debug():                                                                #debug function (activate in set.txt debug_tool 1
    def debug_variables():                                                  #this is function to display variables in debug
        while True:
            try:
                canvas.delete("debug")
                canvas.create_text(40, 40, text="x: " + str(int(x)), tag="debug")
                canvas.create_text(40, 60, text="y: " + str(int(y)), tag="debug")
                canvas.create_text(40, 100, text="x: " + str(int(xmap)), tag="debug")
                canvas.create_text(40, 120, text="y: " + str(int(y)), tag="debug")
                canvas.update()
            except:
                pass
            time.sleep(0.25)
    canvas = tkinter.Canvas(height= 600, width=400)
    canvas.pack()
    canvas.create_text(85, 25, text="COORDINATES ON CANVAS:")
    canvas.create_text(85, 85, text="COORDINATES ON MAP:")
    debug_variables()
    canvas.mainloop()


def menu_settings():                                                        #settings. For now only displays values of settings
    def stop_settings():
        global settings_running
        settings_running = False
    global settings_running
    settings_running = True
    while settings_running:
        pygame.time.delay(delay)
        win.fill((0, 0, 0))
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
        Gui_functions.message_display(win, "SETTINGS", width//2, 50, 100, color=Gui_functions.white)
        Gui_functions.message_display(win, "Height: ", 50, 125, 25, color=Gui_functions.white)
        Gui_functions.message_display(win, str(height), 200, 125, 25, color=Gui_functions.white)
        Gui_functions.message_display(win, "Widht: ", 50, 175, 25, color=Gui_functions.white)
        Gui_functions.message_display(win, str(width), 200, 175, 25, color=Gui_functions.white)
        Gui_functions.message_display(win, "Delay: ", 50, 225, 25, color=Gui_functions.white)
        Gui_functions.message_display(win, str(delay) + " MS", 200, 225, 25, color=Gui_functions.white)
        Gui_functions.button(win, "exit", width - 150, height - 100, 100, 50, Gui_functions.bright_green,
                                 Gui_functions.green, action=stop_settings)
        pygame.display.update()


def pause_variable():                                                       #Changes states of pause variable
    global paused, paused_timer
    if paused is True and 20 < paused_timer:                                #if paused and loop goes 20 times unpause
        paused = False
        paused_timer = 0
    elif paused is not True and 20 < paused_timer:                          #if unpaused and loop goes 20 times unpause
        paused_timer = 0
        paused = True


def load_map(map):                                                          #loading map variables from bin files
    global map_chosing, menu_running, map_dirt, map_dirt_up, map_dirt_down, map_grass, map_finish, map_spawn
    patch_to_map = str(pathlib.Path().absolute()) + nothing_special + "maps" + nothing_special + map + nothing_special
    try:
        with open(patch_to_map + "dirt.dat", 'rb') as fp:                   #loads dirt variables
            map_dirt = pickle.load(fp)
        with open(patch_to_map + "dirt_up.dat", 'rb') as fp:
            map_dirt_up = pickle.load(fp)                                   #loads stairs up
        with open(patch_to_map + "dirt_down.dat", 'rb') as fp:
            map_dirt_down = pickle.load(fp)                                 #loads stairs down
        with open(patch_to_map + "grass.dat", 'rb') as fp:
            map_grass = pickle.load(fp)                                     #loads grass
        with open(patch_to_map + "finish.dat", 'rb') as fp:
            map_finish = pickle.load(fp)                                    #loads finish
        with open(patch_to_map + "spawn.dat", 'rb') as fp:
            map_spawn = pickle.load(fp)                                     #loads spawn point of player
        fp.close()
    except:                                                                 #if error spawn player at x=50 y=50
        map_spawn = [50, 50]
    map_chosing = False                                                     #variables for smoother menu
    menu_running = False


def chose_map():                                                            #function in menu to chose map
    global map_chosing
    map_chosing = True                                                      #variable because of menu
    time.sleep(1)                                                           #sleep because some bugs that ocured
    def stop_map():                                                         #exit map chose menu
        global map_chosing
        map_chosing = False
    while map_chosing:
        pygame.time.delay(delay)                                            #delay between frames
        win.fill((0, 0, 0))                                                 #fill window with black (R,G,B)
        Gui_functions.message_display(win, "CHOSE MAP", width // 2, 50, 100, color=Gui_functions.white)  #Text chose map
        for evt in pygame.event.get():                                      #if exited pygame window break run loop and exit
            if evt.type == pygame.QUIT:
                pygame.quit()
        list = os.listdir(str(pathlib.Path().absolute()) + nothing_special + "maps" + nothing_special) #makes list of maps
        loop = 0
        for i in list:                                                      #creates button of maps
            Gui_functions.button(win, i, width//2 - 50, 100 + loop *60, 100, 50, Gui_functions.bright_green,
                                 Gui_functions.green, action=partial(load_map, i))  #maps button
            loop += 1
        Gui_functions.button(win, "exit", width - 150, height - 100, 100, 50, Gui_functions.bright_green,
                                 Gui_functions.green, action=stop_map)      #exit button
        pygame.display.update()                                             #pygame display update function


def start_screen():                                                         #Main menu
    if map_chosing is False:
        Gui_functions.message_display(win, "MENU", width // 2, 50, 100, color=Gui_functions.white)  #text MENU
        Gui_functions.button(win, "play", width//2 - 50, height//2 - 60, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=chose_map)         #button to chose map
        Gui_functions.button(win, "settings", width // 2 - 50, height // 2, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=menu_settings)     #button to go to settings
        Gui_functions.button(win, "Exit", width // 2 - 50, height // 2 + 60, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=pygame.quit)       #button to exit game



while menu_running:                                                         #main menu loop
    pygame.time.delay(delay)
    for evt in pygame.event.get():                                          #if exited pygame window break loop
        if evt.type == pygame.QUIT:
            pygame.quit()
    win.fill((0, 0, 0))                                                     #fill screen with black (R,G,B)
    start_screen()                                                          #call main menu
    pygame.display.update()                                                 #pygame display update function



try:                                                                        #player spawning into window
    if width - 100 < map_spawn[0]:
        x = 50
        map_move = map_spawn[0] - 50
    else:
        map_move = 0
        x = map_spawn[0]
    y = map_spawn[1]
except:
    map_move = 0
    x = 50
    y = 50

isjump = False                                      #variable needed for jump mechanics
y_velocity = 0
fall_velocity = 0
max_fall_velocity = 5                               #Max speed for falling player
jump_speed = 8                                      #speed of jump
gravitation = 0.4                                   #gravitation needed for falls and jumps
run = True                                          #dont change variable of main loop
inair = True                                        #variable if is character in air
#Loads textures
dirt = pygame.image.load('dirt.jpg')
dirt_down = pygame.image.load('dirt_down.png')
dirt_up = pygame.image.load("dirt_up.png")
dirt_grass = pygame.image.load("dirt_grass.png")
finish = pygame.image.load('finish.png')
player_texture = pygame.image.load(os.path.join('animations', 'adventurer-idle-00.png'))
#charge = pygame.image.load("naboj.png")
#pistol = pygame.image.load("pistol.png")
#player_mask = pygame.mask.from_surface(dirt)

#Lists for colision system
rig_list = []
stairs_up = []
stairs_down = []
right_up = 0
left_up = 0
down = 0
up = 0
right_down = 0
left_down = 0
player_wins = 0
stairs_right = False
jump_begining = False
stairs_left = False
##################
facing = "right"            #variable where is character facing will be used in future for animations

#lists for loading system
load_dirt = []
load_up = []
load_down = []
load_grass = []

#pause variables
paused = False
paused_timer = 0


def optimalization():
    #optimilize game by removing blocks out of the screen from load list and adding block that are on screen
    while True:
        for i in map_dirt:
            if map_move - 140 < i[0] < width + map_move + 140 and i not in load_dirt:
                load_dirt.append(i)
        for i in load_dirt:
            if not map_move - 140 < i[0] < width + map_move + 140:
                load_dirt.remove(i)
        for i in map_dirt_up:
            if map_move - 140 < i[0] < width + map_move + 140 and i not in load_up:
                load_up.append(i)
        for i in load_up:
            if not map_move - 140 < i[0] < width + map_move + 140:
                load_up.remove(i)
        for i in map_dirt_down:
            if map_move - 140 < i[0] < width + map_move + 140 and i not in load_down:
                load_down.append(i)
        for i in load_down:
            if not map_move - 140 < i[0] < width + map_move + 140:
                load_down.remove(i)
        for i in map_grass:
            if map_move - 140 < i[0] < width + map_move + 140 and i not in load_grass:
                load_grass.append(i)
        for i in load_grass:
            if not map_move - 140 < i[0] < width + map_move + 140:
                load_grass.remove(i)
        time.sleep(0.4)


def collision_test():
    #test collisions by using pygame collision function and unvisible copies of player
    global right_up, left_up, up, left_down, stairs_right, stairs_left, right_down, down, player_wins
    try:
        player_wins = hrac.colliderect(ciel)
    except:
        pass
    for i in rig_list:
        right_down = hrac_rig_p_d.colliderect(i)

        if right_down == 1:
            break

    for i in rig_list:
        left_down = hrac_rig_l_d.colliderect(i)
        if left_down == 1:
            break

    for i in rig_list:
        right_up = hrac_rig_p_h.colliderect(i)

        if right_up == 1:
            break

    for i in rig_list:
        left_up = hrac_rig_l_h.colliderect(i)
        if left_up == 1:
            break

    for i in rig_list:
        up = hrac_rig_h.colliderect(i)
        if up == 1:
            break

    for i in rig_list:
        down = hrac_rig_d.colliderect(i)
        if down == 1:
            break

    if left_down == 1 and left_up == 0:
        stairs_left = True
    else:
        stairs_left = False

    if right_down == 1 and right_up == 0:
        stairs_right = True
    else:
        stairs_right = False


# defines and starts threads for optimalization and debug if its enabled
t1 = threading.Thread(target=optimalization)
t2 = threading.Thread(target=debug)
t2.daemon = True
t1.daemon = True
t1.start()
if debug_enable == 1:           # if is debug enabled in settings it will start debug thread
    t2.start()

while run:                                          # Main game loop
    pygame.time.delay(delay)                        #Sets delay between frames based on variable in settings
    paused_timer += 1                               #timer for pause function
    if down == 0 and isjump is False:               #function for falling if nothing is under player
        y += fall_velocity
        if fall_velocity <= max_fall_velocity:
            fall_velocity += gravitation
    else:
        fall_velocity = 0
    for event in pygame.event.get():                #kills loop if canvas is closed
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()                 #variable of all keys pressed
    xmap = x + map_move                             #x position on map
    if not paused:                                  #checks for inputs if not paused
        if keys[pygame.K_LEFT]:                     #go left function
            if left_down == 0:
                if x <= 100 and vel < map_move:     #if player is close to edge move camera
                    map_move -= vel
                elif x <= 0 and map_move == map_move < vel:
                    pass
                else:
                    x -= vel

            else:                               #function for stairs
                if stairs_left:
                    if x <= 100 and vel < map_move:
                        map_move -= vel
                    elif x <= 0 and map_move == map_move < vel:
                        pass
                    else:
                        x -= vel
                    y -= 3
            facing = "left"                     #sets facing to left

        if keys[pygame.K_RIGHT]:                #function to go right
            if right_down == 0:
                if width - 100 <= x:            #if player is close to edge move camera
                    map_move += vel
                else:
                    x += vel
            else:
                if stairs_right:                #function for stairs
                    if width - 100 <= x:
                        map_move += vel
                    else:
                        x += vel
                    y -= 3
            facing = "right"

        #if keys[pygame.K_DOWN] and down == 0: #unused function to go down
        #    y += vel

        if keys[pygame.K_SPACE]:            #if space is pressed start jump
            if not isjump and down == 1:
                isjump = True
                jump_begining = True
                y_velocity = jump_speed

        if isjump:
            if up == 1 and 0 <= y_velocity:     #if object over player stop jumping
                y_velocity = 0
            if jump_begining and down == 0:     #if jump is begining and nothing is under player stop begining jump (because of bug)
                jump_begining = False
            if isjump:
                y -= y_velocity                 #changes y based on set velocity
                y_velocity -= gravitation       #slovs velocity by gravitation
                if y_velocity <= 0:             #if player is on top of jump stop jumping and use function for falling
                    isjump = False
    if keys[pygame.K_ESCAPE] and 20 < paused_timer:
        pause_variable()

    win.fill((255, 255, 255))                   #fill window with white (R,G,B)
    hrac = win.blit(player_texture, (int(x), int(y)))           #blit player on screen
    #make unvisible copies of player for colision detection
    hrac_rig_d = pygame.Rect(int(x), int(y) + 5, 32, 32)        #down
    hrac_rig_h = pygame.Rect(int(x), int(y) - 5, 32, 32)        #up
    hrac_rig_p_h = pygame.Rect(int(x) + 5, int(y) - 10, 32, 32) #right up
    hrac_rig_l_h = pygame.Rect(int(x) - 5, int(y) - 10, 32, 32) #left up
    hrac_rig_p_d = pygame.Rect(int(x) + 5, int(y), 32, 32)      #right down
    hrac_rig_l_d = pygame.Rect(int(x) - 5, int(y), 32, 32)      #left down
    rig_list.clear()                                            #clear rig list
    try:
        ciel = win.blit(finish, (int(map_finish[0]) - map_move, int(map_finish[1])))    #blit finish on screen
    except:
        pass
    try:
        loading.load_blok(dirt, load_dirt, win, map_move, rig_list, height)             #load all dirt blocks
    except:
        pass
    try:
        loading.load_blok(dirt_grass, load_grass, win, map_move, rig_list, height)      #load all grass block
    except:
        pass
    try:
        loading.load_blok_dole(dirt_down, load_down, win, map_move, rig_list, height)   #load all stairs down
    except:
        pass
    try:
        loading.load_blok_hore(dirt_up, load_up, win, map_move, rig_list, height)       #load all stairs up
    except:
        pass
    if paused:                                                                          #pause menu
        #make darker screen (maybe will be as function in future
        s = pygame.Surface((width, height))
        s.set_alpha(128)
        s.fill((255, 255, 255))
        win.blit(s, (0, 0))
        ##################
        Gui_functions.message_display(win, "PAUSED", width // 2, 50, 100)               #pause text
        Gui_functions.button(win, "resume", width//2 - 50, 150, 100, 40, Gui_functions.bright_green,
                             Gui_functions.green, action=pause_variable)                #resume button
        Gui_functions.button(win, "Exit Game", width // 2 - 50, 210, 100, 40, Gui_functions.bright_green,
                             Gui_functions.green, action=pygame.quit)                   #exit game button
    pygame.display.update()                                                             #update screen pygame function
    collision_test()                                                                    #make collision test
pygame.quit()                                                                           #if out of run loop quit