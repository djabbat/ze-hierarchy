"""30 сидов для тестов A и C (быстрый режим)."""
import numpy as np, time, sys
sys.path.insert(0, '.')
from simulator.bot import create_population
from simulator.arena import Arena

results = {'C': [], 'A': []}
t0 = time.time()
steps = 300  # 30 секунд симуляции

for exp_seed in range(30):
    # Тест C
    np.random.seed(exp_seed)
    bots = create_population([0, 30], 60, 80)
    a = Arena(80); a.add_bots(bots)
    pos=np.zeros((steps,120,2))
    for i,b in enumerate(bots): pos[0,i]=[b.x,b.y]
    for s in range(1,steps):
        a.step(0.1)
        for i,b in enumerate(bots): pos[s,i]=[b.x,b.y]
    c=np.array([40,40])
    ag=np.array([b.age_days for b in bots])
    R=np.sqrt((pos[:,:,0]-c[0])**2+(pos[:,:,1]-c[1])**2)
    HI_C=(R[:,ag==30][:,:,None]>R[:,ag==0][:,None,:]).mean()
    results['C'].append(HI_C)
    
    # Тест A
    np.random.seed(1000+exp_seed)
    bots = create_population([0], 120, 80)
    a = Arena(80); a.add_bots(bots)
    pos=np.zeros((steps,120,2))
    for i,b in enumerate(bots): pos[0,i]=[b.x,b.y]
    for s in range(1,steps):
        a.step(0.1)
        for i,b in enumerate(bots): pos[s,i]=[b.x,b.y]
    R=np.sqrt((pos[:,:,0]-c[0])**2+(pos[:,:,1]-c[1])**2)
    HI_A=(R[:,:60][:,:,None]>R[:,60:][:,None,:]).mean()
    results['A'].append(HI_A)
    
    if (exp_seed+1)%10==0:
        print(f"  {exp_seed+1}/30 за {time.time()-t0:.0f}с", flush=True)

HI_C=np.array(results['C'])
HI_A=np.array(results['A'])
print(f"\n=== 30 СИДОВ ===")
print(f"Тест C (0 vs 30): mean={HI_C.mean():.4f} std={HI_C.std():.4f}")
print(f"Тест A (контроль): mean={HI_A.mean():.4f} std={HI_A.std():.4f}")
print(f"Разница: {HI_C.mean()-HI_A.mean():+.4f}")

from scipy import stats
t, p = stats.ttest_ind(HI_C, HI_A)
d = (HI_C.mean()-HI_A.mean())/np.sqrt((HI_C.std()**2+HI_A.std()**2)/2)
print(f"t-test: t={t:.4f}, p={p:.6f}, Cohen's d={d:.4f}")
print(f"Время: {time.time()-t0:.0f}с")
