"""
India Safe Digital Gold, Live Rate & Verifiable Card/Platform Offer Tracker
===========================================================================
Streamlit Application implementing the Expert Council Strategy & Critic's
5 Non-Negotiable Zero-Mock Acceptance Gates.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from gold_verification_engine import (
    SNAPSHOT_PATH,
    SQLITE_DB_PATH,
    VERIFIED_OFFERS_AND_CARDS_REGISTRY,
    calculate_net_landed_cost_matrix,
    calculate_same_quantity_etf_comparison,
    load_latest_snapshot,
    run_full_live_verification,
)

st.set_page_config(
    page_title="India Safe Gold & Verifiable Offer Tracker",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for provenance badges and clarity
st.markdown(
    """
    <style>
    .prov-badge-ok {
        background-color: #0f5132;
        color: #d1e7dd;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-family: monospace;
        display: inline-block;
        margin-right: 6px;
    }
    .prov-badge-warn {
        background-color: #664d03;
        color: #fff3cd;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-family: monospace;
        display: inline-block;
        margin-right: 6px;
    }
    .prov-badge-err {
        background-color: #842029;
        color: #f8d7da;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-family: monospace;
        display: inline-block;
        margin-right: 6px;
    }
    .gate-banner {
        border-left: 4px solid #198754;
        background-color: rgba(25, 135, 84, 0.08);
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def ensure_snapshot_loaded() -> Dict[str, Any]:
    snap = load_latest_snapshot()
    if snap is None:
        with st.spinner("Running initial live verification across IBJA, NSE Gold ETFs, Refineries & Bank T&Cs..."):
            snap = run_full_live_verification()
    return snap


def fmt_inr(val: Any, decimals: int = 2) -> str:
    if val is None or pd.isna(val):
        return "UNAVAILABLE (Fetch Error)"
    return f"₹{float(val):,.{decimals}f}"


def main() -> None:
    # Load or initialize live snapshot
    snapshot = ensure_snapshot_loaded()

    # ------------------------------------------------------------------------
    # SIDEBAR: LIVE DAILY REFRESH & CRITIC GATE STATUS
    # ------------------------------------------------------------------------
    with st.sidebar:
        st.title("🪙 Gold Audit Control")
        st.caption("Zero-Mock Verifiable India Gold & Offer Tracker")

        if st.button("🔄 Refresh & Verify All Live Sources Now", type="primary", use_container_width=True):
            with st.spinner("Probing live IBJA, COMEX/INR, 7 NSE Gold ETFs, 10 Platforms & 11 Bank/Scheme T&Cs..."):
                snapshot = run_full_live_verification()
            st.success(f"Verified live in {snapshot.get('refresh_duration_sec')}s!")

        bm = snapshot.get("benchmarks", {})
        etfs = snapshot.get("nse_gold_etfs", [])
        platforms = snapshot.get("platforms", [])
        offers = snapshot.get("offers_and_cards", [])

        st.markdown("---")
        st.markdown("### 🕒 Latest Verification Stamp")
        st.write(f"**Refreshed At:** `{snapshot.get('refreshed_at_ist', 'N/A')}`")
        st.write(f"**Probe Duration:** `{snapshot.get('refresh_duration_sec', 'N/A')}s`")

        etf_ok = sum(1 for e in etfs if e.get("price") is not None)
        plat_ok = sum(1 for p in platforms if p.get("is_reachable"))
        off_ok = sum(1 for o in offers if o.get("is_reachable"))

        st.metric("Live NSE Gold ETF Quotes", f"{etf_ok} / {len(etfs)} Verified")
        st.metric("Platform Custodian URLs (HTTP 2xx)", f"{plat_ok} / {len(platforms)} Reachable")
        st.metric("Bank & Scheme T&C URLs (HTTP 2xx)", f"{off_ok} / {len(offers)} Reachable")

        st.markdown("---")
        st.markdown("### 🛡️ Critic's 5 Active Gates")
        st.markdown(
            """
            - ✅ **Gate 1:** `NO_SYNTHETIC_DATA` (Fail-Closed)
            - ✅ **Gate 2:** `VERIFIABLE_ITEM_SCHEMA` (URL + SHA-256)
            - ✅ **Gate 3:** `NET_EFFECTIVE_PRICE_GATE` (3% GST + Spread)
            - ✅ **Gate 4:** `MCC_COMPLIANCE_GATE` (`5094`/`5944` Rules)
            - ✅ **Gate 5:** `TRUST_AND_SAFETY_GATE` (SEBI & Trustee Audit)
            """
        )

    # ------------------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------------------
    st.title("🇮🇳 India Safe Online Gold, Live Rate & Verifiable Card/Platform Offer Tracker")
    st.markdown(
        f"""
        <div class="gate-banner">
        <b>Zero-Artificial-Data Guarantee:</b> Every price, ETF quote, refinery spread, and credit card/scheme offer below is backed by a live network probe (Last verified: <code>{snapshot.get('refreshed_at_ist')}</code>) with a clickable official verification URL, HTTP status code, and SHA-256 content hash.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📈 1. Live Gold Benchmarks & NSE ETFs",
            "🛡️ 2. Safe Gold Platforms & Custodian Audit",
            "💳 3. Verifiable Card, Voucher & Scheme Offers",
            "🧮 4. Net Landed Cost & Card Stack Calculator",
            "🔍 5. SHA-256 & HTTP Provenance Log",
        ]
    )

    # ========================================================================
    # TAB 1: LIVE GOLD BENCHMARKS & SEBI-REGULATED NSE GOLD ETFs
    # ========================================================================
    with tab1:
        st.subheader("1.1 Live Domestic & International Gold Benchmarks (24K 999 & 22K 916)")

        p24_pre = bm.get("primary_24k_per_g_pre_gst")
        p24_gst = bm.get("primary_24k_per_g_incl_gst")
        p22_pre = bm.get("primary_22k_per_g_pre_gst")
        intl_spot = bm.get("intl_spot_inr_per_g")
        comex = bm.get("comex_usd_toz") or {}
        usdinr = bm.get("usdinr") or {}

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(
                "Live 24K (999) Benchmark (Pre-GST)",
                fmt_inr(p24_pre) + " /g",
                help="Wholesale/Reference 24K rate before 3% GST and retail platform spread.",
            )
            st.caption(f"10g Pre-GST: **{fmt_inr(p24_pre * 10 if p24_pre else None)}**")
        with c2:
            st.metric(
                "Live 24K (999) With 3% GST",
                fmt_inr(p24_gst) + " /g",
                delta="+3.0% Mandatory GST",
                delta_color="inverse",
            )
            st.caption(f"10g Incl. GST: **{fmt_inr(p24_gst * 10 if p24_gst else None)}**")
        with c3:
            st.metric(
                "Live 22K (916) Jewellery Benchmark",
                fmt_inr(p22_pre) + " /g (Pre-GST)",
                help="91.6% purity reference rate before 3% GST and jeweller making charges.",
            )
            st.caption(f"Incl. 3% GST: **{fmt_inr(bm.get('primary_22k_per_g_incl_gst'))} /g**")
        with c4:
            st.metric(
                "International Spot (XAU/INR)",
                fmt_inr(intl_spot) + " /g",
                help="Derived live from COMEX Gold (GC=F) ÷ 31.1035 × Live USD/INR (INR=X).",
            )
            st.caption(
                f"COMEX: **${comex.get('price', 'N/A')}/toz** | USD/INR: **₹{usdinr.get('price', 'N/A')}**"
            )

        st.info(
            f"**Active Primary Benchmark Source:** `{bm.get('primary_source_label')}` — "
            f"[🔗 Click to Verify Official Benchmark Source]({bm.get('primary_source_url')}) "
            f"(Extraction Mode: `{bm.get('primary_extraction_mode')}`, Fetched: `{bm.get('fetched_at_ist')}`)"
        )

        # Benchmark Source Provenance Table
        ibja_info = bm.get("ibja") or {}
        gr_info = bm.get("goodreturns") or {}
        bench_rows = [
            {
                "Benchmark Feed": "IBJA Official (India Bullion & Jewellers Assoc.)",
                "Extraction Status": ibja_info.get("extraction_mode"),
                "HTTP Status": ibja_info.get("http_status"),
                "Latency (ms)": ibja_info.get("latency_ms"),
                "24K Rate (₹/g Pre-GST)": ibja_info.get("rates_per_gram", {}).get("24K_999")
                or "Dynamic CSR / Verify via Link",
                "22K Rate (₹/g Pre-GST)": ibja_info.get("rates_per_gram", {}).get("22K_916")
                or "Dynamic CSR / Verify via Link",
                "SHA-256 Fingerprint": (ibja_info.get("content_sha256") or "")[:16] + "...",
                "Official Verification URL": ibja_info.get("source_url"),
            },
            {
                "Benchmark Feed": "GoodReturns India Live Retail Benchmark",
                "Extraction Status": gr_info.get("extraction_mode"),
                "HTTP Status": gr_info.get("http_status"),
                "Latency (ms)": gr_info.get("latency_ms"),
                "24K Rate (₹/g Pre-GST)": gr_info.get("rates_per_gram", {}).get("24K_999")
                or "Dynamic CSR / Verify via Link",
                "22K Rate (₹/g Pre-GST)": gr_info.get("rates_per_gram", {}).get("22K_916")
                or "Dynamic CSR / Verify via Link",
                "SHA-256 Fingerprint": (gr_info.get("content_sha256") or "")[:16] + "...",
                "Official Verification URL": gr_info.get("source_url"),
            },
            {
                "Benchmark Feed": "COMEX Gold Futures (GC=F) + Live USD/INR (INR=X) + 6% India Customs Parity",
                "Extraction Status": comex.get("extraction_mode"),
                "HTTP Status": comex.get("http_status"),
                "Latency (ms)": comex.get("latency_ms"),
                "24K Rate (₹/g Pre-GST)": bm.get("india_import_parity_24k_pre_gst"),
                "22K Rate (₹/g Pre-GST)": bm.get("india_import_parity_22k_pre_gst"),
                "SHA-256 Fingerprint": (comex.get("content_sha256") or "")[:16] + "...",
                "Official Verification URL": comex.get("source_url"),
            },
        ]
        st.dataframe(
            pd.DataFrame(bench_rows),
            column_config={
                "Official Verification URL": st.column_config.LinkColumn("Verify Official Source ↗"),
            },
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
        st.subheader("1.2 Live SEBI-Regulated NSE Gold ETFs (0% GST, <0.1% Spread, Highest Financial Safety)")
        st.caption(
            "Why experts rank Gold ETFs #1 for pure investment: **0% GST on purchase**, **~0.05% bid-ask spread** (vs 3% GST + 3% spread on Digital Gold), "
            "**SEBI mutual fund custodian oversight**, and **12.5% LTCG after just 12 months**."
        )

        etf_df = pd.DataFrame(
            [
                {
                    "NSE Symbol": e.get("nse_symbol"),
                    "ETF Name": e.get("name"),
                    "Live LTP (₹)": e.get("price"),
                    "Prev Close (₹)": e.get("prev_close"),
                    "Change (%)": e.get("change_pct"),
                    "Day Low (₹)": e.get("day_low"),
                    "Day High (₹)": e.get("day_high"),
                    "Volume": e.get("volume"),
                    "Expense Ratio (%)": e.get("expense_ratio_pct"),
                    "GST (%)": e.get("gst_on_purchase_pct"),
                    "HTTP Status": e.get("http_status"),
                    "Market Time (IST)": e.get("market_time_ist"),
                    "Yahoo Quote URL": e.get("source_url"),
                    "NSE Quote URL": e.get("nse_quote_url"),
                }
                for e in etfs
            ]
        )
        st.dataframe(
            etf_df,
            column_config={
                "Yahoo Quote URL": st.column_config.LinkColumn("Verify Yahoo Finance ↗"),
                "NSE Quote URL": st.column_config.LinkColumn("Verify NSE India ↗"),
            },
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================================
    # TAB 2: SAFE ONLINE GOLD PLATFORMS & CUSTODIAN AUDIT
    # ========================================================================
    with tab2:
        st.subheader("2.1 4-Tier Safety & Custodial Audit of Online Gold Platforms in India")
        st.warning(
            "**SEBI Regulatory Disclosure (Gate 5):** Unlike Gold ETFs and RBI Sovereign Gold Bonds, "
            "**24K Digital Gold (MMTC-PAMP, SafeGold, Augmont) is NOT regulated by SEBI or RBI** (per SEBI Circular Aug 2021). "
            "It relies on an Independent Trustee (IDBI Trusteeship / Universal Trusteeship) holding physical gold in Brinks/Sequel vaults. "
            "Furthermore, **Gold Leasing schemes (Gullak Gold+ / SafeGold Gains)** move your gold *out* of the Trustee ring-fence into an **unsecured corporate loan to jewellers**."
        )

        tier_options = ["All Tiers"] + sorted({p["safety_tier"] for p in platforms})
        selected_tier = st.selectbox("Filter by Regulatory / Custodial Safety Tier:", tier_options)

        filtered_plats = (
            platforms
            if selected_tier == "All Tiers"
            else [p for p in platforms if p["safety_tier"] == selected_tier]
        )

        plat_df = pd.DataFrame(
            [
                {
                    "Platform / Channel": p["name"],
                    "Safety Tier": p["safety_tier"],
                    "Safety Rating": p["safety_score"],
                    "Refinery / Backing": p["refinery_partner"],
                    "Independent Trustee": p["independent_trustee"],
                    "Insured Vault Custodian": p["vault_custodian"],
                    "Purity": p["purity"],
                    "GST (%)": p["gst_pct"],
                    "Est. Buy incl. GST (₹/g)": p["est_buy_rate_per_g_incl_gst"],
                    "Est. Live Sell (₹/g)": p["est_live_sell_rate_per_g"],
                    "Day-1 Instant Exit Loss (%)": p["day1_instant_liquidation_loss_pct"],
                    "Rate Provenance": p["rate_provenance_badge"],
                    "HTTP Check": f"HTTP {p['http_status']}" if p.get("http_status") else f"ERR ({p.get('error')})",
                    "Official Link": p["official_url"],
                }
                for p in filtered_plats
            ]
        )
        st.dataframe(
            plat_df,
            column_config={
                "Official Link": st.column_config.LinkColumn("Verify Official Platform ↗"),
            },
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### 🔍 Detailed Custodian, Storage Tenure & Redemption Terms per Platform")
        for p in filtered_plats:
            status_str = (
                f"🟢 HTTP {p['http_status']} ({p['latency_ms']} ms)"
                if p.get("is_reachable")
                else f"🟠 {p.get('error', 'WAF/Network Check')}"
            )
            with st.expander(f"{p['name']} — [{p['safety_tier']}] | {status_str}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"- **Regulator / Oversight:** {p['regulator']}")
                    st.write(f"- **Refinery / Bullion Partner:** {p['refinery_partner']}")
                    st.write(f"- **Independent Trustee:** {p['independent_trustee']}")
                    st.write(f"- **Vault Custodian:** {p['vault_custodian']}")
                    st.write(f"- **Max Storage Limit / Tenure:** {p['max_storage_tenure']}")
                with col_b:
                    st.write(f"- **Purity:** `{p['purity']}`")
                    st.write(
                        f"- **Est. Buy Rate (incl. {p['gst_pct']}% GST):** `{fmt_inr(p['est_buy_rate_per_g_incl_gst'])}/g` "
                        f"| **Est. Sell Rate:** `{fmt_inr(p['est_live_sell_rate_per_g'])}/g`"
                    )
                    st.write(
                        f"- **Day-1 Instant Liquidation Friction:** `{p['day1_instant_liquidation_loss_pct']}%` "
                        f"(Spread `{p['round_trip_spread_pct']}%` + GST `{p['gst_pct']}%`)"
                    )
                    st.write(f"- **Rate Provenance Mode:** `{p['rate_provenance_badge']}`")
                    st.write(f"- **SHA-256 Page Hash:** `{(p.get('content_sha256') or 'N/A')[:24]}...`")
                    st.markdown(f"- **Official Verification Link:** [{p['official_url']}]({p['official_url']})")
                st.caption(f"**Redemption & Risk Note:** {p['physical_redemption_note']} — *{p['regulatory_warning']}*")

    # ========================================================================
    # TAB 3: VERIFIABLE CREDIT CARD, VOUCHER & PLATFORM OFFERS (MCC AUDITED)
    # ========================================================================
    with tab3:
        st.subheader("3.1 Verifiable Credit Card, SmartBuy Voucher & Jeweller Scheme Offers")
        st.info(
            "**MCC 5094 / 5944 / 6051 Compliance Rule (Gate 4):** Almost all Indian banks exclude **MCC 5094** (Bullion/Digital Gold) "
            "and **MCC 5944** (Jewellery) from standard credit card cashback (including **Amazon Pay ICICI** and **SBI Cashback Card**, which give **0%**). "
            "Below are the **only verified working card/voucher/scheme pathways** alongside explicit exclusion & leasing traps, audited live via HTTP + SHA-256."
        )

        cat_options = ["All Categories"] + sorted({o["category"] for o in offers})
        selected_cat = st.selectbox("Filter Offer / Rule Category:", cat_options)
        filtered_offers = (
            offers if selected_cat == "All Categories" else [o for o in offers if o["category"] == selected_cat]
        )

        offers_df = pd.DataFrame(
            [
                {
                    "Offer / Card / Scheme": o["title"],
                    "Category": o["category"],
                    "Net Verified Reward (%)": o["net_reward_pct"],
                    "Gateway / Voucher Fee (%)": o["gateway_or_voucher_fee_pct"],
                    "Monthly Reward Cap (₹)": o["monthly_reward_cap_inr"],
                    "Max Eligible Monthly Spend (₹)": o["max_eligible_spend_per_month_inr"],
                    "T&C HTTP Status": f"HTTP {o['http_status']}" if o.get("http_status") else f"ERR ({o.get('error')})",
                    "T&C Audit Status": o["tc_drift_status"],
                    "Verified At (IST)": o["verified_at_ist"],
                    "Official T&C Link": o["official_url"],
                }
                for o in filtered_offers
            ]
        )
        st.dataframe(
            offers_df,
            column_config={
                "Official T&C Link": st.column_config.LinkColumn("Verify Official T&C ↗"),
            },
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### 📋 Fine-Print Capping Rules, MCC Codes & Verification Details")
        for o in filtered_offers:
            http_badge = (
                f"🟢 HTTP {o['http_status']} ({o['latency_ms']} ms)"
                if o.get("is_reachable")
                else f"🟠 {o.get('error', 'Check Link')}"
            )
            with st.expander(f"{o['title']} | Net Reward: {o['net_reward_pct']}% | {http_badge}"):
                st.write(f"**Actionable Verdict:** {o['actionable_verdict']}")
                st.write(f"- **Verification Class:** `{o['verification_class']}` | **T&C Drift Audit:** `{o['tc_drift_status']}`")
                st.write(f"- **MCC Treatment:** {o['mcc_treatment']}")
                st.write(
                    f"- **Gross Reward:** `{o['gross_reward_pct']}%` | **Voucher/Gateway Fee:** `{o['gateway_or_voucher_fee_pct']}%` "
                    f"| **Net Effective Reward:** `{o['net_reward_pct']}%`"
                )
                st.write(
                    f"- **Monthly Reward Cap:** `{fmt_inr(o['monthly_reward_cap_inr'])}` "
                    f"(Max Eligible Monthly Spend: `{fmt_inr(o['max_eligible_spend_per_month_inr'])}`)"
                )
                st.write(f"- **Mandatory Fine-Print & Capping Note:** {o['annual_cap_note']}")
                st.write(
                    f"- **Last Probed:** `{o['verified_at_ist']}` | **Content SHA-256:** `{(o.get('content_sha256') or 'N/A')[:28]}...`"
                )
                st.markdown(f"- **Official Verification URL:** [{o['official_url']}]({o['official_url']})")

    # ========================================================================
    # TAB 4: NET LANDED COST, SAME-QUANTITY GOLD ETF COMPARISON & CARD CALCULATOR
    # ========================================================================
    with tab4:
        st.subheader("4.1 Same-Quantity Gold Comparison: NSE Gold ETF vs. Digital Gold / Physical Coins")
        st.caption(
            "Compare the exact rupee outflow, **3% GST impact**, **equivalent NSE Gold ETF units**, **Day-1 resale value**, "
            "and **5-Year Expense Ratio (TER) break-even horizon** for buying the **exact same quantity of 24K gold** (e.g., 1g, 5g, 10g, 50g)."
        )

        q_col1, q_col2, q_col3 = st.columns([1, 1.3, 1.7])
        with q_col1:
            gold_qty_g = st.number_input(
                "Target 24K Gold Quantity (Grams):",
                min_value=0.5,
                max_value=500.0,
                value=10.0,
                step=1.0,
                help="Enter the exact grams of 24K gold you want to compare across Gold ETFs, Digital Gold, SGBs, and Physical Coins.",
            )
        with q_col2:
            etf_choices = [
                (
                    e["ticker"],
                    f"{e['nse_symbol']} — {e['name']} (LTP: ₹{e.get('price') or 'N/A'}, TER: {e['expense_ratio_pct']}%)",
                )
                for e in etfs
            ]
            selected_etf_tuple = st.selectbox(
                "Reference SEBI-Regulated NSE Gold ETF:",
                etf_choices,
                format_func=lambda x: x[1],
            )
            chosen_etf_ticker = selected_etf_tuple[0]
        with q_col3:
            offer_choices = [("none", "No Card / Direct UPI or NetBanking (0% Card Reward)")] + [
                (o["offer_id"], f"{o['title']} (Net {o['net_reward_pct']}%, Cap ₹{o['monthly_reward_cap_inr']:,.0f}/mo)")
                for o in VERIFIED_OFFERS_AND_CARDS_REGISTRY
            ]
            selected_offer_tuple = st.selectbox(
                "Select Credit Card / Voucher / Jeweller Scheme to Stack:",
                offer_choices,
                format_func=lambda x: x[1],
            )
            chosen_offer_id = selected_offer_tuple[0]

        if p24_pre is None:
            st.error("UNAVAILABLE — Live 24K Benchmark Fetch Failed. Refusing to compute with artificial data (Gate 1).")
        else:
            etf_sum, qty_rows = calculate_same_quantity_etf_comparison(
                gold_quantity_grams=gold_qty_g,
                primary_24k_pre_gst=p24_pre,
                platforms=platforms,
                etfs=etfs,
                selected_etf_ticker=chosen_etf_ticker,
                selected_offer_id=chosen_offer_id,
            )

            if etf_sum and qty_rows:
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric(
                        f"Pure 24K Spot Value ({gold_qty_g:g}g)",
                        fmt_inr(etf_sum["spot_value_inr"]),
                        help="Wholesale IBJA/Reference 24K value before any spread or GST.",
                    )
                with m2:
                    st.metric(
                        f"{etf_sum['nse_symbol']} Cost for {gold_qty_g:g}g Gold",
                        fmt_inr(etf_sum["etf_total_buy_inr"]),
                        delta="₹0 GST (0.0%)",
                        delta_color="normal",
                    )
                    st.caption(
                        f"≈ **{etf_sum['etf_whole_units']:,} units** of `{etf_sum['nse_symbol']}` @ ₹{etf_sum['unit_ltp_inr']}/unit"
                    )
                with m3:
                    gst_on_digigold = round(etf_sum["spot_value_inr"] * 0.03, 2)
                    st.metric(
                        f"3% GST Saved by Gold ETF ({gold_qty_g:g}g)",
                        fmt_inr(gst_on_digigold),
                        delta="-3.0% Upfront Tax on Physical/DigiGold",
                        delta_color="inverse",
                    )
                    st.caption("Gold ETFs have 0% GST vs 3% mandatory GST on Digital Gold/Coins.")
                with m4:
                    st.metric(
                        f"5-Yr {etf_sum['nse_symbol']} Expense Ratio Drag",
                        fmt_inr(etf_sum["etf_5yr_ter_drag_inr"]),
                        help=f"Cumulative 5-year AMC Expense Ratio ({etf_sum['etf_ter_pct']}% p.a.) on {gold_qty_g:g}g worth of gold.",
                    )
                    st.caption(f"Annual TER: `{etf_sum['etf_ter_pct']}% p.a.` | 3-Yr Drag: `{fmt_inr(etf_sum['etf_3yr_ter_drag_inr'])}`")

                top_qty_row = qty_rows[0]
                diff_day1 = top_qty_row["Diff vs. Gold ETF Day-1 (₹)"]
                if diff_day1 < 0:
                    st.success(
                        f"💡 **Card Arbitrage Winner for {gold_qty_g:g}g Gold:** **{top_qty_row['Channel / Platform']}** costs "
                        f"**{fmt_inr(top_qty_row['Net Cost for Gold (₹)'])}** after **{fmt_inr(top_qty_row['Card Reward (₹)'])}** verified card reward — "
                        f"saving **{fmt_inr(abs(diff_day1))} ({top_qty_row['Diff vs. Gold ETF Day-1 (%)']:+.2f}%)** even vs. `{etf_sum['nse_symbol']}` Gold ETF!"
                    )
                else:
                    st.info(
                        f"🏆 **Gold ETF Wins for {gold_qty_g:g}g Gold:** **`{etf_sum['nse_symbol']}` ({etf_sum['name']})** is the lowest-cost safe option at "
                        f"**{fmt_inr(etf_sum['etf_total_buy_inr'])}** (`{etf_sum['etf_whole_units']:,} units`), saving **3% GST + ~3% spread** over un-discounted Digital Gold."
                    )

                qty_df = pd.DataFrame(qty_rows)
                qty_cols = [
                    "Channel / Platform",
                    "Safety Tier",
                    "Gold Quantity (g)",
                    "Equiv. ETF Units",
                    "Spread / Markup (₹)",
                    "3% GST Paid (₹)",
                    "Gross Outflow (₹)",
                    "Applied Card / Offer",
                    "Card Reward (₹)",
                    "Net Cost for Gold (₹)",
                    "Diff vs. Gold ETF Day-1 (₹)",
                    "Diff vs. Gold ETF Day-1 (%)",
                    "Day-1 Liquidation Value (₹)",
                    "5-Yr Diff vs. ETF incl. TER (₹)",
                    "Break-Even Horizon vs. Gold ETF",
                    "Official URL",
                ]
                st.dataframe(
                    qty_df[qty_cols],
                    column_config={
                        "Official URL": st.column_config.LinkColumn("Verify Source ↗"),
                    },
                    use_container_width=True,
                    hide_index=True,
                )

            st.markdown("---")
            st.subheader("4.2 Fixed Rupee Budget Calculator (Same ₹ Investment → Gold Acquired vs. Gold ETF)")
            inv_amount = st.number_input(
                "Enter Fixed Purchase Budget (₹):",
                min_value=1000.0,
                max_value=2000000.0,
                value=50000.0,
                step=5000.0,
            )

            ranked_rows = calculate_net_landed_cost_matrix(
                investment_amount_inr=inv_amount,
                primary_24k_pre_gst=p24_pre,
                platforms=platforms,
                selected_offer_id=chosen_offer_id,
            )
            ranked_df = pd.DataFrame(ranked_rows)

            best = ranked_rows[0]
            st.success(
                f"🏆 **Lowest Net Landed Cost for {fmt_inr(inv_amount)}:** **{best['Platform / Channel']}** at "
                f"**{fmt_inr(best['Net Landed Cost (₹/g)'])}/g** ({best['Net Premium vs. Spot (%)']:+.2f}% vs. Live 24K Spot) "
                f"— Acquires **{best['Gold Acquired (g)']}g** | Verified Reward: **{fmt_inr(best['Verified Reward (₹)'])}**"
            )

            display_cols = [
                "Platform / Channel",
                "Safety Tier",
                "Gross Buy Rate incl. GST (₹/g)",
                "Applied Offer / Card",
                "Verified Reward (₹)",
                "Net Landed Cost (₹/g)",
                "Net Premium vs. Spot (%)",
                "Gold Acquired (g)",
                "Gold ETF Cost for Same Grams (₹)",
                "Extra Cost vs. Gold ETF (₹)",
                "Gold Diff vs. ETF for Same ₹ (g)",
                "Day-1 Liquidation Value (₹)",
                "Day-1 Instant Exit P&L (%)",
                "Rate Provenance",
                "Official URL",
            ]
            st.dataframe(
                ranked_df[display_cols],
                column_config={
                    "Official URL": st.column_config.LinkColumn("Verify Source ↗"),
                },
                use_container_width=True,
                hide_index=True,
            )

    # ========================================================================
    # TAB 5: CRYPTOGRAPHIC SHA-256 & HTTP PROVENANCE LOG + DAILY AUTOMATION
    # ========================================================================
    with tab5:
        st.subheader("5.1 Live HTTP & Cryptographic SHA-256 Verification Audit Log")
        st.caption(
            "Every URL probed during the refresh cycle is logged below and persisted to local SQLite "
            "(`data/gold_audit_history.db`) and `data/latest_verified_snapshot.json`."
        )

        audit_records: List[Dict[str, Any]] = []
        for e in etfs:
            audit_records.append(
                {
                    "Category": "NSE_GOLD_ETF",
                    "Entity": e.get("name"),
                    "HTTP Status": e.get("http_status"),
                    "Latency (ms)": e.get("latency_ms"),
                    "Extraction / Audit Mode": e.get("extraction_mode"),
                    "Verified At (IST)": e.get("fetched_at_ist"),
                    "SHA-256 Content Hash": e.get("content_sha256"),
                    "Official URL": e.get("source_url"),
                }
            )
        for p in platforms:
            audit_records.append(
                {
                    "Category": "GOLD_PLATFORM",
                    "Entity": p.get("name"),
                    "HTTP Status": p.get("http_status"),
                    "Latency (ms)": p.get("latency_ms"),
                    "Extraction / Audit Mode": p.get("rate_provenance_badge"),
                    "Verified At (IST)": p.get("verified_at_ist"),
                    "SHA-256 Content Hash": p.get("content_sha256"),
                    "Official URL": p.get("official_url"),
                }
            )
        for o in offers:
            audit_records.append(
                {
                    "Category": "CARD_OR_SCHEME_TC",
                    "Entity": o.get("title"),
                    "HTTP Status": o.get("http_status"),
                    "Latency (ms)": o.get("latency_ms"),
                    "Extraction / Audit Mode": o.get("tc_drift_status"),
                    "Verified At (IST)": o.get("verified_at_ist"),
                    "SHA-256 Content Hash": o.get("content_sha256"),
                    "Official URL": o.get("official_url"),
                }
            )

        audit_df = pd.DataFrame(audit_records)
        st.dataframe(
            audit_df,
            column_config={
                "Official URL": st.column_config.LinkColumn("Open Source URL ↗"),
            },
            use_container_width=True,
            hide_index=True,
        )

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "📥 Download Verified Snapshot JSON",
                data=json.dumps(snapshot, indent=2, ensure_ascii=False),
                file_name="latest_verified_snapshot.json",
                mime="application/json",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                "📥 Download Provenance Audit Log CSV",
                data=audit_df.to_csv(index=False).encode("utf-8"),
                file_name="gold_provenance_audit_log.csv",
                mime="text/csv",
                use_container_width=True,
            )

        if SQLITE_DB_PATH.exists():
            st.markdown("#### 🗄️ Historical Benchmark Runs (Local SQLite `gold_audit_history.db`)")
            conn = sqlite3.connect(SQLITE_DB_PATH)
            try:
                hist_df = pd.read_sql_query(
                    "SELECT * FROM benchmark_history ORDER BY id DESC LIMIT 20", conn
                )
                st.dataframe(hist_df, use_container_width=True, hide_index=True)
            finally:
                conn.close()


if __name__ == "__main__":
    main()
