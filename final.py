#Python final project
#葉庭涵 B135090026
#https://finalproject-ljvsdder6dvb7pn5ueh9vj.streamlit.app/

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="熱力學作業解題網站", layout="wide")
st.title("熱力學作業解題網站")
st.markdown(
    "針對普物二:熱力學"
)

st.sidebar.header("參數設定")
gas_type = st.sidebar.selectbox(
    "氣體公式", ["理想氣體", "凡德瓦氣體"]
)
T = st.sidebar.number_input("溫度(K)")
n = st.sidebar.number_input("物質的量(mol)")
R = 8.314
a = 3.64 if gas_type == "凡德瓦氣體 (Van der Waals)" else 0.0
b = 0.0427 if gas_type == "凡德瓦氣體 (Van der Waals)" else 0.0

V_array = np.linspace(0.5, 10.0, 50)

# 單位換算
V_m3 = V_array * 1e-3
b_m3 = b * 1e-3 * n
a_pa = a * 0.1

# 算壓力
if gas_type == "理想氣體 (Ideal Gas)":
    P_array = (n * R * T) / V_m3
else:
    P_array = (n * R * T) / (V_m3 - b_m3) - a_pa * (n / V_m3) ** 2

P_bar = P_array / 1e5

# 算內能
if gas_type == "理想氣體 (Ideal Gas)":
    U_array = np.full_like(V_array, 1.5 * n * R * T)
else:
    U_array = 1.5 * n * R * T - (a_pa * (n**2) / V_m3)

df = pd.DataFrame(
    {
        "體積": V_array,
        "壓力": P_bar,
        "內能": U_array,
    }
)

# 算PV
df["PV_乘積_bar_L"] = df["體積_Volume_L"] * df["壓力_Pressure_bar"]

# 網頁前端
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("數據圖表")

    chart_data = df.set_index("體積_Volume_L")

    st.markdown("**壓力對體積**")
    st.line_chart(chart_data["壓力_Pressure_bar"], color="#FF4B4B")

    st.markdown("**內能對體積**")
    st.line_chart(chart_data["內能_InternalEnergy_J"], color="#0068C9")

with col2:
    st.subheader("數據表")
    st.dataframe(df.style.format("{:.3f}"), height=300)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下載此熱力學數據 (CSV)",
        data=csv,
        file_name=f"thermo_data_{T}K.csv",
        mime="text/csv",
    )

st.write("---")
st.subheader("數據摘要")

col3, col4, col5 = st.columns(3)
with col3:
    st.metric(
        label="最高壓力",
        value=f"{df['壓力_Pressure_bar'].max():.2f} bar",
    )
with col4:
    st.metric(
        label="最低內能",
        value=f"{df['內能_InternalEnergy_J'].min():.2f} J",
    )
with col5:
    pv_std = df["PV_乘積_bar_L"].std()
    st.metric(
        label="PV標準差 (波動度)",
        value=f"{pv_std:.4f}",
        help="理想氣體的標準差應接近 0",
    )

st.markdown("""
程式碼背後的運作邏輯：
1. NumPy在背景負責快速進行大量的物理公式矩陣運算。
2. Pandas將算好的多維陣列組裝成有標籤、有結構的DataFrame，並計算（如 PV_乘積）。
3. Streamlit當作前端橋樑，直接用st.dataframe(df)把 Pandas 的表格完美畫在瀏覽器上，並提供一鍵下載。
""")
