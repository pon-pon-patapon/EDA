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

    # EDAプロットの作成
    fig = go.Figure()

    # Perturbationが1のデータを黒い線でプロット
    perturbation_1 = data[data["Perturbation"] == 1]
    fig.add_trace(go.Scatter(x=perturbation_1["Time_sec"], y=perturbation_1["EDA"],
                             mode="lines", line=dict(color="black", width=2),
                             name="Perturbation: 1"))

    # Perturbationが2のデータを青い線でプロット
    perturbation_2 = data[data["Perturbation"] == 2]
    fig.add_trace(go.Scatter(x=perturbation_2["Time_sec"], y=perturbation_2["EDA"],
                             mode="lines", line=dict(color="blue", width=2),
                             name="Perturbation: 2"))

    # Dig1が1のポイントを赤い丸で強調表示
    dig1_points = data[data["Dig1"] == 1]
    fig.add_trace(go.Scatter(x=dig1_points["Time_sec"], y=dig1_points["EDA"],
                             mode="markers", marker=dict(color="red", size=10, line=dict(color="black", width=1)),
                             name="Dig1 Points"))

    # グラフのタイトルとラベルを設定
    fig.update_layout(title="EDA over Time with Perturbation Colors and Dig1 Points",
                      xaxis_title="Time_sec", yaxis_title="EDA")

    # 選択されたポイントを保持するためのセッション状態
    if "selected_points" not in st.session_state:
        st.session_state.selected_points = []

    # 選択されたポイントをプロットに追加
    for point in st.session_state.selected_points:
        fig.add_trace(go.Scatter(x=[point["Time_sec"]], y=[point["EDA"]],
                                 mode="markers", marker=dict(color="blue", size=10),
                                 name="Selected Point"))

    # グラフを表示
    st.plotly_chart(fig, use_container_width=True)

    # 選択されたポイントのテーブル表示
    st.write("## Selected Points Table")
    selected_x = st.number_input("Select X (Time_sec)", value=0.0)
    selected_y = st.number_input("Select Y (EDA)", value=0.0)

    # 選択したポイントを追加
    if st.button("Add Point"):
        st.session_state.selected_points.append({"Time_sec": selected_x, "EDA": selected_y})

    # 選択したポイントを削除
    if st.button("Clear Points"):
        st.session_state.selected_points.clear()

    # 選択されたポイントをテーブルで表示
    st.write("### Selected Points")
    st.write(pd.DataFrame(st.session_state.selected_points))
