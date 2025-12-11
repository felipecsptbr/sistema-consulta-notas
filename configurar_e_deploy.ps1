Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🚀 CONFIGURAR E ENVIAR PARA GITHUB - PASSO A PASSO" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Detectei que você é o usuário: " -NoNewline -ForegroundColor Yellow
Write-Host "felipecsptbr" -ForegroundColor Green
Write-Host ""

Write-Host "OPÇÕES:" -ForegroundColor White
Write-Host ""
Write-Host "1) Usar repositório existente" -ForegroundColor Cyan
Write-Host "2) Criar novo repositório" -ForegroundColor Cyan
Write-Host ""

$opcao = Read-Host "Escolha uma opção (1 ou 2)"

if ($opcao -eq "1") {
    Write-Host ""
    Write-Host "📝 Digite o nome do seu repositório existente:" -ForegroundColor Yellow
    Write-Host "   (apenas o nome, ex: sistema-notas)" -ForegroundColor Gray
    Write-Host ""
    $repoNome = Read-Host "Nome do repositório"
    
    if ([string]::IsNullOrWhiteSpace($repoNome)) {
        Write-Host ""
        Write-Host "❌ Nome inválido!" -ForegroundColor Red
        exit 1
    }
    
    $repoUrl = "https://github.com/felipecsptbr/$repoNome.git"
    
} elseif ($opcao -eq "2") {
    Write-Host ""
    Write-Host "📝 Vamos criar um novo repositório!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Sugestões de nome:" -ForegroundColor Gray
    Write-Host "  • sistema-consulta-notas" -ForegroundColor White
    Write-Host "  • sistema-notas-escolar" -ForegroundColor White
    Write-Host "  • consulta-notas-alunos" -ForegroundColor White
    Write-Host ""
    
    $repoNome = Read-Host "Digite o nome do novo repositório"
    
    if ([string]::IsNullOrWhiteSpace($repoNome)) {
        Write-Host ""
        Write-Host "❌ Nome inválido!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "🌐 Abrindo GitHub para você criar o repositório..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
    Start-Process "https://github.com/new?name=$repoNome&description=Sistema+de+Consulta+de+Notas+Acadêmicas"
    
    Write-Host ""
    Write-Host "📋 INSTRUÇÕES:" -ForegroundColor Cyan
    Write-Host "   1. Nome: $repoNome" -ForegroundColor White
    Write-Host "   2. Descrição: Sistema de Consulta de Notas Acadêmicas" -ForegroundColor White
    Write-Host "   3. Visibilidade: ☑️  Public" -ForegroundColor White
    Write-Host "   4. ❌ NÃO marque 'Add a README file'" -ForegroundColor Red
    Write-Host "   5. Clique em 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    Read-Host "Pressione ENTER depois de criar o repositório no GitHub"
    
    $repoUrl = "https://github.com/felipecsptbr/$repoNome.git"
    
} else {
    Write-Host ""
    Write-Host "❌ Opção inválida!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "  🔗 CONFIGURANDO REPOSITÓRIO" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

Write-Host "📦 URL do repositório: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Remover origin antigo e adicionar novo
git remote remove origin 2>$null
git remote add origin $repoUrl
git branch -M main

Write-Host "✅ Repositório configurado!" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "  📤 ENVIANDO CÓDIGO PARA GITHUB" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

Write-Host "⏳ Fazendo push..." -ForegroundColor Yellow
Write-Host ""

# Fazer push
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ SUCESSO! CÓDIGO ENVIADO PARA GITHUB                   ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Seu repositório: https://github.com/felipecsptbr/$repoNome" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host "  🚀 PRÓXIMO PASSO: DEPLOY NO STREAMLIT CLOUD" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Agora faça o deploy:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Acesse: https://share.streamlit.io" -ForegroundColor White
    Write-Host "2. Clique 'Deploy now' no card do GitHub" -ForegroundColor White
    Write-Host "3. Preencha:" -ForegroundColor White
    Write-Host "   • Repository: felipecsptbr/$repoNome" -ForegroundColor Cyan
    Write-Host "   • Branch: main" -ForegroundColor Cyan
    Write-Host "   • Main file: Home.py" -ForegroundColor Cyan
    Write-Host "4. Clique 'Deploy!'" -ForegroundColor White
    Write-Host ""
    
    $abrirStreamlit = Read-Host "Deseja abrir o Streamlit Cloud agora? (s/n)"
    
    if ($abrirStreamlit -eq "s" -or $abrirStreamlit -eq "S") {
        Start-Process "https://share.streamlit.io"
        Write-Host ""
        Write-Host "🌐 Streamlit Cloud aberto no navegador!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  📱 EM 2-3 MINUTOS SEU APP ESTARÁ ONLINE!" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "❌ ERRO ao fazer push!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "• Repositório não existe" -ForegroundColor White
    Write-Host "• Não tem permissão" -ForegroundColor White
    Write-Host "• Credenciais incorretas" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Tente autenticar com:" -ForegroundColor Yellow
    Write-Host "   gh auth login" -ForegroundColor White
    Write-Host ""
    Write-Host "Ou configure manualmente:" -ForegroundColor Yellow
    Write-Host "   git remote set-url origin https://github.com/felipecsptbr/$repoNome.git" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Read-Host "Pressione ENTER para sair"
