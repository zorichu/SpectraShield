import streamlit as st
import pandas as pd

from src.detector import detect_threat


st.set_page_config(
    page_title="SpectraShield",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #070b10;
    color: #d8e1e8;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #e8f0f5;
}

.brand {
    font-size: 28px;
    font-weight: 700;
    color: #e8f0f5;
}

.subtitle {
    color: #81909d;
    font-size: 13px;
}

.status {
    background: #092b29;
    color: #43e6c5;
    padding: 8px 16px;
    border-radius: 20px;
    text-align: center;
    font-weight: 600;
}

.network {
    background: #0d151d;
    border: 1px solid #1c2a34;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
    color: #8d9ba6;
    margin: 20px 0;
}

.metric-card {
    background: #0d151d;
    border: 1px solid #1c2a34;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.metric-title {
    color: #7f8d98;
    font-size: 13px;
}

.metric-value {
    color: #e9f1f5;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.metric-danger {
    color: #ff626c;
}

.metric-accent {
    color: #42dfc1;
}

</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown(
    '<div class="brand">🛡️ SpectraShield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">One-way traffic. All-round protection.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">● ACTIVE — ONE-WAY MONITORING</div>',
    unsafe_allow_html=True
)


# NETWORK FLOW BANNER

st.markdown(
    """
    <div class="network">
        Protected Network &nbsp;&nbsp; ━━━━━
        <strong style="color:#42dfc1;">
        DATA DIODE — RX ONLY
        </strong>
        ━━━━━ &nbsp;&nbsp; SpectraShield Sensor
        <br>
        <small>
        Passive replica of observable traffic — no return path into the network.
        </small>
    </div>
    """,
    unsafe_allow_html=True
)


# TRAFFIC INPUT

traffic = pd.read_csv("data/traffic.csv")

st.sidebar.header("Monitoring Controls")

record_count = st.sidebar.slider(
    "Traffic Records",
    20,
    len(traffic),
    100
)

run = st.sidebar.button("▶ Start Monitoring")


# MONITORING

if run:

    selected = traffic.head(record_count)
    results = detect_threat(selected)

    total = len(results)
    threats = len(results[results["threat"] != "Normal"])
    critical = len(results[results["severity"] == "Critical"])

    packets_per_second = int(
        results["packets_per_second"].mean()
    )

    score = abs(
        results["detection_score"]
    ).mean()

    st.markdown("### Monitoring Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Packets / sec</div>
                <div class="metric-value metric-accent">
                    {packets_per_second}
                </div>
                <div class="metric-title">Simulated traffic</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Flows monitored</div>
                <div class="metric-value">{total}</div>
                <div class="metric-title">Current session</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Threats detected</div>
                <div class="metric-value metric-danger">
                    {threats}
                </div>
                <div class="metric-title">Flagged records</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Avg. detection score</div>
                <div class="metric-value metric-accent">
                    {score:.2f}
                </div>
                <div class="metric-title">Prototype model score</div>