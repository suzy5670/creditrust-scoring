import streamlit as st

st.title(":material/account_balance: Notation CrediTrust")

st.markdown(
    """
    <div style="display:flex; gap:14px; margin: 6px 0 18px 0; font-size:1.8rem;">
        <span>💳</span><span>📈</span><span>🔒</span>
    </div>
    <style>
    .team-card {
        background: linear-gradient(135deg, #f4f7fb 0%, #e8eef6 100%);
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(31,58,95,0.12);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .team-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 24px rgba(31,58,95,0.22);
    }
    .team-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(90deg, #1E3A5F, #D97706, #1E3A5F);
        background-size: 200% 100%;
        animation: glisser 3s linear infinite;
    }
    @keyframes glisser {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    .avatar {
        width: 84px; height: 84px;
        border-radius: 50%;
        margin: 0 auto 14px auto;
        display: flex; align-items: center; justify-content: center;
        background: #1E3A5F;
        font-size: 2.2rem;
    }
    .team-role {
        font-style: italic;
        text-transform: uppercase;
        font-size: 0.8rem;
        color: #D97706;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .team-name {
        font-weight: bold;
        font-size: 1.2rem;
        color: #1E3A5F;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.caption("Équipe projet — Département Risque Financier")
st.write("")

col_marge1, col1, col2, col3, col_marge2 = st.columns([0.5, 1, 1, 1, 0.5], gap="large")

membres = [
    ("👩‍💻", "Suz", "Data Lead Tech"),
    ("👩‍🔬", "Mouna", "Data Scientist"),
    ("👩‍💼", "Joséphine", "Data Analyst"),
]

for col, (emoji, nom, role) in zip([col1, col2, col3], membres):
    with col:
        st.markdown(
            f"""
            <div class="team-card">
                <div class="avatar">{emoji}</div>
                <div class="team-role">{role}</div>
                <div class="team-name">{nom}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )