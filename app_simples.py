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
        padding: 2rem 1rem;
    }
    
    /* Estilo do card de notas */
    .nota-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .nota-card h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .nota-card h3 {
        margin: 1rem 0 0 0;
        font-size: 1.8rem;
        font-weight: 400;
    }
    
    .avaliacao-box {
        background: rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    .avaliacao-box p {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .nota-valor {
        font-size: 3.5rem;
        font-weight: bold;
        margin: 0;
        line-height: 1;
    }
    
    .stButton > button {
        background: #2196F3;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #1976D2;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3);
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
        margin: 1.5rem 0;
    }
    
    .student-info h3 {
        margin: 0 0 0.5rem 0;
        color: #333;
    }
    
    .student-info p {
        margin: 0.25rem 0;
        color: #666;
    }
    
    /* Estilo dos inputs */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    /* Esconder label dos inputs quando necessário */
    .element-container:has(> .stSelectbox) label {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'aluno_encontrado' not in st.session_state:
    st.session_state.aluno_encontrado = False
if 'dados_aluno' not in st.session_state:
    st.session_state.dados_aluno = None
if 'turma_selecionada' not in st.session_state:
    st.session_state.turma_selecionada = None

# Header - apenas o título
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🎓 Sistema de Consulta de Notas</h1>", unsafe_allow_html=True)

# Se aluno não foi encontrado ainda, mostrar tela de consulta
if not st.session_state.aluno_encontrado:
    # Carregar turmas
    turmas = db.listar_turmas()
    
    if not turmas:
        st.warning("⚠️ Nenhuma turma disponível no momento.")
        st.info("💡 **Para administradores:** Acesse o sistema de administração para cadastrar turmas.")
    else:
        st.markdown("#### 🎓 Selecione sua turma:")
        turma_selecionada = st.selectbox(
            "Turma",
            options=list(turmas.keys()),
            label_visibility="collapsed"
        )
        
        if turma_selecionada:
            turma_info = turmas[turma_selecionada]
            st.markdown(f"""
            <div class='info-box'>
                ✅ Dados da turma <strong>{turma_selecionada}</strong> carregados!<br>
                📅 {turma_info['data_upload'].split(' às ')[0]}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### 🔑 Digite sua matrícula:")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                matricula = st.text_input(
                    "Matrícula",
                    placeholder="1707075",
                    label_visibility="collapsed",
                    key="matricula_input"
                )
            with col2:
                consultar = st.button("🔍 Consultar", type="primary", use_container_width=True)
            
            if consultar and matricula:
                aluno = db.verificar_aluno(turma_selecionada, matricula)
                if aluno:
                    st.session_state.aluno_encontrado = True
                    st.session_state.dados_aluno = aluno
                    st.session_state.turma_selecionada = turma_selecionada
                    st.rerun()
                else:
                    st.error("❌ Aluno não encontrado!")

else:
    # Tela de notas do aluno
    aluno = st.session_state.dados_aluno
    turma = st.session_state.turma_selecionada
    
    st.markdown(f"""
    <div class='info-box'>
        ✅ Aluno encontrado!
    </div>
    """, unsafe_allow_html=True)
    
    # Informações do aluno
    st.markdown(f"""
    <div class='student-info'>
        <h3>👤 {aluno['nome']}</h3>
        <p><strong>Matrícula:</strong> {st.session_state.dados_aluno.get('matricula', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Card de notas estilo da imagem
    st.markdown(f"""
    <div class='nota-card'>
        <h2>✅ Suas Notas</h2>
        <h3>{aluno['nome']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Exibir notas em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        nota1 = aluno.get('nota1', '-')
        st.markdown(f"""
        <div class='avaliacao-box'>
            <p>📝 Avaliação 01</p>
            <div class='nota-valor'>{nota1}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nota2 = aluno.get('nota2', '-')
        st.markdown(f"""
        <div class='avaliacao-box'>
            <p>📝 Avaliação 02</p>
            <div class='nota-valor'>{nota2}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Média e situação
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        media = aluno.get('media', '-')
        st.metric("🎯 Média Final", media)
    
    with col2:
        situacao = aluno.get('situacao', '-')
        if situacao.lower() == 'aprovado':
            st.success(f"✅ **{situacao.upper()}**")
        elif situacao.lower() == 'reprovado':
            st.error(f"❌ **{situacao.upper()}**")
        else:
            st.info(f"📌 **{situacao}**")
    
    # Gráfico
    notas_display = []
    if nota1 != '-':
        notas_display.append(float(nota1))
    if nota2 != '-':
        notas_display.append(float(nota2))
    
    if len(notas_display) >= 2:
        st.markdown("---")
        st.markdown("### 📊 Desempenho nas Avaliações")
        chart_data = pd.DataFrame({
            'Avaliação': [f'AV {i+1}' for i in range(len(notas_display))],
            'Nota': notas_display
        })
        st.bar_chart(chart_data.set_index('Avaliação'))
    
    # Botão para nova consulta
    st.markdown("---")
    if st.button("🔄 Nova Consulta", use_container_width=True):
        st.session_state.aluno_encontrado = False
        st.session_state.dados_aluno = None
        st.session_state.turma_selecionada = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #999; font-size: 0.9rem;'>© {datetime.now().year} Sistema de Consulta de Notas</p>", unsafe_allow_html=True)
