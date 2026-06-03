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
    "氣體類型", ["理想氣體", "凡德瓦氣體"]
)
gas_molecule = st.sidebar.selectbox(
    "分子類型", ["單原子分子","雙原子分子"]
)
T = st.sidebar.number_input("溫度(K)", min_value = 0.1)
n = st.sidebar.number_input("物質的量(mol)", min_value = 0.1)
R = 8.314
a = 3.64 if gas_type == "凡德瓦氣體" else 0.0
b = 0.0427 if gas_type == "凡德瓦氣體" else 0.0

if gas_molecule == "單原子分子":
    Cv = 1.50 * R
else:
    Cv = 2.50 * R
    
V_array = np.linspace(0.5, 10.0, 50)

# 單位換算
V_m3 = V_array * 1e-3
b_m3 = b * 1e-3 * n
a_pa = a * 0.1

# 算壓力
if gas_type == "理想氣體":
    P_array = (n * R * T) / V_m3
else:
    P_array = (n * R * T) / (V_m3 - b_m3) - a_pa * (n / V_m3) ** 2

P_bar = P_array / 1e5

# 算內能
if gas_type == "理想氣體":
    U_array = np.full_like(V_array, 1.5 * n * R * T)
else:
    U_array = Cv * n * R * T - (a_pa * (n**2) / V_m3)

#算總熵
Vm_array = V_m3 / n  
if gas_type == "理想氣體":
    S_array = Cv * np.log(T) + R * np.log(Vm_array)
else:
    S_array = Cv * np.log(T) + R * np.log(Vm_array - (b * 1e-3))

S_array = n * S_array

df = pd.DataFrame(
    {
        "體積": V_array,
        "壓力": P_bar,
        "內能": U_array,
        "熵": S_array
    }
)

# 算PV
df["PV_乘積"] = df["體積"] * df["壓力"]

# 網頁前端
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("數據圖表")

    chart_data = df.set_index("體積")

    st.markdown("**壓力對體積**")
    st.line_chart(chart_data["壓力"], color="#FF4B4B")

    st.markdown("**內能對體積**")
    st.line_chart(chart_data["內能"], color="#0068C9")

    st.markdown("**熵對體積**")
    st.line_chart(chart_data["熵"], color="#2CA02C")

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

col3, col4, col5, col6 = st.columns(4)
with col3:
    st.metric(
        label="最高壓力",
        value=f"{df['壓力'].max():.2f} bar",
    )
with col4:
    st.metric(
        label="最低內能",
        value=f"{df['內能'].min():.2f} J",
    )
with col5:
    st.metric(
        label="最大熵",
        value=f"{df['熵'].max():.2f} ",
    )
with col6:
    pv_std = df["PV_乘積"].std()
    st.metric(
        label="PV標準差 (波動度)",
        value=f"{pv_std:.4f}",
        help="理想氣體的標準差應接近 0",
    )
st.write("----")
st.subheader("程式碼邏輯:")
st.markdown("""
        1. NumPy在後端進行物理公式矩陣運算。
        2. Pandas將算好的多維陣列組裝成有命名、有結構的DataFrame，並計算。
        3. Streamlit當作前端橋樑，直接用st.dataframe(df)把 Pandas 的表格呈現到前端。
    """)
