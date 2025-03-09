from konstanter_og_variabler import *
import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LSHIFT
import pygame_widgets as pg_w # for å oppdatere widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from colors import *
from klasser_og_funksjoner import Magnetfelt, Elektron, Proton, draw_arrow
import numpy as np
import math

class Simulator:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.skjerm = pg.display.set_mode(size=(lengde, høyde))

        self.partikler = []

        self.alle_magnetfelt = []

        # UI elementer
        self.slider = Slider(self.skjerm, 15, høyde-20, 300, 7, min=-11, max=0.301029996, step=0.001, initial=-11)
        self.slider_output = TextBox(self.skjerm, 15, høyde-60, 210, 30, fontSize=20, borderThickness=1)
        self.slider_output.disable() # kan ikke skrive i tekstboks
        
        self.tidsstatus = 1
        self.reverser_tid_knapp = Button(self.skjerm, 330, høyde-35, 90, 30, text='Reverser tid', fontSize=15,
                             inactiveColour=(200, 200, 200), hoverColour=(230, 230, 230),
                             pressedColour=(150, 150, 150), onClick=self.bytt_tidsretning)
        
        self.kill_status_knapp = Button(self.skjerm, 430, høyde-35, 210, 30, text='Fjerner partikler utenfor skjerm', fontSize=15,
                             inactiveColour=RØD, hoverColour=LYSEGRØNN,
                             pressedColour=LYSERØD, onClick=self.endre_kill_status)
    
        # simuleringsvariabler
        self.medgått_tid = 0
        self.kjører_programmet = True
        self.er_pauset = False
        self.skal_lage_magnetfelt = False
        self.klar_for_magnetfelt = False
        self.magnet_start_posisjon_x, self.magnet_start_posisjon_y = None, None
        self.nytt_magnetfelt = None
        self.bredde_magnetfelt, self.høyde_magnetfelt = None, None
        self.skal_flytte_partikkel = False
        self.styrke_nytt_magnetfelt = 0.00005  # start-styrken til nye magnetfelt

        self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y = None, None
        self.skal_lage_partikkel = False
        self.skal_lage_proton = False
        self.skal_lage_elektron = False
        self.ny_partikkel = None
        self.temp_pil = None

        self.kill_utenfor_skjerm = False

    def bytt_tidsretning(self):
        self.tidsstatus *= -1

    def endre_kill_status(self):
        if not self.kill_utenfor_skjerm:
            self.kill_status_knapp.inactiveColour = GRØNN
            self.kill_status_knapp.hoverColour = LYSERØD
            self.kill_status_knapp.hoverColour = LYSEGRØNN

        else:
            self.kill_status_knapp.inactiveColour = RØD
            self.kill_status_knapp.hoverColour = LYSEGRØNN
            self.kill_status_knapp.hoverColour = LYSERØD

        self.kill_utenfor_skjerm = not self.kill_utenfor_skjerm

    def handle_events(self, events):
        keys_pressed = pg.key.get_pressed()

        for event in events:
            # print(f"EVENT: {event}")

            if event.type == pg.QUIT:
                self.kjører_programmet = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m: # sier at nå skal vi lage magnetfelt
                    self.skal_lage_magnetfelt = not self.skal_lage_magnetfelt
                elif event.key == pg.K_RIGHT:
                    self.styrke_nytt_magnetfelt *= -1
                elif event.key == pg.K_BACKSPACE:
                    if keys_pressed[K_LSHIFT]:
                        if self.partikler:
                            self.partikler.pop(0)
                    else:
                        if self.alle_magnetfelt:
                            self.alle_magnetfelt.pop()
                elif event.key == pg.K_SPACE:
                    self.er_pauset = not self.er_pauset

                elif event.key == pg.K_p:
                    if not self.skal_lage_proton:
                        self.skal_lage_partikkel = True
                        self.skal_lage_proton = True
                        self.skal_lage_elektron = False
                    else:
                        self.skal_lage_partikkel = False
                        self.skal_lage_proton = False

                elif event.key == pg.K_e:
                    if not self.skal_lage_elektron:
                        self.skal_lage_partikkel = True
                        self.skal_lage_proton = False
                        self.skal_lage_elektron = True
                    else:
                        self.skal_lage_partikkel = False
                        self.skal_lage_elektron = False

            if self.skal_lage_magnetfelt:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # sjekker at det er venstre museklikk
                    self.magnet_start_posisjon_x, self.magnet_start_posisjon_y = pg.mouse.get_pos()
                    self.klar_for_magnetfelt = True
                    self.bredde_magnetfelt, self.høyde_magnetfelt = 0, 0

                elif event.type == pg.MOUSEMOTION and self.klar_for_magnetfelt:
                    mus_x, mus_y = pg.mouse.get_pos()
                    self.bredde_magnetfelt = abs(mus_x - self.magnet_start_posisjon_x)
                    self.høyde_magnetfelt = abs(mus_y - self.magnet_start_posisjon_y)

                    # tegner midlertidig magnetfelt
                    if self.bredde_magnetfelt > 0 and self.høyde_magnetfelt > 0:
                        self.nytt_magnetfelt = Magnetfelt(self.styrke_nytt_magnetfelt, self.bredde_magnetfelt, self.høyde_magnetfelt, 
                                                          self.magnet_start_posisjon_x, self.magnet_start_posisjon_y, farge=LYSEGRØNN)

                elif event.type == pg.MOUSEBUTTONUP and self.nytt_magnetfelt:
                    # legger til permanent magnetfelt
                    self.alle_magnetfelt.append(Magnetfelt(self.styrke_nytt_magnetfelt, self.bredde_magnetfelt, self.høyde_magnetfelt, 
                                                           self.magnet_start_posisjon_x, self.magnet_start_posisjon_y, farge=GRØNN))
                    self.nytt_magnetfelt = None
                    self.skal_lage_magnetfelt, self.klar_for_magnetfelt = False, False

            elif self.skal_lage_partikkel:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y = pg.mouse.get_pos()
                    if self.partikkel_start_posisjon_x < 500 and self.partikkel_start_posisjon_y > høyde-60:
                        return
                    
                    if self.skal_lage_proton:
                        self.ny_partikkel = Proton(self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y, 0, 0, farge=LYSERØD)
                    else:
                        self.ny_partikkel = Elektron(self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y, 0, 0, farge=LYSEBLÅ)

                    self.temp_pil = None

                elif event.type == pg.MOUSEMOTION and self.partikkel_start_posisjon_x:
                    slutt_pos = np.array(pg.mouse.get_pos())
                    start_pos = np.array([self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y])

                    ny_slutt_pos = 2 * start_pos - slutt_pos

                    start_pos = pg.Vector2(tuple(start_pos))
                    ny_slutt_pos = pg.Vector2(tuple(ny_slutt_pos))

                    self.temp_pil = (self.skjerm, start_pos, ny_slutt_pos, LYSEGRÅ)


                elif event.type == pg.MOUSEBUTTONUP:
                    if self.partikkel_start_posisjon_x < 500 and self.partikkel_start_posisjon_y > høyde-60:
                        return
                    slutt_x, slutt_y = pg.mouse.get_pos()
                    
                    dx = self.partikkel_start_posisjon_x - slutt_x
                    dy = self.partikkel_start_posisjon_y - slutt_y

                    temp_vektor = np.array([dx, dy])

                    fart = np.linalg.norm(temp_vektor)
                    temp_vektor = (temp_vektor/fart) * 0.0016*fart**2.9873 # magisk forhold jeg fant med geogebra

                    if np.linalg.norm(temp_vektor) > 1:
                        if self.skal_lage_elektron:
                            partikkel = Elektron(self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y, temp_vektor[0], temp_vektor[1])
                        else:
                            partikkel = Proton(self.partikkel_start_posisjon_x, self.partikkel_start_posisjon_y, temp_vektor[0], temp_vektor[1])
                        
                        self.partikler.append(partikkel)
                        
                        self.ny_partikkel = None
                        self.temp_pil = None

            
            elif event.type == pg.MOUSEBUTTONDOWN and self.er_pauset and self.skal_flytte_partikkel == False:
                self.skal_flytte_partikkel = True
                x, y = event.pos
                for partikkel in self.partikler:
                    if math.sqrt((x - partikkel.pos[0]) ** 2 + (y - partikkel.pos[1]) ** 2) <= partikkel.radius:
                        partikkel.skal_flyttes = True

            elif event.type == pg.MOUSEBUTTONUP and self.er_pauset:
                for partikkel in self.partikler:
                    partikkel.skal_flyttes = False

                self.skal_flytte_partikkel = False

            elif event.type == pg.MOUSEMOTION and self.er_pauset and self.skal_flytte_partikkel:
                x, y  = event.pos
                for partikkel in self.partikler:
                    if partikkel.skal_flyttes:
                        partikkel.pos[0] = x
                        partikkel.pos[1] = y


    def vis_info(self):
        font = pg.font.Font(None, 18)
        info_tekst = f"Tid: {self.medgått_tid:.12f} s\n".rstrip('0').rstrip('.')

        info_tekst += "Partikler:\n"

        for i, partikkel in enumerate(self.partikler):
            info_tekst += f" {i+1}:     Type: {partikkel.__class__.__name__},  v = {np.linalg.norm(partikkel.v):.6} m/s\n"

        info_tekst += f"Styrke på nytt magnetfelt: {self.styrke_nytt_magnetfelt:.5}"

        lines = info_tekst.split("\n")
        y_offset = 10

        for line in lines:
            if line.strip():
                tekst = font.render(line, True, (0, 0, 0))
                self.skjerm.blit(tekst, (10, y_offset))
                y_offset += 15

    def run(self):
        while self.kjører_programmet:
            self.skjerm.fill(HVIT)
            events = pg.event.get()
            self.handle_events(events) 

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[K_UP]:
                self.styrke_nytt_magnetfelt *= 1.05
            elif keys_pressed[K_DOWN]:
                self.styrke_nytt_magnetfelt /= 1.05

            for magnetfelt in self.alle_magnetfelt:
                magnetfelt.tegn(self.skjerm)

            if self.nytt_magnetfelt:
                self.nytt_magnetfelt.tegn(self.skjerm)

            if self.ny_partikkel:
                if self.temp_pil:
                    draw_arrow(*self.temp_pil)

                self.ny_partikkel.tegn_midlertidig(self.skjerm)

            tidsskala = 10**self.slider.getValue()
            self.slider_output.setText(f"Tidsskala: {tidsskala:.8f}")

            if self.kill_utenfor_skjerm:
                for partikkel in self.partikler:
                    if partikkel.pos[0] < 0 or partikkel.pos[0] > lengde or partikkel.pos[1] < 0 or partikkel.pos[1] > høyde:
                        self.partikler.remove(partikkel)

            self.vis_info()

            if not self.er_pauset:
                self.medgått_tid += tidsskala * (1 / FPS) * self.tidsstatus

            for particle in self.partikler:
                for magnetfelt in self.alle_magnetfelt or [None]:
                    particle.oppdater_og_tegn(self.skjerm, magnetfelt, 1 / FPS, tidsskala, lengde, høyde, self.tidsstatus, self.er_pauset)

            self.clock.tick(FPS)
            pg_w.update(events) # oppdaterer importe widgets som sliders
            pg.display.update()

        pg.quit()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()