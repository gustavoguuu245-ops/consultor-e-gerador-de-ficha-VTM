import tkinter as tk
from tkinter import ttk, messagebox
import os
import re

from PIL import Image, ImageTk

from ui.hud_disciplina import HUDDisciplinas
from ui.hud_gerador import HUDGeradorFicha
from ui.constantes import CORES

from motor.savenpcsgerados import carregar_npcs_salvos

from dados import carregar_npcs_base, carregar_icones

from motor.dice_engine import rolar_dados

# ============================================================

ICONES_NPC = carregar_icones(categorias=['npc'])['npc']


# TODO: colocar atributos secundários como opcional para determinaçao de icone
# ex: nem todo personagem que tem taumaturgia é tremere ou deveria ter esse icone
# TODO: colocar um atributo de icone no NPC, para o usuario poder forçar um icone
# TODO: usar mais icones, expandindo além dos emoji (permitir simbolos de clã, por exemplo)
def obter_icone_npc(npc_nome:str, categoria:str, data:dict) -> str:
    nome_lower = npc_nome.lower()
    desc_lower = data.get("descricao", "").lower()
    cat_lower = categoria.lower()
    
    if "tremere" in nome_lower or "taumaturgia" in desc_lower: return ICONES_NPC["tremere"]
    if "gangrel" in nome_lower or "metamorfose" in desc_lower: return ICONES_NPC["gangrel"]
    if "toreador" in nome_lower or "presenca" in desc_lower: return ICONES_NPC["toreador"]
    if "nosferatu" in nome_lower or "ofuscacao" in desc_lower: return ICONES_NPC["nosferatu"]
    if "brujah" in nome_lower: return ICONES_NPC["brujah"]
    if "ventrue" in nome_lower or "dominacao" in desc_lower: return ICONES_NPC["ventrue"]
    if "setita" in nome_lower or "serpentis" in desc_lower: return ICONES_NPC["setita"]
    if "malkaviano" in nome_lower or "demencia" in desc_lower: return ICONES_NPC["malkaviano"]
    if "tzimisce" in nome_lower or "vicissitude" in desc_lower: return ICONES_NPC["tzimisce"]
    if "assamita" in nome_lower or "quietus" in desc_lower: return ICONES_NPC["assamita"]
    if "lasombra" in nome_lower or "tenebrosidade" in desc_lower: return ICONES_NPC["lasombra"]
    if "ravnos" in nome_lower or "quimerismo" in desc_lower: return ICONES_NPC["ravnos"]
    
    if "lobisomem" in cat_lower or "lupino" in nome_lower: return ICONES_NPC["lobisomem"]
    if "mago" in cat_lower or "mago" in nome_lower: return ICONES_NPC["mago"]
    if "fantasma" in cat_lower or "espectro" in nome_lower: return ICONES_NPC["fantasma"]
    if "fada" in cat_lower: return ICONES_NPC["fada"]
    if "principe" in nome_lower: return ICONES_NPC["principe"]
    if "red list" in cat_lower: return ICONES_NPC["redlist"]
    if "inquisicao" in cat_lower or "inquisidor" in nome_lower: return ICONES_NPC["inquisidor"]
    if "anarch" in cat_lower: return ICONES_NPC["anarch"]
    if "policial" in nome_lower: return ICONES_NPC["policial"]
    if "detetive" in nome_lower: return ICONES_NPC["detetive"]
    if "garcom" in nome_lower: return ICONES_NPC["garcom"]
    if "hacker" in nome_lower: return ICONES_NPC["hacker"]
    if "seguranca" in nome_lower: return ICONES_NPC["seguranca"]
    if "capanga" in nome_lower: return ICONES_NPC["capanga"]
    if "gangue" in nome_lower: return ICONES_NPC["gangue"]
    if "ghoul" in nome_lower or "carnical" in nome_lower: return ICONES_NPC["ghoul"]
    
    if "disciplinas" in data: return ICONES_NPC["vampiro"]
    return ICONES_NPC["default"]


