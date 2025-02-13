import pygame as pg
import numpy as np

def vis_info(skjerm, tid, partikler, magnetfelt):
    font = pg.font.Font(None, 24)
    info_tekst = f"Tid: {tid:.5f}\n"

    for i, partikkel in enumerate(partikler):
        info_tekst += f"Partikkel {i+1}: v = {np.linalg.norm(partikkel.v):.5f}\n"

    lines = info_tekst.split("\n")
    y_offset = 14

    for line in lines:
        if line.strip():
            tekst = font.render(line, True, (0, 0, 0))
            skjerm.blit(tekst, (10, y_offset))
            y_offset += 25