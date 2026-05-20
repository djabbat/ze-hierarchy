"""
arena.py — ближайший яркий, усиленный фототаксис.
"""

import numpy as np
from .bot import Bot
from .physics import apply_repulsion


class Arena:
    def __init__(self, size=80.0):
        self.size = size
        self.bots = []
    
    def add_bots(self, bots):
        self.bots.extend(bots)
    
    def apply_walls(self):
        for b in self.bots:
            if b.x<0.5: b.x=0.5; b.theta=np.pi-b.theta
            elif b.x>self.size-0.5: b.x=self.size-0.5; b.theta=np.pi-b.theta
            if b.y<0.5: b.y=0.5; b.theta=-b.theta
            elif b.y>self.size-0.5: b.y=self.size-0.5; b.theta=-b.theta
    
    def step(self, dt):
        n = len(self.bots)
        if n<2:
            for b in self.bots: b.move(dt,0,0,0,0); return
        
        pos = np.array([[b.x,b.y] for b in self.bots])
        leds = np.array([b.led for b in self.bots])
        gx=np.zeros(n); gy=np.zeros(n)
        rx=np.zeros(n); ry=np.zeros(n)
        
        for i, bot in enumerate(self.bots):
            dx = pos[:,0]-bot.x
            dy = pos[:,1]-bot.y
            dist = np.sqrt(dx**2+dy**2)
            dist[i]=999
            
            if bot.led < 0.95:  # старые
                # Ближайший яркий (led > 0.7)
                bright = (leds>0.7) & (dist<30.0) & (dist>0.5)
                if bright.any():
                    j = np.argmin(dist[bright])
                    idx = np.where(bright)[0][j]
                    gx[i] = dx[idx]/dist[idx]*8.0
                    gy[i] = dy[idx]/dist[idx]*8.0
            
            # Репульсор (звук) — слабый, только чтоб не слипались
            close = (dist<2.0) & (dist>0.5)
            if close.any():
                rx[i] = -(dx*close/np.maximum(dist,0.1)).sum()*1.0
                ry[i] = -(dy*close/np.maximum(dist,0.1)).sum()*1.0
        
        for i,bot in enumerate(self.bots):
            bot.move(dt, gx[i],gy[i], rx[i],ry[i])
        
        apply_repulsion(self.bots, dt)
        self.apply_walls()
    
    def get_positions(self): return np.array([[b.x,b.y] for b in self.bots])
    def get_ages(self): return np.array([b.age_days for b in self.bots])
    def get_leds(self): return np.array([b.led for b in self.bots])
