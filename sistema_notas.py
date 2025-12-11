import streamlit as st
from datetime import datetime
import pandas as pd
import database as db
from utils import processar_pdf

# Inicializar banco de dados
db.init_db()

# Configuração da página
st.set_page_config(
    page_title="Sistema de Consulta de Notas",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
    <style>
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo geral */
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Estilo do card de notas */
    .nota-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .avaliacao-box {
        background: rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
        display: inline-block;
        min-width: 150px;
    }
    
    .nota-valor {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: #667eea;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .info-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .student-info {
        background: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_matricula' not in st.session_state:
    st.session_state.user_matricula = None
if 'selected_turma' not in st.session_state:
    st.session_state.selected_turma = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_name = None
    st.session_state.user_matricula = None
    st.session_state.selected_turma = None
    st.rerun()

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🎓 Sistema de Consulta de Notas</h1>", unsafe_allow_html=True)

# Menu de navegação no topo
if st.session_state.logged_in:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info(f"👤 Logado como: **{st.session_state.user_type}** - {st.session_state.user_name}")
    with col2:
        if st.button("🚪 Sair"):
            logout()

st.markdown("---")

# Verificar tipo de usuário
if not st.session_state.logged_in:
    # Tela de seleção de perfil
    tab1, tab2 = st.tabs(["👨‍🎓 Área do Aluno", "🔐 Área do Professor"])
    
    with tab1:
        st.markdown("### 👨‍🎓 Acesso do Aluno")
        
        # Carregar turmas
        turmas = db.listar_turmas()
        
        if not turmas:
            st.warning("⚠️ Nenhuma turma disponível. Aguarde o professor cadastrar as notas.")
        else:
            st.markdown("#### 🎓 Selecione sua turma:")
            turma_selecionada = st.selectbox(
                "Turma",
                options=list(turmas.keys()),
                label_visibility="collapsed"
            )
            
            if turma_selecionada:
                st.success(f"✅ Dados da turma **{turma_selecionada}** carregados com sucesso!")
                st.info(f"📅 Período: {turmas[turma_selecionada]['periodo']} | 🕐 {turmas[turma_selecionada]['data_upload']}")
                
                st.markdown("---")
                st.markdown("#### 🔑 Digite sua matrícula:")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    matricula = st.text_input(
                        "Matrícula",
                        placeholder="Digite sua matrícula (ex: 1707075)",
                        label_visibility="collapsed"
                    )
                with col2:
                    consultar = st.button("🔍 Consultar", type="primary")
                
                if consultar and matricula:
                    aluno = db.verificar_aluno(turma_selecionada, matricula)
                    if aluno:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Aluno"
                        st.session_state.user_matricula = matricula
                        st.session_state.user_name = aluno['nome']
                        st.session_state.selected_turma = turma_selecionada
                        st.rerun()
                    else:
                        st.error("❌ Matrícula não encontrada!")
    
    with tab2:
        st.markdown("### 🔐 Acesso do Professor")
        st.info("⚠️ Área restrita para professores")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
            password = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
            
            if st.button("🔐 Entrar como Professor", type="primary"):
                if username and password:
                    if db.verificar_login_admin(username, password):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Professor"
                        st.session_state.user_name = username.title()
                        st.success("✅ Login realizado!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas!")
            
            st.caption("**Usuários teste:** admin/admin123 ou professor/prof123")

elif st.session_state.user_type == "Aluno":
    # Tela do aluno com notas
    st.markdown("### ✅ Aluno encontrado!")
    
    # Informações do aluno
    st.markdown(f"""
    <div class='student-info'>
        <h3>👤 {st.session_state.user_name}</h3>
        <p><strong>Matrícula:</strong> {st.session_state.user_matricula}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Obter notas do banco
    turmas = db.listar_turmas()
    turma_info = turmas.get(st.session_state.selected_turma)
    notas_turma = db.obter_notas_turma(st.session_state.selected_turma)
    dados_aluno = notas_turma.get(st.session_state.user_matricula, {})
    
    # Card de notas estilo da imagem
    st.markdown("""
    <div class='nota-card'>
        <h2>✅ Suas Notas</h2>
        <h3>{}</h3>
    </div>
    """.format(st.session_state.user_name), unsafe_allow_html=True)
    
    # Exibir notas em colunas
    col1, col2, col3 = st.columns(3)
    
    notas_display = []
    for i in range(1, 4):
        nota_key = f'nota{i}'
        nota = dados_aluno.get(nota_key, '-')
        if nota != '-':
            notas_display.append(float(nota))
    
    with col1:
        st.markdown("""
        <div class='avaliacao-box'>
            <p>📝 Avaliação 01</p>
            <div class='nota-valor'>{}</div>
        </div>
        """.format(dados_aluno.get('nota1', '-')), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='avaliacao-box'>
            <p>📝 Avaliação 02</p>
            <div class='nota-valor'>{}</div>
        </div>
        """.format(dados_aluno.get('nota2', '-')), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='avaliacao-box'>
            <p>📝 Avaliação 03</p>
            <div class='nota-valor'>{}</div>
        </div>
        """.format(dados_aluno.get('nota3', '-')), unsafe_allow_html=True)
    
    # Média e situação
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        media = dados_aluno.get('media', '-')
        st.metric("🎯 Média Final", media, delta=None)
    
    with col2:
        situacao = dados_aluno.get('situacao', '-')
        if situacao.lower() == 'aprovado':
            st.success(f"✅ **Situação:** {situacao.upper()}")
        elif situacao.lower() == 'reprovado':
            st.error(f"❌ **Situação:** {situacao.upper()}")
        else:
            st.info(f"📌 **Situação:** {situacao}")
    
    # Gráfico
    if notas_display:
        st.markdown("---")
        st.markdown("### 📊 Desempenho nas Avaliações")
        chart_data = pd.DataFrame({
            'Avaliação': [f'Nota {i+1}' for i in range(len(notas_display))],
            'Nota': notas_display
        })
        st.bar_chart(chart_data.set_index('Avaliação'))

elif st.session_state.user_type == "Professor":
    # Tela do professor
    st.markdown("### 🔧 Painel do Professor")
    
    tab1, tab2 = st.tabs(["📤 Upload de Notas", "📋 Turmas Cadastradas"])
    
    with tab1:
        st.markdown("#### 📄 Upload de PDF com Notas")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            nome_turma = st.text_input("Nome da Turma:", placeholder="Ex: 4º Período B - ML")
        with col2:
            periodo = st.text_input("Período:", placeholder="Ex: 2025.2")
        
        uploaded_file = st.file_uploader("Selecione o arquivo PDF", type=['pdf'])
        
        if uploaded_file:
            st.success(f"✅ Arquivo '{uploaded_file.name}' carregado ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("📊 Processar e Cadastrar", type="primary"):
                if nome_turma:
                    with st.spinner("Processando PDF..."):
                        from utils import processar_pdf
                        notas = processar_pdf(uploaded_file)
                        
                        if db.cadastrar_turma(nome_turma, periodo, uploaded_file.name, notas):
                            st.success("✅ Turma cadastrada com sucesso!")
                            st.balloons()
                        else:
                            st.error("❌ Erro ao cadastrar. Turma já existe.")
                else:
                    st.error("⚠️ Preencha o nome da turma!")
    
    with tab2:
        st.markdown("#### 📚 Turmas Cadastradas")
        turmas = db.listar_turmas()
        
        if turmas:
            for turma, info in turmas.items():
                with st.expander(f"📚 {turma}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Período", info['periodo'])
                    with col2:
                        st.metric("Alunos", info['total_alunos'])
                    with col3:
                        st.write(f"**Upload:** {info['data_upload']}")
                    
                    if st.checkbox(f"Ver alunos", key=f"ver_{turma}"):
                        notas = db.obter_notas_turma(turma)
                        df = pd.DataFrame([
                            {
                                'Matrícula': mat,
                                'Nome': d['nome'],
                                'N1': d.get('nota1', '-'),
                                'N2': d.get('nota2', '-'),
                                'N3': d.get('nota3', '-'),
                                'Média': d.get('media', '-'),
                                'Situação': d.get('situacao', '-')
                            }
                            for mat, d in notas.items()
                        ])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    if st.button(f"🗑️ Remover", key=f"del_{turma}"):
                        if db.remover_turma(turma):
                            st.success("✅ Turma removida!")
                            st.rerun()
        else:
            st.info("📭 Nenhuma turma cadastrada.")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #666;'>© {datetime.now().year} - Sistema de Consulta de Notas</p>", unsafe_allow_html=True)
