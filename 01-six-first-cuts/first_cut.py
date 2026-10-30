"""Analytics Decoded, Part 0: Six problems, one first cut.
Every dataset below is simulated with a fixed seed. No real person, firm or
programme is described. Run: python first_cut.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- 1. Healthcare
# 6,000 patients start a chronic medicine. Day each patient stops refilling
# (np.inf = still refilling at day 365).
n = 6_000
early = rng.random(n) < 0.45                      # a group that stops quickly
stop_day = np.where(early, rng.exponential(45, n), rng.exponential(900, n))
stop_day = np.where(stop_day > 365, np.inf, stop_day)
pts = pd.DataFrame({"patient_id": range(n), "stop_day": stop_day})

on_therapy = {d: (pts.stop_day > d).mean() for d in (30, 90, 180, 365)}
stopped_yr = pts.stop_day <= 365
share_by_90 = (pts.stop_day[stopped_yr] <= 90).mean()
print("HEALTH  still on therapy:", {d: f"{v:.1%}" for d, v in on_therapy.items()})
print(f"HEALTH  share of first-year stoppers who stop by day 90: {share_by_90:.1%}")

# ---------------------------------------------------------------- 2. BFSI
# 200,000 card transactions; roughly 0.17% are fraud.
n = 200_000
fraud = rng.random(n) < 0.0017
night = np.where(fraud, rng.random(n) < 0.55, rng.random(n) < 0.12)
new_device = np.where(fraud, rng.random(n) < 0.60, rng.random(n) < 0.04)
amount = np.where(fraud, rng.lognormal(7.6, 0.9, n), rng.lognormal(7.0, 1.0, n))
tx = pd.DataFrame({"fraud": fraud, "night": night,
                   "new_device": new_device, "amount": amount.round(0)})

base_rate = tx.fraud.mean()
lazy_accuracy = 1 - base_rate                     # model that says "never fraud"
rule = tx.night & tx.new_device
precision = tx.fraud[rule].mean()
recall = rule[tx.fraud].mean()
print(f"BFSI    fraud rate {base_rate:.3%} | 'never fraud' accuracy {lazy_accuracy:.2%}")
print(f"BFSI    rule night & new device: flags {rule.sum():,} | "
      f"precision {precision:.1%} | recall {recall:.1%}")

# ---------------------------------------------------------------- 3. Technology
# A/B test of a new onboarding screen, 20,000 users per arm.
n_arm = 20_000
a = rng.random(n_arm) < 0.120                     # current screen
b = rng.random(n_arm) < 0.126                     # new screen
pa, pb = a.mean(), b.mean()
diff = pb - pa
se = np.sqrt(pa * (1 - pa) / n_arm + pb * (1 - pb) / n_arm)
lo, hi = diff - 1.96 * se, diff + 1.96 * se
print(f"TECH    activation A {pa:.2%} | B {pb:.2%} | lift {diff*100:+.2f} pts "
      f"| 95% CI [{lo*100:+.2f}, {hi*100:+.2f}] pts")
# users per arm needed to detect 0.6 pts at 80% power, 5% significance
p0, p1 = 0.120, 0.126
need = ((1.96 + 0.84) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / (p1 - p0) ** 2
print(f"TECH    users per arm needed for a 0.6-pt lift: {need:,.0f}")

# ---------------------------------------------------------------- 4. E-commerce
# 5,000 customers over one year of orders.
n = 5_000
orders = rng.negative_binomial(1, 0.25, n) + 1    # orders per customer
basket = rng.lognormal(7.2, 0.7, n)              # typical order value (INR)
revenue = orders * basket
# frequent buyers tend to have bought more recently
last_days_ago = np.minimum(365, rng.exponential(365 / (orders + 1)) + 1).round(0)
cust = pd.DataFrame({"orders": orders, "revenue": revenue.round(0),
                     "recency_days": last_days_ago})
cust = cust.sort_values("revenue", ascending=False).reset_index(drop=True)
top20 = cust.head(int(0.2 * n))
top20_share = top20.revenue.sum() / cust.revenue.sum()
quiet_vips = (top20.recency_days > 90).mean()
print(f"ECOM    top 20% of customers hold {top20_share:.1%} of revenue")
print(f"ECOM    of those top customers, {quiet_vips:.1%} have not ordered in 90+ days")

# ---------------------------------------------------------------- 5. FMCG
# 104 weeks of unit sales for one brand; 8 promotion weeks.
weeks = 104
baseline = 1_000 + 40 * np.sin(np.arange(weeks) * 2 * np.pi / 52)
sales = baseline + rng.normal(0, 30, weeks)
promo_weeks = np.array([10, 22, 34, 46, 62, 74, 86, 98])
for w in promo_weeks:
    sales[w] += 600                               # the bump
    sales[w + 1] -= 150                           # households stocked up
    sales[w + 2] -= 70
fm = pd.DataFrame({"week": range(weeks), "units": sales.round(0),
                   "baseline": baseline.round(0)})
bump = (fm.units - fm.baseline)[promo_weeks].sum()
dip = (fm.units - fm.baseline)[np.r_[promo_weeks + 1, promo_weeks + 2]].sum()
print(f"FMCG    promo-week bump {bump:,.0f} units | post-promo dip {dip:,.0f} units")
print(f"FMCG    net gain {bump + dip:,.0f} units | share of bump borrowed: {-dip / bump:.1%}")

# ---------------------------------------------------------------- 6. Government
# 400 blocks: money released by the treasury vs money beneficiaries say they got.
n = 400
released = rng.lognormal(16.0, 0.4, n)            # INR per block
leak_rate = np.clip(rng.beta(1.2, 6.0, n), 0, 0.9)
received = released * (1 - leak_rate)
gov = pd.DataFrame({"released": released, "received": received})
gov["leaked"] = gov.released - gov.received
overall = gov.leaked.sum() / gov.released.sum()
top10 = gov.sort_values("leaked", ascending=False).head(n // 10)
conc = top10.leaked.sum() / gov.leaked.sum()
print(f"GOV     overall leakage {overall:.1%} | top 10% of blocks hold {conc:.1%} of leaked money")
