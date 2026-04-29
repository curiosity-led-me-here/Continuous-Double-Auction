import numpy as np

ticks = np.arange(start=0.0, stop=11.0, step=1.0, dtype=np.float32)
best = np.random.choice(np.arange(1, len(ticks)-1), size=2)
best_bid = min(best)
best_ask = max(best)

bid_volume = {j:abs(np.random.randn()) for j,_ in enumerate(ticks)}
ask_volume = {j:abs(np.random.randn()) for j,_ in enumerate(ticks)}

spread_vol = 3.0
t = 10
mu_bid = 1.0
mu_ask = 1.0
alpha = 2.0
order_size = 0.1
cancel = 1 / t

for dt in range(t):
    # market orders
    mu_buy = np.random.poisson(mu_bid * dt) * order_size
    mu_sell = np.random.poisson(mu_ask * dt) * order_size
    
    # for buy side
    tick_bid = best_ask
    while mu_buy > 0:
        eat = min(ask_volume[tick_ask][1], mu_buy)
        bid_volume[tick][1] -= eat
        mu_buy -= eat
        if bid_volume[tick][1] == 0:
            tick_bid += 1
    tick_ask = best_ask
    while mu_sell > 0:
        eat = min(ask_volume[tick][1], mu_sell)
        ask_volume[tick][1] -= eat
        mu_sell -= eat
        if ask_volume[tick][1] == 0:
            tick_ask -= 1
    
    # limit orders
    for tick, _ in bid_volume.items():
        if tick < best_ask: 
            lam = alpha * dt
            X = np.random.poisson(lam)
            bid_volume[tick] += X * order_size

    for tick, _ in ask_volume.items():
        if tick > best_bid:
            lam = alpha * dt
            X = np.random.poisson(lam)
            ask_volume[tick] += X * order_size
    
    # random cancellations
    for tick, vol in bid_volume.items():
        k_order = int(vol*1000)
        lam = k_order * cancel * dt
        X = np.random.poisson(lam)
        X = min(X, k_orders)
        k_orders -= X
        bid_volume[tick] = k_orders / 1000

