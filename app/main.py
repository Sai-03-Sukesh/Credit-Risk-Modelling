import streamlit as st
from prediction_helper import predict

# MUST BE FIRST - Page Configuration
st.set_page_config(
    page_title="Credit Risk Modelling",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Modern CSS - COMPLETE FIX
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0ea5e9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Floating Animated Background Blobs */
    .stApp::before {
        content: '';
        position: fixed;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.15), transparent 70%);
        top: -200px;
        right: -200px;
        border-radius: 50%;
        animation: blob1 20s infinite ease-in-out;
        pointer-events: none;
        z-index: 0;
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(147, 51, 234, 0.12), transparent 70%);
        bottom: -150px;
        left: -150px;
        border-radius: 50%;
        animation: blob2 18s infinite ease-in-out;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes blob1 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-50px, 50px) scale(1.1); }
    }
    
    @keyframes blob2 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(50px, -50px) scale(1.15); }
    }
    
    /* Main Container - Clean Glassmorphism */
    .block-container {
        max-width: 1400px !important;
        padding: 3rem 2rem !important;
        background: rgba(15, 23, 42, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        position: relative;
        z-index: 1;
    }
    
    /* Hero Title */
    h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em !important;
        line-height: 1.2 !important;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.125rem;
        font-weight: 500;
        margin-bottom: 3rem;
        letter-spacing: 0.01em;
    }
    
    /* Section Headers */
    .section-header {
        color: #e2e8f0;
        font-size: 1.625rem;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        letter-spacing: -0.01em;
        animation: floatHeader 3s ease-in-out infinite;
    }
    
    @keyframes floatHeader {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    /* Labels */
    .stNumberInput > label,
    .stSelectbox > label {
        color: #e2e8f0 !important;
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
        display: block !important;
        letter-spacing: 0.01em !important;
    }
    
    /* Number Inputs */
    .stNumberInput > div > div > input {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1.125rem !important;
        font-weight: 500 !important;
        padding: 1rem 1.25rem !important;
        height: 56px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: none !important;
    }
    
    .stNumberInput > div > div > input:hover {
        background: rgba(30, 41, 59, 0.7) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        animation: focusGlow 1.5s ease-in-out infinite;
    }
    
    @keyframes focusGlow {
        0%, 100% { box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }
        50% { box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.25); }
    }
    
    # /* ========== NUCLEAR DROPDOWN FIX ========== */
    
    # /* Force white text on EVERYTHING in selectbox */
    # .stSelectbox,
    # .stSelectbox *,
    # .stSelectbox div,
    # .stSelectbox span,
    # .stSelectbox p,
    # .stSelectbox [class*="st-"] {
    #     color: #ffffff !important;
    # }
    
    # /* Main selectbox container */
    # .stSelectbox [data-baseweb="select"] {
    #     background: rgba(30, 41, 59, 0.6) !important;
    #     border: 1px solid rgba(148, 163, 184, 0.2) !important;
    #     border-radius: 12px !important;
    #     min-height: 56px !important;
    # }
    
    # /* Inner content wrapper */
    # .stSelectbox [data-baseweb="select"] > div {
    #     background: transparent !important;
    #     border: none !important;
    #     padding: 0 !important;
    #     color: #ffffff !important;
    # }
    
    # /* Control wrapper (contains the text) */
    # .stSelectbox [data-baseweb="select"] [class*="control"] {
    #     background: transparent !important;
    #     border: none !important;
    #     padding: 1rem 1.25rem !important;
    #     min-height: 56px !important;
    # }
    
    # /* Value container (selected value) */
    # .stSelectbox [data-baseweb="select"] [class*="ValueContainer"] {
    #     padding: 0 !important;
    #     color: #ffffff !important;
    # }
    
    # /* Single value (the actual text) */
    # .stSelectbox [data-baseweb="select"] [class*="singleValue"],
    # .stSelectbox [data-baseweb="select"] [class*="SingleValue"] {
    #     color: #ffffff !important;
    #     font-size: 1.125rem !important;
    #     font-weight: 500 !important;
    # }
    
    # /* Placeholder */
    # .stSelectbox [data-baseweb="select"] [class*="placeholder"],
    # .stSelectbox [data-baseweb="select"] [class*="Placeholder"] {
    #     color: rgba(255, 255, 255, 0.5) !important;
    # }
    
    # /* Input (when typing) */
    # .stSelectbox [data-baseweb="select"] input {
    #     color: #ffffff !important;
    # }
    
    # /* Dropdown indicator (arrow) */
    # .stSelectbox [data-baseweb="select"] [class*="indicatorContainer"] svg,
    # .stSelectbox svg {
    #     fill: #ffffff !important;
    #     color: #ffffff !important;
    # }
    
    # /* Hover state */
    # .stSelectbox [data-baseweb="select"]:hover {
    #     background: rgba(30, 41, 59, 0.7) !important;
    #     border-color: rgba(59, 130, 246, 0.4) !important;
    # }
    
    # /* Focus state */
    # .stSelectbox [data-baseweb="select"]:focus-within {
    #     background: rgba(30, 41, 59, 0.8) !important;
    #     border: 1px solid #3b82f6 !important;
    #     box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    #     animation: focusGlow 1.5s ease-in-out infinite;
    # }
    
    # /* Dropdown menu */
    # .stSelectbox [data-baseweb="popover"],
    # .stSelectbox [role="listbox"] {
    #     background: rgba(30, 41, 59, 0.95) !important;
    #     backdrop-filter: blur(10px) !important;
    #     border: 1px solid rgba(59, 130, 246, 0.3) !important;
    #     border-radius: 12px !important;
    #     padding: 0.5rem !important;
    #     margin-top: 0.5rem !important;
    # }
    
    # /* Menu list */
    # .stSelectbox [class*="menuList"],
    # .stSelectbox [class*="MenuList"] {
    #     background: transparent !important;
    #     padding: 0 !important;
    # }
    
    # /* Individual options */
    # .stSelectbox [role="option"],
    # .stSelectbox [class*="option"] {
    #     color: #000000 !important;
    #     background: transparent !important;
    #     padding: 0.875rem 1rem !important;
    #     font-size: 1.125rem !important;
    #     font-weight: 500 !important;
    #     border-radius: 8px !important;
    #     margin: 0.25rem 0 !important;
    #     transition: all 0.2s ease !important;
    # }
    
    # /* Option hover */
    # .stSelectbox [role="option"]:hover,
    # .stSelectbox [class*="option"]:hover {
    #     background: rgba(59, 130, 246, 0.25) !important;
    #     color: #ffffff !important;
    # }
    
    # /* Selected option */
    # .stSelectbox [role="option"][aria-selected="true"],
    # .stSelectbox [class*="option--is-selected"] {
    #     background: rgba(59, 130, 246, 0.35) !important;
    #     color: #ffffff !important;
    #     font-weight: 600 !important;
    # }
    
    # /* Focused option */
    # .stSelectbox [role="option"][class*="focused"],
    # .stSelectbox [class*="option--is-focused"] {
    #     background: rgba(59, 130, 246, 0.2) !important;
    #     color: #ffffff !important;
    # }
    
    /* Premium Gradient Button */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #9333ea 100%) !important;
        background-size: 200% 200%;
        color: #ffffff !important;
        font-size: 1.125rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 1rem 2.5rem !important;
        border: none !important;
        border-radius: 14px !important;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4) !important;
        margin-top: 2rem !important;
        animation: buttonGradient 3s ease infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes buttonGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::after {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5),
                    0 0 40px rgba(147, 51, 234, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Loan to Income Ratio Card */
    .ratio-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 2rem;
        transition: all 0.3s ease;
    }
    
    .ratio-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        animation: subtlePulse 0.6s ease-in-out;
    }
    
    @keyframes subtlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .ratio-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .ratio-value {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        animation: gradientShift 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Results Section */
    .result-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateX(5px);
    }
    
    .result-label {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .result-value {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    
    /* Column Spacing */
    [data-testid="column"] {
        padding: 0 0.75rem;
    }
    
    /* Step Buttons */
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        background: rgba(59, 130, 246, 0.15) !important;
        border: none !important;
        color: #3b82f6 !important;
        border-radius: 6px !important;
        transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
    }
    
    button[data-testid="stNumberInputStepUp"]:hover,
    button[data-testid="stNumberInputStepDown"]:hover {
        background: rgba(59, 130, 246, 0.25) !important;
        transform: scale(1.15) rotate(5deg) !important;
    }
    
    button[data-testid="stNumberInputStepUp"]:active,
    button[data-testid="stNumberInputStepDown"]:active {
        transform: scale(0.95) !important;
    }
    
    /* Breathing animation for main container */
    .block-container {
        animation: breathe 8s ease-in-out infinite;
    }
    
    @keyframes breathe {
        0%, 100% { 
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        50% { 
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2),
                        0 0 60px rgba(147, 51, 234, 0.15);
        }
    }
    
    /* Entrance animations */
    .stNumberInput, .stSelectbox {
        animation: fadeSlideIn 0.5s ease-out;
    }
    
    @keyframes fadeSlideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Progressive loading for results */
    .result-card:nth-child(1) { animation-delay: 0.1s; }
    .result-card:nth-child(2) { animation-delay: 0.2s; }
    .result-card:nth-child(3) { animation-delay: 0.3s; }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .section-header {
            font-size: 1.25rem;
        }
        
        .block-container {
            padding: 2rem 1rem !important;
        }
        
        .stButton > button {
            font-size: 1rem !important;
            padding: 0.875rem 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("<h1>Credit Risk Modelling</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-driven credit risk scoring for smarter lending decisions</p>', unsafe_allow_html=True)

# Section 1: Borrower Profile
st.markdown('<div class="section-header">🎯 Borrower Profile</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=25)
with col2:
    income = st.number_input('Income', min_value=0, value=1000000)
with col3:
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2000000)

# Section 2: Financial Metrics
st.markdown('<div class="section-header">💳 Financial Metrics</div>', unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)

loan_to_income_ratio = loan_amount / income if income > 0 else 0

with col4:
    st.markdown(f"""
    <div class="ratio-card">
        <div class="ratio-label">Loan to Income Ratio</div>
        <div class="ratio-value">{loan_to_income_ratio:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=12)
with col6:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=0)

# Section 3: Credit Behavior
st.markdown('<div class="section-header">📊 Credit Behavior</div>', unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)

with col7:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=0)
with col8:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1, value=50)
with col9:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=1)

# Section 4: Loan Details
st.markdown('<div class="section-header">🏡 Loan Details</div>', unsafe_allow_html=True)
col10, col11, col12 = st.columns(3)

with col10:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with col11:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with col12:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

# Calculate Risk Button
if st.button('Calculate Risk'):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    
    st.markdown('<div class="section-header">📈 Risk Assessment Results</div>', unsafe_allow_html=True)
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Default Probability</div>
            <div class="result-value">{probability:.2%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with res_col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Credit Score</div>
            <div class="result-value">{credit_score}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with res_col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Risk Rating</div>
            <div class="result-value">{rating}</div>
        </div>
        """, unsafe_allow_html=True)