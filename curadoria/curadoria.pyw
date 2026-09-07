#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Curadoria dadosrgb — assistente de catálogo (desktop, Tkinter).

Edita C:\\0_Apresentacoes\\dadosrgb\\catalogo.js, que é a única fonte de verdade
do índice do site. Não precisa de nada instalado além do Python padrão.

Rodar:  duplo clique neste arquivo, ou  python curadoria.pyw
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ----------------------------------------------------------------------------
# caminhos
# ----------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)                       # .../dadosrgb
CATALOGO = os.path.join(RAIZ, "catalogo.js")

CORES = {
    1: ("#2C5282", "Marinho"),
    2: ("#B05A22", "Cobre"),
    3: ("#6B2FA0", "Ametista"),
    4: ("#0E6B4F", "Esmeralda"),
    5: ("#B0233F", "Granada"),
}

ETIQUETAS = [
    "Painel", "Painel · acesso restrito", "Aberto · sem login", "Apresentação",
    "Estudo analítico", "Documentação", "Documentação · acesso restrito",
    "Manual", "Manual · acesso restrito", "Normativo", "Alocação", "Dados · IA",
    "Fellowship · MGI × BM", "Consulta Legislação",
]

ACOES = ["Ver", "Abrir", "Ler", "Ler manual", "Abrir ecossistema", "Consultar"]

CAMPOS_PROJ = ["id", "titulo", "descricao", "href", "etiqueta", "acao",
               "destaque", "selo", "externo", "oculto", "acesso"]


# ----------------------------------------------------------------------------
# leitura / escrita do catalogo.js
# ----------------------------------------------------------------------------
def ler_catalogo(caminho=CATALOGO):
    with open(caminho, "r", encoding="utf-8") as f:
        txt = f.read()
    i = txt.find("{")
    j = txt.rfind("}")
    if i < 0 or j <= i:
        raise ValueError("Não encontrei o objeto do catálogo neste arquivo.")
    dados = json.loads(txt[i:j + 1])
    return sanear(dados)


def sanear(o):
    """Normaliza a forma. Nada malformado entra no estado."""
    if not isinstance(o, dict) or not isinstance(o.get("colecoes"), list):
        raise ValueError("Estrutura inesperada: falta a lista 'colecoes'.")
    out = {
        "versao": int(o.get("versao") or 1),
        "atualizadoEm": str(o.get("atualizadoEm") or ""),
        "colecoes": [],
    }
    for c in o["colecoes"]:
        if not isinstance(c, dict):
            continue
        cc = {
            "id": str(c.get("id") or "").strip() or "colecao-%d" % (len(out["colecoes"]) + 1),
            "cor": min(5, max(1, int(c.get("cor") or 1))),
            "titulo": str(c.get("titulo") or ""),
            "descricao": str(c.get("descricao") or ""),
            "oculta": bool(c.get("oculta")),
            "projetos": [],
        }
        for p in (c.get("projetos") or []):
            if not isinstance(p, dict):
                continue
            acesso = str(p.get("acesso") or "").strip().lower()
            if acesso not in ("publico", "restrito"):
                # deduz pelo texto da etiqueta quando o campo ainda não existe
                acesso = "restrito" if "restrit" in str(p.get("etiqueta", "")).lower() else "publico"
            cc["projetos"].append({
                "id": str(p.get("id") or "").strip() or "projeto-%d" % (len(cc["projetos"]) + 1),
                "titulo": str(p.get("titulo") or ""),
                "descricao": str(p.get("descricao") or ""),
                "href": str(p.get("href") or ""),
                "etiqueta": str(p.get("etiqueta") or ""),
                "acao": str(p.get("acao") or "Ver"),
                "destaque": bool(p.get("destaque")),
                "selo": str(p.get("selo") or ""),
                "externo": bool(p.get("externo")),
                "oculto": bool(p.get("oculto")),
                "acesso": acesso,
            })
        out["colecoes"].append(cc)
    return out


def js(valor):
    """String JSON com aspas duplas, escapando como o JS espera."""
    return json.dumps("" if valor is None else str(valor), ensure_ascii=False)


def serializar(cat):
    """Saída determinística: mesma ordem de chaves, 2 espaços, LF.
    Duas exportações sem mudança geram bytes idênticos."""
    hoje = datetime.now().strftime("%Y-%m-%d")
    L = []
    L.append("/* dadosrgb — catálogo de projetos.")
    L.append("   Esta é a ÚNICA fonte de verdade do índice. O index.html lê este arquivo.")
    L.append("   Para adicionar/editar um link, use o assistente: curadoria/curadoria.pyw")
    L.append("   (Editar cartão à mão no index.html é inútil: a próxima exportação sobrescreve.)")
    L.append("   cor: 1..5 → var(--c1)..var(--c5). A ORDEM DO ARRAY é a ordem na tela. */")
    L.append("window.CATALOGO = {")
    L.append('  "versao": %d,' % int(cat.get("versao") or 1))
    L.append('  "atualizadoEm": %s,' % js(hoje))
    L.append('  "colecoes": [')
    cols = cat.get("colecoes") or []
    for ci, c in enumerate(cols):
        L.append("    {")
        L.append('      "id": %s,' % js(c.get("id")))
        L.append('      "cor": %d,' % int(c.get("cor") or 1))
        L.append('      "titulo": %s,' % js(c.get("titulo")))
        L.append('      "descricao": %s,' % js(c.get("descricao")))
        L.append('      "oculta": %s,' % ("true" if c.get("oculta") else "false"))
        L.append('      "projetos": [')
        ps = c.get("projetos") or []
        for pi, p in enumerate(ps):
            L.append("        {")
            L.append('          "id": %s,' % js(p.get("id")))
            L.append('          "titulo": %s,' % js(p.get("titulo")))
            L.append('          "descricao": %s,' % js(p.get("descricao")))
            L.append('          "href": %s,' % js(p.get("href")))
            L.append('          "etiqueta": %s,' % js(p.get("etiqueta")))
            L.append('          "acao": %s,' % js(p.get("acao") or "Ver"))
            L.append('          "destaque": %s,' % ("true" if p.get("destaque") else "false"))
            L.append('          "selo": %s,' % js(p.get("selo")))
            L.append('          "externo": %s,' % ("true" if p.get("externo") else "false"))
            L.append('          "oculto": %s,' % ("true" if p.get("oculto") else "false"))
            L.append('          "acesso": %s' % js(p.get("acesso") or "publico"))
            L.append("        }" + ("," if pi < len(ps) - 1 else ""))
        L.append("      ]")
        L.append("    }" + ("," if ci < len(cols) - 1 else ""))
    L.append("  ]")
    L.append("};")
    return "\n".join(L) + "\n"


