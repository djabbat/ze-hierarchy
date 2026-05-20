"""
physics.py — столкновения ботов (repulsion).

Добавляет repulsion при контакте: если два бота ближе чем 1.0 см,
они отталкиваются друг от друга. Предотвращает вихревой миллинг
(Mahadevan 2012) как артефакт иерархии.
"""

import numpy as np
from .bot import Bot


REPULSION_RADIUS = 1.5   # см — дистанция, на которой начинается отталкивание
REPULSION_FORCE = 5.0    # см/с — сила отталкивания


def apply_repulsion(bots: list[Bot], dt: float):
    """
    Применить отталкивание между всеми парами ботов.
    Модифицирует bot.x, bot.y напрямую.
    """
    n = len(bots)
    if n < 2:
        return
    
    for i in range(n):
        fx, fy = 0.0, 0.0
        bi = bots[i]
        
        for j in range(i + 1, n):
            bj = bots[j]
            dx = bi.x - bj.x
            dy = bi.y - bj.y
            dist = np.hypot(dx, dy)
            
            if 0.1 < dist < REPULSION_RADIUS:
                # Сила отталкивания: 1/r (растёт при сближении)
                force = REPULSION_FORCE / max(dist, 0.1)
                # Направление от j к i
                fx += force * dx / dist
                fy += force * dy / dist
        
        # Применяем к обоим (i-тый получит свой вклад, j-тый — от i)
        bi.x += fx * dt
        bi.y += fy * dt
