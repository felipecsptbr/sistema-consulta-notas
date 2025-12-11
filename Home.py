import streamlit as st

st.set_page_config(
    page_title="Sistema de Notas",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 2rem auto;
        max-width: 600px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-card'>
    <h1>🎓 Sistema de Consulta de Notas</h1>
    <p style='color: #666; font-size: 1.1rem; margin: 1rem 0 2rem 0;'>
        Escolha como você deseja acessar o sistema
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 15px; margin: 1rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h2>👨‍🎓</h2>
        <h3>Área do Aluno</h3>
        <p style='color: #666;'>Consulte suas notas</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Consultar Notas", key="aluno", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Consulta_Aluno.py")

with col2:
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 15px; margin: 1rem; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'>
        <h2>🔧</h2>
        <h3>Administração</h3>
        <p style='color: #666;'>Gerenciar turmas</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚙️ Painel Admin", key="admin", use_container_width=True):
        st.switch_page("pages/2_Painel_Admin.py")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 1rem;'>
    <p>Sistema desenvolvido com Streamlit • 2025</p>
</div>
""", unsafe_allow_html=True)
