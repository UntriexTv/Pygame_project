import pygame


def load_blok(blok, list, window, map_move, list_rig, height):              #loads casual block (dirt, grass, etc.)
    kolecko = 0
    rozdiel = height - 500
    try:
        for i in list:
            objekt = window.blit(blok, (list[kolecko][0] - map_move, list[kolecko][1] + rozdiel))
            list_rig.append(objekt)
            kolecko = kolecko + 1
    except:
        pass


def load_blok_dole(blok, zoznam, win, mapposun, zoznamrig, vyska):      #loads stairs down
    kolecko = 0
    rozdiel = vyska - 500
    try:
        for i in zoznam:
            win.blit(blok, (zoznam[kolecko][0] - mapposun, zoznam[kolecko][1] + rozdiel))
            x = zoznam[kolecko][0] - mapposun
            y = zoznam[kolecko][1] + rozdiel
            for i in range(16):
                rig = pygame.Rect(x + (2*i), y + (2*i), 2, 32 - (2*i))
                zoznamrig.append(rig)
            kolecko = kolecko + 1

    except:
        pass


def load_blok_hore(blok, zoznam, win, mapposun, zoznamrig, vyska):      #loads stairs up
    kolecko = 0
    rozdiel = vyska - 500
    try:
        for i in zoznam:
            win.blit(blok, (zoznam[kolecko][0] - mapposun, zoznam[kolecko][1] + rozdiel))
            x = zoznam[kolecko][0] - mapposun
            y = zoznam[kolecko][1] + rozdiel
            for i in range(16):
                rig = pygame.Rect(x + (2*i), y + 32 - (i*2), 2, i*2)
                zoznamrig.append(rig)
            kolecko = kolecko + 1

    except:
        pass
