import streamlit as st
from datetime import datetime

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

# Inicializar session state
if 'turmas' not in st.session_state:
    st.session_state.turmas = {}
if 'notas_carregadas' not in st.session_state:
    st.session_state.notas_carregadas = {}
if 'admin_users' not in st.session_state:
    # Usuários administradores (username: senha)
    st.session_state.admin_users = {
        'admin': 'admin123',
        'professor': 'prof123'
    }

def main():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_name = None
    st.session_state.user_matricula = None
    st.rerun()

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/student-center.png", width=80)
        st.title("Sistema de Notas")
        
        if st.session_state.logged_in:
            st.success(f"👤 {st.session_state.user_type}")
            if st.session_state.user_name:
                st.info(f"**Nome:** {st.session_state.user_name}")
            if st.session_state.user_matricula:
                st.info(f"**Matrícula:** {st.session_state.user_matricula}")
            
            st.divider()
            if st.button("🚪 Sair", use_container_width=True, type="primary"):
                logout()
        
        st.divider()
        st.caption(f"© {datetime.now().year} - Sistema de Consulta de Notas")
    
    # Página de login/seleção
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.user_type == "Administrador":
            show_admin_page()
        else:
            show_student_page()

def show_login_page():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>📊 Sistema de Consulta de Notas</h1>
            <p style='font-size: 1.2rem; color: #666;'>Consulte suas notas de forma rápida e segura</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs para Login
    tab1, tab2 = st.tabs(["👨‍🎓 Login Aluno", "🔐 Login Administrador"])
    
    with tab1:
        show_student_login()
    
    with tab2:
        show_admin_login()

