"""
Epidemic Planner - BIT 2118 Scientific Computing group project
Libraries: NumPy, SciPy, Matplotlib (embedded in a Tkinter window)

Problem: hospitals can hold CAPACITY patients at once. When must we act,
and how strongly, so the number of infected people never exceeds that?

Tasks used:
  13 interpolation        -> fill missing days in case data (interp1d)
  14 curve fitting        -> estimate beta from data (curve_fit)
  15 differentiation      -> new cases per day (np.gradient)
  16 integration          -> total people infected (simpson)
  10/11 root finding      -> latest safe intervention day (root_scalar)
  19 optimization         -> cheapest contact reduction (minimize_scalar)
  18 ODEs                 -> SIR model (solve_ivp)
  20 Monte Carlo          -> probability of overload when beta is uncertain
"""
import tkinter as tk
from tkinter import ttk

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit, root_scalar, minimize_scalar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Fixed assumptions (change these for your own case) -------
N = 1_000_000        # population
I0 = 100             # initially infected
DAYS = 200           # simulation length
CAPACITY = 50_000    # hospital capacity (people infected at once)
GAMMA = 0.10         # recovery rate (1/10 days), assumed known


# ---------------- Model and numerical routines -----------------------------
def sir(t, y, beta, gamma, t_int, reduction):
    """SIR equations. Contact reduction switches on smoothly at day t_int."""
    S, I, R = y
    b = beta * (1 - reduction / (1 + np.exp(-(t - t_int))))
    new = b * S * I / N
    return [-new, new - gamma * I, gamma * I]


def simulate(beta, gamma=GAMMA, t_int=0, reduction=0.0, t=None):
    t = np.linspace(0, DAYS, DAYS + 1) if t is None else t
    sol = solve_ivp(sir, (0, t[-1]), [N - I0, I0, 0], t_eval=t,
                    args=(beta, gamma, t_int, reduction), rtol=1e-7)
    return sol.t, sol.y[0], sol.y[1], sol.y[2]


def peak_infected(beta, t_int, reduction):
    return simulate(beta, GAMMA, t_int, reduction)[2].max()


def infected_model(t, beta):
    """Model used by curve_fit: infected count at times t for a given beta."""
    return simulate(beta, GAMMA, 0, 0.0, t)[2]


def demo_data():
    """Noisy first 40 days of an outbreak (true beta = 0.32), with gaps."""
    rng = np.random.default_rng(1)
    days = np.arange(0, 40, dtype=float)
    cases = infected_model(days, 0.32) * (1 + rng.normal(0, 0.05, len(days)))
    cases[[7, 8, 19, 27, 28, 29]] = np.nan          # days with no report
    return days, cases


def fill_gaps(days, cases):
    """Task 13: linear interpolation over missing days."""
    ok = ~np.isnan(cases)
    return interp1d(days[ok], cases[ok], kind="linear")(days)


def fit_beta(days, cases):
    """Task 14: least-squares fit of beta to the (filled) data."""
    (beta,), _ = curve_fit(infected_model, days, cases, p0=[0.25],
                           bounds=(0.11, 1.5))
    return beta


def latest_safe_day(beta, reduction):
    """Tasks 10/11: day where peak == CAPACITY (root of peak - capacity)."""
    f = lambda d: peak_infected(beta, d, reduction) - CAPACITY
    if f(0) > 0:
        return None            # even acting on day 0 is not enough
    if f(DAYS - 50) < 0:
        return float("inf")    # never a problem
    return root_scalar(f, bracket=[0, DAYS - 50], method="brentq", xtol=0.1).root


def cheapest_reduction(beta, t_int):
    """Task 19: minimise cost = reduction, subject to peak <= capacity.
    Constraint handled with a penalty term."""
    def cost(r):
        excess = max(0.0, peak_infected(beta, t_int, r) - CAPACITY)
        return r + excess / 1000.0
    res = minimize_scalar(cost, bounds=(0, 0.95), method="bounded",
                          options={"xatol": 1e-3})
    return res.x


