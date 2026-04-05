import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
main_data = pd.read_csv(BASE_DIR / "main_data.csv", parse_dates=["order_purchase_timestamp"])
rfm = pd.read_csv(BASE_DIR / "rfm_segment.csv")

st.title("Dashboard Analisis E-Commerce")
st.caption("Fokus analisis: performa penjualan, pengalaman pengiriman, dan segmentasi pelanggan (RFM).")

min_date = main_data["order_purchase_timestamp"].min().date()
max_date = main_data["order_purchase_timestamp"].max().date()

st.sidebar.header("Filter Dashboard")
selected_states = st.sidebar.multiselect(
    "Pilih state pelanggan",
    options=sorted(main_data["customer_state"].dropna().unique().tolist()),
    default=[]
)
date_range = st.sidebar.date_input(
    "Rentang tanggal pembelian",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = main_data.copy()
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["order_purchase_timestamp"].dt.date >= start_date) &
        (filtered["order_purchase_timestamp"].dt.date <= end_date)
    ]
if selected_states:
    filtered = filtered[filtered["customer_state"].isin(selected_states)]

total_orders = int(filtered["order_id"].nunique())
total_revenue = float(filtered["payment_value"].sum())
avg_review = float(filtered["review_score"].mean()) if not filtered.empty else 0.0
late_rate = float(filtered["is_late"].mean() * 100) if not filtered.empty else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
col3.metric("Rata-rata Review", f"{avg_review:.2f}")
col4.metric("Late Delivery Rate", f"{late_rate:.1f}%")

if filtered.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

left, right = st.columns(2)

with left:
    st.subheader("Tren Revenue Bulanan")
    monthly = filtered.groupby("purchase_month")["payment_value"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    monthly.plot(ax=ax, marker="o")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Revenue (R$)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)
    st.pyplot(fig)

with right:
    st.subheader("Top 10 Kategori Utama Berdasarkan Revenue")
    top_cat = (filtered.groupby("primary_category")["payment_value"]
                     .sum()
                     .sort_values(ascending=False)
                     .head(10)
                     .sort_values())
    fig, ax = plt.subplots(figsize=(8, 4))
    top_cat.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (R$)")
    ax.set_ylabel("Kategori")
    st.pyplot(fig)

left, right = st.columns(2)

with left:
    st.subheader("Review vs Keterlambatan Pengiriman")
    delay_order = [
        "Lebih cepat >10 hari",
        "Tepat / lebih cepat <=10 hari",
        "Terlambat 1-5 hari",
        "Terlambat >5 hari",
    ]
    delay_review = (filtered.groupby("delay_bucket")["review_score"]
                          .mean()
                          .reindex(delay_order)
                          .dropna())
    fig, ax = plt.subplots(figsize=(8, 4))
    delay_review.plot(kind="bar", ax=ax)
    ax.set_xlabel("Bucket Keterlambatan")
    ax.set_ylabel("Rata-rata Review")
    ax.tick_params(axis="x", rotation=20)
    ax.set_ylim(0, 5)
    st.pyplot(fig)

with right:
    st.subheader("10 State dengan Late Rate Tertinggi")
    late_by_state = filtered.groupby("customer_state").agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum")
    )
    late_by_state = late_by_state[late_by_state["total_orders"] >= 100]
    late_by_state["late_rate"] = late_by_state["late_orders"] / late_by_state["total_orders"] * 100
    late_by_state = late_by_state.sort_values("late_rate", ascending=False).head(10).sort_values("late_rate")
    fig, ax = plt.subplots(figsize=(8, 4))
    late_by_state["late_rate"].plot(kind="barh", ax=ax)
    ax.set_xlabel("Late Rate (%)")
    ax.set_ylabel("State")
    st.pyplot(fig)

st.subheader("Segmentasi Pelanggan (RFM)")
seg = rfm["segment"].value_counts().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 4))
seg.plot(kind="bar", ax=ax)
ax.set_xlabel("Segmen")
ax.set_ylabel("Jumlah Pelanggan")
ax.tick_params(axis="x", rotation=20)
st.pyplot(fig)

st.markdown(
    '''
    **Insight utama dashboard**
    - Revenue terbesar datang dari kategori dengan kontribusi kategori utama yang konsisten sepanjang periode analisis.
    - Keterlambatan pengiriman berasosiasi kuat dengan turunnya review score.
    - Segmentasi RFM membantu memisahkan pelanggan terbaik, loyal, dan yang mulai berisiko churn.
    '''
)
