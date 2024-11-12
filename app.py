# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Enhanced EDA Data Visualization App")

# ファイルアップロード
uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    fig = go.Figure()

    # Perturbationが1のデータを黒い線で描画
    perturbation_1 = data[data["Perturbation"] == 5]
    fig.add_trace(go.Scatter(x=perturbation_1["Time_sec"], y=perturbation_1["EDA"],
                             mode="lines", line=dict(color="black", width=2),
                             name="Perturbation: 1"))

    # その他のPerturbationの値ごとに異なる色で描画
    for perturbation_value in data["Perturbation"].unique():
        if perturbation_value != 1:
            group_data = data[data["Perturbation"] == perturbation_value]
            fig.add_trace(go.Scatter(x=group_data["Time_sec"], y=group_data["EDA"],
                                     mode="lines", name=f"Perturbation: {perturbation_value}"))

    dig1_points = data[data["Dig1"] == 1]
    fig.add_trace(go.Scatter(x=dig1_points["Time_sec"], y=dig1_points["EDA"],
                             mode="markers", marker=dict(color="red", size=10, line=dict(color="black", width=1)),
                             name="Dig1 Points"))

    fig.update_layout(title="EDA over Time with Perturbation Colors and Dig1 Points",
                      xaxis_title="Time_sec", yaxis_title="EDA")

    if "selected_points" not in st.session_state:
        st.session_state.selected_points = []

    for point in st.session_state.selected_points:
        fig.add_trace(go.Scatter(x=[point["Time_sec"]], y=[point["EDA"]],
                                 mode="markers", marker=dict(color="blue", size=10),
                                 name="Selected Point"))

    st.plotly_chart(fig, use_container_width=True)

    st.write("## Selected Points Table")
    selected_x = st.number_input("Select X (Time_sec)", value=0.0)
    selected_y = st.number_input("Select Y (EDA)", value=0.0)

    if st.button("Add Point"):
        st.session_state.selected_points.append({"Time_sec": selected_x, "EDA": selected_y})

    if st.button("Clear Points"):
        st.session_state.selected_points.clear()

    st.write("### Selected Points")
    st.write(pd.DataFrame(st.session_state.selected_points))
