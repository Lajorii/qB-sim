import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LSHIFT
import pygame_widgets as pg_w
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from colors import HVIT, SORT, RØD, GRØNN, BLÅ, LYSEGRØNN
from klasser import Magnetfelt, Elektron, Proton
from tekstboks import vis_info

# basic stuff
lengde = 1000 # 1 meter
høyde = 700 # 0.7 meter

vindu_størrelse = (lengde, høyde)
pg.init()
clock = pg.time.Clock()
skjerm = pg.display.set_mode(size=vindu_størrelse)
FPS = 60

# deklarerer partikler og magnetfelt

b1 = Magnetfelt(-0.00001, 500, 500, 100, 100, farge=GRØNN)
e1 = Elektron(600, 300, 3e6, 0)
p1 = Proton(0, 250, 3e5, 0) # fart i m/s

partikler = [e1, p1]
alle_magnetfelt = []

slider = Slider(skjerm,
                15, høyde-20, 300, 7,
                min=-11,
                max=0.301029996, # log(10, 2)
                step=0.001,
                initial=-11)
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
    330, høyde-35, 90, 30,  # Posisjon og størrelse
    text='Reverser tid',
    fontSize=15,
    inactiveColour=(200, 200, 200),
    hoverColour=(230, 230, 230),
    pressedColour=(150, 150, 150),
    onClick=tidsstatus.bytt # funksjon referanse
)

skal_lage_magnetfelt = False
klar_for_magnetfelt = False
start_posisjon_x, start_posisjon_y = None, None
nytt_magnetfelt = None

styrke = 0.00005

kjører_programmet = True
er_pauset = False
while kjører_programmet:
    skjerm.fill(HVIT)

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[K_UP]:
        styrke *= 1.05
    elif keys_pressed[K_DOWN]:
        styrke *= .95

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            kjører_programmet = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                if not skal_lage_magnetfelt:
                    skal_lage_magnetfelt = True
                else:
                    skal_lage_magnetfelt = False

            elif event.key == pg.K_RIGHT:
                styrke *= -1

            elif event.key == pg.K_BACKSPACE:
                if keys_pressed[K_LSHIFT]:
                    if len(partikler) > 0:
                        partikler.pop(0)
                else:
                    if len(alle_magnetfelt) > 0:
                        alle_magnetfelt.pop()

            elif event.key == pg.K_SPACE:
                er_pauset = not er_pauset

        if skal_lage_magnetfelt:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_posisjon_x, start_posisjon_y = pg.mouse.get_pos()
                    klar_for_magnetfelt = True

            elif event.type == pg.MOUSEMOTION and klar_for_magnetfelt:
                mus_x, mus_y = pg.mouse.get_pos()
                bredde = abs(mus_x - start_posisjon_x)
                høyde = abs(mus_y - start_posisjon_y)

                if bredde > 0 and høyde > 0:
                    nytt_magnetfelt = Magnetfelt(
                        styrke, bredde, høyde, start_posisjon_x, start_posisjon_y, farge=LYSEGRØNN
                    )

            elif event.type == pg.MOUSEBUTTONUP and nytt_magnetfelt:
                alle_magnetfelt.append(Magnetfelt(
                        styrke, bredde, høyde, start_posisjon_x, start_posisjon_y, farge=GRØNN
                    ))
                nytt_magnetfelt = None
                skal_lage_magnetfelt = False
                klar_for_magnetfelt = False

    if nytt_magnetfelt is not None:
        nytt_magnetfelt.tegn(skjerm)

    tidsskala = 10**slider.getValue()
    slider_output.setText(f"Tidsskala: {tidsskala:.8f}")

    for magnetfelt in alle_magnetfelt:
        magnetfelt.tegn(skjerm)

    vis_info(skjerm, medgått_tid, partikler, alle_magnetfelt, styrke)
    
    if not er_pauset:
        medgått_tid += tidsskala*(1/FPS) * tidsstatus.faktor
        
    for particle in partikler:
        if len(alle_magnetfelt) > 0:
            for magnetfelt in alle_magnetfelt:
                particle.oppdater_og_tegn(skjerm, magnetfelt, 1/FPS, tidsskala, lengde, høyde, tidsstatus.faktor, er_pauset)
        else:
            particle.oppdater_og_tegn(skjerm, None, 1/FPS, tidsskala, lengde, høyde, tidsstatus.faktor, er_pauset)

    clock.tick(FPS)

    pg_w.update(events)
    pg.display.update()

pg.quit()