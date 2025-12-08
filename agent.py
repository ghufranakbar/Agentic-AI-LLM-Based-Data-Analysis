import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
# Lazy load TensorFlow to speed up app startup
# import tensorflow as tf
# from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import re
from io import BytesIO
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------------------------------------------------------
# 1. UI: MODERN PROFESSIONAL THEME
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Agentic AI & LLM Based Analytics", layout="wide", page_icon="AI")

st.markdown("""
<style>
    /* Sophisticated Professional Theme */
    .stApp {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        background-attachment: fixed;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Elegant Card Design */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%);
        border-radius: 12px;
        border: 1px solid rgba(100, 116, 139, 0.2);
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(20, 184, 166, 0.15);
        border-color: rgba(20, 184, 166, 0.3);
    }
    
    /* Professional Typography */
    h1 { 
        color: #ffffff !important; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }
    
    h2 { 
        color: #f1f5f9 !important; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-weight: 600;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 { 
        color: #e2e8f0 !important; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-weight: 600;
        font-size: 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    p, label, span {
        color: #94a3b8 !important;
    }
    
    /* Sophisticated Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #252b3b 0%, #1a1f2e 100%);
        border-right: 1px solid rgba(100, 116, 139, 0.2);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    
    /* Refined Metrics */
    [data-testid="stMetricLabel"] {
        color: #5eead4 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Sophisticated Tab Design */
    .stTabs {
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(100, 116, 139, 0.2);
        padding: 6px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 12px 20px;
        transition: all 0.25s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #5eead4;
        background: rgba(20, 184, 166, 0.08);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
    }
    
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }
    
    /* Clean Dataframe */
    .dataframe {
        background: rgba(248, 250, 252, 0.98) !important;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(100, 116, 139, 0.2);
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px 24px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(20, 184, 166, 0.35) !important;
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
        color: #ffffff !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        color: #ffffff !important;
    }
    
    .stButton > button p {
        color: #ffffff !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
        color: #ffffff !important;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35) !important;
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
    }
    
    .stDownloadButton > button p {
        color: #ffffff !important;
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(100, 116, 139, 0.25);
        border-left: 4px solid #14b8a6;
        color: #e2e8f0;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input Fields */
    .stTextInput input, .stSelectbox select, .stMultiSelect {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1.5px solid rgba(100, 116, 139, 0.25) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #14b8a6 !important;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.12) !important;
        outline: none !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Plotly Charts */
    .js-plotly-plot {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(100, 116, 139, 0.15);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(100, 116, 139, 0.3), transparent);
    }
    
    /* Slider */
    .stSlider {
        padding: 1.25rem 0;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(100, 116, 139, 0.2);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(20, 184, 166, 0.4);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(20, 184, 166, 0.6);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(100, 116, 139, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        transition: all 0.25s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(20, 184, 166, 0.5);
        background: rgba(255, 255, 255, 0.06);
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
        border: none !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & PROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(uploaded_file):
    """Load CSV or Excel files with intelligent parsing and type detection"""
    try:
        df = None
        delimiter_used = None
        encoding_used = None
        
        if uploaded_file.name.endswith('.csv'):
            # Try all combinations of encodings and delimiters
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252', 'utf-16']
            delimiters = [',', ';', '\t', '|']
            
            for encoding in encodings:
                for delimiter in delimiters:
                    try:
                        uploaded_file.seek(0)
                        df_test = pd.read_csv(uploaded_file, sep=delimiter, encoding=encoding, 
                                             low_memory=False, on_bad_lines='skip')
                        # Check if parsing was successful (multiple columns and rows)
                        if df_test is not None and len(df_test.columns) > 1 and len(df_test) > 0:
                            # Verify it's not all NaN
                            if not df_test.isnull().all().all():
                                df = df_test
                                delimiter_used = delimiter
                                encoding_used = encoding
                                break
                    except:
                        continue
                if df is not None:
                    break
            
            if df is None:
                # Last resort: try default pandas read_csv
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, low_memory=False)
                delimiter_used = 'auto'
                encoding_used = 'auto'
                
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file, engine='openpyxl' if uploaded_file.name.endswith('.xlsx') else None)
            delimiter_used = 'N/A'
            encoding_used = 'Excel'
        else:
            st.error("Unsupported file format. Please upload CSV or Excel files.")
            return None
        
        # Validation
        if df is None or df.empty:
            st.error("The uploaded file is empty or couldn't be read properly.")
            return None
        
        # Clean column names (remove extra spaces, special characters)
        df.columns = df.columns.str.strip()
        
        # Auto-detect and convert date columns
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to parse as datetime
                try:
                    if df[col].astype(str).str.match(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}').sum() > len(df) * 0.5:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
                    
                # Try to convert string numbers to actual numbers
                try:
                    if df[col].astype(str).str.replace(',', '').str.replace('$', '').str.match(r'^[+-]?\d+\.?\d*$').sum() > len(df) * 0.8:
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('$', ''), errors='coerce')
                except:
                    pass
        
        # Show parsing info
        if delimiter_used and encoding_used:
            st.success(f"Loaded {len(df):,} rows x {len(df.columns)} columns | Delimiter: '{delimiter_used}' | Encoding: {encoding_used}")
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

@st.cache_data
def analyze_data(df):
    """Comprehensive data analysis with business context detection"""
    analysis = {}
    
    # Basic stats
    analysis['total_rows'] = len(df)
    analysis['total_columns'] = len(df.columns)
    analysis['memory_usage'] = df.memory_usage(deep=True).sum() / 1024**2  # MB
    
    # Column types with datetime
    analysis['numeric_cols'] = df.select_dtypes(include=['number']).columns.tolist()
    analysis['datetime_cols'] = df.select_dtypes(include=['datetime64']).columns.tolist()
    analysis['categorical_cols'] = df.select_dtypes(include=['object', 'category']).columns.tolist()
    analysis['datetime_cols'] = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Missing values
    analysis['missing_values'] = df.isnull().sum().to_dict()
    analysis['missing_percentage'] = (df.isnull().sum() / len(df) * 100).to_dict()
    
    # Numeric statistics with context
    if analysis['numeric_cols']:
        analysis['numeric_stats'] = df[analysis['numeric_cols']].describe()
        # Add value ranges and distributions for context
        analysis['value_ranges'] = {}
        for col in analysis['numeric_cols']:
            analysis['value_ranges'][col] = {
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'unique': df[col].nunique()
            }
    
    # Categorical value distributions
    if analysis['categorical_cols']:
        analysis['category_distributions'] = {}
        for col in analysis['categorical_cols'][:10]:  # Limit to first 10
            top_values = df[col].value_counts().head(10)
            analysis['category_distributions'][col] = {
                'unique_count': df[col].nunique(),
                'top_values': top_values.to_dict(),
                'most_common': top_values.index[0] if len(top_values) > 0 else None
            }
    
    # Detect potential key columns (high cardinality)
    analysis['potential_keys'] = [col for col in df.columns if df[col].nunique() == len(df)]
    
    # Detect constant columns (no variance)
    analysis['constant_columns'] = [col for col in df.columns if df[col].nunique() == 1]
    
    return analysis

@st.cache_data
def detect_date_columns(df):
    """Auto-detect potential date columns"""
    date_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col].head(100), errors='raise')
                date_cols.append(col)
            except:
                pass
    return date_cols

@st.cache_data
def run_deep_learning_core(df):
    """Optional: Deep Learning Anomaly Detection"""
    # Lazy load TensorFlow only when needed to speed up app startup
    import tensorflow as tf
    from tensorflow.keras import layers, models
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) == 0: 
        return df, []

    data = df[numeric_cols].fillna(0)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    
    # Autoencoder
    input_dim = data_scaled.shape[1]
    encoding_dim = max(1, input_dim // 2)
    
    model = models.Sequential([
        layers.Dense(16, activation='relu', input_shape=(input_dim,)),
        layers.Dense(encoding_dim, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(input_dim, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='mse')
    history = model.fit(data_scaled, data_scaled, epochs=20, batch_size=16, verbose=0)
    
    reconstructions = model.predict(data_scaled)
    mse = np.mean(np.power(data_scaled - reconstructions, 2), axis=1)
    threshold = np.percentile(mse, 95)
    
    df['Anomaly_Score'] = mse
    df['Is_Anomaly'] = mse > threshold
    
    # PCA
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
    """Executes AI-generated visualization code and returns the figure"""
    try:
        import io
        from PIL import Image
        
        local_vars = {'df': df, 'plt': plt, 'sns': sns, 'px': px, 'go': go, 'pd': pd, 'np': np}
        exec(code, globals(), local_vars)
        
        # Check for Plotly figure (priority)
        if 'fig' in local_vars:
            return {'type': 'plotly', 'figure': local_vars['fig']}
        
        # Check for matplotlib figure
        if plt.get_fignums():
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            img = Image.open(buf)
            plt.close('all')
            return {'type': 'image', 'figure': img}
        
        # Check for PIL Image
        if 'img' in local_vars and isinstance(local_vars['img'], Image.Image):
            return {'type': 'image', 'figure': local_vars['img']}
        
        return None
    except Exception as e:
        st.error(f"Error executing visualization: {e}")
        return None

def run_agent_brain(query, df, api_key):
    """Enhanced agentic AI system with deep context and proper table formatting"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Build comprehensive context about the data
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Detect data domain
    all_col_names = ' '.join(df.columns.tolist()).lower()
    detected_domain = "general"
    if any(word in all_col_names for word in ['sales', 'revenue', 'price', 'order']):
        detected_domain = "sales/commerce"
    elif any(word in all_col_names for word in ['customer', 'client', 'user']):
        detected_domain = "customer"
    elif any(word in all_col_names for word in ['transaction', 'payment', 'balance']):
        detected_domain = "financial"
    elif any(word in all_col_names for word in ['employee', 'salary', 'department']):
        detected_domain = "HR"
    
    # Statistical context with patterns
    stats_summary = ""
    if numeric_cols:
        stats_summary = f"Numeric Columns ({len(numeric_cols)}): {', '.join(numeric_cols[:15])}\n"
        for col in numeric_cols[:8]:
            mean_val = df[col].mean()
            median_val = df[col].median()
            min_val = df[col].min()
            max_val = df[col].max()
            std_val = df[col].std()
            stats_summary += f"  - {col}: [{min_val:.2f} to {max_val:.2f}], mean={mean_val:.2f}, median={median_val:.2f}, std={std_val:.2f}\n"
    
    # Categorical context with distributions
    cat_summary = ""
    if cat_cols:
        cat_summary = f"Categorical Columns ({len(cat_cols)}): {', '.join(cat_cols[:15])}\n"
        for col in cat_cols[:5]:
            top_vals = df[col].value_counts().head(3)
            unique_count = df[col].nunique()
            if len(top_vals) > 0:
                top_3 = ', '.join([f"'{k}' ({v})" for k, v in top_vals.items()])
                cat_summary += f"  - {col}: {unique_count} unique | Top 3: {top_3}\n"
    
    # Correlations for numeric columns
    correlation_info = ""
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5 and not pd.isna(corr_val):
                    strong_corrs.append(f"{corr_matrix.columns[i]} <-> {corr_matrix.columns[j]}: {corr_val:.3f}")
        if strong_corrs:
            correlation_info = f"Strong Correlations (|r| > 0.5):\n" + "\n".join(strong_corrs[:5]) + "\n"
    
    # Time context
    time_summary = ""
    if datetime_cols:
        time_summary = f"Time Columns: {', '.join(datetime_cols)}\n"
        date_col = datetime_cols[0]
        time_summary += f"  - Period: {df[date_col].min()} to {df[date_col].max()}\n"
        time_summary += f"  - Duration: {(df[date_col].max() - df[date_col].min()).days} days\n"
    
    # Data sample
    sample_rows = min(15, len(df))
    data_sample = df.head(sample_rows).to_string()
    
    # Get data summary
    data_context = f"""
DATASET PROFILE:
- Records: {df.shape[0]:,} rows x {df.shape[1]} columns
- Detected Domain: {detected_domain}
- All Columns: {', '.join(df.columns.tolist())}
- Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

{stats_summary}
{cat_summary}
{correlation_info}
{time_summary}
Sample Data (First {sample_rows} Rows):
{data_sample}

Descriptive Statistics:
{df.describe().to_string() if numeric_cols else 'No numeric columns'}
"""
    
    prompt = f"""
You are an EXPERT DATA ANALYST AI specialized in {detected_domain} data analysis.

USER QUESTION: "{query}"

{data_context}

RESPONSE GUIDELINES:

1. **For data display/table requests**:
   - DO NOT use markdown tables (they display poorly)
   - Instead, describe the query and say "Here are the results:" then provide summary
   - For actual table display, suggest using filters or exports
   - Example: "The top 5 categories by sales are: Category A ($50K), Category B ($45K)..."

2. **For visualization requests**:
   - Generate Python code using plotly express (px) or graph_objects (go) for INTERACTIVE charts
   - For static images/plots, use matplotlib (plt) or seaborn (sns)
   - Plotly: MUST assign result to 'fig' variable
   - Matplotlib: Use plt.figure() and standard plotting, figure will be auto-captured
   - Use EXACT column names from the dataset above
   - Teal theme colors: color_discrete_sequence=['#14b8a6', '#0d9488', '#5eead4']
   - Example Plotly: fig = px.bar(df, x='CategoryColumn', y='ValueColumn', title='Chart Title')
   - Example Matplotlib: plt.figure(figsize=(10,6)); plt.plot(df['x'], df['y']); plt.title('Title')
   - Wrap in ```python ... ```

3. **For analytical questions**:
   - Reference actual values from the sample data
   - Use real column names and numbers
   - Explain patterns and business meaning
   - Be specific: "Sales range from $100 to $5,000 with average of $1,250"

4. **For "what is" questions**:
   - Look at column names and sample values
   - Identify what domain this represents
   - Explain what each row means
   - Highlight key metrics and dimensions

5. **For calculation requests**:
   - Use pandas operations in your explanation
   - Show actual formulas
   - Reference the statistical summary provided

6. **CRITICAL RULES**:
   - Use EXACT column names (case-sensitive)
   - Never invent data - use only what you see above
   - If correlations exist, mention them
   - Provide business context not just numbers
   - Be concise but informative

Respond professionally. Focus on insights, not just descriptions.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"**Error:** {str(e)}. Please try rephrasing your question."

def generate_insights(df, api_key):
    """Generate comprehensive AI insights about the data"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Build comprehensive context with actual data samples
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Statistical summary
    stats_summary = ""
    if numeric_cols:
        stats_summary = "**Numeric Columns:**\n"
        for col in numeric_cols[:10]:
            stats = df[col].describe()
            stats_summary += f"- {col}: Mean={stats['mean']:.2f}, Median={stats['50%']:.2f}, Std={stats['std']:.2f}, Range=[{stats['min']:.2f} to {stats['max']:.2f}]\n"
    
    # Categorical summary
    cat_summary = ""
    if cat_cols:
        cat_summary = "\n**Categorical Columns:**\n"
        for col in cat_cols[:10]:
            top_values = df[col].value_counts().head(5)
            unique_count = df[col].nunique()
            cat_summary += f"- {col}: {unique_count} unique values. Top: {dict(top_values)}\n"
    
    # Correlations
    correlations = ""
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    strong_corr.append(f"{corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}: {corr_val:.3f}")
        if strong_corr:
            correlations = "\n**Strong Correlations (|r| > 0.5):**\n" + "\n".join(strong_corr[:10])
    
    # Data quality
    missing_info = df.isnull().sum()
    quality_summary = ""
    if missing_info.sum() > 0:
        quality_summary = "\n**Data Quality Issues:**\n"
        for col, missing in missing_info[missing_info > 0].items():
            pct = (missing / len(df)) * 100
            quality_summary += f"- {col}: {missing:,} missing ({pct:.1f}%)\n"
    
    # Sample data for context
    sample_data = df.head(5).to_string()
    
    # Detect business domain from column names and data patterns
    all_columns = ' '.join(df.columns.tolist()).lower()
    domain_keywords = {
        'sales': ['revenue', 'sales', 'price', 'quantity', 'order', 'product', 'customer', 'discount'],
        'customer': ['customer', 'client', 'user', 'name', 'email', 'phone', 'address', 'age', 'gender'],
        'financial': ['amount', 'balance', 'transaction', 'payment', 'credit', 'debit', 'account', 'profit'],
        'marketing': ['campaign', 'conversion', 'click', 'impression', 'roi', 'engagement', 'lead', 'channel'],
        'hr': ['employee', 'salary', 'department', 'hire', 'performance', 'attendance', 'leave'],
        'operations': ['inventory', 'stock', 'supplier', 'warehouse', 'shipment', 'delivery', 'logistics'],
        'healthcare': ['patient', 'diagnosis', 'treatment', 'doctor', 'hospital', 'medical', 'symptom'],
        'education': ['student', 'grade', 'course', 'exam', 'teacher', 'school', 'score', 'class']
    }
    
    detected_domains = []
    for domain, keywords in domain_keywords.items():
        if any(keyword in all_columns for keyword in keywords):
            detected_domains.append(domain)
    
    domain_context = f"**Detected Business Domain:** {', '.join(detected_domains) if detected_domains else 'General Analytics'}\n" if detected_domains else ""
    
    # Find time-based columns
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    time_range = ""
    if date_cols:
        date_col = date_cols[0]
        time_range = f"**Time Period:** {df[date_col].min()} to {df[date_col].max()}\n"
    
    prompt = f"""
You are an EXPERT DATA ANALYST specializing in business intelligence. Examine this dataset and provide DEEP, ACTIONABLE insights.

**DATASET OVERVIEW:**
- Records: {len(df):,} rows
- Features: {len(df.columns)} columns  
- Columns: {', '.join(df.columns.tolist()[:20])}{'...' if len(df.columns) > 20 else ''}
- Size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
{domain_context}{time_range}

**ACTUAL DATA SAMPLE (First 5 Records):**
```
{sample_data}
```

{stats_summary}
{cat_summary}
{correlations}
{quality_summary}

**YOUR MISSION:**
Analyze this REAL DATA like you're presenting to a CEO. They need to understand:
1. WHAT this data represents (be specific based on actual values)
2. WHAT patterns and insights you found (use real numbers)
3. WHAT actions they should take (concrete recommendations)

**CRITICAL INSTRUCTIONS:**
DON'T just describe columns. INTERPRET the data! Look at the ACTUAL VALUES.

## 1. What This Data Represents
- Based on column names and values, what domain/business area is this (sales, customer, product, financial, etc.)?
- What does each row likely represent (a transaction, a person, a product, an event, etc.)?
- What is the time period or scope covered?
- Are there obvious identifiers or keys?

## 2. Key Findings From The Actual Data
- Look at the ACTUAL VALUES in the sample data and statistics
- What are 5-7 interesting patterns you see in the numbers?
- Reference SPECIFIC column names and their values
- What stands out as unusual, interesting, or concerning?
- Example: "The 'Revenue' column ranges from $50 to $50,000 with heavy right skew..."

## 3. Relationships & Correlations
- Which columns are related to each other and why does that matter?
- What business relationships do the correlations suggest?
- Are there surprising connections?
- Which variables should be analyzed together to find insights?

## 4. Practical Business Recommendations
- Based on what you see, list 4-6 specific, actionable recommendations
- Prioritize by potential business impact
- Be specific (e.g., "Focus on customers with X > 100 because...")
- Include both opportunities to pursue and risks to mitigate

## 5. Data Quality Assessment
- What's the completeness level? (mention specific columns with issues)
- Are there data collection problems evident?
- What cleaning or preprocessing is needed before analysis?
- What additional data would be valuable to collect?

## 6. Questions To Investigate Next
- List 3-4 specific analytical questions to explore
- Frame as business questions not technical tasks
- Example: "Why do customers in Category X have 2x higher values?"

Be SPECIFIC. Use actual column names. Reference real numbers from the data. Make it actionable.
- Suggest advanced analyses (segmentation, modeling, etc.)
- Identify potential hidden insights

**FORMAT:** Use markdown with clear headers, bullet points, and bold text for emphasis. Be specific and reference actual values from the data.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"**Error generating insights:** {str(e)}\n\nPlease check your API key and try again."

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION
# -----------------------------------------------------------------------------
# Custom Title with Better Styling
st.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 3.5rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        Agentic AI & LLM Based Analytics
    </h1>
    <p style='font-size: 1.3rem; color: #a78bfa; margin-top: 0.5rem; font-weight: 500; letter-spacing: 0.05em;'>
        ANALYTICS PLATFORM
    </p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONFIGURATION & FILTERS ---
with st.sidebar:
    st.markdown("### Configuration")
    
    # Get API key from environment (no user input)
    api_key = os.getenv('GEMINI_API_KEY', '')
    if api_key:
        st.success("API Key Active")
    else:
        st.error("API Key not found in environment")
        st.caption("Add GEMINI_API_KEY to your .env file")
    
    st.markdown("### Data Source")
    
    # Clear data button
    if 'df' in st.session_state or 'uploaded_files' in st.session_state:
        if st.button("Clear All Data & Start Fresh", use_container_width=True, type="secondary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Multiple file upload
    uploaded_files = st.file_uploader(
        "Upload Dataset(s)", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload one or more CSV/Excel files. Multiple files will be combined for analysis."
    )
    
    # Show uploaded files
    if uploaded_files:
        st.caption(f"{len(uploaded_files)} file(s) selected:")
        for idx, file in enumerate(uploaded_files, 1):
            st.caption(f"  {idx}. {file.name}")
    
    if 'df' in st.session_state:
        st.divider()
        st.markdown("### Data Filters")
        
        df_master = st.session_state.df
        analysis = st.session_state.analysis
        
        # Show source file filter if multiple files were combined
        if '_source_file' in df_master.columns:
            st.caption("Filter by Source File")
            source_files = df_master['_source_file'].unique().tolist()
            selected_sources = st.multiselect("Select Files", source_files, default=source_files)
            if selected_sources:
                df_master = df_master[df_master['_source_file'].isin(selected_sources)]
        
        # Categorical filters
        if analysis['categorical_cols']:
            selected_cat = st.selectbox("Filter by Category", ['None'] + analysis['categorical_cols'])
            if selected_cat != 'None':
                unique_vals = df_master[selected_cat].unique()
                selected_vals = st.multiselect(f"Select {selected_cat}", unique_vals, default=unique_vals)
                if selected_vals:
                    df_master = df_master[df_master[selected_cat].isin(selected_vals)]
        
        # Numeric filters
        if analysis['numeric_cols']:
            st.subheader("Numeric Range")
            selected_num = st.selectbox("Filter numeric column", ['None'] + analysis['numeric_cols'])
            if selected_num != 'None':
                min_val = float(df_master[selected_num].min())
                max_val = float(df_master[selected_num].max())
                range_vals = st.slider(f"{selected_num} Range", min_val, max_val, (min_val, max_val))
                df_master = df_master[(df_master[selected_num] >= range_vals[0]) & 
                                     (df_master[selected_num] <= range_vals[1])]
        
        st.session_state.df_filtered = df_master
        st.info(f"Displaying {len(df_master):,} of {len(st.session_state.df):,} records")

# --- MAIN CONTENT ---
if uploaded_files and api_key:
    # Show extract button if data not loaded yet
    if 'df' not in st.session_state:
        if len(uploaded_files) == 1:
            st.info(f"Dataset ready: {uploaded_files[0].name}")
        else:
            st.info(f"{len(uploaded_files)} datasets ready for combined analysis")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Extract & Analyze Data", use_container_width=True, type="primary"):
                with st.spinner("Loading and analyzing dataset(s)..."):
                    all_dfs = []
                    file_sources = []
                    
                    # Load all files
                    for file in uploaded_files:
                        df_temp = load_data(file)
                        if df_temp is not None:
                            # Add source column to track which file data came from
                            df_temp['_source_file'] = file.name
                            all_dfs.append(df_temp)
                            file_sources.append(file.name)
                    
                    if all_dfs:
                        if len(all_dfs) == 1:
                            df = all_dfs[0]
                            st.success(f"Loaded {len(df):,} rows from {file_sources[0]}")
                        else:
                            # Combine multiple datasets
                            try:
                                df = pd.concat(all_dfs, ignore_index=True, sort=False)
                                st.success(f"Combined {len(all_dfs)} files: {len(df):,} total rows")
                                st.info(f"📌 Files combined: {', '.join(file_sources)}")
                            except Exception as e:
                                st.error(f"Error combining files: {e}")
                                st.info("Tip: Files must have similar structures to combine")
                                df = all_dfs[0]  # Fallback to first file
                        
                        st.session_state.df = df
                        st.session_state.analysis = analyze_data(df)
                        st.session_state.df_filtered = df
                        st.session_state.uploaded_files = file_sources
                        
                        # Generate insights in background
                        with st.spinner("Generating AI insights..."):
                            st.session_state.insights = generate_insights(df, api_key)
                        
                        st.success(f"Successfully loaded {len(df):,} records with {len(df.columns)} columns")
                        st.rerun()
        
        # Stop here until button is clicked
        st.stop()
    
    df = st.session_state.df_filtered if 'df_filtered' in st.session_state else st.session_state.df
    analysis = st.session_state.analysis
    
    # --- TABS ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", 
        "Visualizations", 
        "Deep Analysis",
        "AI Insights",
        "AI Assistant"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        st.header("Dataset Overview")
        
        # Show source files if multiple files were combined
        if '_source_file' in df.columns:
            source_files = df['_source_file'].unique()
            if len(source_files) > 1:
                st.info(f"**Combined Analysis** from {len(source_files)} files: {', '.join(source_files)}")
                # Show record count per file
                file_counts = df['_source_file'].value_counts()
                with st.expander("Records per File"):
                    for file, count in file_counts.items():
                        st.caption(f"• {file}: {count:,} rows")
                st.divider()
        
        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Records", f"{analysis['total_rows']:,}")
        with col2:
            st.metric("Total Columns", analysis['total_columns'])
        with col3:
            st.metric("Numeric Columns", len(analysis['numeric_cols']))
        with col4:
            st.metric("Categorical Columns", len(analysis['categorical_cols']))
        with col5:
            st.metric("Memory Size", f"{analysis['memory_usage']:.2f} MB")
        
        st.divider()
        
        # Data Context Summary
        st.subheader("Dataset Context")
        context_col1, context_col2 = st.columns(2)
        
        with context_col1:
            if 'potential_keys' in analysis and analysis['potential_keys']:
                st.info(f"**Unique Identifiers:** {', '.join(analysis['potential_keys'][:3])}")
            
            if 'value_ranges' in analysis and analysis['value_ranges']:
                st.markdown("**Numeric Column Ranges:**")
                for col, ranges in list(analysis['value_ranges'].items())[:5]:
                    st.caption(f"• **{col}**: {ranges['min']:.2f} to {ranges['max']:.2f} (avg: {ranges['mean']:.2f})")
        
        with context_col2:
            if 'category_distributions' in analysis:
                st.markdown("**Categorical Distributions:**")
                for col, dist in list(analysis['category_distributions'].items())[:5]:
                    st.caption(f"• **{col}**: {dist['unique_count']} unique values (most common: {dist['most_common']})")
        
        st.divider()
        
        # Data Preview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Data Preview")
            st.dataframe(df.head(20), use_container_width=True, height=400)
            
            # Export option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Export Data",
                csv,
                "filtered_data.csv",
                "text/csv",
                key='download-csv'
            )
        
        with col2:
            st.subheader("Data Types")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Type': [str(dtype) for dtype in df.dtypes],
                'Non-Null': df.count().values,
                'Null %': [f"{(df[col].isnull().sum() / len(df) * 100):.1f}%" for col in df.columns]
            })
            st.dataframe(dtype_df, use_container_width=True, height=400)
        
        st.divider()
        
        # Statistical Summary
        if analysis['numeric_cols']:
            st.subheader("Statistical Summary")
            st.dataframe(analysis['numeric_stats'].T, use_container_width=True)
        
        # Data Quality Assessment
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            st.subheader("Data Quality Assessment")
            fig_missing = px.bar(
                x=missing_data[missing_data > 0].index,
                y=missing_data[missing_data > 0].values,
                labels={'x': 'Column', 'y': 'Missing Count'},
                title='Missing Values by Column',
                color=missing_data[missing_data > 0].values,
                color_continuous_scale='Reds'
            )
            fig_missing.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_missing, use_container_width=True)
    
    # ==================== TAB 2: VISUALIZATIONS ====================
    with tab2:
        st.header("Visual Analytics")
        
        if analysis['numeric_cols']:
            # Visualization Controls
            col1, col2, col3 = st.columns(3)
            with col1:
                chart_type = st.selectbox("Chart Type", [
                    "Scatter Plot", "Line Chart", "Bar Chart", "Box Plot", 
                    "Histogram", "Heatmap", "Pie Chart", "Area Chart"
                ])
            with col2:
                # Smart default for X-axis (prefer datetime, then categorical, then numeric)
                default_x_options = []
                if 'datetime_cols' in analysis and analysis['datetime_cols']:
                    default_x_options.extend(analysis['datetime_cols'][:3])
                if analysis['categorical_cols']:
                    default_x_options.extend(analysis['categorical_cols'][:5])
                if analysis['numeric_cols']:
                    default_x_options.extend(analysis['numeric_cols'][:3])
                if not default_x_options:
                    default_x_options = ['Index']
                x_axis = st.selectbox("X-Axis", default_x_options)
            with col3:
                # Default to first numeric column
                if len(analysis['numeric_cols']) > 0:
                    y_axis = st.selectbox("Y-Axis", analysis['numeric_cols'], index=0)
                else:
                    st.warning("No numeric columns found for Y-axis")
                    y_axis = None
            
            # Color option for scatter
            color_col = None
            if chart_type in ["Scatter Plot", "Bar Chart", "Line Chart"]:
                color_col = st.selectbox("Color By (optional)", ['None'] + analysis['categorical_cols'])
                color_col = None if color_col == 'None' else color_col
            
            # Generate visualization
            try:
                if chart_type == "Line Chart":
                    x_data = df.index if x_axis == 'Index' else df[x_axis]
                    fig = px.line(df, x=x_data, y=y_axis, color=color_col, title=f"{y_axis} Trend")
                
                elif chart_type == "Bar Chart":
                    if x_axis == 'Index':
                        fig = px.bar(df, y=y_axis, color=color_col, title=f"{y_axis} Distribution")
                    else:
                        # Aggregate if needed
                        if color_col:
                            agg_df = df.groupby([x_axis, color_col])[y_axis].sum().reset_index()
                            fig = px.bar(agg_df, x=x_axis, y=y_axis, color=color_col, barmode='group')
                        else:
                            agg_df = df.groupby(x_axis)[y_axis].sum().reset_index()
                            fig = px.bar(agg_df, x=x_axis, y=y_axis)
                
                elif chart_type == "Scatter Plot":
                    if x_axis == 'Index':
                        fig = px.scatter(df, y=y_axis, color=color_col, title=f"{y_axis} Scatter")
                    else:
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, 
                                       title=f"{y_axis} vs {x_axis}", trendline="ols")
                
                elif chart_type == "Box Plot":
                    fig = px.box(df, y=y_axis, x=color_col if color_col else None, 
                               title=f"{y_axis} Distribution")
                
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=y_axis, color=color_col, nbins=30, 
                                     title=f"{y_axis} Histogram")
                
                elif chart_type == "Heatmap":
                    corr_matrix = df[analysis['numeric_cols']].corr()
                    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                                  title="Correlation Heatmap",
                                  color_continuous_scale='RdBu_r')
                
                elif chart_type == "Pie Chart":
                    if color_col:
                        pie_data = df.groupby(color_col)[y_axis].sum().reset_index()
                        fig = px.pie(pie_data, names=color_col, values=y_axis,
                                   title=f"{y_axis} by {color_col}")
                    else:
                        st.warning("Please select a categorical column for 'Color By'")
                        fig = None
                
                elif chart_type == "Area Chart":
                    x_data = df.index if x_axis == 'Index' else df[x_axis]
                    fig = px.area(df, x=x_data, y=y_axis, color=color_col, 
                                title=f"{y_axis} Area Chart")
                
                if fig:
                    fig.update_layout(height=600, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error creating visualization: {e}")
            
            st.divider()
            
            # Multiple Charts Grid
            st.subheader("Quick Insights Dashboard")
            st.caption("Auto-generated visualizations of key data patterns")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution of first numeric column with context
                if len(analysis['numeric_cols']) > 0:
                    col_name = analysis['numeric_cols'][0]
                    mean_val = df[col_name].mean()
                    median_val = df[col_name].median()
                    fig1 = px.histogram(df, x=col_name, nbins=30,
                                      title=f"Distribution: {col_name}<br><sub>Mean: {mean_val:.2f} | Median: {median_val:.2f}</sub>",
                                      color_discrete_sequence=['#8b5cf6'])
                    fig1.update_layout(height=350, showlegend=False)
                    st.plotly_chart(fig1, use_container_width=True)
                
                # Top categories with percentage
                if analysis['categorical_cols']:
                    cat_col = analysis['categorical_cols'][0]
                    top_cats = df[cat_col].value_counts().head(10)
                    percentages = (top_cats / len(df) * 100).round(1)
                    fig3 = px.bar(x=top_cats.values, y=top_cats.index, orientation='h',
                                title=f"Top 10 Categories: {cat_col}<br><sub>Showing {top_cats.sum():,} of {len(df):,} records</sub>",
                                color=top_cats.values,
                                color_continuous_scale='Viridis',
                                text=[f"{v} ({p}%)" for v, p in zip(top_cats.values, percentages)])
                    fig3.update_traces(textposition='outside')
                    fig3.update_layout(height=350, showlegend=False)
                    st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Correlation heatmap with insights
                if len(analysis['numeric_cols']) >= 2:
                    # Use up to 8 numeric columns for better readability
                    corr_cols = analysis['numeric_cols'][:8]
                    corr = df[corr_cols].corr()
                    
                    # Find strongest correlations
                    strong_corrs = []
                    for i in range(len(corr.columns)):
                        for j in range(i+1, len(corr.columns)):
                            if abs(corr.iloc[i, j]) > 0.5:
                                strong_corrs.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
                    
                    fig2 = px.imshow(corr, text_auto='.2f',
                                   title=f"Correlation Matrix<br><sub>{len(strong_corrs)} strong correlations found</sub>",
                                   color_continuous_scale='RdBu_r',
                                   aspect="auto",
                                   labels=dict(color="Correlation"))
                    fig2.update_layout(height=350)
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Scatter plot with trend line
                if len(analysis['numeric_cols']) >= 2:
                    x_col = analysis['numeric_cols'][0]
                    y_col = analysis['numeric_cols'][1]
                    correlation = df[x_col].corr(df[y_col])
                    
                    fig4 = px.scatter(df.sample(min(1000, len(df))), x=x_col, y=y_col,
                                    title=f"{y_col} vs {x_col}<br><sub>Correlation: {correlation:.3f}</sub>",
                                    color_discrete_sequence=['#8b5cf6'],
                                    opacity=0.5,
                                    trendline="ols")
                    fig4.update_layout(height=350)
                    st.plotly_chart(fig4, use_container_width=True)
        
        else:
            st.info("No numeric columns found for visualization")
    
    # ==================== TAB 3: DEEP ANALYSIS ====================
    with tab3:
        st.header("Advanced Analytics")
        
        if 'df_anomaly' in st.session_state:
            df_anom = st.session_state.df_anomaly
            
            col1, col2, col3 = st.columns(3)
            with col1:
                anomaly_count = df_anom['Is_Anomaly'].sum()
                st.metric("Anomalies Detected", f"{anomaly_count:,}",
                         f"{(anomaly_count/len(df_anom)*100):.2f}%")
            with col2:
                avg_score = df_anom['Anomaly_Score'].mean()
                st.metric("Avg Anomaly Score", f"{avg_score:.4f}")
            with col3:
                max_score = df_anom['Anomaly_Score'].max()
                st.metric("Max Anomaly Score", f"{max_score:.4f}")
            
            st.divider()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Dimensional Reduction Visualization")
                fig_3d = px.scatter_3d(
                    df_anom, x='PCA1', y='PCA2', z='PCA3',
                    color='Is_Anomaly',
                    color_discrete_map={True: '#ff0055', False: '#00d4ff'},
                    opacity=0.6,
                    title="PCA Dimensionality Reduction"
                )
                fig_3d.update_layout(height=500)
                st.plotly_chart(fig_3d, use_container_width=True)
            
            with col2:
                st.subheader("Training Loss")
                if 'loss_history' in st.session_state:
                    loss_df = pd.DataFrame({
                        'Epoch': range(1, len(st.session_state.loss_history) + 1),
                        'Loss': st.session_state.loss_history
                    })
                    fig_loss = px.line(loss_df, x='Epoch', y='Loss',
                                     title="Model Convergence")
                    st.plotly_chart(fig_loss, use_container_width=True)
                
                st.subheader("Anomaly Score Distribution")
                fig_hist = px.histogram(df_anom, x='Anomaly_Score', nbins=50,
                                      color='Is_Anomaly',
                                      title="Score Distribution")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            st.divider()
            st.subheader("Top Anomalies")
            anomalies = df_anom[df_anom['Is_Anomaly']==True].sort_values('Anomaly_Score', ascending=False)
            st.dataframe(anomalies.head(20), use_container_width=True)
        
        else:
            st.info("Running anomaly detection...")
            if st.button("Run Anomaly Detection"):
                with st.spinner("Training autoencoder model..."):
                    df_with_anomalies, loss = run_deep_learning_core(df.copy())
                    st.session_state.df_anomaly = df_with_anomalies
                    st.session_state.loss_history = loss
                    st.rerun()
    
    # ==================== TAB 4: AI INSIGHTS ====================
    with tab4:
        st.header("Intelligent Insights")
        
        if 'insights' in st.session_state:
            st.markdown(st.session_state.insights)
        
        st.divider()
        
        if st.button("Generate New Insights"):
            with st.spinner("Analyzing dataset..."):
                st.session_state.insights = generate_insights(df, api_key)
                st.rerun()
        
        st.divider()
        
        # Key Statistics Cards
        st.subheader("Key Statistics")
        
        if analysis['numeric_cols']:
            cols = st.columns(len(analysis['numeric_cols'][:4]))
            for idx, col_name in enumerate(analysis['numeric_cols'][:4]):
                with cols[idx]:
                    st.metric(
                        col_name,
                        f"{df[col_name].mean():.2f}",
                        f"σ: {df[col_name].std():.2f}"
                    )
    
    # ==================== TAB 5: AI ASSISTANT ====================
    with tab5:
        st.header("Analytics Assistant")
        st.markdown("Natural language queries and custom visualizations")
        
        # Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if msg.get("type") == "plot" and msg.get("fig"):
                    st.plotly_chart(msg["fig"], use_container_width=True)
                elif msg.get("type") == "image" and msg.get("img"):
                    st.image(msg["img"], use_column_width=True)
                else:
                    st.markdown(msg["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = run_agent_brain(prompt, df, api_key)
                    
                    # Try to extract and execute code
                    code_match = re.search(r"```python(.*?)```", response, re.DOTALL)
                    if code_match:
                        code = code_match.group(1).strip()
                        st.code(code, language='python')
                        
                        try:
                            result = execute_custom_plot(code, df)
                            if result:
                                if result['type'] == 'plotly':
                                    st.plotly_chart(result['figure'], use_container_width=True)
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": "Here's your visualization:",
                                        "type": "plot",
                                        "fig": result['figure']
                                    })
                                elif result['type'] == 'image':
                                    st.image(result['figure'], use_column_width=True)
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": "Here's your visualization:",
                                        "type": "image",
                                        "img": result['figure']
                                    })
                            else:
                                # No figure generated, show text response
                                st.markdown(response)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response
                                })
                        except Exception as e:
                            st.error(f"Error: {e}")
                            st.markdown(response)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                    else:
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })

else:
    # Welcome Screen
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Upload one or more CSV/Excel files in the sidebar to begin")
        st.caption("Tip: Upload multiple files for combined analysis")
        
        # Feature grid using native Streamlit components
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Advanced Visualizations**")
            st.caption("Interactive charts and custom visualizations")
            st.markdown("**Predictive Analytics**")
            st.caption("Anomaly detection and pattern recognition")
        
        with col_b:
            st.markdown("**AI-Powered Insights**")
            st.caption("Deep learning analysis with LLM")
            st.markdown("**Natural Language Queries**")
            st.caption("Chat with your data using AI assistant")

# Footer watermark
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; margin-top: 50px; border-top: 1px solid rgba(100, 116, 139, 0.2);'>
    <p style='color: #64748b; font-size: 0.85rem; margin: 0;'>
        Crafted with caffeine and questionable life choices by <strong style='color: #14b8a6;'>Muhammad Ghufran Akbar</strong>
    </p>
    <p style='color: #475569; font-size: 0.75rem; margin: 5px 0 0 0;'>
        For the love of AI, data, and those 3 AM debugging sessions that make you question your sanity
    </p>
</div>
""", unsafe_allow_html=True)
