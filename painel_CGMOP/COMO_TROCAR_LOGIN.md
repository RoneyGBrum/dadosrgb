# Como trocar o login (atrito) do painel público

O "login" das páginas em `painel_CGMOP/` é apenas **atrito** — NÃO é segurança real.
O `.html` é público: qualquer pessoa pode ver o código-fonte e baixar o arquivo direto
pela URL. O portão só desencoraja acesso casual.

Vários usuários são suportados: cada um tem seu próprio `usuário:senha`. As credenciais em
vigor NÃO ficam listadas aqui (este arquivo é público) — estão em
`pipeline/painel/publicar_cgmop.py` (dicionário `USUARIOS`) e no handoff interno do projeto.

## Jeito recomendado (regenera tudo automaticamente)
1. Abra `pipeline/painel/publicar_cgmop.py` e edite o dicionário `USUARIOS`:

       USUARIOS = {
           "cgmop": "nova-senha",       # trocar senha = mudar o valor
           "maria": "senha-da-maria",   # adicionar usuário = nova linha
           # "joao": "...",             # remover = apague a linha
       }

2. Rode:  `python painel/publicar_cgmop.py`  (reescreve as 3 páginas com a nova lista de hashes)
3. Publique:  `cd C:\0_Apresentacoes\dadosrgb && git add painel_CGMOP && git commit -m "atualiza login" && git push`

## Jeito manual (sem rodar o script)
1. Gere o hash de cada `usuario:senha`:

       python -c "import hashlib;print(hashlib.sha256('USUARIO:SENHA'.encode()).hexdigest())"

2. Nos arquivos COM login (`index.html`, `painel_movimentacoes.html`, `anistiados.html` —
   o `painel_publico.html` é ABERTO, não tem portão), localize `var HASHES=[...]` e coloque a
   lista de hashes desejada, ex.: `var HASHES=["hash1","hash2"];`
3. Faça commit e push.

> Lembrete: o login é só **atrito**. O `.html` é público e o dado está embutido nele — quem
> abrir o código-fonte vê tudo, com ou sem senha. Não use senha reutilizada/importante.
> Para forçar novo login em quem já entrou, mude também o `KEY` (`cgmop_auth_v1`).
