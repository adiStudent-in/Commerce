# Generate Ch 6 (Cost) graphs - matplotlib, econ textbook style (matches Ch-5 make_graphs.py)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE = "#1f77b4"
RED = "#d62728"

OUT = r"F:\Class 11\Study OS\Economics Markdown\Micro\Ch - 6"
OUTW = r"F:\Class 11\Study OS\Webpage\Economics"

def save(fig, name):
    fig.savefig(f"{OUT}\\{name}", dpi=160, bbox_inches="tight", facecolor="white")
    fig.savefig(f"{OUTW}\\{name}", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)

# ---- 1. TC, TFC, TVC curves (from lecture schedule, TFC = 12) ----
q = np.array([0, 1, 2, 3, 4, 5])
tfc = np.array([12, 12, 12, 12, 12, 12])
tvc = np.array([0, 6, 10, 15, 24, 35])
tc = tfc + tvc

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
xs = np.linspace(0, 5, 300)
ax.plot(xs, np.interp(xs, q, tc), color=BLUE, lw=2.4, label="TC")
ax.plot(xs, np.interp(xs, q, tvc), color=RED, lw=2.4, label="TVC")
ax.plot(xs, np.interp(xs, q, tfc), color="#999999", lw=2.0, ls="--", label="TFC")
ax.plot(q, tc, "o", color=BLUE, markersize=4.5)
ax.plot(q, tvc, "o", color=RED, markersize=4.5)
ax.axhline(0, color="#1b1b1b", lw=0.8)
ax.annotate("TC = TFC at zero output", xy=(0, 12), xytext=(0.25, 20),
            arrowprops=dict(arrowstyle="-|>", color="#1b1b1b", lw=1.1), fontsize=9.5, weight="bold")
ax.annotate("Vertical distance = TFC (constant)", xy=(3.5, 24), fontsize=9, color="#1b1b1b",
            ha="center", weight="bold")
ax.annotate("TVC starts from zero", xy=(0.4, 4), fontsize=9, color=RED, ha="center")
ax.set_xticks(q)
ax.set_xticklabels(q)
ax.set_yticks([0, 12, 24, 36, 48])
ax.set_ylim(-2, 52)
ax.set_xlabel("Output (in units)", fontsize=10.5)
ax.set_ylabel("Cost (in ₹)", fontsize=10.5)
ax.set_title("Total Cost (TC), Total Variable Cost (TVC) and Total Fixed Cost (TFC)",
             fontsize=12, weight="bold", pad=10)
ax.legend(loc="upper left", fontsize=10, frameon=False)
ax.grid(True, ls=":", lw=0.5, alpha=0.4)
save(fig, "Cost_TC_TFC_TVC.png")

# ---- 2. AFC curve - rectangular hyperbola (TFC = 12) ----
q2 = np.array([1, 2, 3, 4, 5])
afc = 12.0 / q2

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
xs = np.linspace(0.4, 5.4, 400)
ax.plot(xs, 12.0 / xs, color=BLUE, lw=2.4)
ax.plot(q2, afc, "o", color=BLUE, markersize=5)
ax.axhline(0, color="#1b1b1b", lw=0.8)
ax.annotate("AFC = TFC ÷ Q (rectangular hyperbola)", xy=(2.4, 6.8),
            fontsize=9.5, ha="center", weight="bold")
ax.annotate("AFC keeps falling\nbut never zero", xy=(4.3, 3.4), fontsize=9, color=RED,
            ha="center")
ax.annotate("Never touches X-axis", xy=(5.1, 0.7), fontsize=8.5, color=RED, ha="right")
ax.annotate("Never touches Y-axis", xy=(0.5, 13.5), fontsize=8.5, color=RED, ha="left",
            xytext=(1.1, 16.5), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0))
ax.set_xticks(q2)
ax.set_xticklabels(q2)
ax.set_yticks([0, 3, 6, 9, 12])
ax.set_ylim(0, 14)
ax.set_xlim(0, 5.5)
ax.set_xlabel("Output (in units)", fontsize=10.5)
ax.set_ylabel("Average Fixed Cost (in ₹)", fontsize=10.5)
ax.set_title("Average Fixed Cost (AFC) Curve", fontsize=12, weight="bold", pad=10)
ax.grid(True, ls=":", lw=0.5, alpha=0.4)
save(fig, "Cost_AFC_Curve.png")

# ---- 3. AC, AVC, MC curves (from lecture schedules) ----
q3 = np.array([1, 2, 3, 4, 5])
ac = np.array([18, 11, 9, 9, 9.40])
avc = np.array([6, 5, 5, 6, 7])
mc = np.array([6, 4, 5, 9, 11])

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
xs = np.linspace(1, 5, 300)
ax.plot(xs, np.interp(xs, q3, ac), color=BLUE, lw=2.4, label="AC")
ax.plot(xs, np.interp(xs, q3, avc), color=RED, lw=2.4, label="AVC")
ax.plot(xs, np.interp(xs, q3, mc), color="#1a5e4a", lw=2.4, label="MC")
ax.plot(q3, ac, "o", color=BLUE, markersize=4.5)
ax.plot(q3, avc, "o", color=RED, markersize=4.5)
ax.plot(q3, mc, "o", color="#1a5e4a", markersize=4.5)
ax.axhline(0, color="#1b1b1b", lw=0.8)
ax.annotate("MC cuts AVC at its minimum (B)", xy=(3, 5), xytext=(2.1, 8.6),
            arrowprops=dict(arrowstyle="-|>", color="#1b1b1b", lw=1.1), fontsize=9,
            ha="center", weight="bold")
ax.annotate("MC cuts AC at its minimum (A)", xy=(4, 9), xytext=(2.35, 14.5),
            arrowprops=dict(arrowstyle="-|>", color="#1b1b1b", lw=1.1), fontsize=9,
            ha="center", weight="bold")
ax.annotate("Gap = AFC\n(falls, never zero)", xy=(4.45, 8.2), xytext=(4.35, 6.2),
            fontsize=8.5, color=RED, ha="center")
ax.annotate("A", xy=(4, 9.05), fontsize=11, weight="bold", color=BLUE)
ax.annotate("B", xy=(3, 5.05), fontsize=11, weight="bold", color=RED)
ax.set_xticks(q3)
ax.set_xticklabels(q3)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_ylim(0, 21)
ax.set_xlim(0.8, 5.2)
ax.set_xlabel("Output (in units)", fontsize=10.5)
ax.set_ylabel("Cost (in ₹)", fontsize=10.5)
ax.set_title("Average Cost (AC), Average Variable Cost (AVC) and Marginal Cost (MC)",
             fontsize=12, weight="bold", pad=10)
ax.legend(loc="upper right", fontsize=10, frameon=False)
ax.grid(True, ls=":", lw=0.5, alpha=0.4)
save(fig, "Cost_AC_AVC_MC.png")

print("ALL COST GRAPHS DONE")