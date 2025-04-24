import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load CSV file
url = "https://drive.google.com/uc?export=download&id=1U9LrKE5Qr6t8oUf6UiEZF20g3ZriMTLI"
data = pd.read_csv(url)

# Sidebar filters
st.sidebar.title("Filter Pelanggan")
age_range = st.sidebar.slider("Rentang Usia", int(data["age"].min()), int(data["age"].max()), (20, 40))
gender = st.sidebar.selectbox("Jenis Kelamin", options=["All", "Male", "Female"])
region_filter = st.sidebar.multiselect("Pilih Region", options=data["region"].unique(), default=data["region"].unique())
promo_filter = st.sidebar.selectbox("Gunakan Promosi?", options=["All", "Yes", "No"])

# Apply filters
filtered_data = data[
    (data["age"] >= age_range[0]) & (data["age"] <= age_range[1]) &
    (data["region"].isin(region_filter))
]
if gender != "All":
    filtered_data = filtered_data[filtered_data["gender"] == gender]
if promo_filter != "All":
    filtered_data = filtered_data[filtered_data["promotion_usage"] == (1 if promo_filter == "Yes" else 0)]

# Title
st.title("Customer Data Dashboard")
st.markdown("---")

# Summary
st.markdown("### Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Pengeluaran", f"${filtered_data['purchase_amount'].mean():,.0f}")
col2.metric("Rata-rata Kepuasan", f"{filtered_data['satisfaction_score'].mean():.2f}")
col3.metric("Total Pelanggan", len(filtered_data))
st.markdown("---")

# Chart 1: Purchase Amount by Product Category
st.markdown("### Pengeluaran Berdasarkan Kategori Produk")
fig1 = px.bar(filtered_data, x="product_category", y="purchase_amount", color="product_category",
              labels={"purchase_amount": "Jumlah Pembelian"}, title="Total Pembelian per Kategori")
st.plotly_chart(fig1)
st.markdown("---")

# Chart 2: Histogram Satisfaction Score
st.markdown("### Distribusi Skor Kepuasan")
fig2 = px.histogram(filtered_data, x="satisfaction_score", nbins=10, color="satisfaction_score",
                    title="Sebaran Skor Kepuasan Pelanggan")
st.plotly_chart(fig2)
st.markdown("---")

# Chart 3: Customer Distribution by Region
st.markdown("### Distribusi Pelanggan per Region")
fig3 = px.pie(filtered_data, names="region", title="Distribusi Wilayah")
st.plotly_chart(fig3)
st.markdown("---")

# Chart 4: Rata-rata Pengeluaran per Loyalty Status
st.markdown("### Pengeluaran Rata-rata Berdasarkan Status Loyalitas")
avg_spending = filtered_data.groupby("loyalty_status")["purchase_amount"].mean().reset_index()
fig4 = px.bar(avg_spending, x="loyalty_status", y="purchase_amount", color="loyalty_status",
              title="Rata-rata Jumlah Pembelian per Loyalitas")
st.plotly_chart(fig4)
st.markdown("---")

# Chart 5: Purchase Frequency vs Satisfaction
st.markdown("### Frekuensi Pembelian vs Kepuasan")
fig5 = px.box(filtered_data, x="purchase_frequency", y="satisfaction_score", color="purchase_frequency",
              title="Skor Kepuasan per Frekuensi Pembelian")
st.plotly_chart(fig5)
st.markdown("---")

# Chart 6: Promotion Usage Impact
st.markdown("### Pengaruh Promosi terhadap Jumlah Pembelian")
fig6 = px.box(filtered_data, x="promotion_usage", y="purchase_amount", color="promotion_usage",
              title="Jumlah Pembelian berdasarkan Penggunaan Promosi",
              labels={"promotion_usage": "Gunakan Promosi (0=No, 1=Yes)"})
st.plotly_chart(fig6)
st.markdown("---")

# Show raw data (optional)
if st.checkbox("Tampilkan Data Mentah"):
    st.write(filtered_data)