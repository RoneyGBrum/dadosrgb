# Super Prompt — Ecossistema de Painéis CGMOP (dadosrgb.dev.br)

> Documento-mestre que organiza as ideias em pacotes executáveis, com prioridade,
> esforço, dependências e decisões em aberto. Serve como "super prompt": cada fase
> pode ser colada numa sessão para execução. Data-base: 24/08/2026.

Legenda: **P0** = base/bloqueante · **P1** = alto valor · **P2** = desejável ·
Esforço: **P** pequeno · **M** médio · **G** grande · 🔒 decisão necessária · 📊 depende de dado real.

> ⚠ **STATUS 26/08/2026 — PUBLICADO.** O ecossistema está no ar em `dadosrgb.dev.br/painel_CGMOP/`
> (hub + `painel_publico.html` sem proporcionalidade + `anistiados.html`), com login de atrito
> (credenciais fora do repo — ver `publicar_cgmop.py`/handoff). **Decisão do usuário sobrepôs o §1 abaixo:** foi publicado o dado **NOMINAL**
> (nome + CPF mascarado + remuneração individual) no GitHub público — e NÃO só a camada agregada
> que este plano recomendava. O login é só atrito, então a PII mascarada fica exposta/baixável.
> Alternativa futura, se reverter: S3 (`agregados_publico.json`, sem PII). Gerado por
> `pipeline/painel/gerar_painel_publico.py` + `publicar_cgmop.py`.

## ✅ Progresso (24/08/2026)
- **Decidido §1:** dados de nome + CPF mascarado + remuneração bruta são públicos (Portal da Transparência) → podem ir ao domínio; login fica como atrito. Evitar só campos realmente sensíveis (CPF completo, conta bancária).
- **Feito e validado (com dados sintéticos):** A1 competência via `da_referencia` · A3 matrículas origem/destino · A4 nota de transparência no temporal · B1 coluna Saldo/Vagas Ocupadas · B2 PDF mais legível · B3 recorte destacado + renome + ⓘ · C5 "Limpar" destacado · C6 filtros por tema · C8 ordem do Perfil Funcional · C9 UORG (sigla+nome / hierarquia) · C10 botão relatório à direita e com cor própria · C11 glossário de conceitos (17, do arquivo) · C12 animações (barras crescem, linha desenha L→R).
- **Pendente de diagnóstico (rode `tests/diagnostico_dados.py`):** A2 exclusão do GDF (códigos) · confirmação da coluna de competência.
- **Próximo batch:** C1–C4 (filtros: debounce/autocomplete/cascata/multi-seleção) · C7 (Movimentações recolhível sob Perfil Funcional) · C13/C14 (histórico: click-filter + encerramentos) · X1 (transparência nas exportações). Depois D/E/F.
- **Novos utilitários:** `pipeline/tests/gerar_saida_sintetica_painel.py` (valida o front-end sem dado real) e `pipeline/tests/diagnostico_dados.py`.

---

## 0. Contexto e restrições (ler primeiro)

