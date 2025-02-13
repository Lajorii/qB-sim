import pygame as pg
import numpy as np
from colors import HVIT, SORT, RØD, GRØNN, BLÅ

class Magnetfelt:
    def __init__(self, B, lengde, høyde, x, y, farge = GRØNN):
        self.B = B
        self.lengde = lengde
        self.høyde = høyde
        self.farge = farge
        self.x = x
        self.y = y
     
        self.retning = np.array([0, 0, B])


    def tegn(self, skjerm):
        pg.draw.rect(skjerm, self.farge, (self.x, self.y, self.lengde, self.høyde))


class Partikkel:
    def __init__(self, x, y, dx, dy, radius = 4, farge = RØD):
        self.x = x
        self.y = y
        self.v = np.array([dx, dy, 0], dtype='float64') # m/s
        self.start_v = np.array([dx, dy, 0], dtype='float64')
        self.pos = np.array([x, y, 0], dtype='float64')
        self.radius = radius
        self.farge = farge

    def oppdater_og_tegn(self, skjerm, magnetfelt, delta_tid, tidsskala, lengde, høyde, faktor):  # Small timestep
        if magnetfelt is None:
            return
        
        def er_i_magnetfelt(self, magnetfelt):
            return (
                magnetfelt.x <= self.pos[0] <= magnetfelt.x + magnetfelt.lengde and
                magnetfelt.y <= self.pos[1] <= magnetfelt.y + magnetfelt.høyde
            )

        if er_i_magnetfelt(self, magnetfelt):
            F = self.q * np.cross(self.v, magnetfelt.retning) * faktor
            a = F / self.m

            self.v = self.v + a * delta_tid * tidsskala

            self.v = (self.v/np.linalg.norm(self.v)) * np.linalg.norm(self.start_v)

            print(np.linalg.norm(self.v))

        self.pos += self.v*1000 * tidsskala * faktor

        pg.draw.circle(skjerm, self.farge, (self.pos[0], self.pos[1]), self.radius)



class Elektron(Partikkel):
    def __init__(self, x, y, dx, dy, radius = 4, farge = BLÅ):
        super().__init__(x, y, dx, dy, radius, farge)
        self.q = -1.6e-19
        self.m = 9.11e-31

class Proton(Partikkel):
    def __init__(self, x, y, dx, dy, radius = 4, farge = RØD):
        super().__init__(x, y, dx, dy, radius, farge)
        self.q = 1.6e-19
        self.m = 1.67e-27