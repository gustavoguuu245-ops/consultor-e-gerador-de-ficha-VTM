import tkinter as tk
from tkinter import ttk, messagebox
import random
from motor.savenpcsgerados import salvar_npc_em_disco

# Importar o motor de geração
try:
    from motor.gerador_ficha import (
        gerar_ficha, formatar_ficha_texto, REGRAS, CLAS, 
        EDICOES, NATUREZAS, CONCEITOS
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from motor.gerador_ficha import (
        gerar_ficha, formatar_ficha_texto, REGRAS, CLAS,
        EDICOES, NATUREZAS, CONCEITOS
    )

# Importar o banco de dados unificado de NPCs
from dados import carregar_npcs_base
NPCS_BASE = carregar_npcs_base()

CORES = {
    "bg_principal": "#0a0a0c",
    "bg_card": "#111115",
    "bg_input": "#0d0d11",
    "bg_header": "#1a0000",
    "vermelho_sangue": "#660000",
    "vermelho_destaque": "#cc0000",
    "vermelho_claro": "#ff4444",
    "texto_principal": "#e0e0e0",
    "texto_secundario": "#888888",
    "texto_dourado": "#ffcc00",
    "borda_padrao": "#333333",
    "verde_sucesso": "#00ff88",
}


class HUDGeradorFicha:
    """Janela Pop-up para Geração de Fichas de Personagem"""
    
    @classmethod
    def abrir_janela(cls, parent):
        """Abre a janela de geração de fichas"""
        top = tk.Toplevel(parent)
        top.title("Gerador de Fichas - Vampiro: A Máscara")
        top.geometry("900x700")
        top.configure(bg=CORES["bg_principal"])
        top.transient(parent)

        # -------------------------------------------------------------
        # FIX DO BUG DE TEXTO QUE SUMIA NAS COMBOBOXES (Ttk Style Fix)
        # -------------------------------------------------------------
        style = ttk.Style(top)
        style.theme_use("clam")
        
        style.configure("TCombobox",
                        fieldbackground=CORES["bg_input"],
                        background="#222222",
                        foreground=CORES["texto_principal"],
                        darkcolor=CORES["borda_padrao"],
                        lightcolor=CORES["borda_padrao"],
                        arrowcolor=CORES["texto_principal"])

        style.map("TCombobox",
                  fieldbackground=[("readonly", CORES["bg_input"]), ("focus", CORES["bg_input"])],
                  foreground=[("readonly", CORES["texto_principal"]), ("focus", CORES["texto_principal"])],
                  selectbackground=[("readonly", CORES["vermelho_sangue"]), ("focus", CORES["vermelho_sangue"])],
                  selectforeground=[("readonly", "#ffffff"), ("focus", "#ffffff")])
        # -------------------------------------------------------------
        
        # Header
        header = tk.Label(
            top,
            text="🎲 GERADOR DE FICHAS - VAMPIRO: A MÁSCARA",
            font=("Georgia", 12, "bold"),
            bg=CORES["vermelho_sangue"],
            fg="#ffffff",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Container principal
        main = tk.Frame(top, bg=CORES["bg_principal"], padx=15, pady=10)
        main.pack(fill=tk.BOTH, expand=True)
        
        # ========== PAINEL ESQUERDO: CONFIGURAÇÕES ==========
        left = tk.Frame(main, bg=CORES["bg_card"], bd=1, relief=tk.SOLID, width=380)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        
        # --- Seleção de Edição ---
        tk.Label(left, text="EDIÇÃO / SISTEMA", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 9, "bold"), pady=5).pack(fill=tk.X, padx=10)
        
        combo_edicao = ttk.Combobox(left, state="readonly", width=35, font=("Helvetica", 9))
        combo_edicao['values'] = [
            "3ª Edição (Moderno)",
            "Dark Ages (Idade das Trevas)",
        ]
        combo_edicao.set("3ª Edição (Moderno)")
        combo_edicao.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # --- Tipo de Personagem ---
        tk.Label(left, text="TIPO DE PERSONAGEM", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 9, "bold"), pady=5).pack(fill=tk.X, padx=10)
        
        combo_tipo = ttk.Combobox(left, state="readonly", width=35, font=("Helvetica", 9))
        combo_tipo.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # --- Clã ---
        tk.Label(left, text="CLÃ", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 9, "bold"), pady=5).pack(fill=tk.X, padx=10)
        
        combo_cla = ttk.Combobox(left, state="readonly", width=35, font=("Helvetica", 9))
        combo_cla.pack(fill=tk.X, padx=10, pady=(0, 5))

        def atualizar_clas(*args):
            ed = combo_edicao.get()
            tipo = combo_tipo.get()
            cla_anterior = combo_cla.get()
            
            if "Humano" in tipo or "Carniçal" in tipo:
                combo_cla['values'] = ["Nenhum"]
                combo_cla.set("Nenhum")
                combo_cla.config(state="disabled")
            else:
                combo_cla.config(state="readonly")
                if "3ª" in ed:
                    novos_valores = sorted(CLAS["3a_edicao"].keys())
                else:
                    novos_valores = sorted(CLAS["dark_ages"].keys())
                
                combo_cla['values'] = novos_valores
                
                # Se o clã selecionado antes ainda existir na nova lista, mantém ele.
                if cla_anterior in novos_valores:
                    combo_cla.set(cla_anterior)
                else:
                    combo_cla.set(novos_valores[0] if novos_valores else "Brujah")
        
        def atualizar_tipos(*args):
            tipo_anterior = combo_tipo.get()
            opcoes_tipos = [
                "Neófito",
                "Ancilla (50-100 anos)",
                "Ancião (100-200 anos)",
                "Metusalém (1000+ anos)",
                "Humano",
                "Carniçal"
            ]
            combo_tipo['values'] = opcoes_tipos
            
            if tipo_anterior in opcoes_tipos:
                combo_tipo.set(tipo_anterior)
            else:
                combo_tipo.set("Neófito")
                
            atualizar_clas()
        
        combo_edicao.bind("<<ComboboxSelected>>", atualizar_tipos)
        combo_tipo.bind("<<ComboboxSelected>>", atualizar_clas)
        
        # --- Foco ---
        tk.Label(left, text="FOCO DO PERSONAGEM", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 9, "bold"), pady=5).pack(fill=tk.X, padx=10)
        
        combo_foco = ttk.Combobox(left, state="readonly", width=35, font=("Helvetica", 9))
        combo_foco['values'] = ["Automático (baseado no clã)", "Físico", "Social", "Mental", "Aleatório"]
        combo_foco.set("Automático (baseado no clã)")
        combo_foco.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # --- Dados Narrativos ---
        tk.Label(left, text="DADOS NARRATIVOS", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 9, "bold"), pady=5).pack(fill=tk.X, padx=10)
        
        # Nome
        f_nome = tk.Frame(left, bg=CORES["bg_card"])
        f_nome.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_nome, text="Nome:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_nome = tk.Entry(f_nome, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                           insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_nome.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Jogador
        f_jogador = tk.Frame(left, bg=CORES["bg_card"])
        f_jogador.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_jogador, text="Jogador:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_jogador = tk.Entry(f_jogador, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                              insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_jogador.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Crônica
        f_cronica = tk.Frame(left, bg=CORES["bg_card"])
        f_cronica.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_cronica, text="Crônica:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_cronica = tk.Entry(f_cronica, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                              insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_cronica.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Natureza
        f_natureza = tk.Frame(left, bg=CORES["bg_card"])
        f_natureza.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_natureza, text="Natureza:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        combo_natureza = ttk.Combobox(f_natureza, values=["Aleatório"] + sorted(NATUREZAS), 
                                      state="readonly", font=("Helvetica", 8))
        combo_natureza.set("Aleatório")
        combo_natureza.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Comportamento
        f_comp = tk.Frame(left, bg=CORES["bg_card"])
        f_comp.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_comp, text="Comportamento:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        combo_comp = ttk.Combobox(f_comp, values=["Aleatório"] + sorted(NATUREZAS),
                                  state="readonly", font=("Helvetica", 8))
        combo_comp.set("Aleatório")
        combo_comp.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Idade Mortal / Geração
        f_idade = tk.Frame(left, bg=CORES["bg_card"])
        f_idade.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_idade, text="Idade Mortal:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_idade = tk.Entry(f_idade, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                            insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_idade.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Sexo
        f_sexo = tk.Frame(left, bg=CORES["bg_card"])
        f_sexo.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_sexo, text="Sexo:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        combo_sexo = ttk.Combobox(f_sexo, values=["Aleatório", "Masculino", "Feminino", "Não-binário"],
                                  state="readonly", font=("Helvetica", 8))
        combo_sexo.set("Aleatório")
        combo_sexo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Nacionalidade
        f_nac = tk.Frame(left, bg=CORES["bg_card"])
        f_nac.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_nac, text="Nacionalidade:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_nac = tk.Entry(f_nac, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                          insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_nac.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Senhor
        f_senhor = tk.Frame(left, bg=CORES["bg_card"])
        f_senhor.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f_senhor, text="Senhor:", bg=CORES["bg_card"], fg=CORES["texto_principal"],
                font=("Helvetica", 8), width=12, anchor=tk.W).pack(side=tk.LEFT)
        ent_senhor = tk.Entry(f_senhor, bg=CORES["bg_input"], fg=CORES["texto_principal"],
                             insertbackground=CORES["texto_principal"], font=("Helvetica", 8))
        ent_senhor.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # --- Botões de Ação ---
        f_botoes = tk.Frame(left, bg=CORES["bg_card"], pady=10)
        f_botoes.pack(fill=tk.X, padx=10)
        
        # Botão Gerar
        btn_gerar = tk.Button(
            f_botoes,
            text="🎲 GERAR FICHA",
            bg=CORES["vermelho_destaque"],
            fg="#ffffff",
            font=("Helvetica", 10, "bold"),
            activebackground=CORES["vermelho_claro"],
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_gerar.pack(fill=tk.X, pady=(0, 5))
        
        # Botão Salvar
        btn_salvar = tk.Button(
            f_botoes,
            text="💾 SALVAR FICHA NA LISTA",
            bg="#222",
            fg=CORES["texto_principal"],
            font=("Helvetica", 9, "bold"),
            activebackground=CORES["vermelho_sangue"],
            bd=1,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn_salvar.pack(fill=tk.X, pady=(0, 5))
        
        # Botão Exportar
        btn_exportar = tk.Button(
            f_botoes,
            text="📋 COPIAR PARA ÁREA DE TRANSFERÊNCIA",
            bg="#222",
            fg=CORES["texto_principal"],
            font=("Helvetica", 9),
            activebackground=CORES["vermelho_sangue"],
            bd=1,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn_exportar.pack(fill=tk.X)
        
        # ========== PAINEL DIREITO: RESULTADO ==========
        right = tk.Frame(main, bg=CORES["bg_card"], bd=1, relief=tk.SOLID)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="FICHA GERADA", bg=CORES["bg_card"],
                fg=CORES["vermelho_claro"], font=("Helvetica", 10, "bold"), pady=5).pack(fill=tk.X)
        
        # Área de texto com scrollbar
        frame_txt = tk.Frame(right, bg=CORES["bg_card"])
        frame_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_txt)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        txt_resultado = tk.Text(
            frame_txt,
            bg=CORES["bg_input"],
            fg=CORES["texto_principal"],
            font=("Consolas", 9),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            insertbackground="#ffffff"
        )
        txt_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=txt_resultado.yview)
        
        # Variável para armazenar ficha atual
        ficha_atual = [None]
        fichas_salvas = []  # Lista de fichas salvas
        
        # ========== FUNÇÕES DOS BOTÕES ==========
        
        def _mapear_tipo(edicao, tipo_str):
            """Mapeia seleção da UI para chave do REGRAS"""
            is_3a = "3ª" in edicao
            
            if "Neófito" in tipo_str:
                return "neofito_3a" if is_3a else "neofito_da"
            elif "Ancilla" in tipo_str:
                return "ancilla_3a" if is_3a else "ancilla_da"
            elif "Ancião" in tipo_str:
                return "anciao_3a" if is_3a else "anciao_da"
            elif "Metusalém" in tipo_str:
                return "matusalem_3a" if is_3a else "matusalem_da"
            elif "Humano" in tipo_str:
                return "humano_3a" if is_3a else "humano_da"
            elif "Carniçal" in tipo_str:
                return "carnical_3a" if is_3a else "carnical_da"
            return "neofito_3a"
        
        def _mapear_foco(foco_str, cla_nome, edicao):
            """Mapeia foco da UI para valor do motor"""
            if foco_str == "Automático (baseado no clã)":
                if edicao == "3a_edicao" and cla_nome in CLAS["3a_edicao"]:
                    return CLAS["3a_edicao"][cla_nome]["foco"]
                elif edicao == "dark_ages" and cla_nome in CLAS["dark_ages"]:
                    return CLAS["dark_ages"][cla_nome]["foco"]
                return "aleatorio"
            return foco_str.lower()
        
        def gerar():
            try:
                # Coletar dados
                ed = combo_edicao.get()
                tipo_str = combo_tipo.get()
                cla_nome = combo_cla.get() if combo_cla['state'] != 'disabled' else None
                foco_str = combo_foco.get()
                
                nome = ent_nome.get().strip() or f"Personagem_{random.randint(1000,9999)}"
                
                natureza = combo_natureza.get()
                if natureza == "Aleatório":
                    natureza = None
                
                comp = combo_comp.get()
                if comp == "Aleatório":
                    comportamento = None
                else:
                    comportamento = comp
                
                sexo = combo_sexo.get()
                if sexo == "Aleatório":
                    sexo = random.choice(["Masculino", "Feminino"])
                
                # Mapear tipo
                tipo_key = _mapear_tipo(ed, tipo_str)
                
                # Mapear foco
                ed_key = "3a_edicao" if "3ª" in ed else "dark_ages"
                foco = _mapear_foco(foco_str, cla_nome or "", ed_key)
                
                # Gerar ficha
                ficha = gerar_ficha(
                    tipo_personagem=tipo_key,
                    nome=nome,
                    cla=cla_nome if cla_nome != "Nenhum" else None,
                    foco=foco,
                    natureza=natureza,
                    comportamento=comportamento,
                    jogador=ent_jogador.get(),
                    cronica=ent_cronica.get(),
                    nacionalidade=ent_nac.get(),
                    idade_mortal=ent_idade.get(),
                    sexo=sexo,
                    senhor=ent_senhor.get()
                )
                
                ficha_atual[0] = ficha
                
                # Exibir
                texto = formatar_ficha_texto(ficha)
                txt_resultado.delete("1.0", tk.END)
                txt_resultado.insert(tk.END, texto)
                
                # Atualizar título
                top.title(f"Ficha: {nome} - {ficha['cla']} ({ficha['tipo']})")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar ficha:\n{str(e)}")
        
        def salvar():
            if ficha_atual[0] is None:
                messagebox.showwarning("Aviso", "Gere uma ficha primeiro!")
                return
            
            f_data = ficha_atual[0]
            nome_npc = f_data["nome"]
            cat_destino = "Personagens Criados (Gerador)"
            
            # Garantir existência da categoria em memória
            if cat_destino not in NPCS_BASE:
                NPCS_BASE[cat_destino] = {}

            # Estrutura tratada para a interface
            dados_npc_formatados = {
                "edicao": f_data["tipo"],
                "descricao": f"Personagem Gerado. Conceito: {f_data['conceito']} | Natureza: {f_data['natureza']}",
                "atributos": f_data["atributos"],
                "habilidades": f_data["habilidades"],
                "vitalidade": f_data["vitalidade"],
                "forca_de_vontade": f_data.get("forca_vontade", f_data.get("forca_de_vontade", 3)),
                "humanidade": f_data["humanidade"],
                "reserva_padrao": f"Consulte a Ficha Gerada de {nome_npc}"
            }

            if f_data.get("disciplinas"):
                dados_npc_formatados["disciplinas"] = ", ".join([f"{k} {v}" for k, v in f_data["disciplinas"].items()])

            # 1. Salvar na Memória RAM
            NPCS_BASE[cat_destino][nome_npc] = dados_npc_formatados

            # 2. Gravar no Arquivo JSON no Disco
            salvar_npc_em_disco(nome_npc, dados_npc_formatados)

            # 3. Recarregar as categorias da tela principal (se a janela pai for o App)
            try:
                app_main = parent.winfo_toplevel()
                if hasattr(app_main, 'combo_categoria'):
                    categorias_atualizadas = ["TODAS AS CATEGORIAS"] + list(NPCS_BASE.keys())
                    app_main.combo_categoria['values'] = categorias_atualizadas
                    app_main.filtrar_npcs()
            except Exception:
                pass

            messagebox.showinfo(
                "Ficha Salva com Sucesso!", 
                f"O personagem '{nome_npc}' foi salvo no arquivo 'dados/npcs_customizados.json'!\n\nEle estará disponível sempre que abrir o programa."
            )
        
        def exportar():
            if ficha_atual[0] is None:
                messagebox.showwarning("Aviso", "Gere uma ficha primeiro!")
                return
            
            texto = formatar_ficha_texto(ficha_atual[0])
            top.clipboard_clear()
            top.clipboard_append(texto)
            messagebox.showinfo("Copiado!", "Ficha copiada para a área de transferência!")
        
        # Conectar botões
        btn_gerar.config(command=gerar)
        btn_salvar.config(command=salvar)
        btn_exportar.config(command=exportar)
        
        # Inicializar
        atualizar_tipos()
        
        return top, fichas_salvas