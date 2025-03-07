from konstanter_og_variabler import *
import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LSHIFT
import pygame_widgets as pg_w # for å oppdatere widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from colors import *
from klasser import Magnetfelt, Elektron, Proton
import numpy as np

class Simulator:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.skjerm = pg.display.set_mode(size=(lengde, høyde))

        # Initialiserer partikler
        e1 = Elektron(600, 300, 3e6, 0)
        p1 = Proton(0, 250, 3e5, 0)
        self.partikler = [e1, p1]

        self.alle_magnetfelt = []

        # UI elementer
        self.slider = Slider(self.skjerm, 15, høyde-20, 300, 7, min=-11, max=0.301029996, step=0.001, initial=-11)
        self.slider_output = TextBox(self.skjerm, 15, høyde-60, 210, 30, fontSize=20, borderThickness=1)
        self.slider_output.disable() # kan ikke skrive i tekstboks
        
        self.tidsstatus = SimuleringStatus()
        self.button = Button(self.skjerm, 330, høyde-35, 90, 30, text='Reverser tid', fontSize=15,
                             inactiveColour=(200, 200, 200), hoverColour=(230, 230, 230),
                             pressedColour=(150, 150, 150), onClick=self.tidsstatus.bytt)

        # simuleringsvariabler
        self.medgått_tid = 0
        self.kjører_programmet = True
        self.er_pauset = False
        self.skal_lage_magnetfelt = False
        self.klar_for_magnetfelt = False
        self.start_posisjon_x, self.start_posisjon_y = None, None
        self.nytt_magnetfelt = None
        self.bredde_magnetfelt, self.høyde_magnetfelt = None, None
        self.styrke_nytt_magnetfelt = 0.00005  # start-styrken til nye magnetfelt

    def handle_events(self, events):
        keys_pressed = pg.key.get_pressed()

        for event in events:
            print(f"EVENT: {event}")

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

            if self.skal_lage_magnetfelt:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # sjekker at det er venstre museklikk
                    self.start_posisjon_x, self.start_posisjon_y = pg.mouse.get_pos()
                    self.klar_for_magnetfelt = True
                    self.bredde_magnetfelt, self.høyde_magnetfelt = 0, 0

                elif event.type == pg.MOUSEMOTION and self.klar_for_magnetfelt:
                    mus_x, mus_y = pg.mouse.get_pos()
                    self.bredde_magnetfelt = abs(mus_x - self.start_posisjon_x)
                    self.høyde_magnetfelt = abs(mus_y - self.start_posisjon_y)

                    # tegner midlertidig magnetfelt
                    if self.bredde_magnetfelt > 0 and self.høyde_magnetfelt > 0:
                        self.nytt_magnetfelt = Magnetfelt(self.styrke_nytt_magnetfelt, self.bredde_magnetfelt, self.høyde_magnetfelt, 
                                                          self.start_posisjon_x, self.start_posisjon_y, farge=LYSEGRØNN)

                elif event.type == pg.MOUSEBUTTONUP and self.nytt_magnetfelt:
                    # legger til permanent magnetfelt
                    self.alle_magnetfelt.append(Magnetfelt(self.styrke_nytt_magnetfelt, self.bredde_magnetfelt, self.høyde_magnetfelt, 
                                                           self.start_posisjon_x, self.start_posisjon_y, farge=GRØNN))
                    self.nytt_magnetfelt = None
                    self.skal_lage_magnetfelt, self.klar_for_magnetfelt = False, False

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

            if self.nytt_magnetfelt:
                self.nytt_magnetfelt.tegn(self.skjerm)

            tidsskala = 10**self.slider.getValue()
            self.slider_output.setText(f"Tidsskala: {tidsskala:.8f}")

            for magnetfelt in self.alle_magnetfelt:
                magnetfelt.tegn(self.skjerm)

            self.vis_info()

            if not self.er_pauset:
                self.medgått_tid += tidsskala * (1 / FPS) * self.tidsstatus.faktor

            for particle in self.partikler:
                for magnetfelt in self.alle_magnetfelt or [None]:
                    particle.oppdater_og_tegn(self.skjerm, magnetfelt, 1 / FPS, tidsskala, lengde, høyde, self.tidsstatus.faktor, self.er_pauset)

            self.clock.tick(FPS)
            pg_w.update(events) # oppdaterer importe widgets som sliders
            pg.display.update()

        pg.quit()

class SimuleringStatus:
    def __init__(self):
        self.faktor = 1

    def bytt(self):
        self.faktor *= -1

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()