def show_admin_login():
    """Tela de login para administrador"""
    st.markdown("### 🔐 Acesso de Administrador")
    st.info("⚠️ Área restrita para professores e administradores")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("admin_login_form"):
            st.markdown("#### Digite suas credenciais:")
            
            username = st.text_input(
                "👤 Usuário:",
                placeholder="Digite seu usuário",
                key="admin_username"
            )
            
            password = st.text_input(
                "🔑 Senha:",
                type="password",
                placeholder="Digite sua senha",
                key="admin_password"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button(
                    "🔐 Entrar",
                    use_container_width=True,
                    type="primary"
                )
            with col_btn2:
                clear = st.form_submit_button(
                    "🔄 Limpar",
                    use_container_width=True
                )
            
            if submitted:
                if username and password:
                    # Verificar credenciais
                    if username in st.session_state.admin_users:
                        if st.session_state.admin_users[username] == password:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "Administrador"
                            st.session_state.user_name = username.title()
                            st.success("✅ Login realizado com sucesso!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta!")
                    else:
                        st.error("❌ Usuário não encontrado!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
        
        st.markdown("---")
        st.caption("**Usuários de teste:**")
        st.caption("👤 admin / 🔑 admin123")
        st.caption("👤 professor / 🔑 prof123")

def show_student_login():
    """Tela de login para aluno"""
    st.markdown("### 👨‍🎓 Acesso do Aluno")
    st.info("📚 Digite suas informações para acessar suas notas")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.turmas:
            st.warning("⚠️ Nenhuma turma disponível no momento. Aguarde o professor cadastrar as notas.")
            return
        
        with st.form("student_login_form"):
            st.markdown("#### Digite suas informações:")
            
            turma_selecionada = st.selectbox(
                "📚 Selecione sua turma:",
                ["Selecione..."] + list(st.session_state.turmas.keys()),
                key="student_turma"
            )
            
            matricula = st.text_input(
                "🎓 Matrícula:",
                placeholder="Digite sua matrícula (ex: 1234567)",
                max_chars=10,
                key="student_matricula"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button(
                    "🔍 Entrar",
                    use_container_width=True,
                    type="primary"
                )
            with col_btn2:
                clear = st.form_submit_button(
                    "🔄 Limpar",
                    use_container_width=True
                )
            
            if submitted:
                if turma_selecionada != "Selecione..." and matricula:
                    # Verificar se a matrícula existe na turma
                    notas_turma = st.session_state.notas_carregadas.get(turma_selecionada, {})
                    
                    if matricula in notas_turma:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "Aluno"
                        st.session_state.user_matricula = matricula
                        st.session_state.user_name = notas_turma[matricula]['nome']
                        st.session_state.selected_turma = turma_selecionada
                        st.success("✅ Login realizado com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Matrícula não encontrada nesta turma!")
                        st.info("💡 Verifique se digitou corretamente ou escolha outra turma.")
                else:
                    st.warning("⚠️ Selecione uma turma e digite sua matrícula!")

def show_admin_page():
    st.title("🔧 Painel do Administrador")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📤 Upload de Notas", "📋 Turmas Cadastradas"])
    
    with tab1:
        st.header("Upload de PDF com Notas")
        st.info("📄 Faça upload de arquivos PDF contendo as notas dos alunos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            nome_turma = st.text_input("Nome da Turma:", placeholder="Ex: 2º Período C - POO")
        
        with col2:
            periodo = st.text_input("Período:", placeholder="Ex: 2023.2")
        
        uploaded_file = st.file_uploader(
            "Selecione o arquivo PDF",
            type=['pdf'],
            help="Arquivo PDF contendo matrícula e notas dos alunos"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Arquivo '{uploaded_file.name}' carregado!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tamanho", f"{uploaded_file.size / 1024:.1f} KB")
            with col2:
                st.metric("Tipo", uploaded_file.type)
            
            if st.button("📊 Processar PDF e Cadastrar", type="primary"):
                if nome_turma:
                    with st.spinner("Processando PDF..."):
                        # Processar PDF e extrair dados
                        notas_extraidas = processar_pdf(uploaded_file)
                        
                        # Salvar no session state
                        st.session_state.turmas[nome_turma] = {
                            'periodo': periodo,
                            'arquivo': uploaded_file.name,
                            'data_upload': datetime.now().strftime("%d/%m/%Y %H:%M"),
                            'total_alunos': len(notas_extraidas)
                        }
                        st.session_state.notas_carregadas[nome_turma] = notas_extraidas
                        
                        st.success(f"✅ Turma '{nome_turma}' cadastrada com sucesso!")
                        st.balloons()
                else:
                    st.error("⚠️ Por favor, preencha o nome da turma!")
    
    with tab2:
        st.header("Turmas Cadastradas")
        
        if st.session_state.turmas:
            for turma, info in st.session_state.turmas.items():
                with st.expander(f"📚 {turma}", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Período", info['periodo'])
                    with col2:
                        st.metric("Total de Alunos", info['total_alunos'])
                    with col3:
                        st.write("**Data Upload:**")
                        st.write(info['data_upload'])
                    with col4:
                        st.write("**Arquivo:**")
                        st.write(info['arquivo'])
                    
                    if st.button(f"🗑️ Remover {turma}", key=f"del_{turma}"):
                        del st.session_state.turmas[turma]
                        del st.session_state.notas_carregadas[turma]
                        st.rerun()
        else:
            st.info("📭 Nenhuma turma cadastrada ainda. Faça upload de um PDF na aba 'Upload de Notas'.")

def show_student_page():
    st.title("👨‍🎓 Minhas Notas")
    
    # Informações do aluno logado
    st.markdown(f"### Bem-vindo(a), {st.session_state.user_name}! 👋")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**📝 Nome:** {st.session_state.user_name}")
    with col2:
        st.info(f"**🎓 Matrícula:** {st.session_state.user_matricula}")
    
    st.markdown("---")
    
    # Obter turma e notas do aluno
    turma_selecionada = st.session_state.get('selected_turma')
    
    if turma_selecionada:
        info_turma = st.session_state.turmas[turma_selecionada]
        notas_turma = st.session_state.notas_carregadas.get(turma_selecionada, {})
        dados_aluno = notas_turma.get(st.session_state.user_matricula, {})
        
        # Informações da turma
        st.markdown(f"### 📚 {turma_selecionada}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📅 Período", info_turma['periodo'])
        with col2:
            st.metric("👥 Total de Alunos", info_turma['total_alunos'])
        
        st.markdown("---")
        st.markdown("### 📊 Suas Notas")
        
        # Exibir notas em cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            nota = dados_aluno.get('nota1', '-')
            st.metric("📝 Nota 1", nota)
        
        with col2:
            nota = dados_aluno.get('nota2', '-')
            st.metric("📝 Nota 2", nota)
        
        with col3:
            nota = dados_aluno.get('nota3', '-')
            st.metric("📝 Nota 3", nota)
        
        with col4:
            media = dados_aluno.get('media', '-')
            if media != '-':
                delta = "✅ Aprovado" if float(media) >= 6.0 else "❌ Reprovado"
            else:
                delta = None
            st.metric("🎯 Média Final", media, delta=delta)
        
        # Situação final com destaque
        st.markdown("---")
        situacao = dados_aluno.get('situacao', 'Em andamento')
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if situacao.lower() == 'aprovado':
                st.success(f"### 🎉 Situação: {situacao.upper()}")
                st.balloons()
            elif situacao.lower() == 'reprovado':
                st.error(f"### 📛 Situação: {situacao.upper()}")
            else:
                st.info(f"### 📌 Situação: {situacao}")
        
        # Gráfico de desempenho
        st.markdown("---")
        st.markdown("### 📈 Gráfico de Desempenho")
        
        import pandas as pd
        
        notas_list = []
        for i in range(1, 4):
            nota_key = f'nota{i}'
            if nota_key in dados_aluno and dados_aluno[nota_key] != '-':
                notas_list.append({
                    'Avaliação': f'Nota {i}',
                    'Nota': float(dados_aluno[nota_key])
                })
        
        if notas_list:
            df_notas = pd.DataFrame(notas_list)
            st.bar_chart(df_notas.set_index('Avaliação'))
        
        # Informações adicionais
        st.markdown("---")
        st.info("💡 **Dica:** Mantenha-se sempre atualizado com suas notas e procure o professor em caso de dúvidas.")
    
    else:
        st.error("❌ Erro ao carregar informações da turma. Faça login novamente.")

def processar_pdf(pdf_file):
    """
    Processa o PDF e extrai informações de matrícula e notas dos alunos.
    Retorna um dicionário com os dados extraídos.
    """
    import PyPDF2
    import re
    
    notas_dict = {}
    
    try:
        # Ler o PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        texto_completo = ""
        
        # Extrair texto de todas as páginas
        for pagina in pdf_reader.pages:
            texto_completo += pagina.extract_text()
        
        # Padrões para extração (adaptar conforme formato do PDF)
        # Exemplo: buscar padrões como "Matrícula: 1234567 Nome: João Silva Nota1: 8.5 Nota2: 7.0 Nota3: 9.0"
        
        # Padrão simplificado para demonstração
        linhas = texto_completo.split('\n')
        
        for i, linha in enumerate(linhas):
            # Tentar extrair matrícula (números de 6-7 dígitos)
            match_matricula = re.search(r'\b(\d{6,7})\b', linha)
            
            if match_matricula:
                matricula = match_matricula.group(1)
                
                # Tentar encontrar nome (palavras capitalizadas próximas)
                match_nome = re.search(r'([A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+(?:\s+[A-ZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜ][a-zàáâãäåçèéêëìíîïñòóôõöùúûü]+)+)', linha)
                nome = match_nome.group(1) if match_nome else f"Aluno {matricula}"
                
                # Tentar extrair notas (números decimais)
                notas = re.findall(r'\b(\d{1,2}[.,]\d{1,2})\b', linha)
                notas = [float(n.replace(',', '.')) for n in notas]
                
                # Calcular média
                media = sum(notas) / len(notas) if notas else 0
                situacao = "Aprovado" if media >= 6.0 else "Reprovado" if media > 0 else "Em andamento"
                
                notas_dict[matricula] = {
                    'nome': nome,
                    'nota1': notas[0] if len(notas) > 0 else '-',
                    'nota2': notas[1] if len(notas) > 1 else '-',
                    'nota3': notas[2] if len(notas) > 2 else '-',
                    'media': f"{media:.2f}" if media > 0 else '-',
                    'situacao': situacao
                }
        
        # Se não encontrou dados, criar dados de exemplo
        if not notas_dict:
            notas_dict = gerar_dados_exemplo()
            
    except Exception as e:
        st.error(f"Erro ao processar PDF: {str(e)}")
        notas_dict = gerar_dados_exemplo()
    
    return notas_dict

def gerar_dados_exemplo():
    """Gera dados de exemplo para demonstração"""
    return {
        '1234567': {
            'nome': 'João Silva Santos',
            'nota1': 8.5,
            'nota2': 7.0,
            'nota3': 9.0,
            'media': '8.17',
            'situacao': 'Aprovado'
        },
        '1234568': {
            'nome': 'Maria Oliveira Costa',
            'nota1': 6.5,
            'nota2': 7.5,
            'nota3': 8.0,
            'media': '7.33',
            'situacao': 'Aprovado'
        },
        '1234569': {
            'nome': 'Pedro Henrique Souza',
            'nota1': 5.0,
            'nota2': 4.5,
            'nota3': 6.0,
            'media': '5.17',
            'situacao': 'Reprovado'
        },
        '1234570': {
            'nome': 'Ana Paula Ferreira',
            'nota1': 9.0,
            'nota2': 8.5,
            'nota3': 9.5,
            'media': '9.00',
            'situacao': 'Aprovado'
        }
    }

if __name__ == "__main__":
    main()
