/* ═══════════════════════════════════════════════════════════════════════════
   O LINK DO NOTEBOOK: troque só a linha abaixo.
   Deixe as aspas vazias ("") para esconder o botão.
   ═══════════════════════════════════════════════════════════════════════════ */
const LINK_NOTEBOOK = "https://notebook.google.com/notebook/8da91464-bb89-46d1-b1bc-330ea66f7fbf";


/* ───────────────────────────────────────────────────────────────────────────
   O botão «Pergunte ao manual», no canto inferior direito. Ele abre uma
   telinha que explica o assistente e leva ao notebook do Gemini numa nova aba.
   O notebook não pode ser embutido na página (o Google não deixa), por isso o
   link. Se este arquivo faltar, o manual funciona igual, só sem o botão.
   ─────────────────────────────────────────────────────────────────────────── */
(() => {
  if (!LINK_NOTEBOOK) return;

  const EXEMPLOS = [
    'Como eu encontro pesquisadores de uma área no Prospecta?',
    'O que significa a maturidade tecnológica (TRL) no painel?',
    'Como a nota de cada dimensão é calculada?',
  ];

  const css = document.createElement('style');
  css.textContent = `
.nb-botao{position:fixed;right:20px;bottom:20px;z-index:150;display:flex;align-items:center;gap:8px;
  background:var(--azul);color:#fff;border:none;border-radius:99px;padding:11px 17px 11px 14px;
  font:inherit;font-size:13.5px;font-weight:600;cursor:pointer;box-shadow:var(--sombra-g);
  transition:transform .18s,box-shadow .18s}
.nb-botao:hover{transform:translateY(-2px)}
.nb-botao:focus-visible,.nb-fechar:focus-visible,.nb-abrir:focus-visible,.nb-ex button:focus-visible{
  outline:2px solid var(--cobre);outline-offset:2px}
.nb-botao svg{width:18px;height:18px;flex:none}
[data-tema="escuro"] .nb-botao{color:#0D0F12}
.nb-painel{position:fixed;right:20px;bottom:76px;z-index:150;width:360px;max-width:calc(100vw - 32px);
  max-height:calc(100vh - 110px);overflow:auto;background:var(--bg);color:var(--tinta);
  border:1px solid var(--linha);border-radius:var(--raio);box-shadow:var(--sombra-g);
  padding:18px 18px 16px;font-size:14px;line-height:1.55}
.nb-painel[hidden]{display:none}
.nb-cab{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}
.nb-cab strong{font-size:15.5px;letter-spacing:-.01em}
.nb-fechar{background:transparent;border:none;color:var(--tinta-3);font:inherit;font-size:18px;
  line-height:1;padding:4px 6px;border-radius:6px;cursor:pointer}
.nb-fechar:hover{color:var(--tinta);background:var(--bg-3)}
.nb-painel p{margin:0 0 10px;color:var(--tinta-2)}
.nb-aviso{background:var(--cobre-claro);border-left:3px solid var(--cobre);border-radius:6px;
  padding:9px 11px;margin:0 0 12px;font-size:13px;color:var(--tinta)}
.nb-abrir{display:block;text-align:center;background:var(--azul);color:#fff;text-decoration:none;
  border-radius:9px;padding:10px 14px;font-weight:600;margin:0 0 12px}
.nb-abrir:hover{filter:brightness(1.08)}
[data-tema="escuro"] .nb-abrir{color:#0D0F12}
.nb-rot{font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
  color:var(--tinta-3);margin:0 0 6px}
.nb-ex{list-style:none;margin:0;padding:0}
.nb-ex li{margin:0 0 5px}
.nb-ex button{width:100%;text-align:left;background:var(--bg-2);border:1px solid var(--linha);
  color:var(--tinta-2);border-radius:8px;padding:7px 10px;font:inherit;font-size:13px;cursor:pointer}
.nb-ex button:hover{border-color:var(--azul);color:var(--tinta)}
.nb-copiado{font-size:12px;color:var(--verde);min-height:18px;margin:4px 0 0}
@media (max-width:620px){
  .nb-botao{right:16px;bottom:16px;padding:10px 14px 10px 12px;font-size:13px}
  .nb-painel{right:16px;bottom:68px}
}
@media print{.nb-botao,.nb-painel{display:none!important}}
`;
  document.head.appendChild(css);

  const ICONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>' +
    '<path d="M9.5 9.5a2.5 2.5 0 1 1 3.3 2.4c-.5.2-.8.6-.8 1.1v.5"/><path d="M12 16.5h.01"/></svg>';

  const botao = document.createElement('button');
  botao.type = 'button';
  botao.className = 'nb-botao';
  botao.setAttribute('aria-expanded', 'false');
  botao.setAttribute('aria-controls', 'nb-painel');
  botao.innerHTML = ICONE + '<span>Pergunte ao manual</span>';

  const painel = document.createElement('div');
  painel.id = 'nb-painel';
  painel.className = 'nb-painel';
  painel.hidden = true;
  painel.setAttribute('role', 'dialog');
  painel.setAttribute('aria-labelledby', 'nb-titulo');
  painel.innerHTML = `
<div class="nb-cab"><strong id="nb-titulo">Pergunte ao manual</strong>
  <button type="button" class="nb-fechar" aria-label="Fechar">✕</button></div>
<p>Um assistente com IA responde dúvidas sobre o Pipeline Lattes e o Prospecta, com base
  neste manual, nos guias e no código do projeto. Ele abre no <strong>Gemini</strong>, do
  Google, numa nova aba, e pode pedir que você entre numa conta Google.</p>
<div class="nb-aviso"><strong>As respostas são geradas por IA.</strong> Confira no manual antes
  de agir. Não cole dado pessoal: CPF, data de nascimento, contato ou trechos de currículo.</div>
<a class="nb-abrir" target="_blank" rel="noopener noreferrer">Abrir o assistente ↗</a>
<div class="nb-rot">Para começar, copie uma pergunta</div>
<ul class="nb-ex"></ul>
<div class="nb-copiado" aria-live="polite"></div>`;
  painel.querySelector('.nb-abrir').href = LINK_NOTEBOOK;

  const aviso = painel.querySelector('.nb-copiado');
  const lista = painel.querySelector('.nb-ex');
  EXEMPLOS.forEach(texto => {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = texto;
    b.onclick = async () => {
      try {
        await navigator.clipboard.writeText(texto);
        aviso.textContent = 'Copiada. Abra o assistente e cole no campo de pergunta.';
      } catch (_) {
        aviso.textContent = 'Não deu para copiar. Selecione o texto e copie com Ctrl+C.';
      }
    };
    li.appendChild(b);
    lista.appendChild(li);
  });

  const abrir = () => {
    painel.hidden = false;
    botao.setAttribute('aria-expanded', 'true');
    painel.querySelector('.nb-abrir').focus();
  };
  const fechar = (devolverFoco = true) => {
    if (painel.hidden) return;
    painel.hidden = true;
    aviso.textContent = '';
    botao.setAttribute('aria-expanded', 'false');
    if (devolverFoco) botao.focus();
  };

  botao.onclick = () => (painel.hidden ? abrir() : fechar());
  painel.querySelector('.nb-fechar').onclick = () => fechar();
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !painel.hidden) fechar();
  });
  document.addEventListener('click', e => {
    if (!painel.hidden && !painel.contains(e.target) && !botao.contains(e.target)) fechar(false);
  });

  document.body.appendChild(painel);
  document.body.appendChild(botao);
})();
