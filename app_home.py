import streamlit as st
from datetime import datetime
import database as db

# Inicializar banco de dados
db.init_db()

# Configuração da página
st.set_page_config(
    page_title="Sistema de Consulta de Notas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Carregar dados do banco de dados
turmas = db.listar_turmas()
total_alunos = sum(t['total_alunos'] for t in turmas.values()) if turmas else 0

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/student-center.png", width=80)
    st.title("📊 Sistema de Notas")
    
    st.divider()
    st.markdown("### 🎯 Escolha sua área:")
    
    st.page_link("pages/1_Login_Administrador.py", label="🔐 Área do Professor", use_container_width=True)
    st.page_link("pages/2_Login_Aluno.py", label="👨‍🎓 Área do Aluno", use_container_width=True)
    
    st.divider()
    
    # Estatísticas
    if turmas:
        st.markdown("### 📊 Estatísticas:")
        st.metric("Turmas Cadastradas", len(turmas))
        st.metric("Total de Alunos", total_alunos)
    
    st.divider()
    st.caption(f"© {datetime.now().year} - Sistema de Consulta de Notas")

# Página inicial
st.markdown("""
    <div class='main-header'>
        <h1>📊 Sistema de Consulta de Notas</h1>
        <p style='font-size: 1.2rem;'>Consulte suas notas de forma rápida e segura</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("## 👋 Bem-vindo ao Sistema de Consulta de Notas!")

st.markdown("""
Este sistema permite que alunos consultem suas notas e que professores gerenciem as informações acadêmicas.
""")

# Cards de funcionalidades
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>🔐 Área do Professor</h3>
        <p><strong>Funcionalidades:</strong></p>
        <ul>
            <li>Upload de arquivos PDF com notas</li>
            <li>Cadastro de turmas e períodos</li>
            <li>Visualização de todas as turmas</li>
            <li>Gerenciamento completo de dados</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔐 Acessar Área do Professor", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Login_Administrador.py")

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>👨‍🎓 Área do Aluno</h3>
        <p><strong>Funcionalidades:</strong></p>
        <ul>
            <li>Consulta de notas por matrícula</li>
            <li>Visualização de todas as avaliações</li>
            <li>Cálculo automático de média</li>
            <li>Gráfico de desempenho</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👨‍🎓 Acessar Área do Aluno", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Login_Aluno.py")

st.markdown("---")

# Informações adicionais
st.markdown("### 📚 Como usar o sistema:")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Para Professores:**
    1. Clique em "Área do Professor"
    2. Faça login com suas credenciais
    3. Faça upload do PDF com as notas
    4. Gerencie suas turmas
    """)

with col2:
    st.info("""
    **Para Alunos:**
    1. Clique em "Área do Aluno"
    2. Selecione sua turma
    3. Digite sua matrícula
    4. Visualize suas notas
    """)

# Informações do sistema
if turmas:
    st.markdown("---")
    st.success(f"✅ Sistema ativo com **{len(turmas)}** turma(s) cadastrada(s)")
