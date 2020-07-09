import pygame

red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
black = (0,0,0)
white = (255,255,255)


def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(display, text, x, y, height, font="comicsansms", color=black):
    largeText = pygame.font.SysFont(font,height)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((x),(y))
    display.blit(TextSurf, TextRect)


def button(display, msg,x,y,w,h,ic,ac,action=None, font="comicsansms", height=20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))

    try:
        smallText = pygame.font.SysFont(font,height)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        display.blit(textSurf, textRect)
    except:
        pass