"""
visualize.py — визуализация симуляции иерархии.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # для headless-сервера
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def animate_trajectories(data: dict, output: str = 'hierarchy.gif',
                         max_frames: int = 500):
    """Анимировать траектории ботов."""
    from matplotlib.animation import FuncAnimation
    
    positions = data['positions']
    times = data['times']
    ages = data['ages']
    leds = data['leds']
    
    T, N = positions.shape[0], positions.shape[1]
    arena_size = data.get('params', {}).get('arena_size', 60.0)
    
    # Цвета по возрасту
    unique_ages = sorted(set(ages))
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(unique_ages)))
    age_to_color = {a: colors[i] for i, a in enumerate(unique_ages)}
    bot_colors = [age_to_color[a] for a in ages]
    
    # Если слишком много кадров, прореживаем
    if T > max_frames:
        step = T // max_frames
        indices = np.arange(0, T, step)
        positions = positions[indices]
        leds = leds[indices]
        times = times[indices]
        T = len(indices)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def update(frame):
        ax.clear()
        ax.set_xlim(0, arena_size)
        ax.set_ylim(0, arena_size)
        ax.set_aspect('equal')
        ax.set_title(f't = {times[frame]:.1f} с')
        
        # Рисуем ботов
        for i in range(N):
            size = 5 + 10 * leds[frame, i]  # размер пропорционален яркости LED
            ax.scatter(positions[frame, i, 0], positions[frame, i, 1],
                      s=size, c=[bot_colors[i]], alpha=0.8)
        
        # Легенда возрастов
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor=age_to_color[a], 
                   markersize=10, label=f'{a:.0f} дн')
            for a in unique_ages
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return ax
    
    anim = FuncAnimation(fig, update, frames=T, interval=50)
    anim.save(output, writer='pillow', fps=20)
    plt.close()
    print(f"Анимация сохранена: {output}")


def plot_hierarchy_matrix(data: dict, output: str = 'hierarchy_matrix.png'):
    """Построить матрицу следования."""
    from analysis.metrics import compute_flow_matrix
    
    positions = data['positions']
    times = data['times']
    ages = data['ages']
    
    F = compute_flow_matrix(positions, times, ages)
    N = len(ages)
    
    # Сортируем по возрасту
    order = np.argsort(ages)
    
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(F[order][:, order], cmap='Blues', vmin=0, vmax=F.max())
    ax.set_xlabel('Кому следуют (j)')
    ax.set_ylabel('Кто следует (i)')
    ax.set_title('Матрица следования (отсортирована по возрасту)')
    
    # Метки
    sorted_ages = ages[order]
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels([f'{a:.0f}' for a in sorted_ages], fontsize=6)
    ax.set_yticklabels([f'{a:.0f}' for a in sorted_ages], fontsize=6)
    
    plt.colorbar(im, label='P(следует)')
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Матрица следования сохранена: {output}")


def plot_positions(data: dict, output: str = 'positions.png'):
    """Построить финальные позиции."""
    positions = data['positions']
    ages = data['ages']
    leds = data['leds']
    arena_size = data.get('params', {}).get('arena_size', 60.0)
    
    T = positions.shape[0]
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # Начальные позиции
    ax = axes[0]
    for i in range(positions.shape[1]):
        size = 5 + 10 * leds[0, i]
        ax.scatter(positions[0, i, 0], positions[0, i, 1],
                  s=size, alpha=0.7)
    ax.set_xlim(0, arena_size)
    ax.set_ylim(0, arena_size)
    ax.set_aspect('equal')
    ax.set_title('Начало (t=0)')
    
    # Конечные позиции
    ax = axes[1]
    for i in range(positions.shape[1]):
        size = 5 + 10 * leds[-1, i]
        ax.scatter(positions[-1, i, 0], positions[-1, i, 1],
                  s=size, alpha=0.7)
    ax.set_xlim(0, arena_size)
    ax.set_ylim(0, arena_size)
    ax.set_aspect('equal')
    ax.set_title(f'Конец (t={data["times"][-1]:.1f} с)')
    
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Позиции сохранены: {output}")


def plot_hi_over_time(data: dict, output: str = 'hi_over_time.png',
                      window: int = 100):
    """Построить HI во времени."""
    from analysis.metrics import compute_hierarchy_index
    
    positions = data['positions']
    times = data['times']
    ages = data['ages']
    
    T = positions.shape[0]
    half_window = window // 2
    
    HI = []
    t_vals = []
    
    for t in range(half_window, T - half_window, half_window):
        start = t - half_window
        end = t + half_window
        hi = compute_hierarchy_index(
            positions[start:end], times[start:end], ages
        )
        HI.append(hi)
        t_vals.append(times[t])
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t_vals, HI, 'b-', linewidth=2)
    ax.axhline(0.5, color='gray', linestyle='--', label='random (0.5)')
    ax.axhline(max(HI) * 0.9, color='red', linestyle=':', 
               label=f'90% max ({max(HI)*0.9:.2f})')
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('HI (индекс иерархии)')
    ax.set_title('Иерархия во времени')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"HI во времени сохранён: {output}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        data_dir = Path(__file__).parent.parent / 'data'
        files = sorted(data_dir.glob('sim_hierarchy_*.npz'))
        if not files:
            print("Нет файлов данных. Сначала запустите simulator/run.py")
            sys.exit(1)
        fname = files[-1]
    else:
        fname = Path(sys.argv[1])
    
    print(f"Загрузка: {fname}")
    data = dict(np.load(fname))
    
    # Создаём папку для графиков
    out_dir = Path(__file__).parent.parent / 'figures'
    out_dir.mkdir(exist_ok=True)
    
    plot_positions(data, str(out_dir / 'positions.png'))
    plot_hi_over_time(data, str(out_dir / 'hi_over_time.png'))
    plot_hierarchy_matrix(data, str(out_dir / 'hierarchy_matrix.png'))
    animate_trajectories(data, str(out_dir / 'hierarchy.gif'), max_frames=300)
    
    print(f"\nВсе визуализации в: {out_dir}/")