def monte_carlo(beta, t_int, reduction, runs=200, spread=0.03):
    """Task 20: beta is uncertain -> probability that peak exceeds capacity."""
    rng = np.random.default_rng(42)
    betas = np.clip(rng.normal(beta, spread, runs), 0.12, None)
    peaks = np.array([peak_infected(b, t_int, reduction) for b in betas])
    return peaks, (peaks > CAPACITY).mean()


# ---------------- User interface -------------------------------------------
class App:
    SLIDERS = [("Infection rate (beta)", 0.12, 0.60, 0.32, 0.01),
               ("Intervention day", 0, 150, 20, 1),
               ("Contact reduction", 0, 0.9, 0.6, 0.05)]

    def __init__(self, root):
        root.title("Epidemic Planner")
        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True)
        self.tab1, self.tab2, self.tab3 = (ttk.Frame(nb) for _ in range(3))
        nb.add(self.tab1, text="1. Simulation")
        nb.add(self.tab2, text="2. Fit to data")
        nb.add(self.tab3, text="3. Planning tools")
        self.build_sim_tab()
        self.build_fit_tab()
        self.build_plan_tab()
        self.update_sim()

    # --- helper to put a matplotlib figure in a tab
    def make_plot(self, parent, side="right"):
        fig = Figure(figsize=(7, 4.6), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(side=side, fill="both", expand=True)
        return fig, canvas

    def params(self):
        return [v.get() for v in self.vars]       # beta, day, reduction

    # --- Tab 1: simulation
    def build_sim_tab(self):
        left = ttk.Frame(self.tab1, padding=10)
        left.pack(side="left", fill="y")
        self.vars = []
        for name, lo, hi, init, res in self.SLIDERS:
            v = tk.DoubleVar(value=init)
            tk.Scale(left, label=name, from_=lo, to=hi, resolution=res,
                     orient="horizontal", length=230, variable=v,
                     command=lambda _e: self.update_sim()).pack(pady=4)
            self.vars.append(v)
        self.readout = tk.Label(left, justify="left", font=("Consolas", 10))
        self.readout.pack(pady=15, anchor="w")
        self.fig1, self.canvas1 = self.make_plot(self.tab1)

    def update_sim(self):
        if len(self.vars) < 3:
            return
        beta, day, red = self.params()
        t, S, I, R = simulate(beta, GAMMA, day, red)
        _, _, I0_, _ = simulate(beta)                 # no intervention
        ax = self.fig1.clear() or self.fig1.add_subplot(111)
        ax.plot(t, I0_, "--", color="gray", label="No intervention")
        ax.plot(t, I, lw=2.5, label="With intervention")
        ax.axhline(CAPACITY, color="red", ls=":", label="Hospital capacity")
        ax.fill_between(t, I, CAPACITY, where=I > CAPACITY, color="red", alpha=.3)
        ax.axvline(day, color="green", alpha=.4)
        ax.set(xlabel="Day", ylabel="Currently infected", title="Infection curve")
        ax.legend(); ax.grid(alpha=.3)
        self.fig1.tight_layout(); self.canvas1.draw_idle()

        pk = I.argmax()
        new_cases = np.gradient(N - S, t)                    # Task 15
        total = simpson(new_cases, x=t)                      # Task 16
        self.readout.config(text=(
            f"R0 = {beta / GAMMA:.2f}\n"
            f"Peak day: {t[pk]:.0f}\n"
            f"Peak infected: {I[pk]:,.0f}\n"
            f"Peak new cases/day: {new_cases.max():,.0f}\n"
            f"Total ever infected: {total:,.0f}\n"
            f"Over capacity: {'YES' if I[pk] > CAPACITY else 'no'}"))

    # --- Tab 2: fit to data
    def build_fit_tab(self):
        left = ttk.Frame(self.tab2, padding=10)
        left.pack(side="left", fill="y")
        ttk.Button(left, text="Load demo outbreak data",
                   command=self.run_fit).pack(fill="x", pady=5)
        self.fit_text = tk.Label(left, justify="left", font=("Consolas", 10),
                                 text="Click the button.\n\nSteps:\n"
                                      "1. Some days are missing\n"
                                      "2. interp1d fills the gaps\n"
                                      "3. curve_fit estimates beta")
        self.fit_text.pack(pady=15, anchor="w")
        self.fig2, self.canvas2 = self.make_plot(self.tab2)

    def run_fit(self):
        days, raw = demo_data()
        filled = fill_gaps(days, raw)
        beta = fit_beta(days, filled)
        t = np.linspace(0, 60, 200)
        ax = self.fig2.clear() or self.fig2.add_subplot(111)
        ax.scatter(days, filled, s=15, color="orange", label="Interpolated (gaps filled)")
        ax.scatter(days, raw, s=15, color="black", label="Reported data")
        ax.plot(t, infected_model(t, beta), lw=2, label=f"Fitted model, beta={beta:.3f}")
        ax.set(xlabel="Day", ylabel="Currently infected", title="Fitting beta to data")
        ax.legend(); ax.grid(alpha=.3)
        self.fig2.tight_layout(); self.canvas2.draw_idle()
        self.vars[0].set(round(beta, 2))               # send to Tab 1
        self.update_sim()
        self.fit_text.config(text=(
            f"Missing days: {int(np.isnan(raw).sum())}\n"
            f"Fitted beta: {beta:.3f}\n"
            f"Fitted R0: {beta / GAMMA:.2f}\n\n"
            "(beta copied to Tab 1)"))

    # --- Tab 3: planning tools
    def build_plan_tab(self):
        left = ttk.Frame(self.tab3, padding=10)
        left.pack(side="left", fill="y")
        for text, cmd in [("Latest safe intervention day", self.do_day),
                          ("Cheapest contact reduction", self.do_opt),
                          ("Overload probability (Monte Carlo)", self.do_mc)]:
            ttk.Button(left, text=text, command=cmd).pack(fill="x", pady=5)
        self.plan_text = tk.Label(left, justify="left", font=("Consolas", 10),
                                  wraplength=260, text="Uses beta, day and\n"
                                  "reduction from Tab 1.")
        self.plan_text.pack(pady=15, anchor="w")
        self.fig3, self.canvas3 = self.make_plot(self.tab3)

    def do_day(self):
        beta, _, red = self.params()
        d = latest_safe_day(beta, red)
        if d is None:
            msg = "Not possible: even acting on day 0\nwith this reduction is not enough."
        elif d == float("inf"):
            msg = "Capacity is never exceeded."
        else:
            msg = f"Latest safe day: {d:.1f}\n(with {red:.0%} contact reduction)"
            t, _, I, _ = simulate(beta, GAMMA, d, red)
            ax = self.fig3.clear() or self.fig3.add_subplot(111)
            ax.plot(t, I, lw=2); ax.axhline(CAPACITY, color="red", ls=":")
            ax.axvline(d, color="green", alpha=.5)
            ax.set(xlabel="Day", ylabel="Currently infected",
                   title=f"Acting on day {d:.0f} just touches capacity")
            ax.grid(alpha=.3); self.fig3.tight_layout(); self.canvas3.draw_idle()
        self.plan_text.config(text=msg)

    def do_opt(self):
        beta, day, _ = self.params()
        r = cheapest_reduction(beta, day)
        t, _, I, _ = simulate(beta, GAMMA, day, r)
        ax = self.fig3.clear() or self.fig3.add_subplot(111)
        ax.plot(t, I, lw=2); ax.axhline(CAPACITY, color="red", ls=":")
        ax.set(xlabel="Day", ylabel="Currently infected",
               title=f"Smallest reduction that works: {r:.0%}")
        ax.grid(alpha=.3); self.fig3.tight_layout(); self.canvas3.draw_idle()
        self.plan_text.config(text=f"Cheapest reduction: {r:.1%}\n"
                                   f"(intervention on day {day:.0f})")

    def do_mc(self):
        beta, day, red = self.params()
        peaks, p = monte_carlo(beta, day, red)
        ax = self.fig3.clear() or self.fig3.add_subplot(111)
        ax.hist(peaks, bins=25, color="steelblue")
        ax.axvline(CAPACITY, color="red", ls=":", label="Capacity")
        ax.set(xlabel="Peak infected", ylabel="Number of runs",
               title="Peak size when beta is uncertain (200 runs)")
        ax.legend(); self.fig3.tight_layout(); self.canvas3.draw_idle()
        self.plan_text.config(text=f"Probability of overload:\n{p:.1%}")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()