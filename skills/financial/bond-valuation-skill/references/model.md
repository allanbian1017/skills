# Valuation equations and QA

## Single bond
P = Σ CF_t / (1+y/m)^(m*t), with redemption cash flow at maturity. Ensure correct coupon frequency, clean vs dirty price, accrued interest, call schedule and day count.

## Rolling bond ETF
Fund YTM is a snapshot statistic, not an assured realized CAGR. Rebalance, rolling maturities, changes in rates/spreads, expenses, default, FX and distributions affect realized returns. For 5-year scenarios model cash flows and terminal NAV in consistent currency.

## Local price sensitivity
ΔP/P ≈ -D_mod Δy + 0.5 Convexity (Δy)^2.
If separate durations are provided: ΔP/P ≈ -D_rate Δr - D_spread Δs + convexity correction.
Δy uses decimal units: 50 bp = 0.005. Do not apply total duration to both rate and spread independently unless methodology supports it.

## FX conversion
R_TWD = (1+R_USD)*(FX_end/FX_start)-1, where FX is TWD per USD, for an unhedged investment and matched cash-flow assumptions. For multi-year distributed cash flows convert each at its receipt date; this shortcut is a single-period approximation.

## IRR and reverse pricing
P_entry = Σ_{t=1..T} CF_t/(1+r_required)^t + TerminalValue_T/(1+r_required)^T.
For monthly distributions use actual monthly periods or annualized XIRR. Treat reinvestment and withdrawal scenarios separately. Price inputs and terminal NAV must be in the same currency and distribution convention.

## Relative return hurdle
R_required = matched risk-free expected total return + policy risk premium. A yield-to-maturity is not a like-for-like five-year expected total return for a rolling long-duration ETF. Avoid comparing USD yields with TWD outcomes without FX conversion.

## QA checklist
- Confirm fund identity, current month and exact data as-of dates.
- NAV vs market price consistency; premium/discount = price/NAV - 1.
- Ratings sum approximately to 100%, account for cash/unrated.
- Validate expense ratio vs management/custody fee components; do not subtract expenses twice from net yield.
- If provider YTM is gross or net, state treatment; do not assume.
- Compare credit risk with rating- and duration-matched peers.
- Distinguish nominal return, real return, distribution yield, YTM, YTW, IRR and tax-adjusted spendable cash.
- Separate a hypothetical hurdle price from an objectively observed market quote.
- Show scenario assumption ranges and model confidence.