def calcular_nivel_ameaca(data):
    atributos = data.get("atributos", {})
    habilidades = data.get("habilidades", {})
    
    fisicos = 0
    for attr in ["Forca", "Destreza", "Vigor"]:
        try:
            val = str(atributos.get(attr, "0")).split("/")[0]
            fisicos += int(val)
        except: pass
    
    combate = 0
    for hab in ["Briga", "Armas de Fogo", "Armas Brancas", "Esquiva"]:
        try:
            combate += int(habilidades.get(hab, 0))
        except: pass
    
    total = fisicos + combate + (5 if "disciplinas" in data else 0)
    
    if total <= 8: return ("LEVE", "#44aa44")
    elif total <= 14: return ("MEDIA", "#ffaa00")
    elif total <= 20: return ("PERIGOSA", "#ff4444")
    else: return ("LETAL", "#ff0000")


class AppGerenciadorNPC:
    def __init__(self, root):
        self.root = root
        self.root.title("Vampiro: A Mascara - Gerenciador Canonico de NPCs & Grimorio Arcano")
        self.root.geometry("1280x720")
        self.root.configure(bg=CORES["bg_principal"])
        self.root.minsize(1100, 700)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=CORES["bg_principal"], foreground=CORES["texto_principal"], font=("Helvetica", 9))
        self.style.configure("TLabelframe", background=CORES["bg_card"], foreground=CORES["vermelho_destaque"], bordercolor=CORES["borda_padrao"])
        self.style.configure("TLabelframe.Label", font=("Helvetica", 9, "bold"), foreground=CORES["vermelho_claro"], background=CORES["bg_card"])
        self.style.configure("TButton", background="#222222", foreground="#ffffff", bordercolor="#555555", font=("Helvetica", 8, "bold"))
        self.style.map("TButton", background=[("active", CORES["vermelho_sangue"])])
        self.style.configure("TCombobox", fieldbackground=CORES["bg_input"], background=CORES["bg_input"], foreground=CORES["texto_principal"])

        self.mostrar_texto_livro = tk.BooleanVar(value=False)
        self.bg_image = None
        self.historico_rolagens = []
        self.npcs_encontro = []
        
        self.carregar_assets()
        self.npcs_base = carregar_npcs_base()
        self.npcs_base.update(carregar_npcs_salvos())
        self.setup_ui()

        
    def carregar_assets(self):
        asset_path = os.path.join("assets", "moldura.png")
        if os.path.exists(asset_path):
            try:
                img_pil = Image.open(asset_path)
                img_pil = img_pil.resize((1280, 780), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img_pil)
            except Exception as e:
                print(f"Aviso ao carregar imagem: {e}")

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=1280, height=780, bg=CORES["bg_principal"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)

         # parte dos botoes 
        header = tk.Label(
            self.root, 
            text="GERENCIADOR CANONICO DE NPCs - VAMPIRO: A MASCARA (3a ED / V20 / V5 / RED LIST)", 
            font=("Georgia", 11, "bold"), 
            bg=CORES["vermelho_sangue"], 
            fg="#ffffff", 
            pady=6
        )
        self.canvas.create_window(640, 18, window=header, width=1280)

        # Container Principal expandido verticalmente
        main_frame = tk.Frame(self.root, bg=CORES["bg_principal"], bd=1, relief=tk.RIDGE)
        self.canvas.create_window(640, 375, window=main_frame, width=1240, height=650)

        # ============================================================
        # PAINEL ESQUERDO
        
        left_panel = tk.Frame(main_frame, bg=CORES["bg_card"], bd=1, relief=tk.SOLID, width=360)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 4), pady=8)
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="ARQUIVOS DA MASCARADA", bg=CORES["bg_card"], 
                fg=CORES["vermelho_claro"], font=("Georgia", 10, "bold"), pady=4).pack(fill=tk.X, padx=8)
        
        btn_disciplinas = tk.Button(
            left_panel, 
            text="Consultar Grimorio Arcano (3a Ed)", 
            command=lambda: HUDDisciplinas.abrir_janela(self.root),
            bg=CORES["vermelho_sangue"], fg="#ffffff", font=("Helvetica", 8, "bold"),
            activebackground=CORES["vermelho_destaque"], activeforeground="#ffffff",
            cursor="hand2", bd=0, padx=6, pady=4
        )
        btn_disciplinas.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Button de gerador de ficha
        btn_gerador = tk.Button(
            left_panel, 
            text="🎲 Gerador de Fichas (3a Ed / DA)", 
            command=lambda: HUDGeradorFicha.abrir_janela(self.root),
            bg="#440000", fg="#ffffff", font=("Helvetica", 8, "bold"),
            activebackground=CORES["vermelho_destaque"], activeforeground="#ffffff",
            cursor="hand2", bd=0, padx=6, pady=4
        )
        btn_gerador.pack(fill=tk.X, padx=8, pady=(0, 8))
        # Busca
        tk.Label(left_panel, text="Buscar Nome / Cla / Conceito:", bg=CORES["bg_card"], 
                fg=CORES["texto_principal"], font=("Helvetica", 8, "bold")).pack(anchor=tk.W, padx=8)
        self.ent_busca = tk.Entry(left_panel, bg=CORES["bg_input"], fg=CORES["texto_principal"], 
                                 insertbackground=CORES["texto_principal"], borderwidth=1, font=("Helvetica", 8))
        self.ent_busca.pack(fill=tk.X, padx=8, pady=(1, 4))
        self.ent_busca.bind("<KeyRelease>", self.filtrar_npcs)

        # Filtro por Edicao
        tk.Label(left_panel, text="Edicao / Fonte Canonica:", bg=CORES["bg_card"], 
                fg=CORES["texto_principal"], font=("Helvetica", 8, "bold")).pack(anchor=tk.W, padx=8)
        self.combo_edicao = ttk.Combobox(
            left_panel, 
            state="readonly", 
            values=["TODAS AS EDICOES", "3a Edicao", "V20 / Dark Ages", "V5", "Red List / V20"]
        )
        self.combo_edicao.set("TODAS AS EDICOES")
        self.combo_edicao.pack(fill=tk.X, padx=8, pady=(1, 4))
        self.combo_edicao.bind("<<ComboboxSelected>>", self.filtrar_npcs)

        # Categorias
        tk.Label(left_panel, text="Categoria de Antagonistas:", bg=CORES["bg_card"], 
                fg=CORES["texto_principal"], font=("Helvetica", 8, "bold")).pack(anchor=tk.W, padx=8)
        self.combo_categoria = ttk.Combobox(
            left_panel, 
            state="readonly", 
            values=["TODAS AS CATEGORIAS"] + list(self.npcs_base.keys())
        )
        self.combo_categoria.set("TODAS AS CATEGORIAS")
        self.combo_categoria.pack(fill=tk.X, padx=8, pady=(1, 4))
        self.combo_categoria.bind("<<ComboboxSelected>>", self.filtrar_npcs)

        # Lista Painel Esquerdo com altura controlada
        tk.Label(left_panel, text="Selecione o Dossie:", bg=CORES["bg_card"], 
                fg=CORES["texto_principal"], font=("Helvetica", 8, "bold")).pack(anchor=tk.W, padx=8)
        
        frame_lista = tk.Frame(left_panel, bg=CORES["bg_card"])
        frame_lista.pack(fill=tk.X, padx=8, pady=(1, 4))
        
        scrollbar_list = tk.Scrollbar(frame_lista, bg=CORES["bg_input"], troughcolor=CORES["bg_card"])
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_npcs = tk.Listbox(
            frame_lista, 
            bg=CORES["bg_input"], 
            fg=CORES["texto_principal"], 
            selectbackground=CORES["vermelho_sangue"], 
            selectforeground="#ffffff", 
            borderwidth=0,
            font=("Consolas", 8),
            height=18, # parte para configurar o lado esquerdo altura do dossie e rolagem dos dados
            yscrollcommand=scrollbar_list.set
        )
        self.listbox_npcs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_list.config(command=self.listbox_npcs.yview)
        self.listbox_npcs.bind("<<ListboxSelect>>", self.exibir_npc_selecionado)

        # Rolador D10 FIXO rolagem de dados
        rolador_box = tk.LabelFrame(left_panel, text=" Rolador Storyteller D10 ", 
                                   bg=CORES["bg_card"], fg=CORES["vermelho_claro"], 
                                   font=("Helvetica", 8, "bold"), padx=6, pady=4)
        rolador_box.pack(fill=tk.X, padx=8, pady=(4, 8))

        f_inputs = tk.Frame(rolador_box, bg=CORES["bg_card"])
        f_inputs.pack(fill=tk.X)
        
        tk.Label(f_inputs, text="Dados:", bg=CORES["bg_card"], fg=CORES["texto_secundario"], font=("Helvetica", 8)).grid(row=0, column=0, sticky=tk.W)
        self.ent_dados = tk.Spinbox(f_inputs, from_=1, to=25, width=4, bg=CORES["bg_input"], fg=CORES["texto_principal"], buttonbackground="#333333", font=("Consolas", 8))
        self.ent_dados.delete(0, tk.END)
        self.ent_dados.insert(0, "5")
        self.ent_dados.grid(row=0, column=1, padx=2)

        tk.Label(f_inputs, text="Dif:", bg=CORES["bg_card"], fg=CORES["texto_secundario"], font=("Helvetica", 8)).grid(row=0, column=2, sticky=tk.W, padx=(6, 0))
        self.ent_dif = tk.Spinbox(f_inputs, from_=2, to=10, width=4, bg=CORES["bg_input"], fg=CORES["texto_principal"], buttonbackground="#333333", font=("Consolas", 8))
        self.ent_dif.delete(0, tk.END)
        self.ent_dif.insert(0, "6")
        self.ent_dif.grid(row=0, column=3, padx=2)

        btn_rolar = tk.Button(rolador_box, text="ROLAR TESTE", command=self.executar_rolagem,
                             bg=CORES["vermelho_sangue"], fg="#ffffff", font=("Helvetica", 8, "bold"),
                             activebackground=CORES["vermelho_destaque"], bd=0, padx=4, pady=3, cursor="hand2")
        btn_rolar.pack(fill=tk.X, pady=(3, 0))

        self.lbl_resultado = tk.Label(rolador_box, text="Aguardando rolagem...", bg=CORES["bg_card"], 
                                     fg=CORES["texto_dourado"], font=("Consolas", 8, "italic"))
        self.lbl_resultado.pack(pady=2)

        # ============================================================
        # PAINEL DIREITO
        
        right_panel = tk.Frame(main_frame, bg=CORES["bg_card"], bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 8), pady=8)

        # Header do Card Superior
        self.card_header = tk.Frame(right_panel, bg=CORES["bg_header"], bd=1, relief=tk.SOLID)
        self.card_header.pack(fill=tk.X, padx=8, pady=(8, 4))
        
        self.lbl_nome_npc = tk.Label(self.card_header, text="Selecione um NPC", bg=CORES["bg_header"], 
                                    fg=CORES["vermelho_claro"], font=("Georgia", 13, "bold"))
        self.lbl_nome_npc.pack(anchor=tk.W, padx=8, pady=(4, 1))
        
        self.lbl_info_rapida = tk.Label(self.card_header, text="", bg=CORES["bg_header"], 
                                       fg=CORES["texto_secundario"], font=("Helvetica", 8))
        self.lbl_info_rapida.pack(anchor=tk.W, padx=8, pady=(0, 2))

        self.lbl_reserva_rapida = tk.Label(self.card_header, text="", bg=CORES["vermelho_sangue"], 
                                          fg="#ffffff", font=("Helvetica", 9, "bold"), padx=6, pady=3, anchor="w", justify=tk.LEFT)
        self.lbl_reserva_rapida.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Botoes de Acao
        frame_botoes = tk.Frame(right_panel, bg=CORES["bg_card"])
        frame_botoes.pack(fill=tk.X, padx=8, pady=2)
        
        self.btn_copiar = tk.Button(frame_botoes, text="Copiar Ficha", command=self.copiar_ficha,
                                   bg="#222", fg=CORES["texto_principal"], font=("Helvetica", 8),
                                   activebackground=CORES["vermelho_sangue"], bd=1, padx=8, pady=3, cursor="hand2")
        self.btn_copiar.pack(side=tk.LEFT, padx=(0, 4))
        
        self.btn_adicionar_encontro = tk.Button(frame_botoes, text="Add ao Encontro", command=self.adicionar_encontro,
                                               bg=CORES["vermelho_sangue"], fg="#ffffff", font=("Helvetica", 8, "bold"),
                                               activebackground=CORES["vermelho_destaque"], bd=0, padx=8, pady=3, cursor="hand2")
        self.btn_adicionar_encontro.pack(side=tk.LEFT, padx=(0, 4))
        
        self.btn_lore = tk.Button(
            frame_botoes, 
            text="Ver Lore", 
            command=self.abrir_janela_lore,
            bg="#222", 
            fg=CORES["texto_principal"], 
            font=("Helvetica", 8),
            activebackground=CORES["vermelho_sangue"], 
            bd=1, 
            padx=8, 
            pady=3, 
            cursor="hand2"
        )
        self.btn_lore.pack(side=tk.LEFT)

        # Texto da Ficha 
        frame_texto = tk.Frame(right_panel, bg=CORES["bg_card"])
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        scrollbar_ficha = tk.Scrollbar(frame_texto)
        scrollbar_ficha.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_ficha = tk.Text(
            frame_texto, 
            bg=CORES["bg_card"], 
            fg=CORES["texto_principal"], 
            font=("Consolas", 10), 
            wrap=tk.WORD, 
            borderwidth=0,
            insertbackground=CORES["texto_principal"],
            spacing3=4, 
            yscrollcommand=scrollbar_ficha.set
        )
        self.txt_ficha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 10))

        def _on_mousewheel(event):
            self.txt_ficha.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.txt_ficha.bind("<MouseWheel>", _on_mousewheel)

        self.filtrar_npcs(None)

    def _converter_para_dots(self, valor, maximo=5):
        try:
            val_str = str(valor).split("/")[0]
            val_int = int(val_str)
            return f"{'●' * val_int}{'○' * (maximo - val_int)} ({val_int})"
        except ValueError:
            return str(valor)

    def obter_lista_filtrada(self):
        termo = self.ent_busca.get().lower().strip()
        edicao_sel = self.combo_edicao.get()
        cat_sel = self.combo_categoria.get()

        resultados = []

        for cat, npcs in self.npcs_base.items():
            if cat_sel != "TODAS AS CATEGORIAS" and cat != cat_sel:
                continue
            
            for npc_nome, data in npcs.items():
                desc = data.get("descricao", "").lower()
                
                if termo and (termo not in npc_nome.lower() and termo not in desc):
                    continue
                
                if edicao_sel != "TODAS AS EDICOES":
                    ed_npc = data.get("edicao", "3a Edicao").lower()
                    if edicao_sel == "3a Edicao" and not ("3a" in ed_npc or "third" in ed_npc or "generica" in ed_npc): continue
                    elif edicao_sel == "V20 / Dark Ages" and not ("v20" in ed_npc or "dark ages" in ed_npc): continue
                    elif edicao_sel == "V5" and not ("v5" in ed_npc or "5a" in ed_npc): continue
                    elif edicao_sel == "Red List / V20" and not ("red list" in ed_npc or "procurado" in ed_npc): continue

                resultados.append((npc_nome, cat, data))
                
        return resultados

    def filtrar_npcs(self, event=None):
        self.listbox_npcs.delete(0, tk.END)
        self.npcs_filtrados = self.obter_lista_filtrada()

        for npc_nome, cat, data in self.npcs_filtrados:
            icone = obter_icone_npc(npc_nome, cat, data)
            reserva = data.get("reserva_padrao", "")
            dados_str = ""
            match = re.search(r'(\d+)\s*dados', reserva.lower())
            if match:
                dados_str = f" ({match.group(1)}d)"
            
            self.listbox_npcs.insert(tk.END, f"{icone} {npc_nome}{dados_str}")

        if self.npcs_filtrados:
            self.listbox_npcs.selection_set(0)
            self.exibir_npc_selecionado(None)

    def exibir_npc_selecionado(self, event=None):
        sel = self.listbox_npcs.curselection()
        if not sel or not hasattr(self, 'npcs_filtrados') or not self.npcs_filtrados:
            return

        idx = sel[0]
        npc_nome, cat, data = self.npcs_filtrados[idx]
        self.npc_atual = (npc_nome, cat, data)

        ameaca, cor_ameaca = calcular_nivel_ameaca(data)
        icone = obter_icone_npc(npc_nome, cat, data)
        
        self.lbl_nome_npc.config(text=f"{icone} {npc_nome.upper()}")
        
        edicao = data.get("edicao", "Generica")
        self.lbl_info_rapida.config(text=f"AMEACA: {ameaca}  |  EDICAO: {edicao}  |  CATEGORIA: {cat}")
        
        reserva = data.get("reserva_padrao", "Consulte o livro")
        self.lbl_reserva_rapida.config(text=f"RESERVA: {reserva}")

        # Montar texto completo
        texto = f"{'='*65}\n"
        texto += f" DOSSIE CONFIDENCIAL: {npc_nome.upper()}\n"
        texto += f"{'='*65}\n\n"
        
        texto += f"DESCRICAO / CONCEITO:\n{data.get('descricao', 'N/A')}\n\n"

        texto += "ATRIBUTOS CANONICOS\n"
        texto += f"{'-'*45}\n"
        atrs = data.get("atributos", {})
        
        fisicos = ["Força", "Destreza", "Vigor"]
        sociais = ["Carisma", "Manipulação", "Aparência"]
        mentais = ["Percepção", "Inteligência", "Raciocínio"]
        
        fis_str = [f"• {k}: {self._converter_para_dots(atrs[k])}" for k in fisicos if k in atrs]
        if fis_str: texto += "  FISICOS: " + " | ".join(fis_str) + "\n"
        
        soc_str = [f"• {k}: {self._converter_para_dots(atrs[k])}" for k in sociais if k in atrs]
        if soc_str: texto += "  SOCIAIS: " + " | ".join(soc_str) + "\n"
            
        men_str = [f"• {k}: {self._converter_para_dots(atrs[k])}" for k in mentais if k in atrs]
        if men_str: texto += "  MENTAIS: " + " | ".join(men_str) + "\n"

        texto += f"\nHABILIDADES DE DESTAQUE\n"
        texto += f"{'-'*45}\n"
        habs = data.get("habilidades", {})
        for k, v in habs.items():
            texto += f"  • {k:<18}: {self._converter_para_dots(v)}\n"

        texto += f"\n{'='*65}\n"
        if "disciplinas" in data: texto += f"DISCIPLINAS / PODERES: {data['disciplinas']}\n"
        if "humanidade" in data:   texto += f"HUMANIDADE / TRILHA   : {data['humanidade']}\n"
        texto += f"VITALIDADE            : {data.get('vitalidade', 7)} Niveis\n"
        texto += f"FORCA DE VONTADE      : {data.get('forca_de_vontade', 3)}\n"
        if "equipamento" in data: texto += f"EQUIPAMENTO / ARMAS   : {data['equipamento']}\n"
        texto += "\n\n\n"
        if self.mostrar_texto_livro.get() and "texto_livro" in data:
            texto += f"\n{'='*65}\n"
            texto += f"LORE & REGISTRO INTEGRAL DO LIVRO:\n"
            texto += f"{'='*65}\n"
            texto += f"{data['texto_livro']}\n"

        self.txt_ficha.delete("1.0", tk.END)
        self.txt_ficha.insert(tk.END, texto)
        self.txt_ficha.yview_moveto(0)

    def executar_rolagem(self):
        try:
            qtd = int(self.ent_dados.get())
            dif = int(self.ent_dif.get())
            res = rolar_dados(qtd, dif)
            
            txt = f"[{', '.join(map(str, res['resultados']))}] | {res['mensagem']}"
            cor = CORES["verde_sucesso"] if res['sucessos'] > 0 else (CORES["amarelo_atencao"] if res['mensagem'] == "Falha Simples" else CORES["vermelho_falha"])
            self.lbl_resultado.config(text=txt, fg=cor)
            
        except ValueError:
            messagebox.showerror("Erro", "Insira numeros validos para os dados e a dificuldade.")

    def copiar_ficha(self):
        if not hasattr(self, 'npc_atual'): 
            messagebox.showwarning("Aviso", "Selecione um NPC primeiro!")
            return
            
      
        texto_completo = self.txt_ficha.get("1.0", tk.END).strip()
        
        if texto_completo:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto_completo)
            messagebox.showinfo(
                "Ficha Copiada!", 
                "A ficha completa do dossier foi copiada para a área de transferência!\nPronta para colar no Discord, WhatsApp ou Bloco de Notas."
            )
        else:
            messagebox.showwarning("Aviso", "A ficha selecionada está vazia.")

    def adicionar_encontro(self):
        if not hasattr(self, 'npc_atual'): return
        self.npcs_encontro.append(self.npc_atual)
        messagebox.showinfo("Encontro", f"{self.npc_atual[0]} adicionado ao encontro!\nTotal: {len(self.npcs_encontro)}")

    def abrir_janela_lore(self):
        """Abre uma nova janela popup com a Lore integral do NPC"""
        if not hasattr(self, 'npc_atual'):
            messagebox.showwarning("Aviso", "Selecione um NPC primeiro!")
            return

        npc_nome, cat, data = self.npc_atual
        texto_livro = data.get("texto_livro", "Nenhuma Lore detalhada registrada para este NPC.")

        # Criar Janela
        janela_lore = tk.Toplevel(self.root)
        janela_lore.title(f"Lore & Registro Canonico - {npc_nome.upper()}")
        janela_lore.geometry("700x500")
        janela_lore.configure(bg=CORES["bg_principal"])

        
        lbl_titulo = tk.Label(
            janela_lore, 
            text=f"📖 LORE INTEGRAL: {npc_nome.upper()}", 
            bg=CORES["vermelho_sangue"], 
            fg="#ffffff", 
            font=("Georgia", 11, "bold"),
            pady=8
        )
        lbl_titulo.pack(fill=tk.X)

      
        frame_corpo = tk.Frame(janela_lore, bg=CORES["bg_card"], padx=10, pady=10)
        frame_corpo.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_corpo)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        txt_lore = tk.Text(
            frame_corpo, 
            bg=CORES["bg_input"], 
            fg=CORES["texto_principal"], 
            font=("Consolas", 10), 
            wrap=tk.WORD, 
            borderwidth=1,
            relief=tk.SOLID,
            insertbackground="#ffffff",
            yscrollcommand=scrollbar.set
        )
        txt_lore.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=txt_lore.yview)

        # Inserir o texto da Lore 
        txt_lore.insert(tk.END, texto_livro)
        txt_lore.config(state=tk.DISABLED)

        # Scroll do mouse na popup
        txt_lore.bind("<MouseWheel>", lambda e: txt_lore.yview_scroll(int(-1 * (e.delta / 120)), "units"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGerenciadorNPC(root)
    root.mainloop()