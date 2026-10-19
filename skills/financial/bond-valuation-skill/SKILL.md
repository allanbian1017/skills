---
name: bond-etf-relative-valuation
description: Analyze bond ETFs and individual bonds with verified current market data, relative required returns, duration/credit/FX scenarios, cash-flow sustainability, and reverse-priced entry thresholds. Use when asked to value a bond ETF, compare fixed-income opportunities, or decide whether to hold/add/reduce.
---

# Bond ETF Relative Valuation

## Purpose
Provide a reproducible, evidence-led valuation and decision framework. Do not confuse distribution yield with yield to maturity, or a modeled entry threshold with intrinsic value. Default output language follows the user.

## Workflow
1. **Identify instrument**: ticker, legal name, exchange, domicile, index, currency of assets and trading, hedging, distribution policy, target maturity vs perpetual rolling fund. Verify ticker-to-fund identity.
2. **Set as-of date**: use current local date; verify latest market close and NAV. Record timestamp, timezone, source URL, publication date and portfolio as-of date separately. Avoid mixing data dates without a bridge.
3. **Retrieve primary evidence**: issuer fund page, official factsheet/monthly report, holdings file, prospectus, exchange disclosures, index provider; then official Treasury yield curves and central-bank data. Supplement with reliable third-party feeds only when necessary. Follow source hierarchy and document any inaccessible fields. Never invent current data or reuse previous-chat figures as current.
4. **Extract and verify**: market price, NAV and premium/discount; weighted YTM/YTW and their methodology; effective/modified duration and convexity; average maturity; ratings; issuer/sector concentration; OAS or suitable matched index proxy; total expense ratio; coupon, distribution, ROC and historical distributions; FX hedge policy; liquidity and bid-ask spread. Distinguish fund data from benchmark data.
5. **Match benchmarks**: select currency- and horizon-consistent risk-free alternatives. For credit spread, use same-date duration/curve-matched spread or index OAS, not raw YTM minus a single Treasury tenor as definitive OAS. Contrast alternative Treasury and bond ETFs using comparable net expected total returns, not distribution yields.
6. **Required relative return**: R_required = R_risk_free + required risk premium for duration, credit, liquidity, structural risks, with no double-counting. Risk premiums are policy assumptions, not observed spreads. Provide a defensible range and sensitivity. For TWD investors, explicitly model FX and taxes; do not add arbitrary FX premium to a USD return then also subtract FX in forecast.
7. **Forecast total return**: build bear/base/bull scenarios at 1 and 5 years; separate Treasury curve change, credit OAS change, spread-duration and rate-duration if available, carry, roll-down, reinvestment, expenses, defaults/downgrades, and FX. For short horizon, approximate local-price return as carry + roll - D_rate*ΔTreasury - D_spread*ΔOAS + 0.5*convexity*(Δyield)^2 - costs; document simplifications. For 5 years, model annual cash flows and rolling portfolio duration/yield rather than blindly applying current YTM for five years. Show nominal USD and TWD total returns and IRR, cash distributions separately, and after-tax if tax assumptions are verified.
8. **Reverse price**: for each scenario, discount projected distributions and terminal value at the required IRR. Present a range, sensitivity and margin of safety relative to the latest observed price. Warn that terminal price assumptions and NAV/FX alignment matter. If evidence insufficient, label result illustrative, not an executable entry price.
9. **Decision**: hold/add/reduce/watch with confidence level, drivers, triggers, concentration and liquidity constraints. Show what would falsify the thesis and what to monitor next. For income goals, distinguish stable spendable cash from mark-to-market total return.

## Data quality and stopping rules
- Tag each critical input: **Verified official**, **Verified secondary**, **Proxy**, **Assumption**, or **Unavailable**, plus date.
- Search for the latest issuer factsheet and official holdings before using proxies. When source is a PDF, read its text and relevant pages, and cite the original URL and page.
- If YTM/YTW, duration or as-of dates are missing, do not assert a precise fair value or confident entry recommendation. You may run an explicitly illustrative sensitivity model.
- Never infer YTM from distributions; never treat YTM as guaranteed fund return; never equate Fed policy rate moves with long-end Treasury yield changes; never assume a perpetual ETF matures at par.
- Use at least one independent cross-check for price/NAV and a reasonableness check for duration and rating distribution.
- For convexity and credit-spread sensitivities, use provider measures if possible; otherwise disclose first-order approximation.
- Avoid false precision: round modeled prices appropriately and describe material uncertainty.

## Required report format
1. Executive conclusion and decision, data freshness/confidence.
2. Instrument profile and primary-source table (value, date, provenance, quality).
3. Treasury curve, matched credit OAS and relative-value comparison.
4. Duration, convexity, credit and FX risk decomposition.
5. One-year and five-year bear/base/bull assumptions, annual cash flows, total return and IRR.
6. Required return methodology and reverse-priced entry range with margin of safety.
7. Income sustainability, after-tax TWD cash flow, portfolio concentration and alternatives.
8. Decision triggers, key limitations and links to original sources.

For formulas, worked examples, and QA checks see [references/model.md](references/model.md).
