"""10 сидов, арена 40x40, без шума."""
import numpy as np, time, sys
sys.path.insert(0, '.')
from simulator.bot import create_population
from simulator.arena import Arena

results = {'C':[], 'A':[], 'R_n':[], 'R_o':[]}
t0=time.time()
steps=1500

for seed in range(10):
    np.random.seed(seed)
    bots = create_population([0,30], 60, 40)
    for b in bots: b.noise_angle = 0.0
    a = Arena(40); a.add_bots(bots)
    pos=np.zeros((steps,120,2))
    for i,b in enumerate(bots): pos[0,i]=[b.x,b.y]
    for s in range(1,steps):
        a.step(0.1)
        for i,b in enumerate(bots): pos[s,i]=[b.x,b.y]
    ag=np.array([b.age_days for b in bots])
    R=np.sqrt((pos[:,:,0]-20)**2+(pos[:,:,1]-20)**2)
    HI=(R[:,ag==30][:,:,None]>R[:,ag==0][:,None,:]).mean()
    results['C'].append(HI)
    results['R_n'].append(R[:,ag==0].mean())
    results['R_o'].append(R[:,ag==30].mean())
    
    # контроль
    np.random.seed(1000+seed)
    bots = create_population([0], 120, 40)
    for b in bots: b.noise_angle = 0.0
    a = Arena(40); a.add_bots(bots)
    pos=np.zeros((steps,120,2))
    for i,b in enumerate(bots): pos[0,i]=[b.x,b.y]
    for s in range(1,steps):
        a.step(0.1)
        for i,b in enumerate(bots): pos[s,i]=[b.x,b.y]
    R=np.sqrt((pos[:,:,0]-20)**2+(pos[:,:,1]-20)**2)
    HI_A=(R[:,:60][:,:,None]>R[:,60:][:,None,:]).mean()
    results['A'].append(HI_A)
    
    print(f"  seed={seed}: C={HI:.3f} A={HI_A:.3f} Rn={results['R_n'][-1]:.1f} Ro={results['R_o'][-1]:.1f}")

HI_C=np.array(results['C'])
HI_A=np.array(results['A'])
print(f"\n=== 10 СИДОВ, 40x40, без шума ===")
print(f"Тест C: mean={HI_C.mean():.4f} std={HI_C.std():.4f}")
print(f"Тест A: mean={HI_A.mean():.4f} std={HI_A.std():.4f}")
print(f"Разница: {HI_C.mean()-HI_A.mean():+.4f}")

from scipy import stats
t,p=stats.ttest_ind(HI_C,HI_A)
d=(HI_C.mean()-HI_A.mean())/np.sqrt((HI_C.std()**2+HI_A.std()**2)/2)
print(f"t-test: t={t:.4f} p={p:.6f} d={d:.4f}")
print(f"Rn={np.mean(results['R_n']):.1f} Ro={np.mean(results['R_o']):.1f}")
print(f"Время: {time.time()-t0:.0f}с")
