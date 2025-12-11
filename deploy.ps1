# Script de Deploy para GitHub
# Execute este script após criar o repositório no GitHub

Write-Host "🚀 Deploy para GitHub e Streamlit Cloud" -ForegroundColor Cyan
Write-Host ""

# Solicitar URL do repositório
$repoUrl = Read-Host "Cole a URL do seu repositório GitHub (ex: https://github.com/usuario/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ URL não fornecida!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Configurando repositório remoto..." -ForegroundColor Yellow

# Remover origin existente se houver
git remote remove origin 2>$null

# Adicionar novo origin
git remote add origin $repoUrl

# Renomear branch para main
git branch -M main

Write-Host "✅ Repositório configurado!" -ForegroundColor Green
Write-Host ""
Write-Host "📤 Enviando código para GitHub..." -ForegroundColor Yellow

# Push para GitHub
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deploy concluído com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Próximos passos:" -ForegroundColor Cyan
    Write-Host "1. Acesse https://share.streamlit.io"
    Write-Host "2. Faça login com sua conta GitHub"
    Write-Host "3. Clique em 'New app'"
    Write-Host "4. Selecione seu repositório"
    Write-Host "5. Branch: main"
    Write-Host "6. Main file: Home.py"
    Write-Host "7. Clique em 'Deploy!'"
    Write-Host ""
    Write-Host "🌐 Seu app estará disponível em alguns minutos!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push!" -ForegroundColor Red
    Write-Host "Verifique se você tem permissão no repositório" -ForegroundColor Yellow
}