- **Fonte de código:** `C:\0_Desenvolvimento\Movimentacao_pessoal\pipeline` (ETL + `painel/gerar_painel.py`).
- **Dados (sensíveis):** ficam em `PASTA_DADOS` (OneDrive), **fora do repositório**. O assistente **não acessa** essa pasta — mudanças que dependem de dado real são entregues como **código + comando**, e **você roda**. Validação de front-end é feita com **dados sintéticos** (`tests/gerar_dados_sinteticos.py`), sem tocar no dado real.
- **Ecossistema:** `C:\0_Apresentacoes\dadosrgb\` é um **GitHub Pages público** (domínio `dadosrgb.dev.br`). Já hospeda: `painel-anistiados`, `lip-estudo-licencas`, `movimentacao-pessoal`, `limites-reembolso`, `recruta-gov`, etc. O novo ecossistema vai em `painel_CGMOP/`.
- **Princípios de ciência comportamental** (valem para todo o ecossistema): facilitar; evitar reatância (convite, ações reversíveis); enquadramento (seções e contexto); compatibilidade estímulo-resposta (cores com significado — origem âmbar × destino verde); ancoragem/disponibilidade/representatividade (médias e totais em destaque, top-N realçado). **Resumo: se quiser encorajar algo, FACILITE.**

---

## 1. 🔒 DECISÃO CRÍTICA — segurança e onde cada painel é hospedado

GitHub Pages é **público e estático**. Duas verdades técnicas incontornáveis:

1. **Senha em HTML estático não protege dado.** Qualquer pessoa vê o código-fonte e baixa o arquivo direto pela URL. Um "login" em JS é só **atrito** (desencoraja acesso casual), nunca segurança real.
2. **Dado sensível embutido num arquivo público = vazamento.** Nome, CPF, remuneração individual num `.html` no GitHub ficam acessíveis a qualquer um, com ou sem "login".

Você já reconheceu isso para os anistiados ("não poderemos expor dados sensíveis pois o site ficará no github"). O mesmo vale para o painel de ativos completo e o histórico nominal.

**Arquitetura recomendada — duas camadas:**

| Camada | O que contém | Onde hospeda | "Login" |
|---|---|---|---|
| **Pública** (no domínio) | Só dados **agregados/anonimizados** (contagens, %, rankings por órgão; sem nome/CPF/remuneração individual) | GitHub Pages `dadosrgb.dev.br` | Atrito leve (opcional) |
| **Interna** (dado sensível) | Ficha nominal, CPF mascarado, remuneração individual, relação nominal completa | **Fora do GitHub**: pasta de rede/OneDrive/SharePoint da equipe (abre local), ou host com auth de verdade | Controle de acesso do host |

Consequência prática: o **painel_CGMOP completo** (ativos com ficha individual, anistiados com "quem são") é **interno** e roda a partir de `PASTA_DADOS`. A **cópia pública reduzida** (item F1) e versões agregadas dos temas vão para o domínio.

**Decisões que preciso de você (ver perguntas no fim):**
- (a) Confirmar o modelo de duas camadas? Ou insistir em tudo no domínio (exigiria host com backend/auth real — ex. Cloudflare Access/Netlify Identity — fora do "só HTML")?
- (b) Nível de anonimização aceitável na camada pública (ex.: sem nome; CPF mascarado; remuneração só em faixas/agregada por órgão?).
- (c) O "usuário/senha no HTML" fica só como atrito na camada pública — ok?

> Todo o resto do plano assume o **modelo de duas camadas**. Se você decidir diferente, ajusto as fases D/E.

---

## 2. Fases de execução (ordem recomendada)

Cada fase é fechada e verificável. As Fases A–C melhoram o **painel interno atual** (rápido, sem novas decisões). D–F são o **ecossistema** (dependem da decisão §1).

- **Fase A — Correções de dados/pipeline** (P0) → base correta para todos os painéis.
- **Fase B — Aba Proporcionalidade + Ficha PDF** (P1) → ganhos rápidos e visíveis.
- **Fase C — Filtros, layout, animações, histórico** (P1) → o grosso da UX.
- **Fase D — Fracionamento do ecossistema + auth de atrito** (P1, 🔒) → ativos / histórico / links / login.
- **Fase E — Painéis novos: Anistiados, Licenças, Redistribuição** (P1/P2, 🔒📊).
- **Fase F — Cópia pública reduzida + transparência de exportação** (P2) → por último, para espelhar o interno.

---

## 3. Backlog detalhado (cada ideia vira um item rastreável)

### Fase A — Correções de dados / pipeline  📊 (você roda)
- **A1 · Competência real** (P0, P) — `mes_referencia` deve vir da **data real da carga do fatoServidor** (coluna de `timestamp`/`da_referencia`/`da_carga`), não de `datetime.now()`. *Ação:* confirmar a coluna via `diagnostico_dados.py`; ajustar `enriquecimento`/`main`; propagar ao painel e ao rótulo "Competência".
- **A2 · Exclusão do GDF** (P0, M) — remover movimentações **internas ao GDF**: quando **origem E destino** ∈ {PMDF, GDF, PCDF, CBMDF} (códigos a confirmar no `dim_orgao`). **Manter** quando um deles é federal (ex.: PMDF→MGI) — aí usa-se o cadastro do GDF só para remuneração/cargo. *Regra:* excluir o movimento se ambas as pontas forem GDF-família. Constante nova `ORGAOS_GDF_EXCLUIR` em `config.py`.
- **A3 · Matrícula origem/destino** (P1, P) — expor `matricula_origem` e `matricula_destino` no `output_schema` e no detalhe do servidor.
- **A4 · Discrepância total × acumulado (histórico)** (P1, M) — o acumulado do gráfico temporal conta só movimentos **com data válida**; movimentos sem `data_ingresso_real` (sentinela) ficam de fora → total ≠ acumulado. *Ação:* quantificar e (i) exibir nota de transparência + (ii) considerar barra "sem data" ou reconciliar o KPI.

### Fase B — Proporcionalidade + Ficha PDF
- **B1 · Coluna "Saldo / Vagas Ocupadas"** (P1, P) — `saldo_por_ocupadas` (C/E) **já é calculado** em `saldo.py`; só falta **exibir** na tabela da aba e **no PDF**.
- **B2 · PDF da proporcionalidade — visual** (P1, M) — fontes maiores e mais escuras, cabeçalho com mais peso, zebra nas linhas, destaque de saldo (cor origem/destino), menos "apático". Legibilidade > densidade.
- **B3 · Recorte mais destacado + rótulo** (P1, P) — botões do toggle maiores/realçados; renomear **"Só as que contam (§7 art.93)" → "Só as que contam para a proporcionalidade"** (e um ⓘ com a regra).

### Fase C — Filtros, layout, animações, histórico
- **C1 · Filtros mais leves** (P0, M) — o gargalo é o filtro **"contém"** (varre 54k linhas por tecla). *Ação:* (i) **debounce**; (ii) trocar "contém" por **seleção com autocomplete** (datalist/multiselect) onde faz sentido; (iii) índices pré-computados por coluna; (iv) o **fracionamento** (Fase D) alivia o peso global.
- **C2 · Autocomplete em todos os filtros** (P1, M) — mostrar opções conforme digita (nem sempre se sabe o nome exato).
- **C3 · Filtros em cascata** (P1, G) — ao aplicar um filtro, os demais mostram **só valores compatíveis** (ex.: filtrou "MGI" → só UORGs/carreiras/UF do MGI). Recalcular domínios a partir do índice filtrado.
- **C4 · Multi-seleção por filtro** (P1, M) — permitir vários valores no mesmo filtro (OR interno).
- **C5 · "Limpar filtros" mais visível** (P1, P) — botão destacado e sempre à mão.
- **C6 · Filtros organizados por temas** (P1, P) — agrupar por proximidade (Servidor / Órgãos / Exercício / Cargo…), reduzindo carga cognitiva.
- **C7 · "Movimentações" vira seção recolhível sob "Perfil Funcional"** (P1, G) — deixa de ser aba; herda os **filtros globais do topo** (os que já existem no topo **não se repetem** aqui); mantém **filtros extras** + **seletor de colunas** com opção **"incluir todas as colunas do banco"**.
- **C8 · Perfil Funcional — reordenar** (P1, P) — ordem: **Possui função; Nível de liderança; Recebe rendimento; PGD**.
- **C9 · UORG com sigla + hierarquia** (P1, M) — sempre exibir **SIGLA + nome** (busca por qualquer um); quando só a sigla for usada, mostrar a **hierarquia** (ex.: MGI/SGP/DEPRO/CGMOP).
- **C10 · Botão "Gerar relatório" diferenciado** (P1, P) — cor distinta do "quantitativo total" **ou** movê-lo para a direita.
- **C11 · Conceitos dos tipos de movimentação** (P1, M) — trazer as definições de `CONCEITOS SITUAÇÕES FUNCIONAIS.xlsx` num ⓘ discreto/elegante (popover) perto de "Tipos de movimentação" e da situação no detalhe.
- **C12 · Animações de entrada** (P2, M) — barras "crescendo" no load e ao filtrar; linha do temporal **desenhando da esquerda p/ direita**. Respeitar `prefers-reduced-motion`.
- **C13 · Histórico — click-to-filter** (P1, M) — hoje o recorte histórico é estático; permitir clicar nos gráficos para filtrar (exige computar o histórico no navegador ou um índice do histórico).
- **C14 · Histórico — gráfico de ENCERRAMENTOS** (P1, M) — espelho do "novas por ano": **acumulado de encerramentos** (área/linha) + **barras por ano** (via `data_saida`).

### Detalhe do servidor
- **F-det1 · Ficha PDF — visual motivador** (P1, M) — sair do "apático": tipografia com hierarquia, cabeçalho institucional com cor, blocos com respiro, destaque dos campos-chave. (junto de A3 · matrículas.)

### Exportações (todas)
- **X1 · Transparência nas exportações** (P1, P) — XLSX/PDF carregam um cabeçalho com **parâmetros de extração, busca e filtros aplicados** e data de geração.

### Fase D — Ecossistema (🔒 depende de §1)
- **D1 · Fracionar** (P1, G) — `painel_CGMOP/` como hub com páginas integradas: **Ativos (completo)** ↔ **Histórico (leve: relação nominal + dados básicos)** ↔ **Anistiados**. Links cruzados no topo (ativos↔inativos↔anistiados).
- **D2 · Auth de atrito** (P1, M, 🔒) — usuário/senha só como atrito, **apenas na camada pública/anonimizada** (ver §1). Idealmente dentro do HTML (hash de senha no JS; não é segurança real — deixar isso explícito).
- **D3 · Histórico leve** (P1, M) — 216k linhas: embutir só o essencial (relação nominal + campos básicos) e/ou agregados; evitar o peso do painel completo.

### Fase E — Painéis novos (🔒📊)
- **E1 · Anistiados** (P1, G) — público: `anistiados = carreira 180 OU situação 43 OU ocorrência de ingresso ∈ {01119, 01074, 01183}`. **Ficha funcional COMPLETA** (não é sobre movimentação): quantos, quem, de onde vieram, remuneração detalhada, por onde passaram, quando voltaram, onde estão hoje, órgãos de reforma, ativo/excluído, cargo/carreira/classe, tempo de retorno. **PDF + XLSX** com colunas escolhidas. **Muito didático** (público leigo). ⚠️ conflito: "quem são" + ficha individual **vs.** "sem dado sensível no GitHub" → decidir masking (fica interno? ou anonimiza?).
- **E2 · Licença Afastamento Internacional** (P2, M) — inspirar em `lip-estudo-licencas`.
- **E3 · Licença Capacitação** (P2, M) — idem.
- **E4 · Redistribuição** (P2, M) — menos importante; hoje o módulo está desativado no ETL.

### Fase F — Público + fechamento
- **F1 · Cópia pública reduzida** (P2, M) — **por último**, espelho do interno mas só com **movimentação ativa + histórico** (agregados), **sem proporcionalidade nem outros temas**. Idêntica visualmente, menos informação, **sem dado sensível**.

---

## 4. Sugestões minhas (extra)

- **S1 · Base compartilhada** — extrair CSS/JS comuns (tema, filtros, gráficos, export) para um `assets/comum.js`+`comum.css` reutilizados por todos os painéis do ecossistema (menos duplicação, visual consistente). Como GitHub Pages serve arquivos, dá para não ser "autocontido" e compartilhar assets — reduz tamanho total.
- **S2 · Formato de dados mais leve** — para painéis grandes, trocar CSV embutido por **JSON colunar comprimido** (ou dados já agregados no build) → arquivos menores e parse mais rápido. Combina com C1.
- **S3 · Camada pública = só agregados no build** — gerar no pipeline um `agregados_publico.json` (sem PII) que alimenta a camada pública; o sensível nunca sai do build interno.
- **S4 · Índice/hub do ecossistema** — uma home `painel_CGMOP/index.html` com cartões para cada painel (Ativos, Histórico, Anistiados, Licenças…), no padrão da home do `dadosrgb`.
- **S5 · Acessibilidade** — contraste AA, navegação por teclado, `prefers-reduced-motion` (casa com C12), rótulos ARIA nos filtros.
- **S6 · Rodapé de proveniência** — em cada painel: competência, data de geração, fonte (SIAPE/Data Lake), aviso de uso interno — reforça confiança (disponibilidade/ancoragem).
- **S7 · Versionamento** — como está em git, marcar cada publicação com um `label`/commit para rastrear o que foi ao ar.

---

## 5. Perguntas em aberto (bloqueiam D/E/F)

1. **Segurança/hospedagem (§1):** modelo de duas camadas (interno sensível fora do GitHub + público agregado no domínio)? Ou tudo no domínio com auth real (muda hospedagem)?
2. **Anonimização pública:** o que pode aparecer na camada pública — sem nome? CPF mascarado? remuneração só agregada/faixas?
3. **Anistiados (E1):** a ficha individual fica **interna** (com dado real) e só uma versão **agregada** vai ao público? Ou anonimizamos a individual o suficiente para publicar?
4. **Schema (rodar `diagnostico_dados.py`):** qual coluna de competência existe no fatoServidor? Quais os códigos exatos de PMDF/GDF/PCDF/CBMDF? Os campos de anistiados (carreira 180 / situação 43 / ocorrências) batem? Onde ficam as **definições** de conceito no `CONCEITOS SITUAÇÕES FUNCIONAIS.xlsx`?
5. **Ordem:** começo pela **Fase A+B+C** (painel interno, sem novas decisões) enquanto você decide §1? (recomendo que sim.)

---

## 6. O que já dá para começar sem esperar (proposta)

Fases **A, B e C** não dependem da decisão de segurança e são o maior volume de valor no painel que você já usa. Posso executá-las validando o front-end com **dados sintéticos** (sem tocar no dado real), e te entrego os comandos para rodar o pipeline/painel com o dado verdadeiro. As Fases **D/E/F** entram assim que §1 estiver decidido.