def slug(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40]
    return s or "item"


# ----------------------------------------------------------------------------
# validação
# ----------------------------------------------------------------------------
def validar(cat):
    probs = []
    ids, hrefs = {}, {}
    for ci, c in enumerate(cat["colecoes"]):
        rot = c.get("titulo") or ("Coleção %d" % (ci + 1))
        if not (c.get("titulo") or "").strip():
            probs.append(("Coleção %d está sem título" % (ci + 1), ci, None))
        if not (c.get("id") or "").strip():
            probs.append(("Coleção «%s» está sem id" % rot, ci, None))
        vis = [p for p in c["projetos"] if not p.get("oculto")]
        if not c.get("oculta") and not vis:
            probs.append(("«%s» não tem nenhum projeto visível" % rot, ci, None))
        dest = [p for p in vis if p.get("destaque")]
        if len(dest) > 1:
            probs.append(("«%s» tem %d projetos em destaque (só pode 1)" % (rot, len(dest)), ci, None))
        for pi, p in enumerate(c["projetos"]):
            nome = p.get("titulo") or "Projeto %d" % (pi + 1)
            if not (p.get("titulo") or "").strip():
                probs.append(("Projeto sem título em «%s»" % rot, ci, pi))
            if not (p.get("href") or "").strip():
                probs.append(("«%s» está sem endereço" % nome, ci, pi))
            pid = p.get("id")
            if pid:
                if pid in ids:
                    probs.append(("id repetido: «%s»" % pid, ci, pi))
                ids[pid] = True
            h = p.get("href")
            if h:
                if h in hrefs:
                    probs.append(("Dois projetos apontam para %s" % h, ci, pi))
                hrefs[h] = True
    return probs


def checar_href(href):
    """Existe no disco? (só para links internos)"""
    if not href:
        return None, ""
    if re.match(r"^https?://", href, re.I):
        return None, "link externo — não dá para verificar aqui"
    rel = href[2:] if href.startswith("./") else href.lstrip("/")
    alvo = os.path.join(RAIZ, rel.replace("/", os.sep))
    if os.path.isdir(alvo):
        if os.path.exists(os.path.join(alvo, "index.html")):
            return True, "pasta encontrada (index.html existe)"
        return False, "a pasta existe, mas não tem index.html"
    if os.path.exists(alvo):
        return True, "arquivo encontrado"
    return False, "não encontrei nada nesse endereço"


