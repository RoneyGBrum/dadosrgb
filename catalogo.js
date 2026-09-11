/* dadosrgb — catálogo de projetos.
   Esta é a ÚNICA fonte de verdade do índice. O index.html lê este arquivo.
   Para adicionar/editar um link, use o assistente: curadoria/curadoria.pyw
   (Editar cartão à mão no index.html é inútil: a próxima exportação sobrescreve.)
   cor: 1..5 → var(--c1)..var(--c5). A ORDEM DO ARRAY é a ordem na tela.
   colunas (coleção): 0 automático, ou 2 / 3 / 4 cartões por linha.
   cor (projeto): 0 herda a da coleção, ou 1..5 para destoar.
   largura (projeto): "auto" | "normal" | "largo" (2 col.) | "cheio" (linha toda). */
window.CATALOGO = {
  "versao": 1,
  "atualizadoEm": "2026-09-11",
  "colecoes": [
    {
      "id": "movimentacao-cgmop",
      "cor": 1,
      "colunas": 0,
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
          "cor": 0,
          "largura": "auto",
          "destaque": true,
          "selo": "Principal",
          "externo": false,
          "oculto": false,
          "acesso": "restrito"
        },
        {
          "id": "painel-publico",
          "titulo": "Painel público de Movimentações",
          "descricao": "A versão aberta do painel de Movimentações — vigentes e histórico, gráficos e a relação nominal, sem os dados individuais sensíveis. Acesso direto, sem senha.",
          "href": "./painel_CGMOP/painel_publico.html",
          "etiqueta": "Aberto · sem login",
          "acao": "Abrir",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "movimentacao-pessoal",
          "titulo": "Movimentação de Pessoal",
          "descricao": "A transformação da mobilidade na Administração Pública Federal. CGMOP · DEPRO · SGP · MGI.",
          "href": "./movimentacao-pessoal/",
          "etiqueta": "Apresentação",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "funasa-painel-servidores",
          "titulo": "Painel de Servidores — FUNASA",
          "descricao": "Visão consolidada do quadro de servidores da fundação.",
          "href": "./funasa-painel-servidores/",
          "etiqueta": "Painel",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "projecao-correios",
          "titulo": "Projeção dos Correios",
          "descricao": "Projeção de cenários para movimentações dos Correios.",
          "href": "./projecao_correios/",
          "etiqueta": "Apresentação",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    },
    {
      "id": "anistiados",
      "cor": 2,
      "colunas": 0,
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
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "pdi-desligamento",
          "titulo": "PDI — Desligamento Incentivado",
          "descricao": "Impacto financeiro do PDI dos anistiados (Lei 15.367/2026), com simulador de cenários e recorte temporal.",
          "href": "./pdi_plano_desligamento_incentivado/",
          "etiqueta": "Estudo analítico",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    },
    {
      "id": "estudos-dados",
      "cor": 3,
      "colunas": 0,
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
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "m",
          "titulo": "Mara Legis",
          "descricao": "Acervo Mara Legis: Inteligência Jurídica em Movimentação de Servidores",
          "href": "https://notebook.google.com/notebook/f526e962-e813-443b-bee0-87f059d46800",
          "etiqueta": "Consulta Legislação",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": true,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    },
    {
      "id": "fellowship",
      "cor": 4,
      "colunas": 0,
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
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "fellowship-fluxo-trabalho",
          "titulo": "Proposta de Fluxo de Trabalho",
          "descricao": "Papéis, procedimentos e padronização do WBG Fellowship Program.",
          "href": "./fellowship-fluxo-trabalho/",
          "etiqueta": "Fellowship · MGI × BM",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "fellowship-diretrizes",
          "titulo": "Diretrizes Operacionais",
          "descricao": "Consolidação da parceria e garantia de previsibilidade do programa de bolsas.",
          "href": "./fellowship-diretrizes/",
          "etiqueta": "Fellowship · MGI × BM",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    },
    {
      "id": "institucionais",
      "cor": 5,
      "colunas": 0,
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
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "recruta-gov",
          "titulo": "Recruta.gov",
          "descricao": "A nova engenharia de alocação de servidores públicos.",
          "href": "./recruta-gov/",
          "etiqueta": "Alocação",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "recruta-apresentacao",
          "titulo": "Recruta.gov — Apresentação",
          "descricao": "Dez minutos de método e o roteiro da demonstração: a régua única de nove dimensões, o que o sistema não faz, e as sete paradas da demo. Navegação por teclado, cronômetro e notas do apresentador.",
          "href": "./recruta-gov/apresentacao/",
          "etiqueta": "Apresentação",
          "acao": "Apresentar",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "recruta-apresentacao-comite",
          "titulo": "Recruta.gov — Apresentação para decisão",
          "descricao": "A versão longa, de trinta a quarenta minutos, para quem decide a continuidade do sistema: o problema que ele resolve, a régua de nove dimensões medida sobre a base inteira, a procedência de cada nota, a demonstração ao vivo no meio da apresentação e o que o sistema recusa responder quando não tem base. Catorze slides com notas do apresentador, tema claro forçável para projetor e roteiro de demonstração cronometrado.",
          "href": "./recruta-gov/apresentacao-comite/",
          "etiqueta": "Apresentação",
          "acao": "Apresentar",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "limites-reembolso",
          "titulo": "Limites de Reembolso",
          "descricao": "Parâmetros e limites vigentes. MGI/SGP/DEPRO/CGMOP/DGIMP.",
          "href": "./limites-reembolso/",
          "etiqueta": "Normativo",
          "acao": "Ver",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    },
    {
      "id": "manuais",
      "cor": 2,
      "colunas": 0,
      "titulo": "Manuais e documentação",
      "descricao": "Como cada sistema funciona, como operar e o que cada número significa.",
      "oculta": false,
      "projetos": [
        {
          "id": "cgmop-manual",
          "titulo": "Manual do Ecossistema CGMOP",
          "descricao": "Documentação completa do ecossistema de painéis: o que o sistema faz, a arquitetura, a instalação, os três caminhos de execução e o pipeline em cinco etapas. Traz os números da rodada corrente e os conceitos que mudam o número (vigente ≠ ativo, pessoas ≠ vínculos).",
          "href": "./painel_CGMOP/manual.html",
          "etiqueta": "Documentação · acesso restrito",
          "acao": "Ler manual",
          "cor": 0,
          "largura": "auto",
          "destaque": true,
          "selo": "Restrito",
          "externo": false,
          "oculto": false,
          "acesso": "restrito"
        },
        {
          "id": "recruta-manual",
          "titulo": "Manual do Recruta.Gov",
          "descricao": "Funcionamento e operação: o acervo em números, o problema que o sistema resolve sem termos técnicos, as nove dimensões da régua de avaliação e a operação aba a aba do assistente — início, pipeline e servidores, com cache, reprocessamento e acessos.",
          "href": "./recruta-gov/manual/",
          "etiqueta": "Documentação",
          "acao": "Ler manual",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        },
        {
          "id": "manual-pipeline-lattes",
          "titulo": "Pipeline Lattes — Manual de Referência",
          "descricao": "Guia de instalação, manual de operação e documentação técnica em cinco partes: entender o mecanismo de classificação, instalar o ambiente, as quatro etapas em detalhe, calibrar os números ajustáveis e adaptar o sistema. CNPq × CNI.",
          "href": "./pipeline-lattes/",
          "etiqueta": "Manual · CNPq × CNI",
          "acao": "Ler manual",
          "cor": 0,
          "largura": "auto",
          "destaque": false,
          "selo": "",
          "externo": false,
          "oculto": false,
          "acesso": "publico"
        }
      ]
    }
  ]
};
