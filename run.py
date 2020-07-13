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


def debug():
    def debug_variables():
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


def menu_settings():
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


def pause_variable():
    global paused, paused_timer
    if paused is True and 20 < paused_timer:
        paused = False
        paused_timer = 0
    elif paused is not True and 20 < paused_timer:
        paused_timer = 0
        paused = True


def load_map(map):
    global map_chosing, menu_running, map_dirt, map_dirt_up, map_dirt_down, map_grass, map_finish, map_spawn
    patch_to_map = str(pathlib.Path().absolute()) + nothing_special + "maps" + nothing_special + map + nothing_special
    try:
        with open(patch_to_map + "dirt.dat", 'rb') as fp:
            map_dirt = pickle.load(fp)
        with open(patch_to_map + "dirt_up.dat", 'rb') as fp:
            map_dirt_up = pickle.load(fp)
        with open(patch_to_map + "dirt_down.dat", 'rb') as fp:
            map_dirt_down = pickle.load(fp)
        with open(patch_to_map + "grass.dat", 'rb') as fp:
            map_grass = pickle.load(fp)
        with open(patch_to_map + "finish.dat", 'rb') as fp:
            map_finish = pickle.load(fp)
        with open(patch_to_map + "spawn.dat", 'rb') as fp:
            map_spawn = pickle.load(fp)
        fp.close()
    except:
        map_spawn = [50, 50]
    map_chosing = False
    menu_running = False


def chose_map():
    global map_chosing
    map_chosing = True
    time.sleep(1)
    def stop_map():
        global map_chosing
        map_chosing = False
    while map_chosing:
        pygame.time.delay(delay)
        win.fill((0, 0, 0))
        Gui_functions.message_display(win, "CHOSE MAP", width // 2, 50, 100, color=Gui_functions.white)
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
        list = os.listdir(str(pathlib.Path().absolute()) + nothing_special + "maps" + nothing_special)
        loop = 0
        for i in list:
            Gui_functions.button(win, i, width//2 - 50, 100 + loop *60, 100, 50, Gui_functions.bright_green,
                                 Gui_functions.green, action=partial(load_map, i))
            loop += 1
        Gui_functions.button(win, "exit", width - 150, height - 100, 100, 50, Gui_functions.bright_green,
                                 Gui_functions.green, action=stop_map)
        pygame.display.update()


def start_screen():
    if map_chosing is False:
        Gui_functions.message_display(win, "MENU", width // 2, 50, 100, color=Gui_functions.white)
        Gui_functions.button(win, "play", width//2 - 50, height//2 - 60, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=chose_map)
        Gui_functions.button(win, "settings", width // 2 - 50, height // 2, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=menu_settings)
        Gui_functions.button(win, "Exit", width // 2 - 50, height // 2 + 60, 100, 50, Gui_functions.bright_green,
                             Gui_functions.green, action=pygame.quit)



while menu_running:
    pygame.time.delay(delay)
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
    win.fill((0, 0, 0))
    start_screen()
    pygame.display.update()



try:
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
facing = "right"            #variable where is character facing will be used for animations

#lists for loading system
load_dirt = []
load_up = []
load_down = []
load_grass = []

#pause variables
paused = False
paused_timer = 0


def optimalization():
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
if debug_enable == 1:           # if is debug enabled in settings it will start
    t2.start()

while run:                                          # Main game loop
    pygame.time.delay(delay)                        #Sets delay between frames based on variable in settings
    paused_timer += 1                               #timer for pause function
    if down == 0 and isjump is False:               #function for falling
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
    if not paused:
        if keys[pygame.K_LEFT]:
            if left_down == 0:
                if x <= 100 and vel < map_move:
                    map_move -= vel
                elif x <= 0 and map_move == map_move < vel:
                    pass
                else:
                    x -= vel

            else:
                if stairs_left:
                    if x <= 100 and vel < map_move:
                        map_move -= vel
                    elif x <= 0 and map_move == map_move < vel:
                        pass
                    else:
                        x -= vel
                    y -= 3
            facing = "left"

        if keys[pygame.K_RIGHT]:
            if right_down == 0:
                if width - 100 <= x:
                    map_move += vel
                else:
                    x += vel
            else:
                if stairs_right:
                    if width - 100 <= x:
                        map_move += vel
                    else:
                        x += vel
                    y -= 3
            facing = "right"

        if keys[pygame.K_DOWN] and down == 0:
            y += vel

        if keys[pygame.K_SPACE]:
            if not isjump and down == 1:
                isjump = True
                jump_begining = True
                y_velocity = jump_speed

        if isjump:
            if up == 1 and 0 <= y_velocity:
                y_velocity = 0
            if jump_begining and down == 0:
                jump_begining = False
            if not jump_begining and down == 1:
                y_velocity = 0
                isjump = False
            if isjump:
                y -= y_velocity
                y_velocity -= gravitation
                if y_velocity <= 0:
                    isjump = False
                jump_begining = False
    if keys[pygame.K_ESCAPE] and 20 < paused_timer:
        if paused:
            paused = False
        else:
            paused = True
        paused_timer = 0

    win.fill((255, 255, 255))
    hrac = win.blit(player_texture, (int(x), int(y)))
    #guns.zbran(win, "pistol", x+16, y, strana, pistol)

    hrac_rig_d = pygame.Rect(int(x), int(y) + 5, 32, 32)
    hrac_rig_h = pygame.Rect(int(x), int(y) - 5, 32, 32)
    hrac_rig_p_h = pygame.Rect(int(x) + 5, int(y) - 10, 32, 32)
    hrac_rig_l_h = pygame.Rect(int(x) - 5, int(y) - 10, 32, 32)
    hrac_rig_p_d = pygame.Rect(int(x) + 5, int(y), 32, 32)
    hrac_rig_l_d = pygame.Rect(int(x) - 5, int(y), 32, 32)
    rig_list.clear()
    try:
        ciel = win.blit(finish, (int(map_finish[0]) - map_move, int(map_finish[1])))
    except:
        pass
    try:
        loading.load_blok(dirt, load_dirt, win, map_move, rig_list, height)
    except:
        pass
    try:
        loading.load_blok(dirt_grass, load_grass, win, map_move, rig_list, height)
    except:
        pass
    try:
        loading.load_blok_dole(dirt_down, load_down, win, map_move, rig_list, height)
    except:
        pass
    try:
        loading.load_blok_hore(dirt_up, load_up, win, map_move, rig_list, height)
    except:
        pass
    if paused:
        s = pygame.Surface((width, height))
        s.set_alpha(128)
        s.fill((255, 255, 255))
        win.blit(s, (0, 0))
        Gui_functions.message_display(win, "PAUSED", width // 2, 50, 100)
        Gui_functions.button(win, "resume", width//2 - 50, 150, 100, 40, Gui_functions.bright_green,
                             Gui_functions.green, action=pause_variable)
        Gui_functions.button(win, "Exit Game", width // 2 - 50, 210, 100, 40, Gui_functions.bright_green,
                             Gui_functions.green, action=pygame.quit)
    pygame.display.update()
    collision_test()
pygame.quit()