# ----------------------------------------------------------------------------
# aplicação
# ----------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Curadoria dadosrgb — catálogo do índice")
        self.geometry("1180x760")
        self.minsize(980, 620)

        self.cat = None
        self.sel = None            # ("col", ci) ou ("proj", ci, pi)
        self.pilha = []            # desfazer
        self.sujo = False
        self._carregando = False

        self._estilo()
        self._menu()
        self._layout()
        self.carregar()
        self.protocol("WM_DELETE_WINDOW", self.sair)
        self.bind("<Control-s>", lambda e: self.salvar())
        self.bind("<Control-z>", lambda e: self.desfazer())

    # ---------- estilo ----------
    def _estilo(self):
        s = ttk.Style(self)
        try:
            s.theme_use("vista")
        except tk.TclError:
            pass
        s.configure("Titulo.TLabel", font=("Segoe UI", 11, "bold"))
        s.configure("Dica.TLabel", foreground="#5B6478")
        s.configure("Erro.TLabel", foreground="#B0233F")
        s.configure("Ok.TLabel", foreground="#0E6B4F")
        s.configure("Cab.TLabel", font=("Segoe UI", 8, "bold"), foreground="#7E8899")

    # ---------- menu ----------
    def _menu(self):
        m = tk.Menu(self)
        arq = tk.Menu(m, tearoff=0)
        arq.add_command(label="Recarregar do disco", command=self.carregar)
        arq.add_command(label="Salvar  (Ctrl+S)", command=self.salvar)
        arq.add_separator()
        arq.add_command(label="Abrir pasta do site", command=self.abrir_pasta)
        arq.add_command(label="Restaurar de um backup…", command=self.restaurar_backup)
        arq.add_separator()
        arq.add_command(label="Sair", command=self.sair)
        m.add_cascade(label="Arquivo", menu=arq)

        ed = tk.Menu(m, tearoff=0)
        ed.add_command(label="Desfazer  (Ctrl+Z)", command=self.desfazer)
        ed.add_separator()
        ed.add_command(label="Validar agora", command=self.pintar_problemas)
        m.add_cascade(label="Editar", menu=ed)

        aj = tk.Menu(m, tearoff=0)
        aj.add_command(label="Como publicar", command=self.ajuda_publicar)
        aj.add_command(label="Sobre o acesso restrito", command=self.ajuda_restrito)
        m.add_cascade(label="Ajuda", menu=aj)
        self.config(menu=m)

    # ---------- layout ----------
    def _layout(self):
        topo = ttk.Frame(self, padding=(10, 8))
        topo.pack(fill="x")
        ttk.Label(topo, text="Curadoria dadosrgb", style="Titulo.TLabel").pack(side="left")
        self.lb_estado = ttk.Label(topo, text="", style="Dica.TLabel")
        self.lb_estado.pack(side="left", padx=12)
        ttk.Button(topo, text="Salvar catálogo", command=self.salvar).pack(side="right")
        ttk.Button(topo, text="Publicar (git)", command=self.publicar).pack(side="right", padx=6)
        ttk.Button(topo, text="Desfazer", command=self.desfazer).pack(side="right")

        corpo = ttk.Panedwindow(self, orient="horizontal")
        corpo.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # ----- esquerda: árvore -----
        esq = ttk.Frame(corpo)
        corpo.add(esq, weight=1)

        self.arv = ttk.Treeview(esq, show="tree", selectmode="browse")
        self.arv.pack(fill="both", expand=True)
        self.arv.bind("<<TreeviewSelect>>", self.ao_selecionar)
        for n, (hexa, _) in CORES.items():
            self.arv.tag_configure("cor%d" % n, foreground=hexa)
        self.arv.tag_configure("oculto", foreground="#9AA3B0")

        bar = ttk.Frame(esq)
        bar.pack(fill="x", pady=(6, 0))
        ttk.Button(bar, text="+ Coleção", command=self.nova_colecao, width=11).pack(side="left")
        ttk.Button(bar, text="+ Projeto", command=self.novo_projeto, width=11).pack(side="left", padx=4)
        ttk.Button(bar, text="↑", command=lambda: self.mover(-1), width=3).pack(side="left")
        ttk.Button(bar, text="↓", command=lambda: self.mover(1), width=3).pack(side="left", padx=2)
        ttk.Button(bar, text="Mover para…", command=self.mover_para, width=11).pack(side="left", padx=4)
        ttk.Button(bar, text="Duplicar", command=self.duplicar, width=9).pack(side="left")
        ttk.Button(bar, text="Excluir", command=self.excluir, width=9).pack(side="left", padx=4)

        # ----- direita: formulário + problemas -----
        dir_ = ttk.Frame(corpo)
        corpo.add(dir_, weight=2)

        self.form = ttk.Frame(dir_, padding=(12, 6))
        self.form.pack(fill="both", expand=True)

        probs = ttk.LabelFrame(dir_, text="Verificação", padding=8)
        probs.pack(fill="x", pady=(6, 0))
        self.lst_probs = tk.Listbox(probs, height=4, activestyle="none",
                                    borderwidth=0, highlightthickness=0)
        self.lst_probs.pack(fill="x")
        self.lst_probs.bind("<Double-Button-1>", self.ir_para_problema)
        self._probs = []

    # ------------------------------------------------------------------ dados
    def carregar(self):
        try:
            self.cat = ler_catalogo()
        except Exception as e:
            messagebox.showerror("Não consegui abrir o catálogo",
                                 "%s\n\nArquivo: %s" % (e, CATALOGO))
            self.cat = {"versao": 1, "atualizadoEm": "", "colecoes": []}
        self.pilha.clear()
        self.sujo = False
        self.sel = None
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()
        self.estado("catálogo carregado")

    def snap(self):
        self.pilha.append(json.dumps(self.cat, ensure_ascii=False))
        if len(self.pilha) > 60:
            self.pilha.pop(0)
        self.sujo = True

    def desfazer(self):
        if not self.pilha:
            self.estado("nada para desfazer")
            return
        self.cat = json.loads(self.pilha.pop())
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()
        self.estado("desfeito")

    def estado(self, txt=""):
        marca = " · alterações não salvas" if self.sujo else ""
        n_col = len(self.cat["colecoes"])
        n_prj = sum(len(c["projetos"]) for c in self.cat["colecoes"])
        self.lb_estado.config(text="%d coleções · %d projetos%s%s"
                              % (n_col, n_prj, marca, ("  —  " + txt) if txt else ""))

    # ------------------------------------------------------------------ árvore
    def pintar_arvore(self):
        aberto = {i for i in self.arv.get_children("") if self.arv.item(i, "open")}
        self.arv.delete(*self.arv.get_children(""))
        for ci, c in enumerate(self.cat["colecoes"]):
            _, nome_cor = CORES[c["cor"]]
            rot = "%s   [%s]%s" % (c["titulo"] or "(sem título)", nome_cor,
                                   "  · oculta" if c.get("oculta") else "")
            iid = "c%d" % ci
            tags = ["cor%d" % c["cor"]] + (["oculto"] if c.get("oculta") else [])
            self.arv.insert("", "end", iid=iid, text=rot, open=(iid in aberto or True),
                            tags=tuple(tags))
            for pi, p in enumerate(c["projetos"]):
                marcas = []
                if p.get("destaque"):
                    marcas.append("★")
                if p.get("acesso") == "restrito":
                    marcas.append("🔒")
                if p.get("externo"):
                    marcas.append("↗")
                if p.get("oculto"):
                    marcas.append("oculto")
                suf = ("   " + " ".join(marcas)) if marcas else ""
                self.arv.insert(iid, "end", iid="c%dp%d" % (ci, pi),
                                text=(p["titulo"] or "(sem título)") + suf,
                                tags=("oculto",) if p.get("oculto") else ())

    def ao_selecionar(self, _=None):
        s = self.arv.selection()
        if not s:
            return
        iid = s[0]
        m = re.match(r"^c(\d+)(?:p(\d+))?$", iid)
        if not m:
            return
        ci = int(m.group(1))
        self.sel = ("proj", ci, int(m.group(2))) if m.group(2) is not None else ("col", ci)
        self.pintar_form()

    def _selecionar_iid(self, iid):
        if self.arv.exists(iid):
            self.arv.selection_set(iid)
            self.arv.see(iid)

    # ------------------------------------------------------------ formulário
    def _validar_sel(self):
        """A seleção pode ter ficado para trás (desfazer, exclusão, reordenação)."""
        s = self.sel
        if not s:
            return
        cols = self.cat["colecoes"]
        if not (0 <= s[1] < len(cols)):
            self.sel = None
            return
        if s[0] == "proj" and not (0 <= s[2] < len(cols[s[1]]["projetos"])):
            self.sel = ("col", s[1])

    def pintar_form(self):
        self._validar_sel()
        for w in self.form.winfo_children():
            w.destroy()
        if not self.sel:
            ttk.Label(self.form, text="Selecione uma coleção ou um projeto à esquerda.",
                      style="Dica.TLabel").pack(pady=30)
            return
        if self.sel[0] == "col":
            self._form_colecao(self.cat["colecoes"][self.sel[1]])
        else:
            _, ci, pi = self.sel
            self._form_projeto(self.cat["colecoes"][ci], self.cat["colecoes"][ci]["projetos"][pi])

    # --- helpers de campo ---
    def _linha(self, pai, rotulo):
        ttk.Label(pai, text=rotulo.upper(), style="Cab.TLabel").pack(anchor="w", pady=(8, 2))

    def _entrada(self, pai, rotulo, valor, ao_mudar, limite=None, valores=None):
        self._linha(pai, rotulo)
        var = tk.StringVar(value=valor or "")
        if valores:
            w = ttk.Combobox(pai, textvariable=var, values=valores)
        else:
            w = ttk.Entry(pai, textvariable=var)
        w.pack(fill="x")
        cont = ttk.Label(pai, text="", style="Dica.TLabel")
        if limite:
            cont.pack(anchor="e")

        def mudou(*_):
            if self._carregando:
                return
            v = var.get()
            if limite:
                cont.config(text="%d / %d" % (len(v), limite),
                            style="Erro.TLabel" if len(v) > limite else "Dica.TLabel")
            ao_mudar(v)
        var.trace_add("write", mudou)
        if limite:
            cont.config(text="%d / %d" % (len(valor or ""), limite))
        return w, var

    def _texto(self, pai, rotulo, valor, ao_mudar, limite=240, altura=5):
        self._linha(pai, rotulo)
        w = tk.Text(pai, height=altura, wrap="word", relief="solid", borderwidth=1,
                    font=("Segoe UI", 9))
        w.insert("1.0", valor or "")
        w.pack(fill="x")
        cont = ttk.Label(pai, text="%d / %d" % (len(valor or ""), limite), style="Dica.TLabel")
        cont.pack(anchor="e")

        def mudou(_=None):
            if self._carregando:
                return
            v = w.get("1.0", "end-1c")
            cont.config(text="%d / %d" % (len(v), limite),
                        style="Erro.TLabel" if len(v) > limite else "Dica.TLabel")
            ao_mudar(v)
        w.bind("<KeyRelease>", mudou)
        return w

    def _check(self, pai, rotulo, valor, ao_mudar):
        var = tk.BooleanVar(value=bool(valor))

        def mudou():
            if self._carregando:
                return
            ao_mudar(var.get())
        ttk.Checkbutton(pai, text=rotulo, variable=var, command=mudou).pack(anchor="w", pady=2)
        return var

    def _mudou_campo(self, alvo, chave, valor, repintar=False):
        if alvo.get(chave) == valor:
            return
        self.snap()
        alvo[chave] = valor
        if repintar:
            self.pintar_arvore()
        self.pintar_problemas()
        self.estado()

    # --- coleção ---
    def _form_colecao(self, c):
        self._carregando = True
        ttk.Label(self.form, text="Coleção", style="Titulo.TLabel").pack(anchor="w")

        self._entrada(self.form, "Título", c["titulo"],
                      lambda v: self._mudou_campo(c, "titulo", v, True), 60)
        self._texto(self.form, "Descrição", c["descricao"],
                    lambda v: self._mudou_campo(c, "descricao", v), 140, 3)

        self._linha(self.form, "Cor da coleção")
        fr = ttk.Frame(self.form)
        fr.pack(fill="x")
        var_cor = tk.IntVar(value=c["cor"])

        def trocar_cor():
            if self._carregando:
                return
            self._mudou_campo(c, "cor", var_cor.get(), True)
        for n, (hexa, nome) in CORES.items():
            cel = ttk.Frame(fr)
            cel.pack(side="left", padx=(0, 10))
            tk.Label(cel, background=hexa, width=3, height=1).pack(side="left", padx=(0, 4))
            ttk.Radiobutton(cel, text=nome, value=n, variable=var_cor,
                            command=trocar_cor).pack(side="left")

        self._entrada(self.form, "Identificador (id)", c["id"],
                      lambda v: self._mudou_campo(c, "id", v), 40)
        ttk.Label(self.form, text="O id vira a âncora da seção no site (#col-N usa a posição).",
                  style="Dica.TLabel").pack(anchor="w")
        self._check(self.form, "Ocultar esta coleção do site", c.get("oculta"),
                    lambda v: self._mudou_campo(c, "oculta", v, True))
        self._carregando = False

    # --- projeto ---
    def _form_projeto(self, c, p):
        self._carregando = True
        cab = ttk.Frame(self.form)
        cab.pack(fill="x")
        ttk.Label(cab, text="Projeto", style="Titulo.TLabel").pack(side="left")
        ttk.Label(cab, text="  em «%s»" % c["titulo"], style="Dica.TLabel").pack(side="left")

        nb = ttk.Notebook(self.form)
        nb.pack(fill="both", expand=True, pady=(6, 0))
        ab1 = ttk.Frame(nb, padding=10)
        ab2 = ttk.Frame(nb, padding=10)
        nb.add(ab1, text="Conteúdo")
        nb.add(ab2, text="Acesso e exibição")

        # ---- aba conteúdo ----
        def set_titulo(v):
            self._mudou_campo(p, "titulo", v, True)
            if not p.get("id") or p["id"].startswith(("projeto-", "novo-")):
                p["id"] = slug(v)
        self._entrada(ab1, "Título", p["titulo"], set_titulo, 60)
        self._texto(ab1, "Descrição", p["descricao"],
                    lambda v: self._mudou_campo(p, "descricao", v),
                    300 if p.get("destaque") else 240, 5)

        self._linha(ab1, "Endereço (href)")
        fr_h = ttk.Frame(ab1)
        fr_h.pack(fill="x")
        var_h = tk.StringVar(value=p["href"])
        e_h = ttk.Entry(fr_h, textvariable=var_h)
        e_h.pack(side="left", fill="x", expand=True)
        ttk.Button(fr_h, text="Procurar…", width=10,
                   command=lambda: self._escolher_href(var_h)).pack(side="left", padx=(6, 0))
        lb_h = ttk.Label(ab1, text="", style="Dica.TLabel")
        lb_h.pack(anchor="w")

        def href_mudou(*_):
            if self._carregando:
                return
            v = normalizar_href(var_h.get())
            self._mudou_campo(p, "href", v)
            if re.match(r"^https?://", v, re.I) and not p.get("externo"):
                p["externo"] = True
                self.pintar_arvore()
            ok, msg = checar_href(v)
            lb_h.config(text=msg, style="Ok.TLabel" if ok else ("Erro.TLabel" if ok is False else "Dica.TLabel"))
        var_h.trace_add("write", href_mudou)
        ok0, msg0 = checar_href(p["href"])
        lb_h.config(text=msg0, style="Ok.TLabel" if ok0 else ("Erro.TLabel" if ok0 is False else "Dica.TLabel"))

        self._entrada(ab1, "Etiqueta", p["etiqueta"],
                      lambda v: self._mudou_campo(p, "etiqueta", v), 34, ETIQUETAS)
        self._entrada(ab1, "Texto do link", p["acao"],
                      lambda v: self._mudou_campo(p, "acao", v), 22, ACOES)
        self._entrada(ab1, "Identificador (id)", p["id"],
                      lambda v: self._mudou_campo(p, "id", v), 40)

        # ---- aba acesso ----
        self._linha(ab2, "Acesso")
        var_ac = tk.StringVar(value=p.get("acesso") or "publico")

        lb_ac = ttk.Label(ab2, text="", style="Dica.TLabel", wraplength=520, justify="left")

        def trocar_acesso():
            if self._carregando:
                return
            self._mudou_campo(p, "acesso", var_ac.get(), True)
            atualiza_ac()

        ttk.Radiobutton(ab2, text="Público — qualquer pessoa abre", value="publico",
                        variable=var_ac, command=trocar_acesso).pack(anchor="w")
        ttk.Radiobutton(ab2, text="Restrito — a página pede usuário e senha", value="restrito",
                        variable=var_ac, command=trocar_acesso).pack(anchor="w")

        fr_senha = ttk.Frame(ab2)
        fr_senha.pack(fill="x", pady=(6, 0))
        ttk.Button(fr_senha, text="Definir senha do acesso restrito…",
                   command=self.definir_senha).pack(side="left")
        lb_ac.pack(anchor="w", pady=(6, 0))

        def atualiza_ac():
            if var_ac.get() == "restrito":
                lb_ac.config(text="A senha não fica no catálogo: ela é gravada dentro das páginas "
                                  "protegidas. Use o botão acima para trocá-la.")
                for w in fr_senha.winfo_children():
                    w.state(["!disabled"])
            else:
                lb_ac.config(text="Sem senha. O endereço abre direto.")
                for w in fr_senha.winfo_children():
                    w.state(["disabled"])
        atualiza_ac()

        ttk.Separator(ab2).pack(fill="x", pady=10)
        self._linha(ab2, "Exibição")
        self._check(ab2, "Cartão principal da coleção (destaque)", p.get("destaque"),
                    lambda v: self._destaque(c, p, v))
        self._entrada(ab2, "Selo (só aparece no cartão principal)", p.get("selo"),
                      lambda v: self._mudou_campo(p, "selo", v), 18)
        self._check(ab2, "Abrir em nova aba (link externo)", p.get("externo"),
                    lambda v: self._mudou_campo(p, "externo", v, True))
        self._check(ab2, "Ocultar do site (mantém o conteúdo aqui)", p.get("oculto"),
                    lambda v: self._mudou_campo(p, "oculto", v, True))

        ttk.Separator(ab2).pack(fill="x", pady=10)
        self._linha(ab2, "Mover para outra coleção")
        var_mv = tk.StringVar(value="%d · %s" % (self.sel[1] + 1, c["titulo"]))
        opts = ["%d · %s" % (i + 1, x["titulo"]) for i, x in enumerate(self.cat["colecoes"])]
        cb = ttk.Combobox(ab2, textvariable=var_mv, values=opts, state="readonly")
        cb.pack(fill="x")
        cb.bind("<<ComboboxSelected>>", lambda e: self._mover_colecao(opts.index(var_mv.get())))
        self._carregando = False

    def _destaque(self, c, p, v):
        self.snap()
        if v:
            for o in c["projetos"]:
                o["destaque"] = False
            if not p.get("selo"):
                p["selo"] = "Principal"
        p["destaque"] = v
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()

    def _mover_colecao(self, destino):
        if self.sel[0] != "proj":
            return
        _, ci, pi = self.sel
        if destino == ci:
            return
        self.snap()
        item = self.cat["colecoes"][ci]["projetos"].pop(pi)
        item["destaque"] = False
        self.cat["colecoes"][destino]["projetos"].append(item)
        self.sel = ("proj", destino, len(self.cat["colecoes"][destino]["projetos"]) - 1)
        self.pintar_arvore()
        self._selecionar_iid("c%dp%d" % (self.sel[1], self.sel[2]))
        self.pintar_form()
        self.pintar_problemas()

    def _escolher_href(self, var):
        cam = filedialog.askopenfilename(
            title="Escolha a página dentro da pasta do site",
            initialdir=RAIZ, filetypes=[("Páginas", "*.html"), ("Todos", "*.*")])
        if not cam:
            return
        try:
            rel = os.path.relpath(cam, RAIZ).replace(os.sep, "/")
        except ValueError:
            messagebox.showwarning("Fora da pasta",
                                   "Escolha um arquivo dentro de %s" % RAIZ)
            return
        if rel.endswith("/index.html"):
            rel = rel[: -len("index.html")]
        var.set("./" + rel)

    # ------------------------------------------------------------ operações
    def nova_colecao(self):
        self.snap()
        n = len(self.cat["colecoes"])
        self.cat["colecoes"].append({
            "id": "colecao-%d" % (n + 1), "cor": (n % 5) + 1,
            "titulo": "Nova coleção", "descricao": "", "oculta": False, "projetos": [],
        })
        self.sel = ("col", n)
        self.pintar_arvore()
        self._selecionar_iid("c%d" % n)
        self.pintar_form()
        self.pintar_problemas()

    def novo_projeto(self):
        if not self.sel:
            messagebox.showinfo("Escolha a coleção",
                                "Selecione antes a coleção que vai receber o projeto.")
            return
        ci = self.sel[1]
        self.snap()
        c = self.cat["colecoes"][ci]
        c["projetos"].append({
            "id": "projeto-%d" % (len(c["projetos"]) + 1), "titulo": "Novo projeto",
            "descricao": "", "href": "", "etiqueta": "", "acao": "Ver",
            "destaque": False, "selo": "", "externo": False, "oculto": False,
            "acesso": "publico",
        })
        self.sel = ("proj", ci, len(c["projetos"]) - 1)
        self.pintar_arvore()
        self._selecionar_iid("c%dp%d" % (ci, self.sel[2]))
        self.pintar_form()
        self.pintar_problemas()

    def mover_para(self):
        """Troca o projeto de seção. Para coleção, reposiciona na ordem."""
        if not self.sel:
            messagebox.showinfo("Escolha um item", "Selecione antes o projeto ou a coleção.")
            return
        cols = self.cat["colecoes"]
        if self.sel[0] == "col":
            opts = ["posição %d" % (i + 1) for i in range(len(cols))]
            titulo = "Mover a coleção «%s» para qual posição?" % cols[self.sel[1]]["titulo"]
        else:
            opts = ["%d · %s" % (i + 1, c["titulo"]) for i, c in enumerate(cols)]
            titulo = "Mover «%s» para qual seção?" % \
                     cols[self.sel[1]]["projetos"][self.sel[2]]["titulo"]
        atual = self.sel[1]
        escolha = EscolherDestino(self, titulo, opts, atual).resultado
        if escolha is None or escolha == atual:
            return
        if self.sel[0] == "col":
            self.snap()
            c = cols.pop(atual)
            cols.insert(escolha, c)
            self.sel = ("col", escolha)
            self.pintar_arvore()
            self._selecionar_iid("c%d" % escolha)
        else:
            self._mover_colecao(escolha)
        self.pintar_form()
        self.pintar_problemas()

    def duplicar(self):
        if not self.sel:
            return
        self.snap()
        if self.sel[0] == "col":
            ci = self.sel[1]
            novo = json.loads(json.dumps(self.cat["colecoes"][ci]))
            novo["id"] = novo["id"] + "-copia"
            novo["titulo"] = novo["titulo"] + " (cópia)"
            self.cat["colecoes"].insert(ci + 1, novo)
            self.sel = ("col", ci + 1)
        else:
            _, ci, pi = self.sel
            ps = self.cat["colecoes"][ci]["projetos"]
            novo = json.loads(json.dumps(ps[pi]))
            novo["id"] = novo["id"] + "-copia"
            novo["titulo"] = novo["titulo"] + " (cópia)"
            novo["destaque"] = False
            ps.insert(pi + 1, novo)
            self.sel = ("proj", ci, pi + 1)
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()

    def excluir(self):
        if not self.sel:
            return
        if self.sel[0] == "col":
            c = self.cat["colecoes"][self.sel[1]]
            if not messagebox.askyesno(
                    "Excluir coleção",
                    "Excluir «%s» e seus %d projetos?\n\nDá para desfazer com Ctrl+Z."
                    % (c["titulo"], len(c["projetos"]))):
                return
            self.snap()
            self.cat["colecoes"].pop(self.sel[1])
        else:
            _, ci, pi = self.sel
            p = self.cat["colecoes"][ci]["projetos"][pi]
            if not messagebox.askyesno(
                    "Excluir projeto",
                    "Excluir «%s»?\n\nDica: «Ocultar do site» tira do ar sem perder o conteúdo.\n"
                    "Dá para desfazer com Ctrl+Z." % p["titulo"]):
                return
            self.snap()
            self.cat["colecoes"][ci]["projetos"].pop(pi)
        self.sel = None
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()

    def mover(self, d):
        if not self.sel:
            return
        self.snap()
        if self.sel[0] == "col":
            a = self.cat["colecoes"]
            i = self.sel[1]
            j = i + d
            if not (0 <= j < len(a)):
                self.pilha.pop()
                return
            a[i], a[j] = a[j], a[i]
            self.sel = ("col", j)
            novo_iid = "c%d" % j
        else:
            _, ci, pi = self.sel
            a = self.cat["colecoes"][ci]["projetos"]
            j = pi + d
            if not (0 <= j < len(a)):
                self.pilha.pop()
                return
            a[pi], a[j] = a[j], a[pi]
            self.sel = ("proj", ci, j)
            novo_iid = "c%dp%d" % (ci, j)
        self.pintar_arvore()
        self._selecionar_iid(novo_iid)
        self.estado()

    # ------------------------------------------------------------ problemas
    def pintar_problemas(self):
        self._probs = validar(self.cat)
        self.lst_probs.delete(0, "end")
        if not self._probs:
            self.lst_probs.insert("end", "  Tudo certo para publicar.")
            self.lst_probs.itemconfig(0, foreground="#0E6B4F")
        else:
            for msg, _, _ in self._probs:
                self.lst_probs.insert("end", "  • " + msg)
            for i in range(len(self._probs)):
                self.lst_probs.itemconfig(i, foreground="#B0233F")
        self.estado()

    def ir_para_problema(self, _=None):
        s = self.lst_probs.curselection()
        if not s or not self._probs:
            return
        _, ci, pi = self._probs[s[0]]
        self.sel = ("col", ci) if pi is None else ("proj", ci, pi)
        self._selecionar_iid("c%d" % ci if pi is None else "c%dp%d" % (ci, pi))
        self.pintar_form()

    # ------------------------------------------------------------ salvar
    def salvar(self):
        probs = validar(self.cat)
        if probs:
            if not messagebox.askyesno(
                    "Ainda há problemas",
                    "A verificação achou %d problema(s):\n\n• %s\n\nSalvar assim mesmo?"
                    % (len(probs), "\n• ".join(m for m, _, _ in probs[:6]))):
                return
        try:
            if os.path.exists(CATALOGO):
                bak = os.path.join(
                    RAIZ, "catalogo.js.bak-%s" % datetime.now().strftime("%Y%m%d-%H%M%S"))
                shutil.copy2(CATALOGO, bak)
            with open(CATALOGO, "w", encoding="utf-8", newline="\n") as f:
                f.write(serializar(self.cat))
        except Exception as e:
            messagebox.showerror("Não consegui salvar", str(e))
            return
        self.sujo = False
        self.estado("salvo em catalogo.js")
        messagebox.showinfo(
            "Salvo",
            "catalogo.js foi atualizado (com backup).\n\n"
            "O site só muda depois de publicar no GitHub:\n"
            "use o botão «Publicar (git)» ou faça commit e push você mesmo.")

    def restaurar_backup(self):
        cam = filedialog.askopenfilename(
            title="Escolha um backup", initialdir=RAIZ,
            filetypes=[("Backups", "catalogo.js.bak-*"), ("Todos", "*.*")])
        if not cam:
            return
        try:
            dados = ler_catalogo(cam)
        except Exception as e:
            messagebox.showerror("Backup inválido", str(e))
            return
        self.snap()
        self.cat = dados
        self.pintar_arvore()
        self.pintar_form()
        self.pintar_problemas()
        self.estado("backup carregado (ainda não salvo)")

    def publicar(self):
        if self.sujo:
            messagebox.showwarning("Salve antes",
                                   "Há alterações não salvas. Clique em «Salvar catálogo» primeiro.")
            return
        if not messagebox.askyesno(
                "Publicar no GitHub",
                "Vou rodar:\n\n  git add catalogo.js\n  git commit\n  git push\n\n"
                "O site atualiza cerca de 1 minuto depois. Continuar?"):
            return
        msg = "catálogo: atualiza índice"
        try:
            for cmd in (["git", "add", "catalogo.js"],
                        ["git", "commit", "-m", msg],
                        ["git", "push"]):
                r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
                if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
                    messagebox.showerror("Falhou em: %s" % " ".join(cmd),
                                         (r.stdout + "\n" + r.stderr).strip()[:900])
                    return
        except FileNotFoundError:
            messagebox.showerror("git não encontrado",
                                 "Não achei o git no PATH. Publique pelo GitHub Desktop.")
            return
        messagebox.showinfo("Publicado", "Enviado. O site atualiza em cerca de 1 minuto.")
        self.estado("publicado")

    def abrir_pasta(self):
        try:
            os.startfile(RAIZ)
        except Exception:
            messagebox.showinfo("Pasta do site", RAIZ)

    # ------------------------------------------------------------ senha
    def definir_senha(self):
        DialogoSenha(self)

    def ajuda_publicar(self):
        messagebox.showinfo(
            "Como publicar",
            "1. Edite aqui e clique em «Salvar catálogo» (faz backup automático).\n"
            "2. Clique em «Publicar (git)» — ele faz add, commit e push.\n"
            "3. Espere cerca de 1 minuto: o GitHub Pages reconstrói o site.\n\n"
            "Se preferir, pule o passo 2 e use o GitHub Desktop.")

    def ajuda_restrito(self):
        messagebox.showinfo(
            "Sobre o acesso restrito",
            "Marcar «Restrito» no catálogo é só a etiqueta que aparece no cartão.\n\n"
            "A senha de verdade fica dentro das páginas protegidas de painel_CGMOP.\n"
            "Use «Definir senha do acesso restrito…» para trocá-la em todas de uma vez.\n\n"
            "Lembre: a página é pública no GitHub. A senha é atrito, não segurança — "
            "quem abrir o código-fonte vê o conteúdo. Não reutilize senha importante.")

    def sair(self):
        if self.sujo and not messagebox.askyesno(
                "Sair sem salvar", "Há alterações não salvas. Sair mesmo assim?"):
            return
        self.destroy()


