## THANKS GEMINI FOR THIS FANCY PRINT FUNCTION!!!
def print_order_book(t, ticks, bid_volume, ask_volume, best_bid, best_ask, price_history):
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    spread = ticks[best_ask] - ticks[best_bid] if best_ask < len(ticks) and best_bid >= 0 else 0.0
    out = []
    out.append(f"{'='*41}")
    out.append(f" t: {t:02d} | spread: {spread:.2f} ".center(41, '='))
    out.append(f"{'Bid':>12} | {'Ticks':^7} | {'Ask':<12}")
    out.append("-" * 41)
    for i in range(len(ticks) - 1, -1, -1):
        price = ticks[i]
        if i == best_ask:
            price_str = f"{RED}{BOLD}{price:^7.2f}{RESET}"
            ask_str = f"{RED}{BOLD}{ask_volume.get(i, 0):.2f}*{RESET}" if ask_volume.get(i, 0) > 0 else ""
        elif i > best_ask and ask_volume.get(i, 0) > 0:
            price_str = f"{price:^7.2f}"
            ask_str = f"{RED}{ask_volume[i]:.2f}{RESET}"
        else:
            ask_str = ""
        if i == best_bid:
            price_str = f"{GREEN}{BOLD}{price:^7.2f}{RESET}"
            bid_str = f"{GREEN}{BOLD}*{bid_volume.get(i, 0):.2f}{RESET}" if bid_volume.get(i, 0) > 0 else ""
        elif i < best_bid and bid_volume.get(i, 0) > 0:
            price_str = f"{price:^7.2f}"
            bid_str = f"{GREEN}{bid_volume[i]:.2f}{RESET}"
        else:
            bid_str = ""
        if best_bid < i < best_ask:
            price_str = f"{GRAY}{price:^7.2f}{RESET}"
        elif i != best_ask and i != best_bid:
            price_str = f"{price:^7.2f}"
        clean_bid = f"*{bid_volume.get(i, 0):.2f}" if (i == best_bid and bid_str) else f"{bid_volume.get(i, 0):.2f}" if bid_str else ""
        clean_ask = f"{ask_volume.get(i, 0):.2f}*" if (i == best_ask and ask_str) else f"{ask_volume.get(i, 0):.2f}" if ask_str else ""
        bid_pad = " " * (12 - len(clean_bid))
        ask_pad = " " * (12 - len(clean_ask))
        out.append(f"{bid_pad}{bid_str} | {price_str} | {ask_str}{ask_pad}")
    out.append("=" * 41)
    if price_history:
        H = 6
        W = 41
        hist = price_history[-W:]
        min_p = min(hist)
        max_p = max(hist)
        rng = max_p - min_p if max_p != min_p else 1
        grid = [[" " for _ in range(W)] for _ in range(H)]
        for x, p in enumerate(hist):
            y = int((p - min_p) / rng * (H - 1))
            if x > 0:
                prev_y = int((hist[x-1] - min_p) / rng * (H - 1))
                step = 1 if y > prev_y else -1
                for fill_y in range(prev_y + step, y, step):
                    grid[H - 1 - fill_y][x] = "│"
            grid[H - 1 - y][x] = "•"
        out.append("".center(41))
        for row in grid:
            out.append("".join(row))
        out.append(f"CUR: {price_history[-1]:.2f} | MIN: {min_p:.2f} | MAX: {max_p:.2f}".center(41))
        out.append("=" * 41)
    output_str = "\n".join(out)
    lines = len(out)
    move_up = f"\033[{lines}A" if t > 0 else ""
    print(f"{move_up}{output_str}")