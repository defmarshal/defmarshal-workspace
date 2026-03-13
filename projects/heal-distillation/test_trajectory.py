from heal.data import load_aime
from heal.teacher import generate_trajectories
import time

print('Loading AIME problem...')
problems = load_aime(num_samples=1)
p = problems[0]['problem']
print('Problem (truncated):', p[:200])
print('Generating trajectory...')
start = time.time()
trajs = generate_trajectories(p, n=1)
print('Got', len(trajs), 'trajectory in', time.time()-start, 's')
if trajs:
    print('Preview:', trajs[0][:200])
else:
    print('No trajectory generated')
