# 🏛️ Expert Council Strategy & Critic Sign-Off: India Safe Gold & Verifiable Offer Tracker

> [!IMPORTANT]
> **Strict Zero-Artificial-Data Mandate:** Every benchmark rate, NSE Gold ETF quote, digital gold refinery spread, jeweller savings scheme, and credit card/voucher offer tracked by this application is governed by **5 Non-Negotiable Acceptance Gates** enforced by the Verification Critic. **Zero synthetic, random, or hardcoded fallback prices are permitted.**

---

## 1. Multi-Expert Panel & Deliberation Summary

Three specialized experts were convened to design, challenge, and sign off on the strategy before writing code:

1. **Indian Digital Gold & Bullion Domain Expert** — Mapped the legal, custodial, and tax structure of all online gold channels in India, including SEBI/RBI rules, trustee deeds, BIS HUID hallmarking, and bank Merchant Category Code (`MCC 5094`, `5944`, `6051`) exclusions.
2. **FinTech App Design & Data Pipeline Architect** — Designed the local-first, GitHub-deployable Python/Streamlit architecture, dual-class verification engine (`LIVE_PUBLIC_SCRAPE` vs. `VERIFIED_POLICY_RULE` with SHA-256 T&C drift auditing), and automated daily refresh workflow.
3. **Chief Verification & Accuracy Critic** — Audited both proposals, caught and corrected a common misconception in the initial app draft (clarifying that **Amazon Pay ICICI Credit Card explicitly excludes Digital Gold and Gold Coins (`MCC 5094`) from its 5% Prime reward**), enforced the July 1, 2026 HDFC SmartBuy **3,000 RP/month brand-voucher sub-cap**, and mandated explicit labeling between directly scraped DOM rates (`LIVE_RATE_PARSED`) and benchmark-derived platform rates (`LIVE_BENCHMARK + PUBLISHED_SPREAD`).

```mermaid
flowchart LR
    DG["1. Digital Gold Expert\n(Custodians, GST, MCC 5094/5944,\nSEBI Rules & Jeweller Schemes)"] --> CRITIC["3. Verification Critic\n(5 Zero-Mock Gates +\nMCC & CSR Honesty Audit)"]
    ARCH["2. App Design Expert\n(Live Scrapers, SHA-256 T&C Hash,\nSQLite/JSON & GitHub Cron)"] --> CRITIC
    CRITIC -->|"UNCONDITIONAL SIGN-OFF"| IMPL["4. Implementation\n(Digital-Gold-India)"]
```

---

## 2. Domain Strategy: Safe Ways to Buy Gold Online in India

