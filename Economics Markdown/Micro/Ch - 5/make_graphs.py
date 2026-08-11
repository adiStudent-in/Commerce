# Generate Ch 5 (Production Function) graphs — matplotlib, econ textbook style
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"
BLUE = "#1f77b4"
RED = "#d62728"
GREY = "#666666"

OUT = r"F:\Class 11\Study OS\Economics Markdown\Micro\Ch - 5"
OUTW = r"F:\Class 11\Study OS\Webpage\Economics"


def save(fig, name):
    fig.savefig(f"{OUT}\\{name}", dpi=160, bbox_inches="tight", facecolor="white")
    fig.savefig(f"{OUTW}\\{name}", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# ── 1. Production flow diagram ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

# Inputs box
ax.add_patch(mpatches.FancyBboxPatch((0.4, 1.2), 2.6, 3.6, boxstyle="round,pad=0.08",
             fc="#e8f0ec", ec=BLUE, lw=1.6))
ax.text(1.7, 4.15, "INPUTS", ha="center", va="center", fontsize=11, weight="bold", color="#1a5e4a")
ax.text(1.7, 3.25, "Land", ha="center", fontsize=10)
ax.text(1.7, 2.65, "Labour", ha="center", fontsize=10)
ax.text(1.7, 2.05, "Capital", ha="center", fontsize=10)
ax.text(1.7, 1.45, "Raw material", ha="center", fontsize=10)

# Production process box
ax.add_patch(mpatches.FancyBboxPatch((4.4, 1.2), 2.6, 3.6, boxstyle="round,pad=0.08",
             fc="#fff8e5", ec="#d4a12a", lw=1.6))
ax.text(5.7, 4.15, "PRODUCTION", ha="center", va="center", fontsize=11, weight="bold", color="#8b6914")
ax.text(5.7, 3.3, "Transformation", ha="center", fontsize=10)
ax.text(5.7, 2.6, "Process", ha="center", fontsize=10)
ax.text(5.7, 1.8, "(Factory / Firm)", ha="center", fontsize=9.5)

# Output box
ax.add_patch(mpatches.FancyBboxPatch((8.4, 1.2), 1.6, 3.6, boxstyle="round,pad=0.08",
             fc="#e8f0ec", ec=BLUE, lw=1.6))
ax.text(9.2, 4.15, "OUTPUT", ha="center", va="center", fontsize=11, weight="bold", color="#1a5e4a")
ax.text(9.2, 3.25, "Finished", ha="center", fontsize=10)
ax.text(9.2, 2.65, "Goods", ha="center", fontsize=10)
ax.text(9.2, 1.9, "Wheat\u2192Atta", ha="center", fontsize=9)

for x0, x1 in [(3.05, 4.35), (7.05, 8.35)]:
    ax.annotate("", xy=(x1, 3.0), xytext=(x0, 3.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#1b1b1b"))
ax.text(3.65, 3.35, "Combined", ha="center", fontsize=9.5, color=GREY)
ax.text(7.6, 3.35, "Goods", ha="center", fontsize=9.5, color=GREY)
ax.text(5.7, 0.35, "Production = transformation of inputs into output", ha="center",
        fontsize=11, weight="bold", color="#1b1b1b")
save(fig, "Production_Function_Flow.png")


# ── 2. TP & MP curves with 3 phases (Law of Variable Proportions) ────────────
labour = np.array([1, 2, 3, 4, 5, 6])
tp = np.array([10, 30, 45, 52, 52, 48])
mp = np.array([10, 20, 15, 7, 0, -4])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 8.2), sharex=False)
for ax in (ax1, ax2):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# TP curve
ax1.plot(labour, tp, "-o", color=BLUE, lw=2.2, markersize=5, zorder=3, label="TP")
# smooth spline
xs = np.linspace(1, 6, 300)
tps = np.interp(xs, labour, tp)
ax1.plot(xs, tps, color=BLUE, lw=2.2, zorder=2)
ax1.annotate("Point of Inflexion (Q)", xy=(2.25, 35), fontsize=9.5, color=RED,
             ha="center", weight="bold")
ax1.annotate("M (TP is maximum)", xy=(5, 53), xytext=(4.2, 58),
             arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2), fontsize=9.5,
             color=RED, weight="bold")
