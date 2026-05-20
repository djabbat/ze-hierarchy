"""
run.py — запуск симуляции Ze-Hierarchy.
"""

import numpy as np
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from simulator.bot import create_population
from simulator.arena import Arena


def simulate(bots, arena_size=100.0, total_time=60.0, dt=0.05,
             save_every=0.5, seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    arena = Arena(size=arena_size)
    arena.add_bots(bots)
    
    save_steps = max(1, int(save_every / dt))
    n_bots = len(bots)
    total_steps = int(total_time / dt)
    n_saves = total_steps // save_steps + 1
    
    positions = np.zeros((n_saves, n_bots, 2))
    leds = np.zeros((n_saves, n_bots))
    times = np.zeros(n_saves)
    ages = np.array([b.age_days for b in bots])
    
    print(f"[{time.strftime('%H:%M:%S')}] {n_bots} ботов, {total_time:.0f}с, "
          f"dt={dt}, арена {arena_size}×{arena_size}")
    
    t0 = time.time()
    
    for i, bot in enumerate(bots):
        positions[0, i] = [bot.x, bot.y]
        leds[0, i] = bot.led
    times[0] = 0.0
    save_idx = 1
    
    for step in range(1, total_steps + 1):
        t = step * dt
        arena.step(dt)
        
        if step % save_steps == 0:
            for i, bot in enumerate(bots):
                positions[save_idx, i] = [bot.x, bot.y]
                leds[save_idx, i] = bot.led
            times[save_idx] = t
            save_idx += 1
    
    elapsed = time.time() - t0
    print(f"[{time.strftime('%H:%M:%S')}] Готово за {elapsed:.1f}с "
          f"(x{elapsed/total_time:.1f})")
    
    return {
        'positions': positions[:save_idx],
        'leds': leds[:save_idx],
        'ages': ages,
        'times': times[:save_idx],
    }


def run_test(ages_days=[0, 30], bots_per_group=10, arena_size=100.0,
             total_time=60.0, seed=42):
    bots = create_population(ages_days, bots_per_group, arena_size)
    return simulate(bots, arena_size, total_time, seed=seed)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'test'
    
    if mode == 'full':
        data = run_test([0, 30], 60, 100.0, 120.0, 42)
    elif mode == 'control':
        data = run_test([0], 60, 100.0, 120.0, 42)
    else:
        data = run_test([0, 30], 10, 100.0, 60.0, 42)
    
    save_path = Path(__file__).parent.parent / 'data'
    save_path.mkdir(exist_ok=True)
    fname = save_path / 'sim_result.npz'
    
    np.savez_compressed(fname,
        positions=data['positions'],
        leds=data['leds'],
        ages=data['ages'],
        times=data['times'])
    
    print(f"Сохранено: {fname}")
    print(f"Анализ: python3 -m analysis.metrics {fname}")
