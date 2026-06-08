---
name: term-sheet-review
description: >
  Review a VC or angel term sheet in plain language — valuation mechanics,
  liquidation preference, pro-rata rights, information rights, board, protective
  provisions, ESOP pool. Explains each term for a non-lawyer founder.
  Use when reviewing a term sheet or asking "what does this term mean".
argument-hint: "[paste term sheet or describe the key terms]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:term-sheet-review

0. **Preamble (output first, before any review):**
   > ⚠️ **This analysis is educational guidance for a non-lawyer founder — not legal advice. Have a Finnish startup lawyer review before responding to the investor or signing. RED findings below require attorney input before you act — they are not negotiating scripts.**
1. Load profile. If placeholders, stop.
1.5. **Input gate:** The user must provide either (a) actual term sheet text or (b) a structured list of specific terms (e.g., "pre-money €4M, 1× non-participating liquidation preference, 20% ESOP pool pre-money"). If only a verbal description is provided, ask the user to paste the actual term sheet or specific terms before proceeding — do not run a review on a vague description.
2. Run term-by-term review in plain language. Flag aggressive terms. Explain each in 1–2 sentences.
3. Output: term table with explanation + RED/AMBER/GREEN status.
4. **Escalation rule:** If any RED finding is present, output immediately after the table:

   > 🛑 **STOP — consult a lawyer before responding to the investor.**
   > This term sheet has RED finding(s). RED findings are not negotiating points to handle from this analysis — they require a Finnish startup lawyer to assess the impact on your cap table, exit economics, and founder control before you respond. Forward this analysis to your outside counsel and ask them to review these specific items before your next communication with the investor.

---

## Term sheet review

For each term, explain what it means in plain language and flag if it deviates from Finnish/Nordic market standard.

### Valuation
- **Pre-money valuation**: company value before the investment. Post-money = pre-money + investment amount.
- **Fully diluted**: valuation calculated including all options, convertible notes, warrants. Check: is the ESOP pool included pre-money (dilutes founders) or post-money (dilutes everyone)?

**Finnish/Nordic market: ESOP pool typically included pre-money. If post-money: note but not unusual.**

### Liquidation preference
- **1× non-participating**: investor gets 1× their money back before common shareholders in a liquidation/exit, then does NOT also participate in remaining proceeds. **Market standard — GREEN.**
- **1× participating**: investor gets 1× back AND participates pro-rata in remaining proceeds. **Aggressive — AMBER.**
- **>1× or full ratchet**: investor gets more than invested back. **Very aggressive — RED. Push back.**

### Pro-rata right
Right for investor to participate in future rounds to maintain their ownership %. **Market standard — GREEN.** Super pro-rata (right to more than maintain %) is aggressive.

### Board composition
Ask: how many seats total, who gets them? Market standard for seed:
- 2 founder seats
- 1 lead investor seat
- 1 independent (optional)
Giving investors majority board control at seed is **RED**.

### Protective provisions (veto rights)
Investors typically require consent for: new share issuance, M&A/exit, budget approval, incurring debt above threshold, hiring/firing CEO. List each one — standard list GREEN, unusual additions AMBER.

### Information rights
Quarterly financials + annual audited accounts = **GREEN**. Monthly board pack demands on a sub-€500k round = **AMBER**.

### Anti-dilution
See sha-review — broad-based weighted average = **GREEN**; full ratchet = **RED**.

### ESOP/option pool
What size? Typical at seed: 10–15% pre-money. If investor demands 20%+ pre-money: **AMBER** (dilutes founders significantly).

### Tesi co-investment (if applicable)

`[Tesi terms — last_verified: 2026-06-01. Verify current Tesi co-investment terms directly at tesi.fi for live deals.]`

If Tesi (Finnish Industry Investment Ltd) is co-investing:
- Tesi co-invests **pari passu** alongside private lead investors — same share class, same price, no preference over other investors
- No management fees or carried interest on Tesi's portion
- Tesi follows market standard terms set by the private lead — they do not lead rounds
- Tesi requires the company to be Finnish-domiciled (or have substantial Finnish operations) and the lead investor to be a qualified VC or institutional investor
- Flag: terms that give Tesi any preference over private investors or that deviate from pari passu are non-standard and warrant verification with Tesi directly

---

## What this skill does NOT do

- **Convertible notes / SAFEs**: Covers priced equity rounds only.
- **Non-Finnish term sheets**: Applies Finnish/Nordic market standards. UK, US Delaware, and Swedish term sheets have different market norms.
- **SHA negotiation**: Covers the term sheet stage. For the full SHA review after signing, use `/fi-startup-legal:sha-review`.
- **ESOP pool design**: For option pool mechanics, use `/fi-startup-legal:esop-designer`.
- **Legal advice**: Outputs are legal support tools. No attorney-client relationship or privilege is created.

---

## Guardrail

Term sheet review identifies market-standard vs. aggressive terms. This is educational guidance for a non-lawyer founder — not legal advice. Have a Finnish startup lawyer review the full term sheet before signing. Non-binding term sheets can create moral obligations and set negotiation anchors. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