### Tier 1: SEBI & RBI Regulated Electronic Gold (Highest Financial Safety)
| Instrument | Regulator | Purity & Backing | GST at Purchase | Buy–Sell Spread | Tax Rule (Post-Budget 2024–2026) | Official Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NSE/BSE Listed Gold ETFs** (`GOLDBEES.NS`, `SETFGOLD.NS`, `HDFCGOLD.NS`, `GOLDIETF.NS`, `GOLD1.NS`, `GOLDCASE.NS`, `TATAGOLD.NS`) | **SEBI** (Mutual Fund Regulations, 1996) | **99.5% (24K)** LBMA physical bars with SEBI-registered Custodians | **0.00%** | **0.03% – 0.12%** | **12.5% LTCG** after **>12 months** (no indexation); slab rate if ≤12m | [sebi.gov.in](https://www.sebi.gov.in) / [nseindia.com](https://www.nseindia.com) |
| **Sovereign Gold Bonds (SGBs)** *(Secondary Market on NSE/BSE)* | **RBI** & Govt. of India (G-Sec Act, 2006) | **999 Purity** Govt guarantee + **2.50% p.a.** interest | **0.00%** | Secondary market liquidity premium (**3%–10%**) | Tax-free if held to 8-yr maturity; **12.5% LTCG** (>12m) on secondary sale | [rbi.org.in](https://www.rbi.org.in) |

### Tier 2: Accredited Refinery 24K Digital Gold (Trustee-Backed, Unregulated by SEBI/RBI)
All retail fintech apps (PhonePe, Google Pay, Paytm, Amazon Pay, Jar, Gullak, Jupiter) distribute gold vaulted by one of **three wholesale bullion providers**:

| Refinery / Provider | Purity | Independent Trustee | Vault Custodian | Free Storage Limit | Partner Storefronts | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MMTC-PAMP India Pvt. Ltd.** *(JV with Govt's MMTC Ltd; India's only LBMA-accredited refiner)* | **24K 999.9** (99.99%) | **Universal Trusteeship Services Ltd. (UTSL)** | Brinks / Loomis / MMTC-PAMP Vaults | Up to **5 years** | Direct, Google Pay, Paytm, Jupiter, Aditya Birla | [mmtcpamp.com](https://www.mmtcpamp.com/digital-gold) |
| **SafeGold** *(Digital Gold India Pvt. Ltd.)* | **24K 995** (ledger) / **999.9** (coins) | **IDBI Trusteeship Services Ltd. (ITSL)** | **Brinks India Pvt. Ltd.** | **2–5 years** (0.05%/mo thereafter) | Direct, PhonePe, Amazon Pay, Tanishq, CaratLane, Tata Neu | [safegold.com](https://www.safegold.com) |
| **Augmont Goldtech Pvt. Ltd.** *(BIS licensed & NABL accredited)* | **24K 999** (99.9%) | **IDBI Trusteeship Services Ltd. (ITSL)** | **Sequel Logistics** Vaults | Up to **5 years** | Direct, Gullak, Jar, Candere, Muthoot | [augmont.com](https://www.augmont.com/digi-gold) |

> [!WARNING]
> **SEBI Regulatory Notice & Gold Leasing Warning:**
> 1. Per SEBI's August 2021 directive (`NSE/COMP/49566`), **Digital Gold is not a SEBI/RBI-regulated security**, and stockbrokers are barred from selling it. It carries **3% upfront GST** plus a **2.5%–3.5% buy–sell spread** (~5.5%–6.5% immediate Day-1 liquidation friction).
> 2. **Gold Leasing schemes** (e.g., *Gullak Gold+* or *SafeGold Gains* offering 4%–5% extra gold p.a.) move your gold **out of the IDBI Trustee ring-fence** into an **unsecured corporate loan to jewellers**, carrying counterparty default risk.

### Tier 3: Organised BIS-Hallmarked National Jewellers (Digital-to-Jewellery & Schemes)
* **Tanishq (`tanishq.co.in`)**: SafeGold-powered 24K Digital Gold redeemable at 400+ stores + **Golden Harvest Scheme (GHS)** (10 monthly installments; up to **75% of 1st installment discount** on jewellery in month 11; *not valid on 24K gold coins*).
* **CaratLane (`caratlane.com`)**: SafeGold-powered **eGold** + **CaratLane PoP! Plan** (9 monthly installments; up to **30%–50% of 1st installment bonus** on studded/gold jewellery in month 10; *not valid on coins*).
* **Malabar Gold & Diamonds (`malabargoldanddiamonds.com`)**: 24K (999/995) BIS Hallmarked Coins + **Golden Bloom / Golden Glitz** 11-month advance schemes (waiving up to **14%–18% making charges** on 22K jewellery).
* **Kalyan Jewellers & Candere (`candere.com` / `kalyanjewellers.net`)**: **Double Gold Rate Protection (DGRP)** (locks gold rate on booking with 10% advance; if gold price drops at checkout, buyer gets the lower rate).

---

## 3. Credit Card MCC (`5094` / `5944` / `6051`) Compliance & Verifiable Offer Matrix

Most Indian banks exclude **MCC 5094** (*Precious Metals/Bullion*) and **MCC 5944** (*Jewellery Stores*) from base rewards, or charge a **1% + GST Quasi-Cash fee (`MCC 6051`)** on wallet/digital gold loads. Our app enforces strict MCC truth tables:

| Card / Route | Target Platform | Verified Net Reward | Key Capping & MCC Fine Print | Official Verification Link |
| :--- | :--- | :--- | :--- | :--- |
| **Tata Neu Infinity HDFC Credit Card** *(Direct Swipe)* | **Tanishq, Mia by Tanishq, CaratLane** | **5.0% NeuCoins** (1 NeuCoin = ₹1) | Valid on non-EMI retail/online jewellery & eligible store purchases. **Capped at ₹3L/month (15,000 NeuCoins) & ₹6L/year (30,000 NeuCoins)** on Tanishq. Raw digital gold blocks excluded. | [hdfcbank.com](https://www.hdfcbank.com/personal/pay/cards/credit-cards/tata-neu-infinity-hdfc-bank-credit-card) |
| **HDFC Infinia / DCB Metal via SmartBuy GyFTR** *(Voucher Route)* | **Myntra / Tanishq Brand Vouchers** | **~9.9% – 16.5% RP** (up to 3,000 bonus RP/mo cap) | **July 1, 2026 Rule:** Brand vouchers on SmartBuy GyFTR have a **3,000 accelerated RP/month sub-cap**. **Oct 1, 2024 Rule:** Tanishq voucher point redemption capped at **50,000 RP/quarter**. GyFTR Tanishq vouchers often restrict 24K Gold Coins—verify voucher SKU before purchase. | [hdfcbank.com](https://www.hdfcbank.com/personal/pay/cards/credit-cards/infinia-credit-card) |
| **Amex Platinum Travel Credit Card** *(Direct / Multiplier)* | **Tanishq, CaratLane, Malabar, Myntra** | **~2% base + ~5.5%–7.5% Milestone Return** (at ₹4L spend) | Jewellery (`MCC 5944`) counts toward the **₹4,00,000 annual milestone** (40,000 MR points + ₹10,000 Taj Voucher). | [americanexpress.com/in](https://www.americanexpress.com/in/credit-cards/platinum-travel-credit-card/) |
| **Amazon Pay ICICI / SBI Cashback / Axis Cards** *(Direct Swipe Trap)* | **Digital Gold & Gold Coins (`MCC 5094`)** | **0.0% Reward** *(Excluded)* | **Compliance Warning:** ICICI Amazon Pay MITC, SBI Cashback MITC, and Axis MITC explicitly **exclude MCC 5094/5944** (Gold Coins, Digital Gold, Jewellery) from cashback/points. | [sbicard.com](https://www.sbicard.com/en/personal/credit-cards/rewards/cashback-sbi-card.page) |

---

## 4. Critic's 5 Non-Negotiable Acceptance Gates (All Passed ✅)

1. **Gate 1 (`NO_SYNTHETIC_DATA`)**: Zero random jitter or dummy fallback numbers. Every price is fetched live from public financial/bullion sources; any unreachable endpoint fails closed with `FETCH_ERROR (HTTP <code>)`.
2. **Gate 2 (`VERIFIABLE_ITEM_SCHEMA`)**: Every UI item exposes `source_name`, clickable `source_url`, IST `fetched_at` timestamp, `http_status`, `latency_ms`, `content_sha256`, and explicit `extraction_mode` (`LIVE_RATE_PARSED` vs. `LIVE_BENCHMARK_PLUS_PUBLISHED_SPREAD` vs. `LIVE_POLICY_VERIFIED`).
3. **Gate 3 (`NET_EFFECTIVE_PRICE_GATE`)**: Ranks options by **Net Landed Cost per Gram of 24K Equivalent**:
   $$\text{Net Landed Cost/g} = \text{Base Rate/g} + \text{Spread/Minting} + \text{3\% GST} + \text{Gateway/Voucher Fee} - \text{Verified Capped Reward/g}$$
4. **Gate 4 (`MCC_COMPLIANCE_GATE`)**: Direct swipes on `MCC 5094/5944` default to 0% unless verified by official bank MITC; voucher routes deduct GyFTR fees and apply monthly/quarterly reward caps.
5. **Gate 5 (`TRUST_AND_SAFETY_GATE`)**: Displays Refinery, Independent Trustee, Vault Partner, Storage Limit, and the mandatory SEBI Aug 2021 unregulated product & gold-leasing counterparty risk warnings.
