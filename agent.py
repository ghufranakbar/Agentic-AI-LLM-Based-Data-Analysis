import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import re

# -----------------------------------------------------------------------------
# 1. UI: CYBERPUNK ENTERPRISE THEME
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SENTINEL: The Ultimate Data Core", layout="wide", page_icon="🧿")

st.markdown("""
<style>
    /* Global Deep Space Theme */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #111111 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* Glassmorphism Cards */
    div[data-testid="stMetric"], div[class*="stMarkdown"], .stDataFrame {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 200, 0.1);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Neon Text & Headers */
    h1, h2, h3 { color: #00ffc8 !important; font-family: 'Courier New', monospace; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.95);
        border-right: 1px solid #00ffc8;
    }
    
    /* Plotly Chart Backgrounds */
    .js-plotly-plot .plotly .main-svg {
        background: rgba(0,0,0,0) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DEEP LEARNING ENGINE (Runs on Full Data)
# -----------------------------------------------------------------------------
@st.cache_data
def run_deep_learning_core(df):
    """
    Runs the heavy TensorFlow Autoencoder on the full dataset once.
    Returns df with 'Anomaly_Score', 'Is_Anomaly', and PCA coordinates.
    """
    # 1. Select Numerics
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) == 0: return df, [], []

    data = df[numeric_cols].fillna(0)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    
    # 2. AUTOENCODER (Robust Architecture)
    input_dim = data_scaled.shape[1]
    encoding_dim = max(1, input_dim // 2)
    
    model = models.Sequential([
        layers.Dense(16, activation='relu', input_shape=(input_dim,)),
        layers.Dense(encoding_dim, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(input_dim, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='mse')
    
    # Train
    history = model.fit(data_scaled, data_scaled, epochs=20, batch_size=16, verbose=0)
    
    # Anomaly Scoring
    reconstructions = model.predict(data_scaled)
    mse = np.mean(np.power(data_scaled - reconstructions, 2), axis=1)
    threshold = np.percentile(mse, 95) # Top 5% are anomalies
    
    df['Anomaly_Score'] = mse
    df['Is_Anomaly'] = mse > threshold
    
    # 3. PCA (Robust Fix for Small Data)
    n_components = min(3, input_dim)
    if n_components > 0:
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(data_scaled)
        df['PCA1'] = pca_result[:, 0] if n_components >= 1 else 0
        df['PCA2'] = pca_result[:, 1] if n_components >= 2 else 0
        df['PCA3'] = pca_result[:, 2] if n_components >= 3 else 0
    else:
        df['PCA1'] = 0; df['PCA2'] = 0; df['PCA3'] = 0
        
    return df, history.history['loss']

# -----------------------------------------------------------------------------
# 3. AGENTIC FUNCTIONS (Chat & Code)
# -----------------------------------------------------------------------------
def execute_custom_plot(code, df):
    """Executes AI-generated Matplotlib code"""
    try:
        local_vars = {'df': df, 'plt': plt, 'sns': sns}
        plt.style.use('dark_background') # Force Cyberpunk style
        exec(code, globals(), local_vars)
        return local_vars.get('fig')
    except Exception as e:
        return f"Error executing code: {e}"

def run_agent_brain(query, df, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    context = df.head().to_markdown()
    
    prompt = f"""
    You are SENTINEL. User Query: "{query}"
    Data Sample: {context}
    
    INSTRUCTIONS:
    1. If user asks for a chart/plot, WRITE PYTHON CODE wrapped in ```python ... ``` using matplotlib/seaborn.
       - Always define 'fig'. Ex: `fig, ax = plt.subplots()`
       - Use colors 'cyan', 'magenta', 'lime' for neon look.
    2. If user asks for insights/stats, just answer in text.
    """
    return model.generate_content(prompt).text

def generate_sitrep(df, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    stats = df.describe().to_markdown()
    prompt = f"Analyze this data stats: {stats}. Write a 3-bullet executive summary (SITREP) of the key trends and risks."
    return model.generate_content(prompt).text

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION
# -----------------------------------------------------------------------------
st.title("🧿 SENTINEL: The Ultimate Data Core")

# --- A. SIDEBAR: DATA & FILTERS ---
with st.sidebar:
    st.header("1. LINK SYSTEM")
    api_key = st.text_input("API Key", type="password")
    uploaded_file = st.file_uploader("Ingest Data", type="csv")
    
    st.divider()
    
    # DYNAMIC FILTERS (The "Tableau" Feature)
    if uploaded_file and 'processed_df' in st.session_state:
        st.header("2. SLICERS")
        df_master = st.session_state.processed_df
        
        # Identify categorical columns for filters
        cat_cols = df_master.select_dtypes(include=['object', 'category']).columns
        
        # Create a slicer for the first valid categorical column found (to keep UI clean)
        if len(cat_cols) > 0:
            slicer_col = st.selectbox("Filter Dimension", cat_cols)
            unique_vals = df_master[slicer_col].unique()
            selected_vals = st.multiselect("Select Values", unique_vals, default=unique_vals)
            
            # Apply Filter to a View (Master DF stays intact)
            if selected_vals:
                df_view = df_master[df_master[slicer_col].isin(selected_vals)]
            else:
                df_view = df_master
        else:
            df_view = df_master # No filters possible
    else:
        df_view = None

if uploaded_file and api_key:
    # --- B. INITIAL PROCESSING (Run once) ---
    if 'processed_df' not in st.session_state:
        raw_df = pd.read_csv(uploaded_file)
        with st.spinner("🔄 INITIALIZING NEURAL CORE & AUTOENCODER..."):
            proc_df, loss_history = run_deep_learning_core(raw_df)
            st.session_state.processed_df = proc_df
            st.session_state.loss_history = loss_history
            st.session_state.sitrep = generate_sitrep(proc_df, api_key)
            # Trigger reload to catch the filter logic above
            st.rerun()

    # Use the Filtered View for Dashboard
    df = df_view 
    if df is None: df = st.session_state.processed_df # Fallback

    # --- C. THE DASHBOARD TABS ---
    tab_bi, tab_deep, tab_chat = st.tabs(["📊 BI Command Deck", "🧬 Neural Lab", "💬 Sentinel Agent"])
    
    # 1. BI COMMAND DECK (Tableau Style)
    with tab_bi:
        # KPI ROW
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Records in View", len(df))
        anom_count = df['Is_Anomaly'].sum()
        k2.metric("Critical Anomalies", int(anom_count), delta="Risk Level", delta_color="inverse")
        
        # Pick numeric metric for stats
        num_cols = df.select_dtypes(include=['number']).columns
        metric_col = num_cols[0] if len(num_cols) > 0 else None
        
        if metric_col:
            k3.metric(f"Total {metric_col}", f"{df[metric_col].sum():,.0f}")
            k4.metric(f"Avg {metric_col}", f"{df[metric_col].mean():,.2f}")
        
        st.divider()
        st.markdown(f"**📝 AI SITREP:** {st.session_state.sitrep}")
        st.divider()
        
        # INTERACTIVE PLOTLY GRID
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📈 Trend Monitor")
            if metric_col:
                # Try to find a date axis, otherwise use index
                fig_line = px.line(df, y=metric_col, title=f"{metric_col} Trend", template="plotly_dark")
                st.plotly_chart(fig_line, use_container_width=True)
                
        with c2:
            st.subheader("🧬 Anomaly Radar")
            if len(num_cols) >= 2:
                fig_scat = px.scatter(df, x=num_cols[0], y=num_cols[1], color="Is_Anomaly", 
                                      color_discrete_map={False: "#00C9FF", True: "#FF0055"},
                                      title="Anomaly Detection Map", template="plotly_dark")
                st.plotly_chart(fig_scat, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("🔥 Correlation Matrix")
            if len(num_cols) > 0:
                corr = df[num_cols].corr()
                fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis", template="plotly_dark")
                st.plotly_chart(fig_corr, use_container_width=True)
        with c4:
            st.subheader("📊 Distribution Scan")
            if metric_col:
                fig_hist = px.histogram(df, x=metric_col, color="Is_Anomaly", nbins=30, template="plotly_dark")
                st.plotly_chart(fig_hist, use_container_width=True)

    # 2. NEURAL LAB (Deep Learning Internals)
    with tab_deep:
        c_dl1, c_dl2 = st.columns([2,1])
        with c_dl1:
            st.subheader("🧬 3D Latent Space Topology")
            st.caption("This is how the AI 'sees' your data. Red dots are structurally impossible to compress (Anomalies).")
            fig_3d = px.scatter_3d(df, x='PCA1', y='PCA2', z='PCA3', color='Is_Anomaly',
                                   color_discrete_map={False: "cyan", True: "red"},
                                   opacity=0.7, template="plotly_dark", height=500)
            st.plotly_chart(fig_3d, use_container_width=True)
            
        with c_dl2:
            st.subheader("📉 Network Convergence")
            st.caption("Real-time training loss of the Autoencoder.")
            st.line_chart(st.session_state.loss_history)
            
            st.subheader("🚨 Top 5 Anomalies")
            st.dataframe(df[df['Is_Anomaly']==True].head(5))

    # 3. SENTINEL AGENT (Chat & Code)
    with tab_chat:
        st.subheader("💬 Active Command Line")
        
        # Chat History
        if "messages" not in st.session_state: st.session_state.messages = []
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if msg.get("type") == "plot": st.pyplot(msg["content"])
                else: st.markdown(msg["content"])

        if prompt := st.chat_input("Command the Sentinel (e.g., 'Plot a violin chart of Sales by Region')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Processing Protocol..."):
                    raw_res = run_agent_brain(prompt, df, api_key)
                    
                    # Code Extraction
                    code_match = re.search(r"```python(.*?)```", raw_res, re.DOTALL)
                    if code_match:
                        code = code_match.group(1)
                        st.code(code, language='python')
                        fig = execute_custom_plot(code, df)
                        if hasattr(fig, 'savefig'):
                            st.pyplot(fig)
                            st.session_state.messages.append({"role": "assistant", "content": fig, "type": "plot"})
                        else:
                            st.error(f"Plot Error: {fig}")
                    else:
                        st.markdown(raw_res)
                        st.session_state.messages.append({"role": "assistant", "content": raw_res})

else:
    # Empty State Hero Section
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00ffc8;'>SENTINEL CORE ONLINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Awaiting Data Ingest... Upload CSV to Begin.</p>", unsafe_allow_html=True)