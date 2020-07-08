import pygame, pickle, threading, time, os
import loading
import guns
import pathlib
settings = open("set.txt", "r")
settings.readline()
height = int(settings.readline().replace("height ", ""))
width = int(settings.readline().replace("width ", ""))
delay = int(settings.readline().replace("delay_between_frames_ms ", ""))
vel = int(settings.readline().replace("speed ", ""))
nothing_special = settings.readline()
mapa = input("Chose map (default: mapa_new): ")
patch_to_map = str(pathlib.Path().absolute()) + nothing_special + "maps" + nothing_special + mapa + nothing_special
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

pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame")

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

isjump = False
y_velocity = 0
fall_velocity = 0
jump_speed = 8
gravitation = 0.4
run = True
inair = True
dirt = pygame.image.load('dirt.jpg')
dirt_down = pygame.image.load('dirt_down.png')
dirt_up = pygame.image.load("dirt_up.png")
dirt_grass = pygame.image.load("dirt_grass.png")
finish = pygame.image.load('finish.png')
player_texture = pygame.image.load(os.path.join('animations', 'adventurer-idle-00.png'))
charge = pygame.image.load("naboj.png")
pistol = pygame.image.load("pistol.png")
#player_mask = pygame.mask.from_surface(dirt)
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
facing = "right"
load_dirt = []
load_up = []
load_down = []
load_grass = []


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


t1 = threading.Thread(target=optimalization)
t1.start()

while run:
    pygame.time.delay(delay)
    if down == 0 and isjump is False:
        y += fall_velocity
        fall_velocity += gravitation
    else:
        fall_velocity = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    xmap = x + map_move
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
                y -= 5
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
                y -= 5
        facing = "right"

    if keys[pygame.K_DOWN] and down == 0:
        y += vel

    if keys[pygame.K_SPACE]:
        if not isjump:
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
            jump_begining = False

    win.fill((255, 255, 255))
    hrac = win.blit(player_texture, (x, y))
    #guns.zbran(win, "pistol", x+16, y, strana, pistol)

    hrac_rig_d = pygame.Rect(x, y + 5, 32, 32)
    hrac_rig_h = pygame.Rect(x, y - 5, 32, 32)
    hrac_rig_p_h = pygame.Rect(x + 5, y - 10, 32, 32)
    hrac_rig_l_h = pygame.Rect(x - 5, y - 10, 32, 32)
    hrac_rig_p_d = pygame.Rect(x + 5, y, 32, 32)
    hrac_rig_l_d = pygame.Rect(x - 5, y, 32, 32)
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
    pygame.display.update()
    collision_test()
    print("pravo: " + str(right_down) + " lavo: " + str(left_down) + " hore: " + str(up) + " dole: " + str(down) +
          " is jump: " + str(isjump))

pygame.quit()
