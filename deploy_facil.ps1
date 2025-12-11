Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 DEPLOY RÁPIDO - STREAMLIT CLOUD                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar se há mudanças não commitadas
$status = git status --porcelain
if ($status) {
    Write-Host "📦 Adicionando arquivos novos..." -ForegroundColor Yellow
    git add .
    git commit -m "Atualização automática"
    Write-Host "✅ Commit realizado!" -ForegroundColor Green
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "PASSO 1: CONFIGURAR GITHUB" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

$temRepo = Read-Host "Você já criou um repositório no GitHub? (s/n)"

if ($temRepo -eq "n" -or $temRepo -eq "N") {
    Write-Host ""
    Write-Host "📝 Crie seu repositório agora:" -ForegroundColor Yellow
    Write-Host "   1. Acesse: https://github.com/new" -ForegroundColor White
    Write-Host "   2. Nome: sistema-consulta-notas" -ForegroundColor White
    Write-Host "   3. Visibilidade: Public" -ForegroundColor White
    Write-Host "   4. NÃO marque 'Add README'" -ForegroundColor Red
    Write-Host "   5. Clique 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    # Abrir GitHub automaticamente
    $abrirGithub = Read-Host "Deseja abrir o GitHub agora? (s/n)"
    if ($abrirGithub -eq "s" -or $abrirGithub -eq "S") {
        Start-Process "https://github.com/new"
        Write-Host ""
        Write-Host "⏳ Aguardando você criar o repositório..." -ForegroundColor Yellow
        Read-Host "Pressione ENTER depois de criar o repositório"
    }
}

Write-Host ""
$repoUrl = Read-Host "Cole a URL do seu repositório (ex: https://github.com/usuario/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host ""
    Write-Host "❌ URL inválida! Execute o script novamente." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔗 Configurando repositório remoto..." -ForegroundColor Yellow

git remote remove origin 2>$null
git remote add origin $repoUrl
git branch -M main

Write-Host "✅ Repositório configurado!" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "PASSO 2: ENVIAR CÓDIGO PARA GITHUB" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "📤 Fazendo push para GitHub..." -ForegroundColor Yellow

git push -u origin main 2>&1 | Out-String | Write-Host

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Código enviado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host "PASSO 3: DEPLOY NO STREAMLIT CLOUD" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Agora faça o deploy:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Acesse: https://share.streamlit.io" -ForegroundColor White
    Write-Host "2. Faça login com GitHub" -ForegroundColor White
    Write-Host "3. Clique em 'New app'" -ForegroundColor White
    Write-Host "4. Preencha:" -ForegroundColor White
    Write-Host "   • Repository: " -NoNewline -ForegroundColor White
    Write-Host "seu repositório" -ForegroundColor Cyan
    Write-Host "   • Branch: " -NoNewline -ForegroundColor White
    Write-Host "main" -ForegroundColor Cyan
    Write-Host "   • Main file: " -NoNewline -ForegroundColor White
    Write-Host "Home.py" -ForegroundColor Cyan
    Write-Host "5. Clique 'Deploy!'" -ForegroundColor White
    Write-Host ""
    
    $abrirStreamlit = Read-Host "Deseja abrir o Streamlit Cloud agora? (s/n)"
    if ($abrirStreamlit -eq "s" -or $abrirStreamlit -eq "S") {
        Start-Process "https://share.streamlit.io"
    }
    
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ DEPLOY CONCLUÍDO!                                        ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Seu app estará online em 2-3 minutos!" -ForegroundColor Cyan
    Write-Host "🌐 URL: https://seu-app.streamlit.app" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Primeira vez:" -ForegroundColor Yellow
    Write-Host "   1. Acesse o painel admin" -ForegroundColor White
    Write-Host "   2. Faça upload do PDF com notas" -ForegroundColor White
    Write-Host "   3. Os alunos podem consultar!" -ForegroundColor White
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "• Credenciais do GitHub incorretas" -ForegroundColor White
    Write-Host "• Repositório não existe ou URL errada" -ForegroundColor White
    Write-Host "• Sem permissão no repositório" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Tente:" -ForegroundColor Yellow
    Write-Host "   git config --global credential.helper manager" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
    Write-Host ""
}

Read-Host "Pressione ENTER para sair"