ax1.annotate("TP falls", xy=(5.7, 49.5), fontsize=9, color=RED, ha="center")
ax1.axhline(0, color="#1b1b1b", lw=0.8)
ax1.set_xticks(labour)
ax1.set_xticklabels([])
ax1.set_yticks([0, 10, 20, 30, 40, 50])
ax1.set_ylim(-2, 62)
ax1.set_ylabel("Total Product (in units)", fontsize=10.5)
ax1.set_title("Total Product (TP) Curve", fontsize=12, weight="bold", pad=10)
ax1.legend(loc="lower right", fontsize=10, frameon=False)

# MP curve
ax2.axhline(0, color="#1b1b1b", lw=0.8)
ax2.plot(labour, mp, "-o", color=RED, lw=2.2, markersize=5, zorder=3, label="MP")
ax2.annotate("MP is maximum (20)", xy=(2, 20), xytext=(2.5, 24),
             arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2), fontsize=9.5,
             color=BLUE, weight="bold")
ax2.annotate("S (MP = 0)", xy=(5, 0), xytext=(4.5, 4.5),
             arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2), fontsize=9.5,
             color=BLUE, weight="bold")
ax2.annotate("MP negative", xy=(5.85, -3.2), fontsize=9, color=BLUE, ha="center")
ax2.set_xticks(labour)
ax2.set_xticklabels(labour)
ax2.set_yticks([-4, 0, 10, 20])
ax2.set_ylim(-8, 27)
ax2.set_xlabel("Units of Variable Factor (Labour)", fontsize=10.5)
ax2.set_ylabel("Marginal Product (in units)", fontsize=10.5)
ax2.set_title("Marginal Product (MP) Curve", fontsize=12, weight="bold", pad=10)
ax2.legend(loc="lower right", fontsize=10, frameon=False)

# phase shading on both
for ax in (ax1, ax2):
    ax.axvspan(1, 2.0, color="#e8f0ec", alpha=0.9, zorder=0)
    ax.axvspan(2.0, 5, color="#fff8e5", alpha=0.9, zorder=0)
    ax.axvspan(5, 6, color="#fde8e8", alpha=0.9, zorder=0)
    ax.text(1.5, ax.get_ylim()[1] - 2.5, "Phase I\nIncreasing", ha="center", fontsize=8.5,
            color="#1a5e4a", weight="bold")
    ax.text(3.5, ax.get_ylim()[1] - 2.5, "Phase II\nDiminishing", ha="center", fontsize=8.5,
            color="#8b6914", weight="bold")
    ax.text(5.5, ax.get_ylim()[1] - 2.5, "Phase III\nNegative", ha="center", fontsize=8.5,
            color="#b02a2a", weight="bold")
fig.suptitle("Law of Variable Proportions — Three Phases", fontsize=13.5, weight="bold", y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.96])
save(fig, "TP_MP_Curves.png")


# ── 3. AP & MP relationship ───────────────────────────────────────────────────
labour = np.arange(1, 7)
ap = np.array([10, 15, 15, 13, 10.4, 8])
mp2 = np.array([10, 20, 15, 7, 0, -4])

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
xs = np.linspace(1, 6, 400)
ax.plot(xs, np.interp(xs, labour, ap), color=BLUE, lw=2.4, label="AP")
ax.plot(xs, np.interp(xs, labour, mp2), color=RED, lw=2.4, label="MP")
ax.axhline(0, color="#1b1b1b", lw=0.8)
ax.plot(labour, ap, "o", color=BLUE, markersize=4.5)
ax.plot(labour, mp2, "o", color=RED, markersize=4.5)

# intersection at labour 3 (AP max = 15, MP = 15)
ax.plot([3], [15], "ks", markersize=7, zorder=5)
ax.annotate("MP = AP\nAP is maximum", xy=(3, 15), xytext=(3.35, 19.5),
            arrowprops=dict(arrowstyle="-|>", color="#1b1b1b", lw=1.1), fontsize=9.5,
            ha="center", weight="bold")
ax.annotate("MP > AP\nAP rising", xy=(1.9, 16.5), fontsize=9, color=BLUE, weight="bold")
ax.annotate("MP < AP\nAP falling", xy=(4.7, 8.5), fontsize=9, color=BLUE, weight="bold")
ax.annotate("MP zero / negative\nAP stays positive", xy=(5.5, -1.5), fontsize=8.5,
            color=RED, ha="center")
ax.set_xticks(labour)
ax.set_xticklabels(labour)
ax.set_yticks([-4, 0, 5, 10, 15, 20])
ax.set_ylim(-8, 24)
ax.set_xlabel("Units of Variable Factor (Labour)", fontsize=10.5)
ax.set_ylabel("AP / MP (in units)", fontsize=10.5)
ax.set_title("Relationship between Average Product (AP) and Marginal Product (MP)",
             fontsize=12, weight="bold", pad=10)
