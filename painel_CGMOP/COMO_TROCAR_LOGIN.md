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

2. Rode:  `python painel/publicar_cgmop.py`  (reescreve TODAS as páginas com portão)
3. Publique:  `cd C:\0_Apresentacoes\dadosrgb && git add painel_CGMOP && git commit -m "atualiza login" && git push`

## Por que NÃO existe "jeito manual"
A receita manual que ficava aqui estava **errada em três pontos** (revisão de 02/09/2026) e
trancava os usuários para fora sem dar nenhum aviso:

- ensinava `hashlib.sha256("USUARIO:SENHA")`, mas o portão usa **PBKDF2-HMAC-SHA256** com sal e
  250 mil iterações — os dois produzem 64 caracteres hex, então o hash errado *parece* certo;
- listava **3** páginas com portão, quando são **8** (todas menos `painel_publico.html`), que
  compartilham a MESMA lista de hashes — editar 3 deixaria 5 aceitando a senha revogada;
- mandava mexer na chave de sessão `cgmop_auth_v1`, que hoje é `cgmop_auth_v2`.

Além disso, o portão **canoniza** a entrada (usuário em minúsculas; senha sem `/`, `.`, `-` e
espaços), o que um hash feito à mão também erraria. Use sempre o jeito recomendado acima — é
uma linha de comando e regenera tudo de forma consistente.

> Lembrete: o login é só **atrito**. O `.html` é público e o dado está embutido nele — quem
> abrir o código-fonte vê tudo, com ou sem senha. Não use senha reutilizada/importante.
> Para forçar novo login em quem já entrou, mude também o `KEY` (`cgmop_auth_v1`).
