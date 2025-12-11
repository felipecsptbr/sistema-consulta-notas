import streamlit as st
from datetime import datetime
import pandas as pd
import database as db
from utils import processar_pdf
import os

# Inicializar banco de dados
db.init_db()

# Configuração da página
st.set_page_config(
    page_title="Administração - Sistema de Notas",
    page_icon="🔧",
    layout="wide"
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stat-card h2 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .stat-card p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: white; padding: 1rem 0;'>🔧 Administração - Sistema de Notas</h1>", unsafe_allow_html=True)

# Container principal
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # Estatísticas
    turmas = db.listar_turmas()
    total_turmas = len(turmas)
    total_alunos = sum(info['total_alunos'] for info in turmas.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <h2>{total_turmas}</h2>
            <p>📚 Turmas Cadastradas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <h2>{total_alunos}</h2>
            <p>👨‍🎓 Total de Alunos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <h2>{datetime.now().year}</h2>
            <p>📅 Ano Letivo</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu de opções
    tab1, tab2, tab3 = st.tabs(["📤 Cadastrar Turma", "📋 Listar Turmas", "🗑️ Remover Turma"])
    
    # TAB 1: Cadastrar Nova Turma
    with tab1:
        st.markdown("### 📤 Cadastrar Nova Turma")
        st.markdown("Preencha os dados abaixo e faça upload do PDF com as notas dos alunos.")
        
        with st.form("form_cadastro"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                nome_turma = st.text_input(
                    "📚 Nome da Turma",
                    placeholder="Ex: 4º Período B - ML"
                )
            
            with col2:
                periodo = st.text_input(
                    "📅 Período",
                    placeholder="Ex: 2025.2",
                    value="2025.2"
                )
            
            uploaded_file = st.file_uploader(
                "📄 Selecione o arquivo PDF com as notas",
                type=['pdf'],
                help="Faça upload de um PDF no formato SEREDUC"
            )
            
            submitted = st.form_submit_button("✅ Cadastrar Turma", use_container_width=True, type="primary")
            
            if submitted:
                if not nome_turma:
                    st.error("❌ Por favor, preencha o nome da turma!")
                elif not uploaded_file:
                    st.error("❌ Por favor, selecione um arquivo PDF!")
                else:
                    with st.spinner("⏳ Processando PDF..."):
                        try:
                            notas = processar_pdf(uploaded_file)
                            
                            if not notas:
                                st.error("❌ Nenhum dado encontrado no PDF!")
                            else:
                                st.success(f"✅ {len(notas)} alunos encontrados no PDF")
                                
                                # Mostrar preview dos primeiros alunos
                                with st.expander("👀 Ver primeiros alunos encontrados"):
                                    preview_data = []
                                    for mat, dados in list(notas.items())[:5]:
                                        preview_data.append({
                                            'Matrícula': mat,
                                            'Nome': dados['nome'],
                                            'Nota 1': dados.get('nota1', '-'),
                                            'Nota 2': dados.get('nota2', '-')
                                        })
                                    st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)
                                
                                # Cadastrar no banco
                                if db.cadastrar_turma(nome_turma, periodo, uploaded_file.name, notas):
                                    st.balloons()
                                    st.success("🎉 Turma cadastrada com sucesso!")
                                    st.info("💡 Acesse a aba 'Listar Turmas' para ver os detalhes.")
                                else:
                                    st.error("❌ Erro ao cadastrar turma. Talvez ela já exista!")
                        
                        except Exception as e:
                            st.error(f"❌ Erro ao processar PDF: {str(e)}")
    
    # TAB 2: Listar Turmas
    with tab2:
        st.markdown("### 📋 Turmas Cadastradas")
        
        if not turmas:
            st.info("📭 Nenhuma turma cadastrada ainda.")
        else:
            for turma, info in turmas.items():
                with st.expander(f"📚 **{turma}** ({info['total_alunos']} alunos)", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📅 Período", info['periodo'])
                    
                    with col2:
                        st.metric("👨‍🎓 Total de Alunos", info['total_alunos'])
                    
                    with col3:
                        st.metric("📄 Arquivo", info.get('arquivo', 'N/A'))
                    
                    st.caption(f"🕐 Upload em: {info['data_upload']}")
                    
                    st.markdown("---")
                    st.markdown("**📊 Lista de Alunos:**")
                    
                    # Obter notas da turma
                    notas = db.obter_notas_turma(turma)
                    df_alunos = pd.DataFrame([
                        {
                            'Matrícula': mat,
                            'Nome': d['nome'],
                            'Nota 1': d.get('nota1', '-'),
                            'Nota 2': d.get('nota2', '-'),
                            'Nota 3': d.get('nota3', '-'),
                            'Média': d.get('media', '-'),
                            'Situação': d.get('situacao', '-')
                        }
                        for mat, d in notas.items()
                    ])
                    
                    st.dataframe(
                        df_alunos,
                        use_container_width=True,
                        hide_index=True,
                        height=400
                    )
                    
                    # Botão para baixar CSV
                    csv = df_alunos.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Baixar planilha (CSV)",
                        data=csv,
                        file_name=f"{turma.replace(' ', '_')}_notas.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
    
    # TAB 3: Remover Turma
    with tab3:
        st.markdown("### 🗑️ Remover Turma")
        st.warning("⚠️ **Atenção:** Esta ação não pode ser desfeita!")
        
        if not turmas:
            st.info("📭 Nenhuma turma cadastrada para remover.")
        else:
            turma_remover = st.selectbox(
                "Selecione a turma que deseja remover:",
                options=list(turmas.keys())
            )
            
            if turma_remover:
                st.markdown(f"""
                <div class='card'>
                    <h4>📚 {turma_remover}</h4>
                    <p><strong>Período:</strong> {turmas[turma_remover]['periodo']}</p>
                    <p><strong>Alunos:</strong> {turmas[turma_remover]['total_alunos']}</p>
                    <p><strong>Data:</strong> {turmas[turma_remover]['data_upload']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col2:
                    if st.button("🗑️ Confirmar Remoção", type="primary", use_container_width=True):
                        if db.remover_turma(turma_remover):
                            st.success(f"✅ Turma '{turma_remover}' removida com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao remover turma!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<p style='text-align: center; color: white; padding: 1rem;'>
    © {datetime.now().year} Sistema de Notas - Painel Administrativo
</p>
""", unsafe_allow_html=True)
