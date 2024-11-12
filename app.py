import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# アプリのタイトル
st.title("Enhanced EDA Data Visualization App")

# ファイルアップロード
uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

# アップロードされたファイルを読み込み
if uploaded_file:
    # データを読み込む（カンマ区切り）
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    # Perturbationが1のデータを黒い線でプロット
    fig1 = go.Figure()
    perturbation_1 = data[data["Perturbation"] == 1]
    fig1.add_trace(go.Scatter(x=perturbation_1["Time_sec"], y=perturbation_1["EDA"],
                             mode="lines", line=dict(color="white", width=0.5),
                             name="Perturbation: 1"))

    # Perturbationが2のデータを青い線でプロット
    perturbation_2 = data[data["Perturbation"] == 2]
    fig1.add_trace(go.Scatter(x=perturbation_2["Time_sec"], y=perturbation_2["EDA"],
                             mode="lines", line=dict(color="blue", width=0.5),
                             name="Perturbation: 2"))

    # Dig1が1のポイントを赤い丸で強調表示
    dig1_points = data[data["Dig1"] == 5]
    fig1.add_trace(go.Scatter(x=dig1_points["Time_sec"], y=dig1_points["EDA"],
                             mode="markers", marker=dict(color="red", size=10, line=dict(color="black", width=1)),
                             name="Dig1 Points"))

    # グラフのレイアウト設定（背景白）
    fig1.update_layout(title="EDA over Time with Perturbation Colors and Dig1 Points",
                       xaxis_title="Time_sec", yaxis_title="EDA",
                       template="plotly_white")

    # 2つ目のプロット（例: 移動平均のプロット）
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data["Time_sec"], y=data["EDA"].rolling(window=10).mean(),
                             mode="lines", line=dict(color="green", width=2),
                             name="Moving Average (Window=10)"))

    fig2.update_layout(title="Moving Average of EDA (Window=10)",
                       xaxis_title="Time_sec", yaxis_title="EDA",
                       template="plotly_white")

    # 各グラフを縦に表示
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

    # 選択されたポイントを保持するためのセッション状態
    if "selected_points" not in st.session_state:
        st.session_state.selected_points = []

    # 手動でポイントを追加するための数値入力
    st.write("## Select Points Manually")
    selected_x = st.number_input("Select X (Time_sec)", value=0.0)
    selected_y = st.number_input("Select Y (EDA)", value=0.0)

    # 入力されたポイントをセッション状態に追加
    if st.button("Add Point"):
        st.session_state.selected_points.append({"Time_sec": selected_x, "EDA": selected_y})

    # テーブル内のポイントの削除
    if st.button("Clear Points"):
        st.session_state.selected_points.clear()

    # 選択されたポイントの表示
    st.write("### Selected Points Table")
    if st.session_state.selected_points:
        st.write(pd.DataFrame(st.session_state.selected_points))