def normalizar_href(v):
    v = (v or "").strip()
    if not v:
        return ""
    if re.match(r"^https?://", v, re.I):
        return v
    if v.startswith("./"):
        return v
    if v.startswith("/"):
        return "." + v
    return "./" + v.lstrip("/")


# ----------------------------------------------------------------------------
# diálogo de senha (preenchido conforme o mecanismo real do portão)
# ----------------------------------------------------------------------------
class EscolherDestino(tk.Toplevel):
    """Lista simples de destinos, com teclado."""

    def __init__(self, pai, titulo, opcoes, atual):
        super().__init__(pai)
        self.resultado = None
        self.title("Mover")
        self.transient(pai)
        self.resizable(False, False)
        fr = ttk.Frame(self, padding=14)
        fr.pack(fill="both", expand=True)
        ttk.Label(fr, text=titulo, wraplength=420, justify="left").pack(anchor="w")
        self.lb = tk.Listbox(fr, height=min(10, len(opcoes)), width=52, activestyle="none")
        for o in opcoes:
            self.lb.insert("end", "  " + o)
        self.lb.selection_set(atual)
        self.lb.pack(fill="x", pady=(8, 10))
        self.lb.bind("<Double-Button-1>", lambda e: self.ok())
        self.lb.focus_set()
        bar = ttk.Frame(fr)
        bar.pack(fill="x")
        ttk.Button(bar, text="Mover", command=self.ok).pack(side="right")
        ttk.Button(bar, text="Cancelar", command=self.destroy).pack(side="right", padx=6)
        self.bind("<Return>", lambda e: self.ok())
        self.bind("<Escape>", lambda e: self.destroy())
        self.grab_set()
        pai.wait_window(self)

    def ok(self):
        s = self.lb.curselection()
        self.resultado = s[0] if s else None
        self.destroy()


