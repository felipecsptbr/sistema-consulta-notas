"""
Módulo de gerenciamento de banco de dados SQLite
"""
import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "sistema_notas.db"

def init_db():
    """Inicializa o banco de dados e cria as tabelas necessárias"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela de usuários administradores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de turmas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            periodo TEXT,
            arquivo TEXT,
            data_upload TIMESTAMP,
            total_alunos INTEGER DEFAULT 0
        )
    """)
    
    # Tabela de alunos e notas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
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
        )
    """)
    
    # Inserir usuários admin padrão se não existirem
    try:
        cursor.execute("INSERT INTO usuarios_admin (username, senha) VALUES (?, ?)", 
                      ('admin', 'admin123'))
        cursor.execute("INSERT INTO usuarios_admin (username, senha) VALUES (?, ?)", 
                      ('professor', 'prof123'))
    except sqlite3.IntegrityError:
        pass  # Usuários já existem
    
    conn.commit()
    conn.close()

def verificar_login_admin(username, senha):
    """Verifica credenciais de administrador"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username FROM usuarios_admin 
        WHERE username = ? AND senha = ?
    """, (username, senha))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado is not None

def cadastrar_turma(nome, periodo, arquivo, notas_dict):
    """Cadastra uma nova turma e suas notas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Inserir turma
        cursor.execute("""
            INSERT INTO turmas (nome, periodo, arquivo, data_upload, total_alunos)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, periodo, arquivo, datetime.now().strftime("%d/%m/%Y %H:%M"), len(notas_dict)))
        
        turma_id = cursor.lastrowid
        
        # Inserir notas dos alunos
        for matricula, dados in notas_dict.items():
            nota1 = dados.get('nota1') if dados.get('nota1') != '-' else None
            nota2 = dados.get('nota2') if dados.get('nota2') != '-' else None
            nota3 = dados.get('nota3') if dados.get('nota3') != '-' else None
            media = float(dados.get('media')) if dados.get('media') != '-' else None
            
            cursor.execute("""
                INSERT INTO notas (turma_id, matricula, nome, nota1, nota2, nota3, media, situacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (turma_id, matricula, dados['nome'], nota1, nota2, nota3, media, dados['situacao']))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def listar_turmas():
    """Lista todas as turmas cadastradas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nome, periodo, arquivo, data_upload, total_alunos
        FROM turmas
        ORDER BY data_upload DESC
    """)
    
    turmas = {}
    for row in cursor.fetchall():
        turmas[row[1]] = {  # row[1] é o nome da turma
            'id': row[0],
            'periodo': row[2],
            'arquivo': row[3],
            'data_upload': row[4],
            'total_alunos': row[5]
        }
    
    conn.close()
    return turmas

def obter_notas_turma(nome_turma):
    """Obtém todas as notas de uma turma específica"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Primeiro, obter o ID da turma
    cursor.execute("SELECT id FROM turmas WHERE nome = ?", (nome_turma,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conn.close()
        return {}
    
    turma_id = resultado[0]
    
    # Obter notas dos alunos
    cursor.execute("""
        SELECT matricula, nome, nota1, nota2, nota3, media, situacao
        FROM notas
        WHERE turma_id = ?
    """, (turma_id,))
    
    notas_dict = {}
    for row in cursor.fetchall():
        matricula = row[0]
        notas_dict[matricula] = {
            'nome': row[1],
            'nota1': row[2] if row[2] is not None else '-',
            'nota2': row[3] if row[3] is not None else '-',
            'nota3': row[4] if row[4] is not None else '-',
            'media': f"{row[5]:.2f}" if row[5] is not None else '-',
            'situacao': row[6]
        }
    
    conn.close()
    return notas_dict

def remover_turma(nome_turma):
    """Remove uma turma e todas as suas notas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Obter ID da turma
        cursor.execute("SELECT id FROM turmas WHERE nome = ?", (nome_turma,))
        resultado = cursor.fetchone()
        
        if resultado:
            turma_id = resultado[0]
            
            # Remover notas associadas
            cursor.execute("DELETE FROM notas WHERE turma_id = ?", (turma_id,))
            
            # Remover turma
            cursor.execute("DELETE FROM turmas WHERE id = ?", (turma_id,))
            
            conn.commit()
            return True
        return False
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def verificar_aluno(nome_turma, matricula):
    """Verifica se um aluno existe em uma turma específica e retorna seus dados completos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.nome, n.matricula, n.nota1, n.nota2, n.nota3, n.media, n.situacao
        FROM notas n
        JOIN turmas t ON n.turma_id = t.id
        WHERE t.nome = ? AND n.matricula = ?
    """, (nome_turma, matricula))
    
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return {
            'nome': resultado[0],
            'matricula': resultado[1],
            'nota1': resultado[2],
            'nota2': resultado[3],
            'nota3': resultado[4],
            'media': resultado[5],
            'situacao': resultado[6]
        }
    return None

def adicionar_usuario_admin(username, senha):
    """Adiciona um novo usuário administrador"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO usuarios_admin (username, senha)
            VALUES (?, ?)
        """, (username, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def listar_usuarios_admin():
    """Lista todos os usuários administradores"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, data_criacao
        FROM usuarios_admin
        ORDER BY data_criacao DESC
    """)
    
    usuarios = {}
    for row in cursor.fetchall():
        usuarios[row[0]] = {
            'data_criacao': row[1]
        }
    
    conn.close()
    return usuarios
