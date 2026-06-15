import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi halaman utama dashboard
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# ==========================================
# LOAD DATA (Gunakan caching agar cepat load)
# ==========================================
@st.cache_data
def load_data():
    # Pastikan file CSV gabungan sudah kamu bersihkan atau panggil salah satu file contoh jika di lokal
    # Di sini kita buat fungsi membaca data utama
    df = pd.read_csv("main_data.csv") # Sesuaikan nama file di local nanti
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    return df

# Coba muat data
try:
    df_clean = load_data()
except:
    st.error("Silakan pastikan file dataset (*.csv) berada di folder yang sama dengan file dashboard.py ini!")
    st.stop()

# ==========================================
# SIDEBAR / FILTER DATA
# ==========================================
st.sidebar.header("Filter Analisis")
# Filter Tahun
available_years = sorted(df_clean['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun:", available_years, index=available_years.index(2015))

# Filter data berdasarkan tahun yang dipilih oleh user
df_filtered = df_clean[df_clean['year'] == selected_year]

# ==========================================
# MAIN DASHBOARD CONTENT
# ==========================================
st.title("📊 Air Quality Analysis Dashboard (PRSA Dataset)")
st.markdown("Dashboard interaktif untuk memantau tren kualitas udara dan faktor meteorologi.")

# Baris 1: Tampilkan KPI / Ringkasan Singkat menggunakan kolom
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rata-rata PM2.5", f"{df_filtered['PM2.5'].mean():.2f} µg/m³")
with col2:
    st.metric("Rata-rata SO2", f"{df_filtered['SO2'].mean():.2f} µg/m³")
with col3:
    st.metric("Rata-rata Suhu (TEMP)", f"{df_filtered['TEMP'].mean():.2f} °C")

st.write("---")

# Baris 2: Visualisasi Grafik Interaktif
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.subheader(f"📈 Tren Bulanan PM2.5 di Tahun {selected_year}")
    eda_tren = df_filtered.groupby('month')['PM2.5'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=eda_tren, x='month', y='PM2.5', marker='o', color='red', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)

with graph_col2:
    st.subheader(f"🔍 Korelasi Suhu (TEMP) vs Kadar SO2 ({selected_year})")
    # Ambil sampel data jika terlalu besar agar grafiknya ringan dibuka
    df_sample = df_filtered.sample(min(1000, len(df_filtered)), random_state=42)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(data=df_sample, x='TEMP', y='SO2', scatter_kws={'alpha':0.4}, line_kws={'color':'red'}, ax=ax)
    ax.set_xlabel("Suhu Udara (°C)")
    ax.set_ylabel("Konsentrasi SO2 (µg/m³)")
    st.pyplot(fig)

st.caption("Proyek Akhir Belajar Analisis Data dengan Python - Dicoding")
