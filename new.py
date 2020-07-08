import pygame, pickle, threading, time, os
import loading
import guns
import pathlib
settings = open("set.txt", "r")
settings.readline()
vyska = int(settings.readline().replace("vyska", ""))
sirka = int(settings.readline().replace("sirka ", ""))
delay = int(settings.readline().replace("delay_medzi_fps_ms ", ""))
vel = int(settings.readline().replace("rychlost ", ""))
pismo = settings.readline()
mapa = input("Chose map (default: mapa_new): ")
cesta_k_suboru = str(pathlib.Path().absolute()) + pismo + "mapy" + pismo + mapa + pismo
cesta_k_suboru = "../game/maps/mapa_new/"
try:
    with open(cesta_k_suboru + "dirt.dat", 'rb') as fp:
        mapa_dirt = pickle.load(fp)
    with open(cesta_k_suboru + "dirt_up.dat", 'rb') as fp:
        mapa_dirt_up = pickle.load(fp)
    with open(cesta_k_suboru + "dirt_down.dat", 'rb') as fp:
        mapa_dirt_down = pickle.load(fp)
    with open(cesta_k_suboru + "grass.dat", 'rb') as fp:
        mapa_grass = pickle.load(fp)
    with open(cesta_k_suboru + "finish.dat", 'rb') as fp:
        mapa_finish = pickle.load(fp)
    with open(cesta_k_suboru + "spawn.dat", 'rb') as fp:
        mapa_spawn = pickle.load(fp)
    fp.close()
except:
    mapa_spawn = [50, 50]

pygame.init()
win = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("First Game")

try:
    if sirka - 100 < mapa_spawn[0]:
        x = 50
        mapposun = mapa_spawn[0]-50
    else:
        mapposun = 0
        x = mapa_spawn[0]
    y = mapa_spawn[1]
except:
    mapposun = 0
    x = 50
    y = 50

width = 40
height = 60
isjump = False
y_velocity = 0
pad_velocity = 0
jumprychlost = 8
gravitacia = 0.4
run = True
inair = True
dirt = pygame.image.load('dirt.jpg')
dirt_down = pygame.image.load('dirt_down.png')
dirt_up = pygame.image.load("dirt_up.png")
dirt_grass = pygame.image.load("dirt_grass.png")
finish = pygame.image.load('finish.png')
hrac_texture = pygame.image.load(os.path.join('animations', 'adventurer-idle-00.png'))
naboj = pygame.image.load("naboj.png")
pistol = pygame.image.load("pistol.png")
#player_mask = pygame.mask.from_surface(dirt)
zoznamrig = []
schody_hore = []
schody_dole = []
pravo_h = 0
lavo_h = 0
dole = 0
hore = 0
pravo_d = 0
lavo_d = 0
vyhra = 0
pravo_schody = False
jump_zaciatok = False
lavo_schody = False
strana = "right"
load_dirt = []
load_up = []
load_down = []
load_grass = []


def optimalization():
    while True:
        for i in mapa_dirt:
            if mapposun - 140 < i[0] < sirka + mapposun + 140 and i not in load_dirt:
                load_dirt.append(i)
        for i in load_dirt:
            if not mapposun - 140 < i[0] < sirka + mapposun + 140:
                load_dirt.remove(i)
        for i in mapa_dirt_up:
            if mapposun - 140 < i[0] < sirka + mapposun + 140 and i not in load_up:
                load_up.append(i)
        for i in load_up:
            if not mapposun - 140 < i[0] < sirka + mapposun + 140:
                load_up.remove(i)
        for i in mapa_dirt_down:
            if mapposun - 140 < i[0] < sirka + mapposun + 140 and i not in load_down:
                load_down.append(i)
        for i in load_down:
            if not mapposun - 140 < i[0] < sirka + mapposun + 140:
                load_down.remove(i)
        for i in mapa_grass:
            if mapposun - 140 < i[0] < sirka + mapposun + 140 and i not in load_grass:
                load_grass.append(i)
        for i in load_grass:
            if not mapposun - 140 < i[0] < sirka + mapposun + 140:
                load_grass.remove(i)
        time.sleep(0.4)


