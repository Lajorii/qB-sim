import pygame as pg
from colors import HVIT, SORT, RØD, GRØNN, BLÅ
from klasser import Magnetfelt, Elektron, Proton
from tekstboks import info_boks
import time

# lag en timer som teller opp veldig sakte og bruk den tiden til å regne ut. Gang posisjonen med tusen for å få meter.
# Eventuelt ha en maks reell fart som skalerer farten til partiklen og bruker forholdet mellom farten til å regne ut passelig tid.

# basic stuff
lengde = 1000 # 1 meter
høyde = 700 # 0.7 meter

vindu_størrelse = (lengde, høyde)
pg.init()
clock = pg.time.Clock()
skjerm = pg.display.set_mode(size=vindu_størrelse)
FPS = 60

# deklarerer partikler og magnetfelt
e1 = Elektron(lengde/2+100, 200, 0.0001, 0.0001) # fart i m/s
p1 = Proton(lengde/2+100, 200, 1, 1) # fart i m/s
b1 = Magnetfelt(-0.3, 500, 500, 300, 100) # negativ for å få retning nedover

partikler = [e1, p1]
magnetfelt = [b1]


# løkke for å kjøre
kjører_programmet = True
while kjører_programmet:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            kjører_programmet = False
    skjerm.fill(HVIT)

    delta_tid = clock.get_time() / 1000  # seconds

    print(delta_tid)

    b1.tegn(skjerm)

    info_boks(skjerm, time.time(), partikler, magnetfelt)
    
    for particle in partikler:
        particle.oppdater_og_tegn(skjerm, b1, delta_tid, lengde, høyde)

    
    clock.tick(FPS)
    pg.display.update()

pg.quit()