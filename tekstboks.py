import pygame as pg
import numpy as np

def info_boks(skjerm, tid, partikler, magnetfelt):
    font = pg.font.Font(None, 16)
    tekst = font.render(f"tid: {tid}", True, (0, 0, 0))
    skjerm.blit(tekst, (10, 10))

    for i, partikkel in enumerate(partikler):
        tekst = font.render(f"partikkel {i+1}: posisjon: ({partikkel.pos[0]:.1f}, {partikkel.pos[1]:.1f}) fartsvektor: ({partikkel.v[0]:.1f}, {partikkel.v[1]:.1f}), fart: {np.linalg.norm(partikkel.v):.1f}", True, (0, 0, 0))
        skjerm.blit(tekst, (10, 20 + 20*i))

    for i, felt in enumerate(magnetfelt):
        tekst = font.render(f"magnetfelt {i+1}: retning: {felt.retning}", True, (0, 0, 0))
        skjerm.blit(tekst, (10, 20 + 20*(i + len(partikler))))