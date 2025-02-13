import pygame as pg
import pygame_widgets as pg_w
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from colors import HVIT, SORT, RØD, GRØNN, BLÅ
from klasser import Magnetfelt, Elektron, Proton
from tekstboks import vis_info

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
e1 = Elektron(600, 300, 0.01, 0)
p1 = Proton(0, 250, 0.005, 0) # fart i m/s
b1 = Magnetfelt(-0.00000001, 500, 300, 300, 100) # negativ for å få retning nedover

partikler = [e1, p1]
magnetfelt = [b1]

slider = Slider(skjerm,
                15, høyde-20, 300, 7,
                min=-6,
                max=0,
                step=0.001,
                initial=-6)
slider_output = TextBox(skjerm, 15, høyde-60, 210, 30, fontSize=20, borderThickness=1)
slider_output.disable()
medgått_tid = 0

class SimuleringStatus:
    def __init__(self):
        self.faktor = 1

    def bytt(self):
        self.faktor *= -1

tidsstatus = SimuleringStatus()

button = Button(
    skjerm, 
    400, høyde-50, 70, 20,  # Posisjon og størrelse
    text='Reverser tid',
    fontSize=10,
    inactiveColour=(200, 50, 0),
    hoverColour=(150, 0, 0),
    pressedColour=(0, 200, 20),
    onClick=tidsstatus.bytt # Pass function reference, not call it
)

# løkke for å kjøre
kjører_programmet = True
while kjører_programmet:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            kjører_programmet = False
    skjerm.fill(HVIT)

    tidsskala = 10**slider.getValue()
    slider_output.setText(f"Tidsskala: {tidsskala:.6f}")

    medgått_tid += tidsskala*(1/FPS) * tidsstatus.faktor

    # delta_tid = clock.get_time() / 1000  # seconds
    b1.tegn(skjerm)

    vis_info(skjerm, medgått_tid, partikler, magnetfelt)

    #info_boks(skjerm, time.time(), partikler, magnetfelt)
    
    for particle in partikler:
        particle.oppdater_og_tegn(skjerm, b1, 1/FPS, tidsskala, lengde, høyde, tidsstatus.faktor)

    
    clock.tick(FPS)

    pg_w.update(events)
    pg.display.update()

pg.quit()