ax.legend(loc="upper right", fontsize=10, frameon=False)
ax.grid(True, ls=":", lw=0.5, alpha=0.4)
save(fig, "AP_MP_Curves.png")


# ── 4. Law of Diminishing Returns (MP only, falling) ──────────────────────────
labour = np.array([1, 2, 3, 4, 5])
mpd = np.array([12, 10, 8, 6, 4])

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.axhline(0, color="#1b1b1b", lw=0.8)
xs = np.linspace(1, 5, 300)
ax.plot(xs, np.interp(xs, labour, mpd), color=RED, lw=2.4)
ax.plot(labour, mpd, "o", color=RED, markersize=5)
ax.annotate("MP falls as more labour\nis added to fixed land",
            xy=(3.6, 6.2), fontsize=9.5, ha="center", color="#1b1b1b")
ax.set_xticks(labour)
ax.set_xticklabels(labour)
ax.set_yticks([0, 4, 8, 12])
ax.set_ylim(-1, 14.5)
ax.set_xlabel("Units of Variable Factor (Labour)", fontsize=10.5)
ax.set_ylabel("Marginal Product (in units)", fontsize=10.5)
ax.set_title("Law of Diminishing Returns (Diminishing MP)", fontsize=12, weight="bold", pad=10)
ax.grid(True, ls=":", lw=0.5, alpha=0.4)
save(fig, "Law_Diminishing_Returns.png")


# ── 5. Short Run vs Long Run (variable vs fixed factors) ──────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2))
for ax, title in ((ax1, "Short Run"), (ax2, "Long Run")):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title(title, fontsize=12, weight="bold", color="#1a5e4a", pad=8)

# Short run: some fixed
ax1.add_patch(mpatches.FancyBboxPatch((0.5, 0.6), 2.4, 4.2, boxstyle="round,pad=0.08",
             fc="#fde8e8", ec="#b02a2a", lw=1.5))
ax1.text(1.7, 4.3, "FIXED", ha="center", fontsize=10, weight="bold", color="#b02a2a")
ax1.text(1.7, 3.55, "Land", ha="center", fontsize=9.5)
ax1.text(1.7, 2.95, "Machinery", ha="center", fontsize=9.5)
ax1.text(1.7, 2.35, "Permanent staff", ha="center", fontsize=9.5)
ax1.text(1.7, 1.45, "Cannot change\n(cannot change in\nshort run)", ha="center", fontsize=8.5, color="#b02a2a")

ax1.add_patch(mpatches.FancyBboxPatch((4.6, 0.6), 2.4, 4.2, boxstyle="round,pad=0.08",
             fc="#e8f0ec", ec="#1a5e4a", lw=1.5))
ax1.text(5.8, 4.3, "VARIABLE", ha="center", fontsize=10, weight="bold", color="#1a5e4a")
ax1.text(5.8, 3.55, "Labour", ha="center", fontsize=9.5)
ax1.text(5.8, 2.95, "Raw material", ha="center", fontsize=9.5)
ax1.text(5.8, 2.35, "Power / fuel", ha="center", fontsize=9.5)
ax1.text(5.8, 1.45, "Can be changed", ha="center", fontsize=8.5, color="#1a5e4a")
ax1.text(5, 5.4, "Only variable factors change \u2192 output changes", ha="center",
         fontsize=9, color="#1b1b1b")

# Long run: all variable
ax2.add_patch(mpatches.FancyBboxPatch((1.2, 0.6), 5.6, 4.2, boxstyle="round,pad=0.08",
             fc="#e8f0ec", ec="#1a5e4a", lw=1.6))
ax2.text(4, 4.3, "ALL FACTORS ARE VARIABLE", ha="center", fontsize=10.5, weight="bold",
         color="#1a5e4a")
ax2.text(4, 3.5, "Land  +  Labour  +  Capital  +  Raw material  +  Machinery", ha="center",
         fontsize=9.5)
ax2.text(4, 2.7, "Everything can be changed in the long run", ha="center", fontsize=9,
         color="#1a5e4a")
ax2.text(4, 1.7, "Production can be increased by increasing ALL factors", ha="center",
         fontsize=9, color="#1b1b1b")
fig.suptitle("Short Run vs Long Run — Factors of Production", fontsize=13, weight="bold", y=1.0)
fig.tight_layout()
save(fig, "Short_Run_Long_Run.png")

print("ALL GRAPHS DONE")
