# 🪙 India Safe Online Gold, Live Rate, Gold ETF Comparison & Verifiable Offer Tracker

A **Zero-Artificial-Data** Python/Streamlit application that tracks safe ways to buy gold online in India, compares **SEBI-regulated NSE Gold ETFs vs. Digital Gold / Sovereign Gold Bonds / Physical Coins for the exact same quantity of gold (e.g., 1g, 5g, 10g, 50g)**, and audits **Credit Card, SmartBuy Voucher, and Jeweller Scheme offers** daily with live HTTP status and cryptographic `SHA-256` provenance.

📄 **Full Multi-Expert Strategy & Critic Sign-Off:** [`docs/EXPERT_COUNCIL_STRATEGY.md`](docs/EXPERT_COUNCIL_STRATEGY.md)

---

## ✨ Key Features

1. **📈 Live Domestic & International Gold Benchmarks (`Tab 1`)**
   - Scrapes live official **IBJA (India Bullion and Jewellers Association)** 999 (24K), 995, 916 (22K), 750 (18K), and 585 (14K) rates from `ibjarates.com`.
   - Scrapes live retail 24K/22K benchmarks from `goodreturns.in`.
   - Computes real-time **International Spot (`XAU/INR`)** and **India Landed Customs Parity** from live `COMEX Gold (GC=F)` and `USD/INR (INR=X)`.
   - Tracks **7 SEBI-Regulated NSE Gold ETFs** (`GOLDBEES.NS`, `SETFGOLD.NS`, `HDFCGOLD.NS`, `GOLDIETF.NS`, `GOLD1.NS`, `GOLDCASE.NS`, `TATAGOLD.NS`) with live LTP, volume, Expense Ratio (`TER`), and 0% GST advantage.

2. **🛡️ 4-Tier Safe Online Gold & Custodian Audit (`Tab 2`)**
   - Audits **Tier 1 (SEBI Gold ETFs & RBI SGBs)**, **Tier 2 (MMTC-PAMP, SafeGold, Augmont 24K Digital Gold)**, **Tier 3 (Tanishq, CaratLane, Malabar, Candere BIS-Hallmarked Jewellers)**, and **Tier 4 (Authorized E-Commerce Bullion Coins)**.
   - Displays **Refinery Partner**, **Independent Trustee** (`IDBI Trusteeship` / `Universal Trusteeship`), **Insured Vault Custodian** (`Brinks` / `Sequel`), **Max Free Storage Tenure**, and **Day-1 Instant Liquidation Loss %**.

3. **💳 Verifiable Credit Card, Voucher & Jeweller Scheme Tracker (`Tab 3`)**
   - Enforces Indian Credit Card **MCC `5094` (Bullion/Digital Gold)**, **MCC `5944` (Jewellery)**, and **MCC `6051` (Quasi-Cash)** rules.
   - Tracks verified working card/voucher pathways (`Tata Neu Infinity 5% NeuCoins`, `Tata Neu Plus 2%`, `HDFC Infinia 16.5% / DCB Metal 9.9% SmartBuy GyFTR Vouchers` with the **July 1, 2026 3,000 bonus RP/month sub-cap**, `Amex Platinum Travel Milestone`, `Tanishq GHS`, `CaratLane PoP!`, `Malabar Golden Bloom`, `Candere DGRP`).
   - Explicitly flags **0% Cashback Traps** (`Amazon Pay ICICI`, `SBI Cashback Card` on `MCC 5094`) and **Unsecured Gold Leasing Counterparty Risk** (`Gullak Gold+` / `SafeGold Gains`).

4. **🧮 Head-to-Head Gold ETF vs. Digital Gold / Card Calculator for Same Gold Quantity (`Tab 4`)**
   - **Same-Quantity Gold Comparison (`1g`, `5g`, `10g`, `50g`, etc.):** Shows exact **equivalent NSE Gold ETF units** (`GOLDBEES`, `GOLDCASE`, `TATAGOLD`, etc.), **3% GST saved by Gold ETF**, **Spread/Markup cost**, **Verified Card Reward**, **Day-1 Resale Value**, and **5-Year Expense Ratio (`TER`) Break-Even Horizon**.
   - **Same-Rupee-Budget Calculator:** Ranks all 10 channels by **Net Landed Cost per Gram of 24K Equivalent** for any ₹ investment amount.

5. **🔍 Cryptographic `SHA-256` & HTTP Provenance Audit Log (`Tab 5`)**
   - Every benchmark, ETF, platform, and bank T&C URL is probed live and logged with `http_status`, `latency_ms`, `verified_at_ist`, and `content_sha256` in both [`data/latest_verified_snapshot.json`](data/latest_verified_snapshot.json) and SQLite (`data/gold_audit_history.db`).

---

## 🚀 Quick Start (Local)

```bash
pip install -r requirements.txt

# 1. Run live verification refresh (updates data/latest_verified_snapshot.json & SQLite DB)
python gold_verification_engine.py --refresh

# 2. Launch the interactive 5-tab Streamlit dashboard
streamlit run app.py
```

---

## ⏰ Automated Twice-Daily Refresh (GitHub Actions)

[`.github/workflows/daily_gold_refresh.yml`](.github/workflows/daily_gold_refresh.yml) automatically runs `python gold_verification_engine.py --refresh` twice daily at **09:30 AM IST** and **06:30 PM IST** (Monday–Saturday, aligned with IBJA AM/PM rate sessions and NSE market hours) and commits the updated verified snapshot and SQLite audit history back to the repository.
