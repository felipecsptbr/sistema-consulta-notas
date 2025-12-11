# Sistema de Consulta de Notas

Sistema web desenvolvido com Python e Streamlit para consulta de notas acadêmicas.

## 🗄️ Banco de Dados

O sistema utiliza **SQLite** para persistência de dados:

- **Arquivo:** `sistema_notas.db`
- **Tabelas:**
  - `usuarios_admin` - Credenciais dos professores/administradores
  - `turmas` - Informações das turmas cadastradas
  - `notas` - Notas dos alunos por turma

### Estrutura do Banco:

```sql
-- Tabela de usuários administradores
CREATE TABLE usuarios_admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de turmas
CREATE TABLE turmas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    periodo TEXT,
    arquivo TEXT,
    data_upload TIMESTAMP,
    total_alunos INTEGER DEFAULT 0
);

-- Tabela de notas
CREATE TABLE notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    turma_id INTEGER NOT NULL,
    matricula TEXT NOT NULL,
    nome TEXT NOT NULL,
    nota1 REAL,
    nota2 REAL,
    nota3 REAL,
    media REAL,
    situacao TEXT,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE CASCADE,
    UNIQUE(turma_id, matricula)
);
```

## 📋 Funcionalidades

### Administrador
- ✅ Upload de arquivos PDF contendo notas dos alunos
- ✅ Cadastro de turmas e períodos
- ✅ Visualização de turmas cadastradas
- ✅ Gerenciamento de dados (adicionar/remover turmas)

### Aluno
- ✅ Consulta de notas por matrícula
- ✅ Visualização de notas individuais (Nota 1, Nota 2, Nota 3)
- ✅ Cálculo automático de média
- ✅ Visualização da situação (Aprovado/Reprovado)

## 🚀 Instalação

1. Clone ou baixe o projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Executar o Sistema

Execute o comando:
```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

## 👥 Acesso

### Administrador
- Selecione "Administrador" na tela inicial
- Senha padrão: `admin123`

### Aluno
- Selecione "Aluno" na tela inicial
- Digite sua matrícula na tela de consulta

## 📄 Formato do PDF

O sistema tenta extrair automaticamente os dados do PDF. Para melhor compatibilidade, o PDF deve conter:
- Matrícula do aluno (6-7 dígitos)
- Nome do aluno
- Notas (formato decimal)

Exemplo de linha no PDF:
```
Matrícula: 1234567 Nome: João Silva Nota1: 8.5 Nota2: 7.0 Nota3: 9.0
```

## 🔧 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework web
- **PyPDF2** - Leitura de arquivos PDF
- **SQLite** - Banco de dados local
- **Pandas** - Manipulação de dados
- **Pillow** - Manipulação de imagens

## 📝 Observações

- O sistema utiliza **SQLite** para persistência de dados
- Os dados são salvos no arquivo `sistema_notas.db`
- **Backup:** Faça cópias regulares do arquivo `.db`
- As credenciais padrão são criadas automaticamente na primeira execução

## 🎨 Customização

Você pode modificar:
- Senha do administrador no arquivo `app.py` (variável na função `show_login_page`)
- Critério de aprovação (média >= 6.0)
- Layout e cores do sistema
- Padrões de extração do PDF na função `processar_pdf`

## 📧 Suporte

Para dúvidas ou sugestões, entre em contato com o administrador do sistema.
