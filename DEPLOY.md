# 🚀 Guia de Deploy - Streamlit Cloud

## Passo 1: Preparar o Repositório GitHub

1. **Criar repositório no GitHub:**
   - Acesse https://github.com/new
   - Nome: `sistema-consulta-notas`
   - Descrição: `Sistema de Consulta de Notas Acadêmicas`
   - Visibilidade: Public ou Private
   - Clique em "Create repository"

2. **Fazer push do código:**
   ```bash
   cd C:\xampp\htdocs\systemnotas
   git init
   git add .
   git commit -m "Deploy inicial do Sistema de Notas"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/sistema-consulta-notas.git
   git push -u origin main
   ```

## Passo 2: Deploy no Streamlit Cloud

1. **Acessar Streamlit Cloud:**
   - Acesse https://share.streamlit.io
   - Faça login com sua conta GitHub

2. **Criar novo app:**
   - Clique em "New app"
   - Selecione o repositório: `sistema-consulta-notas`
   - Branch: `main`
   - Main file path: `Home.py`
   - Clique em "Deploy!"

3. **Aguardar deploy:**
   - O Streamlit Cloud instalará as dependências
   - O app estará disponível em: `https://SEU-APP.streamlit.app`

## 📁 Estrutura Necessária

```
sistema-consulta-notas/
├── Home.py                  # Página inicial (OBRIGATÓRIO)
├── pages/
│   ├── app_simples.py      # Consulta de alunos
│   └── admin_web.py        # Painel administrativo
├── database.py             # Gerenciamento do banco
├── utils.py                # Utilitários
├── requirements.txt        # Dependências
├── .streamlit/
│   └── config.toml         # Configurações
└── README.md              # Documentação
```

## ⚙️ Arquivos Importantes

### requirements.txt
```
streamlit>=1.39.0
PyPDF2>=3.0.1
Pillow>=10.4.0
pandas>=2.0.0
```

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
port = 8501
```

## 🗄️ Banco de Dados

O SQLite criará automaticamente o arquivo `sistema_notas.db` na primeira execução.

**Nota:** No Streamlit Cloud, o banco de dados é volátil e será resetado a cada redeploy. Para produção, considere usar um banco em nuvem.

## 🔐 Variáveis de Ambiente (Opcional)

Se precisar de senhas ou chaves:

1. No Streamlit Cloud, vá em "Settings"
2. Clique em "Secrets"
3. Adicione suas variáveis:
   ```toml
   admin_password = "sua_senha_aqui"
   ```

4. No código:
   ```python
   import streamlit as st
   senha = st.secrets["admin_password"]
   ```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
- Verifique se o módulo está no `requirements.txt`
- Adicione a versão correta

### Erro: "Database is locked"
- Use `check_same_thread=False` no SQLite
- Considere usar PostgreSQL

### App não carrega
- Verifique os logs no Streamlit Cloud
- Teste localmente: `streamlit run Home.py`

## 📱 URLs do Sistema

Após o deploy:
- **Home:** `https://seu-app.streamlit.app`
- **Consulta Aluno:** `https://seu-app.streamlit.app/app_simples`
- **Admin:** `https://seu-app.streamlit.app/admin_web`

## 🔄 Atualizar o App

Para atualizar após mudanças:
```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

O Streamlit Cloud fará redeploy automaticamente!

## 📞 Suporte

- Documentação: https://docs.streamlit.io
- Comunidade: https://discuss.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues

---

**✅ Pronto!** Seu sistema estará online e acessível de qualquer lugar!
