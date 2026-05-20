"""
metrics.py — расчёт метрик иерархии по данным симуляции.
"""

import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def compute_flow_matrix(positions: np.ndarray, times: np.ndarray,
                        ages: np.ndarray) -> np.ndarray:
    """
    Вычислить матрицу следования: F[i, j] = вероятность, что i следует за j.
    
    positions: (T, N, 2) — траектории
    times: (T,) — временные метки
    ages: (N,) — возраст ботов
    """
    T, N = positions.shape[0], positions.shape[1]
    
    # Вычисляем направления движения для каждого бота
    # На каждом шаге: velocity = (pos[t+1] - pos[t-1]) / 2
    velocities = np.zeros_like(positions)
    velocities[1:-1] = (positions[2:] - positions[:-2]) / 2
    velocities[0] = velocities[1]
    velocities[-1] = velocities[-2]
    
    # Нормализуем направления
    speed = np.linalg.norm(velocities, axis=2)
    direction = np.zeros_like(velocities)
    mask = speed > 0.01
    direction[mask] = velocities[mask] / speed[mask][:, None]
    
    # Матрица следования
    F = np.zeros((N, N))
    
    for t in range(1, T - 1):
        for i in range(N):
            if speed[t, i] < 0.01:
                continue
            
            for j in range(N):
                if i == j:
                    continue
                
                # Вектор от i к j
                dx = positions[t, j, 0] - positions[t, i, 0]
                dy = positions[t, j, 1] - positions[t, i, 1]
                dist = np.hypot(dx, dy)
                
                if dist < 0.5 or dist > 20.0:  # слишком далеко или слишком близко
                    continue
                
                # Единичный вектор от i к j
                to_j = np.array([dx, dy]) / dist
                
                # Скалярное произведение направления i с вектором к j
                # Если > 0 — i движется по направлению к j
                cos_angle = np.dot(direction[t, i], to_j)
                
                if cos_angle > 0.7:  # угол < 45°
                    F[i, j] += 1
    
    # Нормализуем
    row_sums = F.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    F = F / row_sums
    
    return F


def compute_hierarchy_index(positions: np.ndarray, times: np.ndarray,
                            ages: np.ndarray) -> float:
    """
    Пространственный HI.
    
    Считаем все пары (новый, старый) в каждый момент времени.
    HI = доля моментов, когда старый ДАЛЬШЕ от центра, чем новый.
    
    0.5 — случай (позиция не зависит от возраста)
    > 0.5 — новые в центре, старые по периферии (иерархия)
    < 0.5 — инверсия
    """
    T = len(times)
    center = np.array([positions[:, :, 0].mean(), positions[:, :, 1].mean()])
    
    # Расстояние каждого бота до центра в каждый момент
    R = np.sqrt((positions[:, :, 0] - center[0])**2 + 
                (positions[:, :, 1] - center[1])**2)  # (T, N)
    
    new_mask = ages == ages.min()
    old_mask = ages == ages.max()
    
    n_correct = 0
    n_total = 0
    
    for t in range(T):
        r_new = R[t, new_mask]  # расстояния новых
        r_old = R[t, old_mask]  # расстояния старых
        
        for rn in r_new:
            for ro in r_old:
                n_total += 1
                if ro > rn:  # старый дальше от центра → правильная иерархия
                    n_correct += 1
    
    if n_total == 0:
        return 0.5
    
    return n_correct / n_total


def compute_leader_radius(positions: np.ndarray, times: np.ndarray,
                          ages: np.ndarray, age_group: float) -> float:
    """
    Радиус лидерства: среднее расстояние от ботов возраста age_group
    до тех, кто за ними следует.
    """
    F = compute_flow_matrix(positions, times, ages)
    N = len(ages)
    
    # Находим ботов этого возраста
    leaders = np.where(ages == age_group)[0]
    
    if len(leaders) == 0:
        return 0.0
    
    # Для каждого лидера: среднее расстояние до тех, кто следует за ним
    radii = []
    
    for leader in leaders:
        followers = np.where(F[:, leader] > F[leader, :])[0]
        followers = followers[followers != leader]
        
        if len(followers) == 0:
            continue
        
        # Среднее расстояние за всё время
        dists = []
        for t in range(positions.shape[0]):
            for f in followers:
                d = np.hypot(positions[t, leader, 0] - positions[t, f, 0],
                            positions[t, leader, 1] - positions[t, f, 1])
                dists.append(d)
        
        if dists:
            radii.append(np.mean(dists))
    
    if not radii:
        return 0.0
    
    return np.mean(radii)


def compute_convergence_time(positions: np.ndarray, times: np.ndarray,
                             ages: np.ndarray, window: int = 100) -> float:
    """
    Время конвергенции иерархии.
    Скользящее окно: считаем HI посегментно, находим, когда HI достигает 90%.
    """
    T = positions.shape[0]
    half_window = window // 2
    
    HI_over_time = []
    t_center = []
    
    for t in range(half_window, T - half_window, half_window):
        start = t - half_window
        end = t + half_window
        HI = compute_hierarchy_index(
            positions[start:end], times[start:end], ages
        )
        HI_over_time.append(HI)
        t_center.append(times[t])
    
    if len(HI_over_time) < 2:
        return times[-1]
    
    HI_over_time = np.array(HI_over_time)
    t_center = np.array(t_center)
    
    # Находим 90% от максимума
    HI_max = np.max(HI_over_time)
    HI_target = 0.9 * HI_max
    
    # Первый раз, когда HI >= HI_target
    idx = np.where(HI_over_time >= HI_target)[0]
    if len(idx) > 0:
        return t_center[idx[0]]
    else:
        return times[-1]


def print_metrics(data: dict):
    """Вывести метрики."""
    positions = data['positions']
    times = data['times']
    ages = data['ages']
    
    print("\n=== МЕТРИКИ ИЕРАРХИИ ===\n")
    
    HI = compute_hierarchy_index(positions, times, ages)
    print(f"HI (индекс иерархии): {HI:.4f}")
    print(f"  > 0.5 → иерархия (молодые лидируют)")
    print(f"  < 0.5 → инверсия (старые лидируют)")
    print(f"  = 0.5 → случай")
    print()
    
    for age in sorted(set(ages)):
        R = compute_leader_radius(positions, times, ages, age)
        print(f"Радиус лидерства (возраст {age:.0f} дн): {R:.1f} см")
    
    print()
    τ = compute_convergence_time(positions, times, ages)
    print(f"Время конвергенции: {τ:.1f} с")
    print()
    
    # Групповой HI
    print("--- Групповые HI ---")
    unique_ages = sorted(set(ages))
    for i, a1 in enumerate(unique_ages):
        for a2 in unique_ages[i+1:]:
            mask1 = ages == a1
            mask2 = ages == a2
            # Создаём подмаску
            mask = mask1 | mask2
            HI_pair = compute_hierarchy_index(
                positions[:, mask], times, ages[mask]
            )
            print(f"  {a1:.0f} vs {a2:.0f} дн: HI = {HI_pair:.4f}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Использовать последний сохранённый файл
        data_dir = Path(__file__).parent.parent / 'data'
        files = sorted(data_dir.glob('sim_hierarchy_*.npz'))
        if not files:
            print("Нет файлов данных. Сначала запустите simulator/run.py")
            sys.exit(1)
        fname = files[-1]
    else:
        fname = Path(sys.argv[1])
    
    print(f"Загрузка: {fname}")
    data = np.load(fname)
    
    print_metrics(data)
