import numpy as np
import matplotlib.pyplot as plt
import time
from terminal import print_order_book

ticks = np.arange(start=0.0, stop=11.0, step=1.0, dtype=np.float32)
best = np.random.choice(np.arange(1, len(ticks)-1), size=2)
best_bid = min(best)
best_ask = max(best)

bid_volume = {j:abs(np.random.randn()) for j,_ in enumerate(ticks)}
ask_volume = {j:abs(np.random.randn()) for j,_ in enumerate(ticks)}

T = 100
mu_bid = 1.0
mu_ask = mu_bid
alpha = 0.05
order_size = 0.1
cancel = 0.01
dt = 1.0
price_history = []

#EVOLUTION LOOP
for t in range(T):
    # market orders
    mu_buy = np.random.poisson(mu_bid * dt) * order_size
    mu_sell = np.random.poisson(mu_ask * dt) * order_size
    
    # for buy side
    tick_ask = best_ask
    while mu_buy > 0:
        eat = min(ask_volume[tick_ask], mu_buy)
        ask_volume[tick_ask] -= eat
        mu_buy -= eat
        if ask_volume[tick_ask] == 0:
            tick_ask += 1
    tick_bid = best_bid
    while mu_sell > 0:
        eat = min(bid_volume[tick_bid], mu_sell)
        bid_volume[tick_bid] -= eat
        mu_sell -= eat
        if bid_volume[tick_bid] == 0:
            tick_bid -= 1
    
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
        X = min(X, k_order)
        k_order -= X
        bid_volume[tick] = k_order / 1000
    for tick, vol in ask_volume.items():
        k_order = int(vol*1000)
        lam = k_order * cancel * dt
        X = np.random.poisson(lam)
        X = min(X, k_order)
        k_order -= X
        ask_volume[tick] = k_order / 1000
    
    price_history.append((best_bid + best_ask) / 2)
    current_asks = [tick for tick, vol in ask_volume.items() if vol > 0.001]
    current_bids = [tick for tick, vol in bid_volume.items() if vol > 0.001]
    best_ask = min(current_asks) if current_asks else len(ticks) - 1
    best_bid = max(current_bids) if current_bids else 0
    print_order_book(t, ticks, bid_volume, ask_volume, best_bid, best_ask, price_history)
    time.sleep(0.5)