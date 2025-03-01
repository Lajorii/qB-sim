import pygame as pg
import numpy as np

def vis_info(skjerm, tid, partikler, alle_magnetfelt, styrke):
    font = pg.font.Font(None, 18)
    info_tekst = f"Tid: {tid:.7f} s\n".rstrip('0').rstrip('.')

    for i, partikkel in enumerate(partikler):
        info_tekst += f"Partikkel {i+1}: v = {np.linalg.norm(partikkel.v):.6}\n"

    info_tekst += f"Styrke på nytt magnetfelt: {styrke:.5}"

    lines = info_tekst.split("\n")
    y_offset = 10

    for line in lines:
        if line.strip():
            tekst = font.render(line, True, (0, 0, 0))
            skjerm.blit(tekst, (10, y_offset))
            y_offset += 15