def collision_test():
    global pravo_h, lavo_h, hore, lavo_d, pravo_schody, lavo_schody, pravo_d, dole, vyhra
    try:
        vyhra = hrac.colliderect(ciel)
    except:
        pass
    for i in zoznamrig:
        pravo_d = hrac_rig_p_d.colliderect(i)

        if pravo_d == 1:
            break

    for i in zoznamrig:
        lavo_d = hrac_rig_l_d.colliderect(i)
        if lavo_d == 1:
            break

    for i in zoznamrig:
        pravo_h = hrac_rig_p_h.colliderect(i)

        if pravo_h == 1:
            break

    for i in zoznamrig:
        lavo_h = hrac_rig_l_h.colliderect(i)
        if lavo_h == 1:
            break

    for i in zoznamrig:
        hore = hrac_rig_h.colliderect(i)
        if hore == 1:
            break

    for i in zoznamrig:
        dole = hrac_rig_d.colliderect(i)
        if dole == 1:
            break

    if lavo_d == 1 and lavo_h == 0:
        lavo_schody = True
    else:
        lavo_schody = False

    if pravo_d == 1 and pravo_h == 0:
        pravo_schody = True
    else:
        pravo_schody = False


t1 = threading.Thread(target=optimalization)
t1.start()

while run:
    pygame.time.delay(delay)
    if dole == 0 and isjump is False:
        y += pad_velocity
        pad_velocity += gravitacia
    else:
        pad_velocity = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    xmap = x + mapposun
    if keys[pygame.K_LEFT]:  # kontrola a posun dolava
        if lavo_d == 0:
            if x <= 100 and vel < mapposun:
                mapposun -= vel
            elif x <= 0 and mapposun == mapposun < vel:
                pass
            else:
                x -= vel

        else:
            if lavo_schody:
                if x <= 100 and vel < mapposun:
                    mapposun -= vel
                elif x <= 0 and mapposun == mapposun < vel:
                    pass
                else:
                    x -= vel
                y -= 5
        strana = "left"

    if keys[pygame.K_RIGHT]:  # kontrola a posun doprava
        if pravo_d == 0:
            if sirka - 100 <= x:
                mapposun += vel
            else:
                x += vel
        else:
            if pravo_schody:
                if sirka - 100 <= x:
                    mapposun += vel
                else:
                    x += vel
                y -= 5
        strana = "right"

    if keys[pygame.K_DOWN] and dole == 0:
        y += vel

    if keys[pygame.K_SPACE]:
        if not isjump:
            isjump = True
            jump_zaciatok = True
            y_velocity = jumprychlost

    if isjump:
        if hore == 1 and 0 <= y_velocity:
            y_velocity = 0
        if jump_zaciatok and dole == 0:
            jump_zaciatok = False
        if not jump_zaciatok and dole == 1:
            y_velocity = 0
            isjump = False
        if isjump:
            y -= y_velocity
            y_velocity -= gravitacia
            jump_zaciatok = False

    win.fill((255, 255, 255))
    hrac = win.blit(hrac_texture, (x, y))
    #zbrane.zbran(win, "pistol", x+16, y, strana, pistol)

    hrac_rig_d = pygame.Rect(x, y + 5, 32, 32)
    hrac_rig_h = pygame.Rect(x, y - 5, 32, 32)
    hrac_rig_p_h = pygame.Rect(x + 5, y - 10, 32, 32)
    hrac_rig_l_h = pygame.Rect(x - 5, y - 10, 32, 32)
    hrac_rig_p_d = pygame.Rect(x + 5, y, 32, 32)
    hrac_rig_l_d = pygame.Rect(x - 5, y, 32, 32)
    zoznamrig.clear()
    try:
        ciel = win.blit(finish, (int(mapa_finish[0]) - mapposun, int(mapa_finish[1])))
    except:
        pass
    try:
        loading.load_blok(dirt, load_dirt, win, mapposun, zoznamrig, vyska)
    except:
        pass
    try:
        loading.load_blok(dirt_grass, load_grass, win, mapposun, zoznamrig, vyska)
    except:
        pass
    try:
        loading.load_blok_dole(dirt_down, load_down, win, mapposun, zoznamrig, vyska)
    except:
        pass
    try:
        loading.load_blok_hore(dirt_up, load_up, win, mapposun, zoznamrig, vyska)
    except:
        pass
    pygame.display.update()
    collision_test()
    print("pravo: " + str(pravo_d) + " lavo: " + str(lavo_d) + " hore: " + str(hore) + " dole: " + str(dole) +
          " is jump: " + str(isjump))

pygame.quit()
