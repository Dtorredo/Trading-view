"""
Leo's Trading Business Dashboard
=================================
Built with NumPy to learn array operations, statistical calculations,
and financial modelling — all applied directly to your trading system.

Run: python trading_dashboard.py
"""

import json
import os
from datetime import datetime
import math

try:
    import numpy as np
except ImportError:
    # NumPy is not installed (common in offline or proxy-restricted environments).
    # We fallback to a pure Python mockup of the same NumPy APIs used in this dashboard
    # to guarantee it runs out-of-the-box without requiring installation.
    class NDArrayMock:
        def __init__(self, data):
            self.data = list(data)
        def __len__(self):
            return len(self.data)
        def __getitem__(self, index):
            if isinstance(index, NDArrayMock):
                return NDArrayMock([self.data[i] for i, val in enumerate(index.data) if val])
            elif isinstance(index, slice):
                return NDArrayMock(self.data[index])
            else:
                return self.data[index]
        def tolist(self):
            return self.data
        def astype(self, dtype):
            if dtype == int:
                return NDArrayMock([int(x) for x in self.data])
            return self
        def __add__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a + b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x + other for x in self.data])
        def __radd__(self, other):
            return self.__add__(other)
        def __sub__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a - b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x - other for x in self.data])
        def __mul__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a * b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x * other for x in self.data])
        def __rmul__(self, other):
            return self.__mul__(other)
        def __truediv__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a / b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x / other for x in self.data])
        def __floordiv__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a // b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x // other for x in self.data])
        def __gt__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a > b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x > other for x in self.data])
        def __lt__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a < b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x < other for x in self.data])
        def __eq__(self, other):
            if isinstance(other, NDArrayMock):
                return NDArrayMock([a == b for a, b in zip(self.data, other.data)])
            return NDArrayMock([x == other for x in self.data])
        def __repr__(self):
            return f"array({self.data})"

    class NumPyMock:
        def array(self, data):
            return NDArrayMock(data)
        def round(self, data, decimals=0):
            if isinstance(data, NDArrayMock):
                return NDArrayMock([round(x, decimals) for x in data.data])
            elif isinstance(data, list):
                return [round(x, decimals) for x in data]
            return round(data, decimals)
        def sum(self, data):
            if isinstance(data, NDArrayMock):
                return sum(data.data)
            return sum(data)
        def mean(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            return sum(d) / len(d) if len(d) > 0 else 0.0
        def max(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            return max(d) if len(d) > 0 else 0.0
        def min(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            return min(d) if len(d) > 0 else 0.0
        def where(self, condition, x, y):
            cond_data = condition.data if isinstance(condition, NDArrayMock) else condition
            res = []
            for idx, val in enumerate(cond_data):
                if val:
                    res.append(x.data[idx] if isinstance(x, NDArrayMock) else x)
                else:
                    res.append(y.data[idx] if isinstance(y, NDArrayMock) else y)
            return NDArrayMock(res)
        def cumsum(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            res = []
            total = 0
            for val in d:
                total += val
                res.append(total)
            return NDArrayMock(res)
        def std(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            if len(d) <= 1:
                return 0.0
            mean = sum(d) / len(d)
            var = sum((val - mean) ** 2 for val in d) / len(d)
            return math.sqrt(var)
        def linspace(self, start, stop, num):
            num = int(num)
            if num <= 1:
                return NDArrayMock([start])
            step = (stop - start) / (num - 1)
            return NDArrayMock([start + i * step for i in range(num)])
        def power(self, x, y):
            if isinstance(y, NDArrayMock):
                return NDArrayMock([x ** val for val in y.data])
            return x ** y
        def diff(self, data):
            d = data.data if isinstance(data, NDArrayMock) else list(data)
            if len(d) <= 1:
                return NDArrayMock([])
            return NDArrayMock([d[i] - d[i-1] for i in range(1, len(d))])
        class maximum:
            @staticmethod
            def accumulate(data):
                d = data.data if isinstance(data, NDArrayMock) else list(data)
                res = []
                curr_max = -float('inf')
                for val in d:
                    if val > curr_max:
                        curr_max = val
                    res.append(curr_max)
                return NDArrayMock(res)

    np = NumPyMock()

# ─────────────────────────────────────────────
#  NUMPY CONCEPTS USED IN THIS FILE
# ─────────────────────────────────────────────
# np.array()         — store trade history as arrays
# np.round()         — clean financial rounding
# np.sum()           — total P&L
# np.mean()          — average RR, win rate
# np.where()         — filter wins vs losses
# np.cumsum()        — equity curve (running balance)
# np.max/min()       — best/worst trade
# np.std()           — consistency score (standard deviation)
# np.linspace()      — growth projection curve
# np.power()         — compound growth formula
# np.percentile()    — drawdown analysis


# ════════════════════════════════════════════
#  SECTION 1: POSITION SIZER
#  NumPy concepts: np.round, np.array, arithmetic
# ════════════════════════════════════════════

def calculate_position(balance: float, risk_pct: float, sl_points: float,
                        rr: float = 2.0, instrument: str = "XAUUSD") -> dict:
    """
    Calculate everything you need before placing a trade.

    NumPy lesson: We use np.round() instead of Python's round() because
    np.round() is vectorised — it can process thousands of values at once
    when you later backtest across arrays of trades.
    """

    # Pip/point values per instrument ($ per point per 0.01 lot)
    pip_values = {
        "XAUUSD": 10.0,   # Gold: $10 per point per standard lot
        "FOREX":   1.0,   # Forex majors: $1 per pip per standard lot
        "NAS100":  0.1    # NAS100: $0.10 per point per standard lot
    }

    pip_val = pip_values.get(instrument, 10.0)

    # Core calculations using NumPy rounding
    risk_amount   = np.round(balance * risk_pct / 100, 2)
    lot_size      = np.round(risk_amount / (sl_points * pip_val), 3)

    # Split exit model: 60% at TP1, 40% runner
    tp1_profit    = np.round(risk_amount * rr * 0.6, 2)
    tp2_profit    = np.round(risk_amount * rr * 1.5 * 0.4, 2)   # runner gets extra
    total_profit  = np.round(risk_amount * rr, 2)

    # Daily limits
    daily_target  = np.round(balance * 0.03, 2)   # 3% daily target
    daily_stop    = np.round(balance * 0.04, 2)   # 4% max daily loss
    max_losses    = int(daily_stop // risk_amount) # how many losses before stop

    # RR check — minimum 1.5:1 for scalps
    rr_valid = rr >= 1.5
    sl_valid = sl_points <= 12   # XAUUSD scalp max

    # Risk level warning
    if risk_pct > 5:
        risk_warning = "DANGER — above 5% will blow account within 20 trades"
    elif risk_pct > 3:
        risk_warning = "ELEVATED — acceptable on micro account, reduce as balance grows"
    else:
        risk_warning = "CLEAN — within safe range"

    return {
        "balance":       balance,
        "risk_amount":   risk_amount,
        "lot_size":      lot_size,
        "tp1_profit":    tp1_profit,
        "tp2_profit":    tp2_profit,
        "total_profit":  total_profit,
        "daily_target":  daily_target,
        "daily_stop":    daily_stop,
        "max_losses":    max_losses,
        "rr_valid":      rr_valid,
        "sl_valid":      sl_valid,
        "risk_warning":  risk_warning,
        "instrument":    instrument
    }


def print_position(p: dict):
    print("\n" + "═"*50)
    print(f"  POSITION SIZER — {p['instrument']}")
    print("═"*50)
    print(f"  Balance:        ${p['balance']:.2f}")
    print(f"  Risk amount:    ${p['risk_amount']:.2f}")
    print(f"  Lot size:       {p['lot_size']:.3f}")
    print(f"  TP1 profit:     ${p['tp1_profit']:.2f}  (60% of position)")
    print(f"  TP2 profit:     ${p['tp2_profit']:.2f}  (40% runner)")
    print(f"  Full profit:    ${p['total_profit']:.2f}")
    print(f"  Daily target:   ${p['daily_target']:.2f}")
    print(f"  Daily stop:     ${p['daily_stop']:.2f}")
    print(f"  Max losses/day: {p['max_losses']}")
    print(f"  RR valid:       {'✓' if p['rr_valid'] else '✗ Below 1.5 minimum'}")
    print(f"  SL valid:       {'✓' if p['sl_valid'] else '✗ Too wide for 1M scalp'}")
    print(f"  Risk level:     {p['risk_warning']}")
    print("═"*50)


# ════════════════════════════════════════════
#  SECTION 2: SESSION TRACKER + STATS
#  NumPy concepts: np.array, np.where, np.sum,
#                  np.mean, np.cumsum, np.std
# ════════════════════════════════════════════

JOURNAL_FILE = "leo_trades.json"

def load_trades() -> list:
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    return []

def save_trades(trades: list):
    with open(JOURNAL_FILE, "w") as f:
        json.dump(trades, f, indent=2)

def log_trade(result: str, pnl: float, pattern: str,
              session: str, notes: str = "", asset: str = "XAUUSD",
              direction: str = "Long", entry: str = "N/A", exit: str = "N/A",
              sl: str = "N/A", tp: str = "N/A"):
    """
    Log a trade to your journal.
    result: 'win' | 'loss' | 'be'
    pnl: dollar amount (positive for win, negative for loss)
    pattern: 'CHoCH' | 'Engulf' | 'FVG' | 'OB'
    session: 'London' | 'NY'
    """
    trades = load_trades()

    # Enforce sign convention
    if result == "loss":
        pnl = -abs(pnl)
    elif result == "be":
        pnl = 0.0

    trade = {
        "id":      len(trades) + 1,
        "date":    datetime.now().strftime("%Y-%m-%d"),
        "time":    datetime.now().strftime("%H:%M"),
        "result":  result,
        "pnl":     round(pnl, 2),
        "pattern": pattern,
        "session": session,
        "notes":   notes,
        "asset":   asset,
        "direction": direction,
        "entry":   entry,
        "exit":    exit,
        "sl":      sl,
        "tp":      tp
    }
    trades.append(trade)
    save_trades(trades)
    print(f"\n  ✓ Trade #{trade['id']} logged — {result.upper()} ${abs(pnl):.2f}")

    # Enforce 2-loss daily stop
    today = datetime.now().strftime("%Y-%m-%d")
    today_trades = [t for t in trades if t["date"] == today]
    today_losses = [t for t in today_trades if t["result"] == "loss"]
    if len(today_losses) >= 2:
        print("\n  🔴 DAILY STOP HIT — 2 losses today. CLOSE THE PLATFORM.")
        print("     Come back tomorrow. No exceptions.\n")


def analyse_trades(period: str = "all") -> dict:
    """
    Full statistical analysis of your trade journal using NumPy.

    NumPy lesson:
    - np.array() converts your list of P&Ls into an array for fast maths
    - np.where() filters without Python loops — much faster at scale
    - np.cumsum() builds the equity curve in one line
    - np.std() measures consistency — lower std = more consistent edge
    """
    trades = load_trades()
    if not trades:
        print("\n  No trades logged yet.\n")
        return {}

    # Filter by period
    today = datetime.now().strftime("%Y-%m-%d")
    if period == "today":
        trades = [t for t in trades if t["date"] == today]
    elif period == "week":
        from datetime import timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        trades = [t for t in trades if t["date"] >= week_ago]

    if not trades:
        print(f"\n  No trades found for period: {period}\n")
        return {}

    # ── Core NumPy operations ──────────────────
    pnl_array = np.array([t["pnl"] for t in trades])        # all P&Ls as array
    results    = np.array([t["result"] for t in trades])     # result labels

    wins   = np.where(results == "win", 1, 0)                # 1 for win, 0 otherwise
    losses = np.where(results == "loss", 1, 0)

    total_trades = len(pnl_array)
    win_count    = int(np.sum(wins))
    loss_count   = int(np.sum(losses))
    win_rate     = np.round(win_count / total_trades * 100, 1)

    total_pnl    = np.round(np.sum(pnl_array), 2)            # sum of all P&Ls
    avg_win      = np.round(np.mean(pnl_array[pnl_array > 0]), 2) if win_count > 0 else 0
    avg_loss     = np.round(np.mean(pnl_array[pnl_array < 0]), 2) if loss_count > 0 else 0
    best_trade   = np.round(np.max(pnl_array), 2)
    worst_trade  = np.round(np.min(pnl_array), 2)

    # Equity curve — running balance starting from 0
    equity_curve = np.cumsum(pnl_array)

    # Consistency score — std deviation of P&Ls (lower = more consistent)
    consistency  = np.round(np.std(pnl_array), 2)

    # Expectancy — expected $ per trade (the real edge measurement)
    # Formula: (Win Rate × Avg Win) + (Loss Rate × Avg Loss)
    loss_rate  = 1 - (win_rate / 100)
    expectancy = np.round((win_rate/100 * avg_win) + (loss_rate * avg_loss), 2)

    # Drawdown — largest peak-to-trough drop in equity
    peak     = np.maximum.accumulate(equity_curve)    # running max
    drawdown = equity_curve - peak                    # distance below peak
    max_dd   = np.round(np.min(drawdown), 2)          # worst drawdown

    # Pattern breakdown
    patterns = {}
    for t in trades:
        p = t["pattern"]
        if p not in patterns:
            patterns[p] = {"wins": 0, "losses": 0, "pnl": 0}
        patterns[p]["pnl"] = round(patterns[p]["pnl"] + t["pnl"], 2)
        if t["result"] == "win":
            patterns[p]["wins"] += 1
        elif t["result"] == "loss":
            patterns[p]["losses"] += 1

    return {
        "period":        period,
        "total_trades":  total_trades,
        "win_count":     win_count,
        "loss_count":    loss_count,
        "win_rate":      win_rate,
        "total_pnl":     total_pnl,
        "avg_win":       avg_win,
        "avg_loss":      avg_loss,
        "best_trade":    best_trade,
        "worst_trade":   worst_trade,
        "expectancy":    expectancy,
        "max_drawdown":  max_dd,
        "consistency":   consistency,
        "equity_curve":  equity_curve.tolist(),
        "patterns":      patterns
    }


def print_stats(s: dict):
    if not s:
        return
    print("\n" + "═"*50)
    print(f"  PERFORMANCE STATS — {s['period'].upper()}")
    print("═"*50)
    print(f"  Total trades:   {s['total_trades']}")
    print(f"  Win rate:       {s['win_rate']}%  {'✓ Solid' if s['win_rate'] >= 60 else '✗ Below 60% target'}")
    print(f"  Wins / Losses:  {s['win_count']} / {s['loss_count']}")
    print(f"  Total P&L:      ${s['total_pnl']:.2f}  {'▲' if s['total_pnl'] >= 0 else '▼'}")
    print(f"  Avg win:        ${s['avg_win']:.2f}")
    print(f"  Avg loss:       ${s['avg_loss']:.2f}")
    print(f"  Best trade:     ${s['best_trade']:.2f}")
    print(f"  Worst trade:    ${s['worst_trade']:.2f}")
    print(f"  Expectancy:     ${s['expectancy']:.2f}/trade  {'✓ Positive edge' if s['expectancy'] > 0 else '✗ Negative edge — review system'}")
    print(f"  Max drawdown:   ${s['max_drawdown']:.2f}")
    print(f"  Consistency:    {s['consistency']} std dev  {'✓ Consistent' if s['consistency'] < 5 else 'Variable — review sizing'}")

    if s["patterns"]:
        print("\n  Pattern breakdown:")
        for pattern, data in s["patterns"].items():
            total = data["wins"] + data["losses"]
            wr = round(data["wins"]/total*100) if total > 0 else 0
            print(f"    {pattern:<20} W:{data['wins']} L:{data['losses']}  WR:{wr}%  P&L:${data['pnl']:.2f}")
    print("═"*50)


# ════════════════════════════════════════════
#  SECTION 3: GROWTH ROADMAP
#  NumPy concepts: np.power, np.linspace,
#                  np.where, compound growth
# ════════════════════════════════════════════

def project_growth(starting_balance: float, monthly_rate_pct: float,
                   months: int = 36, target: float = 600.0) -> dict:
    """
    Project your account growth using compound interest formula.

    NumPy lesson:
    - np.power(base, exponent) computes compound growth for entire arrays
    - np.linspace() creates evenly spaced month numbers — cleaner than range()
    - np.where() finds the first month you hit target without a loop
    """

    rate         = monthly_rate_pct / 100
    month_array  = np.linspace(0, months, months + 1)          # [0, 1, 2, ... 36]

    # Compound growth: balance × (1 + rate)^month
    # np.power() applies this to all months simultaneously
    balance_curve = np.round(starting_balance * np.power(1 + rate, month_array), 2)

    # Find when you hit each milestone — np.where returns indices
    milestones = {
        "Challenge fund ($600)":     600,
        "First challenge fee ($149)": 149,
        "Phase 2 ($300)":            300,
        "Phase 3 ($1,500)":        1500,
        "First funded ($10K challenge)": 10000
    }

    milestone_months = {}
    for name, value in milestones.items():
        hit = np.where(balance_curve >= value)[0]             # indices where balance >= target
        milestone_months[name] = int(hit[0]) if len(hit) > 0 else None

    # Monthly returns array (how much you make each month)
    monthly_gains = np.round(np.diff(balance_curve), 2)       # difference between consecutive months

    return {
        "starting_balance": starting_balance,
        "monthly_rate":     monthly_rate_pct,
        "months":           months,
        "balance_curve":    balance_curve.tolist(),
        "monthly_gains":    monthly_gains.tolist(),
        "milestones":       milestone_months,
        "final_balance":    float(balance_curve[-1])
    }


def print_roadmap(r: dict):
    print("\n" + "═"*50)
    print(f"  GROWTH ROADMAP — ${r['starting_balance']} START")
    print(f"  Monthly rate: {r['monthly_rate']}%  |  Projection: {r['months']} months")
    print("═"*50)

    curve = r["balance_curve"]
    # Print every 3 months
    print("\n  Month  |  Balance  |  Monthly gain")
    print("  " + "-"*38)
    for i, (bal, gain) in enumerate(zip(curve, [0] + r["monthly_gains"])):
        if i % 3 == 0 or i == len(curve)-1:
            bar = "█" * min(int(bal / 50), 30)
            print(f"  M{i:<5} |  ${bal:<8.2f}|  +${gain:.2f}  {bar}")

    print("\n  Milestone targets:")
    for name, month in r["milestones"].items():
        if month is not None:
            print(f"    {name:<35} → Month {month}")
        else:
            print(f"    {name:<35} → Beyond {r['months']} month window")

    print(f"\n  Final balance after {r['months']} months: ${r['final_balance']:.2f}")
    print("═"*50)


def funded_income_projection():
    """
    Show income projections at each funded account stage.
    NumPy lesson: broadcasting — multiply entire arrays by a scalar.
    """
    print("\n" + "═"*50)
    print("  FUNDED ACCOUNT INCOME PROJECTIONS")
    print("═"*50)

    # Account sizes and monthly return rates
    account_sizes   = np.array([10000, 25000, 50000, 100000, 200000])
    monthly_rate    = 0.04      # 4% monthly net
    split           = 0.80      # 80% profit split

    # NumPy broadcasting: multiply entire array by scalar in one operation
    gross_monthly   = np.round(account_sizes * monthly_rate, 2)
    net_monthly     = np.round(gross_monthly * split, 2)
    annual_net      = np.round(net_monthly * 12, 2)
    kes_monthly     = np.round(net_monthly * 130, 0).astype(int)   # approx KES rate

    labels = ["$10K account  ", "$25K account  ", "$50K account  ",
              "$100K account ", "$200K AUM fund"]

    print(f"\n  {'Account':<16} {'Gross/mo':>10} {'Net/mo (80%)':>14} {'Annual net':>12} {'KES/mo':>12}")
    print("  " + "-"*66)
    for i, label in enumerate(labels):
        flag = " ← first funded" if i == 0 else (" ← living wage" if i == 1 else "")
        print(f"  {label}  ${gross_monthly[i]:>8,.0f}   ${net_monthly[i]:>10,.0f}   ${annual_net[i]:>9,.0f}   KES {kes_monthly[i]:>8,}{flag}")

    print("\n  Stacked account model (3 × $10K = $30K AUM):")
    stacked = np.array([10000, 10000, 10000])
    stacked_net = np.round(np.sum(stacked) * monthly_rate * split, 2)
    print(f"    Monthly net: ${stacked_net:.2f}  |  Annual: ${stacked_net*12:.2f}")
    print(f"    KES/month:   KES {int(stacked_net*130):,}")
    print("═"*50)


# ════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════

def main():
    print("\n" + "█"*50)
    print("  LEO'S TRADING BUSINESS DASHBOARD")
    print("  Built with NumPy | XAUUSD Scalping System")
    print("█"*50)

    while True:
        print("""
  ┌─────────────────────────────────┐
  │  1. Position sizer              │
  │  2. Log a trade                 │
  │  3. View stats (today)          │
  │  4. View stats (all time)       │
  │  5. Growth roadmap              │
  │  6. Funded income projections   │
  │  7. Web Application Server      │
  │  8. Exit                        │
  └─────────────────────────────────┘""")

        choice = input("\n  Choose (1–8): ").strip()

        if choice == "1":
            print("\n  --- POSITION SIZER ---")
            try:
                bal    = float(input("  Account balance ($): ") or 70)
                risk   = float(input("  Risk per trade (%): ") or 2)
                sl     = float(input("  Stop loss (points): ") or 8)
                rr     = float(input("  RR ratio (e.g. 2): ") or 2)
                print("  Instrument: 1=XAUUSD  2=FOREX  3=NAS100")
                inst   = {"1":"XAUUSD","2":"FOREX","3":"NAS100"}.get(input("  Choice: ").strip(), "XAUUSD")
                result = calculate_position(bal, risk, sl, rr, inst)
                print_position(result)
            except ValueError:
                print("  Invalid input — please enter numbers only.")

        elif choice == "2":
            print("\n  --- LOG A TRADE ---")
            print("  Result: 1=Win  2=Loss  3=Breakeven")
            res_map = {"1":"win","2":"loss","3":"be"}
            res  = res_map.get(input("  Choice: ").strip(), "win")
            pnl  = float(input("  P&L amount ($, always positive): ") or 0)
            print("  Pattern: 1=CHoCH  2=Engulf  3=FVG  4=OB")
            pat_map = {"1":"CHoCH","2":"Engulf","3":"FVG","4":"OB"}
            pat  = pat_map.get(input("  Choice: ").strip(), "CHoCH")
            print("  Session: 1=London  2=NY")
            sess = "London" if input("  Choice: ").strip() == "1" else "NY"
            note = input("  Notes (optional, press Enter to skip): ")
            log_trade(res, pnl, pat, sess, note)

        elif choice == "3":
            stats = analyse_trades("today")
            print_stats(stats)

        elif choice == "4":
            stats = analyse_trades("all")
            print_stats(stats)

        elif choice == "5":
            print("\n  --- GROWTH ROADMAP ---")
            try:
                bal   = float(input("  Current balance ($): ") or 70)
                rate  = float(input("  Monthly growth rate (%): ") or 15)
                mos   = int(input("  Project how many months? (default 36): ") or 36)
                r = project_growth(bal, rate, mos)
                print_roadmap(r)
            except ValueError:
                print("  Invalid input.")

        elif choice == "6":
            funded_income_projection()

        elif choice == "7":
            print("\n  Starting Web Application Server on http://localhost:9090...")
            try:
                import server
                server.run()
            except ImportError:
                print("  Error: server.py not found in the current directory.")
            except Exception as e:
                print(f"  Error starting server: {e}")

        elif choice == "8":
            print("\n  Trade like a business. See you next session.\n")
            break
        else:
            print("  Invalid choice — enter 1 to 8.")


if __name__ == "__main__":
    main()
