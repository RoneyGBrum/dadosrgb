# Como trocar o login (atrito) do painel público

O "login" das páginas em `painel_CGMOP/` é apenas **atrito** — NÃO é segurança real.
O `.html` é público: qualquer pessoa pode ver o código-fonte e baixar o arquivo direto
pela URL. O portão só desencoraja acesso casual.

## Credenciais atuais (padrão)
- usuário: `cgmop`
- senha: `mgi2026`

## Para trocar
1. Escolha novo usuário/senha.
2. Gere o hash SHA-256 de `usuario:senha` (ex.: no Python):

    python -c "import hashlib;print(hashlib.sha256('NOVOUSER:NOVASENHA'.encode()).hexdigest())"

3. Em CADA arquivo (`index.html`, `painel_publico.html`, `anistiados.html`), localize
   `var HASH_ESPERADO="..."` e troque pelo novo hash.
   (Ou edite USUARIO_PADRAO/SENHA_PADRAO em `pipeline/painel/publicar_cgmop.py` e rode de novo.)
4. Faça commit e push.

> Dica: para forçar novo login em quem já entrou, mude também o `KEY` (`cgmop_auth_v1`).