# --- portão de senha das páginas restritas de painel_CGMOP -------------------
PORTAO_DIR = r"C:\0_Desenvolvimento\Movimentacao_pessoal\pipeline\painel"
PORTAO_JSON = os.path.join(PORTAO_DIR, ".usuarios_portao.json")
PAGINAS_PORTAO = ["anistiados.html", "index.html", "lip.html", "manual.html",
                  "painel_movimentacoes.html", "pessoal.html", "redistribuicao.html",
                  "reembolso.html"]
SAL_PORTAO = "cgmop-painel-2026"
ITER_PORTAO = 250000


def derivar_hash(usuario, senha):
    """Mesma canonização e derivação do JS do portão."""
    import hashlib
    u = (usuario or "").strip().lower()
    p = re.sub(r"[\s/.\-]", "", senha or "")
    msg = ("%s:%s" % (u, p)).encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", msg, SAL_PORTAO.encode("utf-8"),
                               ITER_PORTAO, dklen=32).hex()


class DialogoSenha(tk.Toplevel):
    def __init__(self, pai):
        super().__init__(pai)
        self.title("Senhas do acesso restrito — painel CGMOP")
        self.transient(pai)
        self.geometry("640x520")
        self.usuarios = {}

        fr = ttk.Frame(self, padding=16)
        fr.pack(fill="both", expand=True)
        ttk.Label(fr, text="Quem entra nas páginas protegidas",
                  style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(fr, wraplength=590, justify="left", style="Dica.TLabel",
                  text="Isto é ATRITO, não segurança: o HTML é público e o conteúdo está dentro "
                       "dele. A senha só desencoraja acesso casual — não reutilize senha "
                       "importante.").pack(anchor="w", pady=(2, 10))

        self.tv = ttk.Treeview(fr, columns=("u", "s"), show="headings", height=9)
        self.tv.heading("u", text="Usuário")
        self.tv.heading("s", text="Senha")
        self.tv.column("u", width=240)
        self.tv.column("s", width=240)
        self.tv.pack(fill="both", expand=True)
        self.tv.bind("<<TreeviewSelect>>", self._preencher)

        ed = ttk.Frame(fr)
        ed.pack(fill="x", pady=(8, 0))
        ttk.Label(ed, text="Usuário").grid(row=0, column=0, sticky="w")
        ttk.Label(ed, text="Senha").grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.v_u = tk.StringVar()
        self.v_s = tk.StringVar()
        ttk.Entry(ed, textvariable=self.v_u, width=28).grid(row=1, column=0, sticky="ew")
        ttk.Entry(ed, textvariable=self.v_s, width=28).grid(row=1, column=1, sticky="ew", padx=(8, 0))
        ttk.Button(ed, text="Adicionar / atualizar", command=self.add).grid(row=1, column=2, padx=8)
        ttk.Button(ed, text="Remover", command=self.rem).grid(row=1, column=3)
        ed.columnconfigure(0, weight=1)
        ed.columnconfigure(1, weight=1)

        self.lb_msg = ttk.Label(fr, text="", wraplength=590, justify="left", style="Dica.TLabel")
        self.lb_msg.pack(anchor="w", pady=(10, 0))

        bar = ttk.Frame(fr)
        bar.pack(fill="x", pady=(12, 0))
        ttk.Button(bar, text="Fechar", command=self.destroy).pack(side="right")
        self.bt_aplicar = ttk.Button(bar, text="Aplicar nas 8 páginas", command=self.aplicar)
        self.bt_aplicar.pack(side="right", padx=6)

        self.carregar()
        self.grab_set()

    # ---------- dados ----------
    def carregar(self):
        if not os.path.exists(PORTAO_JSON):
            self.bt_aplicar.state(["disabled"])
            self.lb_msg.config(
                style="Erro.TLabel",
                text="Não encontrei a lista viva de usuários em:\n%s\n\n"
                     "Ela fica fora deste repositório e é a fonte de verdade — sem ela, trocar a "
                     "senha só no HTML seria desfeito na próxima publicação do painel. "
                     "Abra o projeto do pipeline e rode publicar_cgmop.py." % PORTAO_JSON)
            return
        try:
            with open(PORTAO_JSON, "r", encoding="utf-8") as f:
                self.usuarios = json.load(f)
            if not isinstance(self.usuarios, dict):
                raise ValueError("formato inesperado")
        except Exception as e:
            self.usuarios = {}
            self.bt_aplicar.state(["disabled"])
            self.lb_msg.config(style="Erro.TLabel", text="Não consegui ler a lista: %s" % e)
            return
        self.pintar()
        self.lb_msg.config(style="Dica.TLabel",
                           text="Lista viva: %s" % PORTAO_JSON)

    def pintar(self):
        self.tv.delete(*self.tv.get_children())
        for u, s in sorted(self.usuarios.items()):
            self.tv.insert("", "end", values=(u, s))

    def _preencher(self, _=None):
        s = self.tv.selection()
        if not s:
            return
        u, senha = self.tv.item(s[0], "values")
        self.v_u.set(u)
        self.v_s.set(senha)

    def add(self):
        u = self.v_u.get().strip()
        s = self.v_s.get()
        if not u or not s:
            messagebox.showwarning("Faltou preencher", "Informe usuário e senha.", parent=self)
            return
        if re.sub(r"[\s/.\-]", "", s) == "":
            messagebox.showwarning(
                "Senha inválida",
                "O portão ignora espaços e os caracteres / . -\n"
                "Essa senha ficaria vazia. Escolha outra.", parent=self)
            return
        self.usuarios[u] = s
        self.pintar()
        self.v_u.set("")
        self.v_s.set("")

    def rem(self):
        u = self.v_u.get().strip()
        if u in self.usuarios:
            if len(self.usuarios) == 1:
                messagebox.showwarning("Não dá",
                                       "Se remover o último usuário, ninguém mais entra.",
                                       parent=self)
                return
            del self.usuarios[u]
            self.pintar()
            self.v_u.set("")
            self.v_s.set("")

    # ---------- aplicar ----------
    def aplicar(self):
        if not self.usuarios:
            return
        alvos = [os.path.join(RAIZ, "painel_CGMOP", n) for n in PAGINAS_PORTAO]
        faltando = [os.path.basename(a) for a in alvos if not os.path.exists(a)]
        if faltando:
            messagebox.showerror("Páginas ausentes",
                                 "Não achei: %s" % ", ".join(faltando), parent=self)
            return
        if not messagebox.askyesno(
                "Confirmar",
                "Vou regravar as senhas de %d usuário(s) em:\n\n"
                "• %s (lista viva)\n• as 8 páginas protegidas de painel_CGMOP\n\n"
                "Cada página recebe um backup antes. Continuar?"
                % (len(self.usuarios), os.path.basename(PORTAO_JSON)), parent=self):
            return

        self.config(cursor="watch")
        self.update()
        try:
            hashes = sorted({derivar_hash(u, s) for u, s in self.usuarios.items()})
            novo = "var HASHES=[%s]" % ", ".join('"%s"' % h for h in hashes)

            # 1) lista viva primeiro — é ela que manda na próxima publicação
            shutil.copy2(PORTAO_JSON, PORTAO_JSON + ".bak-%s"
                         % datetime.now().strftime("%Y%m%d-%H%M%S"))
            with open(PORTAO_JSON, "w", encoding="utf-8", newline="\n") as f:
                json.dump(self.usuarios, f, ensure_ascii=False, indent=2)
                f.write("\n")

            # 2) as páginas já publicadas
            padrao = re.compile(r'var HASHES=\[[^\]]*\]')
            trocadas, sem_portao = [], []
            for a in alvos:
                with open(a, "r", encoding="utf-8") as f:
                    txt = f.read()
                if not padrao.search(txt):
                    sem_portao.append(os.path.basename(a))
                    continue
                shutil.copy2(a, a + ".bak-%s" % datetime.now().strftime("%Y%m%d-%H%M%S"))
                with open(a, "w", encoding="utf-8", newline="") as f:
                    f.write(padrao.sub(novo, txt, count=1))
                trocadas.append(os.path.basename(a))
        except Exception as e:
            self.config(cursor="")
            messagebox.showerror("Falhou no meio do caminho",
                                 "%s\n\nOs backups .bak-* ficaram ao lado dos arquivos." % e,
                                 parent=self)
            return
        self.config(cursor="")

        aviso = ""
        if sem_portao:
            aviso = "\n\nSem bloco de portão (não mexi): %s" % ", ".join(sem_portao)
        messagebox.showinfo(
            "Senhas trocadas",
            "Atualizei %d página(s) e a lista viva.%s\n\n"
            "Falta publicar: as páginas de painel_CGMOP mudaram, então precisam de "
            "commit e push para valerem no site." % (len(trocadas), aviso), parent=self)


if __name__ == "__main__":
    App().mainloop()
