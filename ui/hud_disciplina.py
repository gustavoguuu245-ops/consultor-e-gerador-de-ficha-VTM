import tkinter as tk
from tkinter import ttk

from dados import carregar_disciplinas

# Dicionario Integrado de Lore & Perfis Narrativos (3a Edicao)
DISCIPLINAS_LORE = carregar_disciplinas(["lore"])["lore"]

class HUDDisciplinas:
    """Janela Pop-up Autonoma para Consulta Disciplinas (3a Edicao)"""

    PODERES_3ED_DETALHADO = carregar_disciplinas(["detalhes"])["detalhes"]

    @classmethod
    def abrir_janela(cls, parent):
        """Abre a Janela Pop-up de Consulta Arcanum de Disciplinas"""
        top = tk.Toplevel(parent)
        top.title("Consulta de Disciplinas(3a Edicao)")
        top.geometry("900x580")
        top.configure(bg="#0a0a0c")
        top.transient(parent)
        top.grab_set()

        # Header Superior Gotico
        header = tk.Label(
            top, 
            text="CONSULTA CANONICA DE DISCIPLINAS & PODERES (3a ED)", 
            font=("Georgia", 11, "bold"), 
            bg="#5a0000", 
            fg="#ffffff", 
            pady=8
        )
        header.pack(fill=tk.X)

        # Painel de Selecao Superior
        f_filtros = tk.Frame(top, bg="#0a0a0c", pady=10, padx=10)
        f_filtros.pack(fill=tk.X)

        tk.Label(f_filtros, text="Edicao:", bg="#0a0a0c", fg="#ffffff", font=("Helvetica", 9, "bold")).grid(row=0, column=0, padx=(0, 5))
        combo_edicao = ttk.Combobox(f_filtros, state="readonly", values=["3a Edicao (Canonico)"], width=22)
        combo_edicao.set("3a Edicao (Canonico)")
        combo_edicao.grid(row=0, column=1, padx=(0, 15))

        tk.Label(f_filtros, text="Selecione a Disciplina:", bg="#0a0a0c", fg="#ffffff", font=("Helvetica", 9, "bold")).grid(row=0, column=2, padx=(0, 5))
        
        lista_disc = list(DISCIPLINAS_LORE.keys())
        combo_disc = ttk.Combobox(f_filtros, state="readonly", values=lista_disc, width=22)
        combo_disc.set(lista_disc[0] if lista_disc else "")
        combo_disc.grid(row=0, column=3, padx=(0, 15))

        # Botao Fechar
        btn_fechar = tk.Button(f_filtros, text="Fechar Grimorio", command=top.destroy,
                              bg="#660000", fg="#ffffff", font=("Helvetica", 9, "bold"),
                              activebackground="#cc0000", bd=0, padx=10, pady=4, cursor="hand2")
        btn_fechar.grid(row=0, column=4, padx=(10, 0))

        # Painel Duplo Principal
        f_corpo = tk.Frame(top, bg="#0a0a0c", padx=10, pady=5)
        f_corpo.pack(fill=tk.BOTH, expand=True)

        # Esquerda: Lore e Perfis Narrativos
        p_esquerda = tk.LabelFrame(f_corpo, text=" Misticismo & Conceito ", 
                                  bg="#111115", fg="#cc0000", font=("Helvetica", 9, "bold"), padx=10, pady=10)
        p_esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        txt_lore = tk.Text(p_esquerda, bg="#111115", fg="#d2ffd6", font=("Consolas", 9), wrap=tk.WORD, borderwidth=0)
        txt_lore.pack(fill=tk.BOTH, expand=True)

        # Direita: Tabela de Poderes N1 ao N6
        p_direita = tk.LabelFrame(f_corpo, text=" Poderes (Nivel 1 ao 6) & Paradas de Dados ", 
                                 bg="#111115", fg="#cc0000", font=("Helvetica", 9, "bold"), padx=10, pady=10)
        p_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        txt_poderes = tk.Text(p_direita, bg="#111115", fg="#ffffff", font=("Consolas", 9), wrap=tk.WORD, borderwidth=0)
        txt_poderes.pack(fill=tk.BOTH, expand=True)

        def atualizar_detalhes(event=None):
            disc_sel = combo_disc.get()
            if not disc_sel:
                return

            # Renderiza a Lore e Tags
            lore_info = DISCIPLINAS_LORE.get(disc_sel, {})
            t_lore = f"DISCIPLINA: {disc_sel.upper()}\n"
            t_lore += f"===================================\n\n"
            t_lore += f"PERFIL NARRATIVO:\n{lore_info.get('perfil', 'Poder ancestral do sangue Cainita.')}\n\n"
            t_lore += "TAGS NARRATIVAS DE USO EM MESA:\n"
            for tag in lore_info.get("tags", ["USO_GERAL"]):
                t_lore += f"  • {tag}\n"

            txt_lore.delete("1.0", tk.END)
            txt_lore.insert(tk.END, t_lore)

            # Renderiza a Lista de Poderes N1 ao N6
            poderes_list = cls.PODERES_3ED_DETALHADO.get(disc_sel, ["Poderes nao mapeados."])
            t_pod = f"PODERES MAPEADOS DA 3a EDICAO:\n"
            t_pod += f"===================================\n\n"
            for p in poderes_list:
                t_pod += f"• {p}\n\n"

            txt_poderes.delete("1.0", tk.END)
            txt_poderes.insert(tk.END, t_pod)

        combo_disc.bind("<<ComboboxSelected>>", atualizar_detalhes)
        atualizar_detalhes()

