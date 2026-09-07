/* dadosrgb — catálogo de projetos.
   Esta é a ÚNICA fonte de verdade do índice. O index.html lê este arquivo.
   Para adicionar/editar um link, use o assistente: dadosrgb.dev.br/curadoria/
   (Editar cartão à mão no index.html é inútil: a próxima exportação sobrescreve.)
   cor: 1..5 → var(--c1)..var(--c5). A ORDEM DO ARRAY é a ordem na tela. */
window.CATALOGO = {
  "versao": 1,
  "atualizadoEm": "2026-09-05",
  "colecoes": [
    {
      "id": "movimentacao-cgmop",
      "cor": 1,
      "titulo": "Movimentação e força de trabalho — CGMOP",
      "descricao": "Os painéis interativos e os estudos de mobilidade de servidores federais.",
      "oculta": false,
      "projetos": [
        {
          "id": "painel-cgmop",
          "titulo": "Painel de Movimentação de Pessoal — CGMOP",
          "descricao": "Ecossistema com Movimentações (vigentes e histórico completo, versões pública e restrita) e Anistiados: cessões, requisições, força de trabalho e reforma administrativa — gráficos, evolução no tempo, proporcionalidade e a relação nominal completa.",
          "href": "./painel_CGMOP/",
          "etiqueta": "Painel · acesso restrito",
          "acao": "Abrir ecossistema",
          "destaque": true,
          "selo": "Principal",
          "externo": false,
          "oculto": false
        },
        {
          "id": "cgmop-manual",
          "titulo": "Manual do Ecossistema CGMOP",
          "descricao": "Documentação completa do pipeline e dos painéis: o que o sistema faz, como rodar, o que cada número significa, a base legal de cada painel e o que fazer quando algo dá errado. Inclui os números da última rodada, atualizados a cada geração.",
          "href": "./painel_CGMOP/manual.html",
          "etiqueta": "Documentação · acesso restrito",
          "acao": "Ler manual",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "painel-publico",
          "titulo": "Painel público de Movimentações",
          "descricao": "A versão aberta do painel de Movimentações — vigentes e histórico, gráficos e a relação nominal, sem os dados individuais sensíveis. Acesso direto, sem senha.",
          "href": "./painel_CGMOP/painel_publico.html",
          "etiqueta": "Aberto · sem login",
          "acao": "Abrir",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "movimentacao-pessoal",
          "titulo": "Movimentação de Pessoal",
          "descricao": "A transformação da mobilidade na Administração Pública Federal. CGMOP · DEPRO · SGP · MGI.",
          "href": "./movimentacao-pessoal/",
          "etiqueta": "Apresentação",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "funasa-painel-servidores",
          "titulo": "Painel de Servidores — FUNASA",
          "descricao": "Visão consolidada do quadro de servidores da fundação.",
          "href": "./funasa-painel-servidores/",
          "etiqueta": "Painel",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "projecao-correios",
          "titulo": "Projeção dos Correios",
          "descricao": "Projeção de cenários para movimentações dos Correios.",
          "href": "./projecao_correios/",
          "etiqueta": "Apresentação",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        }
      ]
    },
    {
      "id": "anistiados",
      "cor": 2,
      "titulo": "Anistiados (Lei 8.878/94 e 15.367/2026)",
      "descricao": "Monitoramento e impacto financeiro do público anistiado.",
      "oculta": false,
      "projetos": [
        {
          "id": "painel-anistiados",
          "titulo": "Painel de Monitoramento — Anistiados",
          "descricao": "Implementação da Lei nº 15.367/2026: reposicionamento na classe e no salário dos anistiados ativos, com evolução mês a mês das correções.",
          "href": "./painel-anistiados/",
          "etiqueta": "Painel",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "pdi-desligamento",
          "titulo": "PDI — Desligamento Incentivado",
          "descricao": "Impacto financeiro do PDI dos anistiados (Lei 15.367/2026), com simulador de cenários e recorte temporal.",
          "href": "./pdi_plano_desligamento_incentivado/",
          "etiqueta": "Estudo analítico",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        }
      ]
    },
    {
      "id": "estudos-dados",
      "cor": 3,
      "titulo": "Estudos analíticos e dados",
      "descricao": "Análises com filtros interativos e leitura autossuficiente.",
      "oculta": false,
      "projetos": [
        {
          "id": "lip-licencas",
          "titulo": "LIP — Licenças de Interesse Particular",
          "descricao": "20.507 licenças e 14.388 servidores, com filtros interativos e leitura autossuficiente.",
          "href": "./lip-estudo-licencas/",
          "etiqueta": "Estudo analítico",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "pipeline-lattes",
          "titulo": "Pipeline Lattes",
          "descricao": "Classificação e quantificação de perfis a partir do Currículo Lattes. CNPq × CNI.",
          "href": "./pipeline-lattes/",
          "etiqueta": "Dados · IA",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "m",
          "titulo": "Mara Legis",
          "descricao": "Acervo Mara Legis: Inteligência Jurídica em Movimentação de Servidores",
          "href": "https://notebook.google.com/notebook/f526e962-e813-443b-bee0-87f059d46800",
          "etiqueta": "Consulta Legislação",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": true,
          "oculto": false
        }
      ]
    },
    {
      "id": "fellowship",
      "cor": 4,
      "titulo": "Programa Fellowship — MGI × Banco Mundial",
      "descricao": "Documentos operacionais da parceria WBG Fellowship Program.",
      "oculta": false,
      "projetos": [
        {
          "id": "fellowship-programa-geral",
          "titulo": "Programa Fellowship",
          "descricao": "Visão geral do programa: o que é, quem custeia e base legal.",
          "href": "./fellowship-programa-geral/",
          "etiqueta": "Fellowship · MGI × BM",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "fellowship-fluxo-trabalho",
          "titulo": "Proposta de Fluxo de Trabalho",
          "descricao": "Papéis, procedimentos e padronização do WBG Fellowship Program.",
          "href": "./fellowship-fluxo-trabalho/",
          "etiqueta": "Fellowship · MGI × BM",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "fellowship-diretrizes",
          "titulo": "Diretrizes Operacionais",
          "descricao": "Consolidação da parceria e garantia de previsibilidade do programa de bolsas.",
          "href": "./fellowship-diretrizes/",
          "etiqueta": "Fellowship · MGI × BM",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        }
      ]
    },
    {
      "id": "institucionais",
      "cor": 5,
      "titulo": "Apresentações institucionais e ferramentas",
      "descricao": "Materiais de diretoria, normativos e ferramentas.",
      "oculta": false,
      "projetos": [
        {
          "id": "trimestral-cgmop",
          "titulo": "Trimestral CGMOP — Planejamento 2025/2026",
          "descricao": "Apresentação à Diretoria: execução do ciclo 2025/2026 e os projetos de 2026.",
          "href": "./trimestral-cgmop/",
          "etiqueta": "Apresentação",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "recruta-gov",
          "titulo": "Recruta.gov",
          "descricao": "A nova engenharia de alocação de servidores públicos.",
          "href": "./recruta-gov/",
          "etiqueta": "Alocação",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "recruta-apresentacao",
          "titulo": "Recruta.gov — Apresentação",
          "descricao": "Dez minutos de método e o roteiro da demonstração: a régua única de nove dimensões, o que o sistema não faz, e as sete paradas da demo. Navegação por teclado, cronômetro e notas do apresentador.",
          "href": "./recruta-gov/apresentacao/",
          "etiqueta": "Apresentação",
          "acao": "Apresentar",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "recruta-manual",
          "titulo": "Recruta.gov — Manual",
          "descricao": "Manual de funcionamento e operação: o pipeline, o assistente, as telas e o método por trás de cada número.",
          "href": "./recruta-gov/manual/",
          "etiqueta": "Documentação",
          "acao": "Ler",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        },
        {
          "id": "limites-reembolso",
          "titulo": "Limites de Reembolso",
          "descricao": "Parâmetros e limites vigentes. MGI/SGP/DEPRO/CGMOP/DGIMP.",
          "href": "./limites-reembolso/",
          "etiqueta": "Normativo",
          "acao": "Ver",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false
        }
      ]
    }
  ]
};
