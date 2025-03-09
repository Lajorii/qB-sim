import pygame as pg
import numpy as np
from colors import *

class Magnetfelt:
    def __init__(self, B, lengde, høyde, x, y, farge = GRØNN):
        self.B = B
        self.lengde = lengde
        self.høyde = høyde
        self.farge = farge
        self.x = x
        self.y = y
        self.font = pg.font.Font(None, 15)
     
        self.retning = np.array([0, 0, B])


    def tegn(self, skjerm):
        pg.draw.rect(skjerm, self.farge, (self.x, self.y, self.lengde, self.høyde))

        styrke_tekst = self.font.render(f"B = {self.B:.5} T", True, (0, 0, 0))
        skjerm.blit(styrke_tekst, (self.x+10, self.y+10))


class Partikkel:
    def __init__(self, x, y, dx, dy, radius = 4, farge = RØD):
        self.x = x
        self.y = y
        self.v = np.array([dx, dy, 0], dtype='float64') # m/s
        self.start_v = np.array([dx, dy, 0], dtype='float64')
        self.pos = np.array([x, y, 0], dtype='float64')
        self.radius = radius
        self.farge = farge

        self.skal_flyttes = False

    def oppdater_og_tegn(self, skjerm, magnetfelt, delta_tid, tidsskala, lengde, høyde, faktor, er_pauset):
        if er_pauset:
            pg.draw.circle(skjerm, self.farge, (self.pos[0], self.pos[1]), self.radius)
            return
        
        if magnetfelt is None:
            self.pos += self.v*1000 * tidsskala * faktor
            pg.draw.circle(skjerm, self.farge, (self.pos[0], self.pos[1]), self.radius)
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

    def tegn_midlertidig(self, skjerm):
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



# en funksjon jeg fant på nettet 
def draw_arrow(
        surface: pg.Surface,
        start: pg.Vector2,
        end: pg.Vector2,
        color: pg.Color,
        body_width: int = 4,
        head_width: int = 15,
        head_height: int = 15,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pg.Surface): The surface to draw on
        start (pg.Vector2): Start position
        end (pg.Vector2): End position
        color (pg.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pg.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pg.Vector2(0, head_height / 2),  # Center
        pg.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pg.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pg.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pg.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pg.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pg.Vector2(body_width / 2, body_length / 2),  # Topright
            pg.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pg.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pg.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        return pg.draw.polygon(surface, color, body_verts)