---
name: equity-valuation
description: Analyze whether a publicly traded company is overvalued using current primary financial data, peer and historical multiples, five-year fundamentals, valuation compression, scenario returns, and a 10% required annualized return. Trigger for stock valuation, fair value, entry price, or questions like "分析 2454" and "Is NVDA overvalued?".
---

# Equity Valuation Skill

## Objective and defaults
Determine whether the **current stock price** offers an attractive risk-adjusted five-year return, rather than whether the company is good. Default holding period: **5 years**. Default required annualized total return: **10%**. Use the stock's listing currency; show FX exposure separately when relevant. These are defaults, override when the user specifies alternatives. Do not create spreadsheets unless requested.

## Required research (browse for every fresh valuation)
1. Identify ticker, exchange, share class, currency, latest **timestamped** price and whether it is live, delayed, or last close. Never fabricate a quote. If the market is open and only last close is available, state that.
2. Retrieve latest company earnings release, regulatory filings, investor presentations and guidance. Prioritize primary sources; identify reporting period, publication date and accounting units. Cross-check diluted shares, EPS, trailing net income, operating cash flow, capex, FCF, debt/cash, margins, ROIC when available, dividends, buybacks, and dilution.
3. Retrieve dated analyst consensus for next 2–3 fiscal years, with sample size/range if available; distinguish estimates from management guidance and your own assumptions. If credible consensus is unavailable, explicitly state this and construct transparent estimates from reported drivers.
4. Retrieve historical multiple range/median and **genuinely comparable** peers; adjust for business mix, cyclicality, accounting and growth. Avoid comparisons with broad sector medians when misleading. Historical multiples must be matched to consistent EPS definitions and time periods.
5. Cite each material time-sensitive fact with source and date; if sources conflict, explain rather than silently selecting one. Never reuse earlier-chat stock prices, EPS forecasts, or citations as current evidence.

## Metric selection
- Profitable nonfinancial businesses: TTM and forward P/E, EV/EBIT or EV/EBITDA where meaningful, FCF yield/P-FCF, revenue/EPS growth, margins, reinvestment, capital intensity, balance sheet, dilution.
- Banks/insurers: P/B, ROE, capital adequacy, credit/underwriting quality and appropriate earnings measures.
- REITs: FFO/AFFO and leverage.
- Unprofitable firms: EV/sales plus unit economics, dilution and path to sustainable FCF; avoid meaningless negative P/E and PEG.
- Cyclical firms: normalize midcycle earnings; don't use peak earnings to claim low P/E.
- Never apply a uniform P/E to all industries.

## Five-year model and timeline integrity
Set `t0` to the date of the observed stock price. Forecast EPS or other relevant per-share metric for the date **five years after t0**, using the correct fiscal-year bridge. When using annual fiscal-year EPS and year-end terminal prices as a simplifying approximation, explicitly label the approximation; do not call it exactly five years from today if it is not.

For a simple earnings-multiple model:
- `EPS_T = EPS_base × product(1 + g_year)` for exactly the modeled growth periods. Prefer explicit year-by-year EPS projections, using credible consensus for near years and justified normalization thereafter.
- `P_T = EPS_T × Exit_PE` (adjust for expected net debt, dilution and unusual items where applicable).
- Price-only `CAGR = (P_T/P_0)^(1/T) - 1`.
- Without dividends, maximum entry price for target return `r`: `P_entry = P_T/(1+r)^T`.
- With dividends, solve `P_entry = sum(D_t/(1+r)^t) + P_T/(1+r)^T` for end-of-period cash dividends, or compute total-return IRR with exact payment timing. State dividend tax assumptions; don't casually add dividend yield to CAGR and call it exact.
- Price-only scenario upside/downside: `P_T/P_0 - 1`. Margin of safety relative to model's maximum entry price: `(P_entry-P_0)/P_entry` (state convention). Also report the price gap `(P_entry/P_0 - 1)` when useful.
- Distinguish nominal from inflation-adjusted returns; identify fees, taxes, FX exclusions.

## Scenarios and valuation compression
Build Bear/Base/Bull cases with **separately justified** operating drivers, EPS paths, and terminal valuation multiples. Do not automatically use a high exit P/E because earnings grow quickly. Explicitly quantify P/E contraction from today's comparable forward multiple to exit multiple. Evaluate risk of an earnings miss *and* simultaneous multiple contraction.

Where practical, provide a sensitivity grid for terminal EPS growth and exit P/E, and identify the break-even assumptions needed to earn the 10% hurdle at the current price. Probabilities are optional and must not be fabricated. DCF or owner-earnings valuation can triangulate if cash-flow inputs are robust; do not pretend DCF is precise.

## Output in Traditional Chinese by default
1. **Verdict first:** undervalued / approximately fair / expensive / too uncertain to conclude, with confidence level and a one-sentence reason. Make the conclusion conditional on assumptions, not a claim of certainty.
2. Quote card: ticker, market, price, price timestamp, currency, market state.
3. Source-backed fundamentals and valuation: TTM/forward multiples, historical and peers, cash flow and financial health.
4. Growth drivers and dated consensus table, separating actuals, consensus, and model estimates.
5. Bear/Base/Bull table: 5-year terminal EPS, exit P/E, terminal price, price CAGR, dividend-inclusive total-return CAGR if supportable, and **10% hurdle entry price**.
6. Sensitivity analysis; explain multiple compression and what expectations are priced in.
7. Catalysts, invalidation conditions, next earnings date if verified, and top risks.
8. Decision: is the current price attractive for the 10% hurdle? Give a **conditional valuation-based** entry price, not a technical support level or guaranteed target. Note missing information.
9. Compact citations linked near claims, source dates, and calculation notes.

## Quality-control checklist
- Verify price × share count and EPS/multiple arithmetic; check units, currency, splits, ADR ratio, fiscal-year alignment, and dilution.
- Recompute every scenario CAGR and entry price independently; avoid false precision (round prices sensibly).
- Verify that 10% is a **total-return** hurdle when dividends matter.
- Distinguish forward P/E from TTM P/E, and analyst consensus from your scenarios.
- If no current price or earnings data can be verified, ask for a source or provide a clearly labeled illustrative model; do **not** issue a current overvaluation verdict.
- No investment outcome is certain; disclose assumptions and major uncertainty without boilerplate dominating the answer.
