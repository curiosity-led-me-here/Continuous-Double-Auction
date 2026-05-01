import numpy as np

ticks = np.arange(start=0.0, stop=11.0, step=1.0, dtype=np.float32)
best = np.random.choice(np.arange(4, 6), size=2)
best_bid = min(best)
best_ask = max(best)
print(best_bid, best_ask)

bid_volume = {j:(abs(np.random.randn()) if j <= best_bid else 0.0) for j,_ in enumerate(ticks)}

print(any(v > 1e-9 for v in list(bid_volume.values())[1:]))