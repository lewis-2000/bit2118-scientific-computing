# Epidemic Planner

**BIT 2118 Scientific Computing: Group Project**

A desktop app that models an outbreak and helps decide when and how strongly to intervene so that hospitals are not overwhelmed. Built with NumPy, SciPy and Matplotlib, with a Tkinter user interface.

- Name: _your name_
- GitHub: _your username_
- Group members: _names_

---

## 1. The problem

An outbreak starts in a population of 1,000,000 people. Hospitals can treat at most 50,000 infected people at the same time. Questions the app answers:

1. How large will the outbreak get, and when does it peak?
2. If we act (for example, reduce contact between people), does the peak stay under hospital capacity?
3. What is the latest day we can act, and what is the smallest reduction in contact that works?
4. If we are unsure about how infectious the disease is, how likely is an overload?

## 2. Installation and running

```
pip install -r requirements.txt
python epidemic_planner.py
```

Tkinter ships with the standard Python installer on Windows and macOS. On Ubuntu/Debian, install it with `sudo apt install python3-tk`.

## 3. The model

The population is split into Susceptible (S), Infected (I) and Recovered (R). The SIR equations are:

```
dS/dt = -beta * S * I / N
dI/dt =  beta * S * I / N - gamma * I
dR/dt =  gamma * I
```

- **beta**: infection rate (how fast infected people pass the disease on)
- **gamma**: recovery rate (fixed at 0.10, so an infection lasts about 10 days)
- **R0 = beta / gamma**: people infected by one case. Above 1 the outbreak grows.
- **Intervention:** from the chosen day, beta is multiplied by (1 - contact reduction). The switch is smoothed over about one day so the solver handles it well.

## 4. Inputs and what the program does with them (Instruction B)

| Input | Where set | Default | Meaning |
|---|---|---|---|
| beta | slider (Tab 1) or fitted (Tab 2) | 0.32 | infection rate |
| Intervention day | slider | 20 | day contact reduction starts |
| Contact reduction | slider | 0.6 | fraction by which contacts fall |
| N | constant in code | 1,000,000 | population |
| I0 | constant in code | 100 | initial infected |
| CAPACITY | constant in code | 50,000 | hospital capacity |
| GAMMA | constant in code | 0.10 | recovery rate |

## 5. How each tool uses the course tasks

| Task | Mathematical concept | Function in code | What it does here |
|---|---|---|---|
| 18 ODEs with SciPy | `solve_ivp` | `simulate` | solves the SIR equations over 200 days |
| 13 Interpolation | linear interpolation, `interp1d` | `fill_gaps` | estimates infected counts on days with no report |
| 14 Curve fitting | least squares, `curve_fit` | `fit_beta` | finds beta that makes the model match the data |
| 15 Numerical differentiation | `np.gradient` | `update_sim` | new cases per day = rate of change of cumulative cases |
| 16 Numerical integration | Simpson's rule, `simpson` | `update_sim` | total people infected = area under the new-case curve |
| 10/11 Root finding | Brent's method, `root_scalar` | `latest_safe_day` | solves peak(day) - capacity = 0 for the day |
| 19 Optimization | `minimize_scalar` | `cheapest_reduction` | smallest contact reduction with peak at or under capacity (constraint handled by a penalty) |
| 20 Monte Carlo | random sampling | `monte_carlo` | draws 200 random betas (normal, standard deviation 0.03) and counts how often the peak exceeds capacity |

## 6. How to use the app

**Tab 1: Simulation.** Drag the sliders. The grey dashed line is the outbreak with no action, the blue line is with the intervention, the dotted red line is hospital capacity, and the red shaded area is the overload. The readout shows R0, peak day, peak infected, peak new cases per day, total ever infected, and whether capacity is exceeded.

**Tab 2: Fit to data.** Click *Load demo outbreak data*. Six days are missing from the data. The app fills them by interpolation (orange points), fits beta to the data (curve), and copies the result to Tab 1.

**Tab 3: Planning tools.** These use the current Tab 1 settings.
- *Latest safe intervention day*: the last day you can start the current contact reduction and still stay under capacity.
- *Cheapest contact reduction*: the smallest reduction that keeps the peak under capacity, for the chosen intervention day.
- *Overload probability*: runs 200 simulations with random beta and shows a histogram of peak sizes.

## 7. Results with the default settings (Instruction D)

| Result | Value | Meaning |
|---|---|---|
| R0 | 3.20 | each case infects about 3 others, so the outbreak grows fast |
| Peak with no intervention | about 324,000 infected | more than six times hospital capacity |
| Peak with day 20 and 60% reduction | about 31,000 infected | stays under capacity |
| Latest safe day (60% reduction) | about day 27 | acting later pushes the peak over 50,000 |
| Cheapest reduction (acting day 20) | about 56% | the minimum that keeps the peak under capacity |
| Overload probability | about 16% | with beta uncertain by plus or minus 0.03, there is still a risk |
| Fitted beta (demo data) | 0.320 | matches the value used to create the demo data |

Reading the graph: without action the infection curve rises steeply and peaks around day 46 at a level far above the red capacity line. Intervention flattens and lowers the curve, which is the "flatten the curve" effect. With the default intervention the peak is delayed to about day 108, and it is much smaller.

## 8. Changing a parameter (Instruction C)

Contact reduction, with infection starting on day 20:

| Contact reduction | Peak infected | Over capacity? |
|---|---|---|
| 40% | about 142,000 | yes |
| 50% | about 85,000 | yes |
| 60% | about 31,000 | no |
| 70% | about 7,800 | no |

Increasing contact reduction lowers the effective infection rate. R0 falls from 3.2 to 1.6 at 50% and to 0.96 at 70%. Once R0 drops near or below 1, the outbreak barely grows after the intervention.

Intervention day, with 60% reduction:

| Intervention day | Peak infected |
|---|---|
| 10 | about 26,500 |
| 20 | about 31,500 |
| 25 | about 42,300 |

Acting later lets more people become infected before contact falls, so the peak grows. The relationship is not linear: the closer you get to day 27, the faster the peak rises toward capacity.

## 9. Assumptions and limitations

- Everyone mixes equally with everyone else (no age groups, no geography).
- beta and gamma are constant, apart from the intervention.
- Recovered people are immune permanently.
- No births, deaths or travel.
- gamma is fixed because early case data can only identify the difference beta - gamma, not each separately.
- The intervention is modelled as an instant, smooth change of beta, which is simpler than how real policies take effect.
- The demo data is simulated with noise, not real case data. To use real data, replace the arrays in `demo_data()` with your own days and case counts.

## 10. Modified related case (Instruction E)

_Fill this in for your own repository. Choose one related case, change the constants at the top of `epidemic_planner.py`, and document it here._

Example structure:

- **Case:** _e.g. a flu outbreak in a school_
- **New assumptions:** _population, initial infected, recovery period, capacity, what the intervention represents_
- **New input data:** _N, I0, CAPACITY, GAMMA, beta range_
- **Output:** _peak, peak day, latest safe day, cheapest reduction, overload probability_
- **Interpretation:** _what the results mean for that case_

Suggested related cases: a school flu outbreak (small N, 10 to 14 day recovery, capacity as the number of students the sick bay can handle), a computer virus in a network (N as number of machines, capacity as IT staff cleanup limit), or rumour spread on social media.
