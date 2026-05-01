import numpy as np
import matplotlib.pyplot as plt
import time
from terminal import print_order_book

ticks = np.arange(start=0.0, stop=11.0, step=1.0, dtype=np.float32)
best = np.random.choice(np.arange(4, 6), size=2)
best_bid = min(best)
best_ask = max(best)
print(best_bid, best_ask)

bid_volume = {j:(abs(np.random.randn()) if j <= best_bid else 0.0) for j,_ in enumerate(ticks)}
ask_volume = {j:(abs(np.random.randn()) if j >= best_ask else 0.0) for j,_ in enumerate(ticks)}

T = 100
mu_bid = 1.0
mu_ask = mu_bid
alpha = 0.05
order_size = 0.1
cancel = 0.01
dt = 1.0
price_history = []

def MarketOrder(best_quote, mu, vol, order_type, tiks=ticks):
    tick = best_quote
    n = len(tiks)
    while mu > 0:
        if vol[tick] > 1e-9:
            eat = min(vol[tick], mu)
            vol[tick] -= eat
            mu -= eat
            if vol[tick] <= 1e-9:
                vol[tick] = 0.0
        else:
            if order_type == "buyside":
                if tick < n - 1:
                    tick += 1
                else:
                    break
            elif order_type == "sellside":
                if tick > 0:
                    tick -= 1
                else:
                    break

#EVOLUTION LOOP
for t in range(T):
    # market orders
    mu_buy = np.random.poisson(mu_bid * dt) * order_size
    mu_sell = np.random.poisson(mu_ask * dt) * order_size
    
    # for buy side
    MarketOrder(best_quote=best_ask, mu=mu_buy, vol=ask_volume)

    # for sell side
    MarketOrder(best_quote=best_bid, mu=mu_sell, vol=bid_volume)

    # limit orders
    X = np.random.poisson(lam=alpha*dt*len(ticks), size=2)
    
    # buyside (including in-spread orders)
    for _ in range(X[0]):
        while True:
            k = np.random.geometric(0.5)
            if best_ask - k >= 0:
                break
        bid_volume[best_ask - k] += order_size

    # sellside (including in-spread orders / marketable orders)
    for _ in range(X[1]):
        while True:
            k = np.random.geometric(0.5)
            if best_bid + k < len(ticks):
                break
        ask_volume[best_bid + k] += order_size
        
    
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