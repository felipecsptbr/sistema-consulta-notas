# 🔒 SEGURANÇA E PRIVACIDADE DE DADOS

## ⚠️ IMPORTANTE - PROTEÇÃO DE DADOS PESSOAIS

Este sistema lida com dados sensíveis de alunos (nomes, matrículas, notas). 
É fundamental garantir a segurança e privacidade dessas informações.

## ✅ O que está protegido (não vai para o GitHub):

### Arquivos bloqueados no .gitignore:
- ✅ `*.db` - Banco de dados SQLite
- ✅ `*.pdf` - PDFs com notas dos alunos
- ✅ `*.csv` - Exportações de dados
- ✅ `exemplo_notas.txt` - Exemplos com dados reais

## 🛡️ Medidas de Segurança Implementadas:

### 1. Banco de Dados
- SQLite local (não enviado ao GitHub)
- Dados são voláteis no Streamlit Cloud
- Recriado a cada deploy (não persiste dados sensíveis)

### 2. Arquivos de Upload
- PDFs não são commitados
- Apenas processados em memória
- Não ficam armazenados permanentemente

### 3. .gitignore Configurado
```
*.db
*.sqlite
*.pdf
*.csv
exemplo_notas.txt
```

## 🚨 NUNCA faça:

❌ `git add *.db`
❌ `git add *.pdf`
❌ Commitar arquivos com dados reais de alunos
❌ Compartilhar o banco de dados em repositórios públicos
❌ Fazer hardcode de senhas no código

## ✅ Boas Práticas:

### Para Desenvolvimento Local:
```bash
# Sempre verifique o que vai commitar
git status

# Verifique o .gitignore antes de add
cat .gitignore

# Não use git add . sem verificar
git add arquivo_especifico.py
```

### Para Produção (Streamlit Cloud):

1. **Dados são temporários**
   - O banco SQLite é recriado a cada deploy
   - Dados não persistem entre redeployments
   - Considere usar PostgreSQL/MySQL em nuvem para produção

2. **Senhas e Credenciais**
   - Use Streamlit Secrets para senhas
   - Acesse: Settings → Secrets no painel do app
   ```toml
   # .streamlit/secrets.toml (NÃO commitar!)
   admin_password = "senha_segura"
   ```

3. **LGPD/GDPR Compliance**
   - Informe aos usuários sobre coleta de dados
   - Implemente política de privacidade
   - Permita exclusão de dados
   - Não compartilhe dados sem consentimento

## 🔍 Como verificar se dados vazaram:

### Verificar histórico do Git:
```bash
# Ver todos os arquivos já commitados
git log --all --full-history -- "*.db"
git log --all --full-history -- "*.pdf"

# Se encontrar algo, remover do histórico:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch sistema_notas.db" \
  --prune-empty --tag-name-filter cat -- --all
```

### Verificar repositório GitHub:
1. Acesse: https://github.com/felipecsptbr/sistema-consulta-notas
2. Procure por arquivos .db, .pdf, .csv
3. Se encontrar, delete e force push

## 📋 Checklist de Segurança:

Antes de cada commit, verifique:

- [ ] `git status` não mostra arquivos .db
- [ ] `git status` não mostra arquivos .pdf
- [ ] `git status` não mostra arquivos .csv
- [ ] .gitignore está atualizado
- [ ] Nenhuma senha no código
- [ ] Nenhum dado pessoal hardcoded

## 🆘 Em caso de vazamento acidental:

1. **Remover arquivo imediatamente:**
   ```bash
   git rm --cached arquivo_sensivel.db
   git commit -m "Remove arquivo sensível"
   git push
   ```

2. **Limpar histórico:**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch arquivo_sensivel.db" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```

3. **Considerar o repositório comprometido**
   - Trocar todas as senhas
   - Notificar usuários afetados
   - Avaliar impacto LGPD

## 📞 Suporte e Dúvidas:

Para questões de segurança críticas:
- Nunca exponha dados em issues públicas
- Contate os mantenedores diretamente
- Relate vulnerabilidades de forma responsável

## 📚 Referências:

- [LGPD - Lei Geral de Proteção de Dados](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security/getting-started/best-practices-for-preventing-data-leaks-in-your-organization)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

**⚠️ LEMBRE-SE:** Dados de alunos são informações sensíveis protegidas por lei!
