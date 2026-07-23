import tkinter as tk
from tkinter import ttk

# Dicionario Integrado de Lore & Perfis Narrativos (3a Edicao)
DISCIPLINAS_LORE = {
    "Animalismo": {
        "perfil": "Dominio sobre feras e a Besta. Permite comandar animais, acalmar o Frenesi e ate projetar a mente em criaturas selvagens.",
        "tags": ["USO_ANIMAIS", "CONTROLE_FRENESI", "SABOTAGEM_REBANHO", "INFORMACOES_NATUREZA"]
    },
    "Auspicios": {
        "perfil": "Sentidos divinos e percepcao extra-sensorial. Ve auras, le a historia de objetos e projeta a consciencia pelo Cordao de Prata.",
        "tags": ["REVELAR_OFUSCACAO", "PROCURAR_SEGREDOS", "CONTRA_INTRIGA", "AVISO_EMBOSCADA"]
    },
    "Demencia": {
        "perfil": "A loucura mistica do cla Malkaviano. Incendeia paixoes sutis, distorce a percepcao da realidade e causa visoes de pesadelo.",
        "tags": ["ATAQUE_MENTAL", "CAOS_POLITICO", "SABOTAGEM_CORTE", "DESESTABILIZAR_ALVO"]
    },
    "Dominacao": {
        "perfil": "Escravidao mental e controle da vontade alheia atraves do olhar. Comandos diretos, alteracao de memorias e possessao.",
        "tags": ["CONTROLE_MENTAL", "ABAFA_MASCARADA", "MODIFICA_MEMORIA", "FORCAR_LEALDADE"]
    },
    "Fortitude": {
        "perfil": "Resistencia fisica sobrenatural. Concede aos Cainitas a capacidade de ignorar impactos fisicos violentos, Fogo e ate a Luz do Sol.",
        "tags": ["RESISTENCIA_DANO", "SOBREVIVER_EMBOSCADA", "IMUNIDADE_FOGO", "DEFESA_PASSIVA"]
    },
    "Metamorfose": {
        "perfil": "Mestria da transformacao fisica do Sangue (Gangrel). Olhos de predador, garras letais, metamorfose em feras ou fusao com a terra.",
        "tags": ["COMBATE_ANIMAL", "FUGA_EMERGENCIAL", "FURTIVIDADE_BRUTA", "SOBREVIVENCIA"]
    },
    "Mortis": {
        "perfil": "Alquimia negra da morte e decomposicao (Cappadocian/Giovanni). Mumifica alvos, murcha membros em combate e ergue cadaveres.",
        "tags": ["ATAQUE_DEGRADANTE", "CONTROLE_CADAVERES", "EVENTO_TERROR", "NECROMANCIA"]
    },
    "Ofuscacao": {
        "perfil": "Ocultamento mental. O vampiro nao fica invisivel fisicamente, mas engana as mentes ao redor para que ignorem sua presenca e rosto.",
        "tags": ["OCULTAMENTO", "FUGIR_INQUISICAO", "INFILTRACAO_SILENCIOSA", "ESPIONAGEM"]
    },
    "Potencia": {
        "perfil": "Vigor e forca fisica titanica. Concede capacidade para esmagar estruturas de aco, quebrar ossos e saltar distancias absurdas.",
        "tags": ["COMBATE_BRUTO", "DANO_MASSIVO", "DESTRUIR_BARREIRAS", "FORCA_PUREZA"]
    },
    "Presenca": {
        "perfil": "Magnetismo pessoal avassalador. Atrai multidoes, inspira adoracao cega, causa transe ou gera panico paralisante em area.",
        "tags": ["DIPLOMACIA_MASSA", "EVITAR_COMBATE", "CHARME_ELISEU", "PRODUCAO_INFLUENCIA"]
    },
    "Quietus": {
        "perfil": "A arte mortal dos assassinos Banu Haqim (Assamitas). Cria zonas de silencio, envenena o proprio sangue e degrada o corpo da vitima.",
        "tags": ["ASSASSINATO_SILENCIOSO", "VENENO_SANGUINEO", "SABOTAGEM_LIDER", "DANO_LETAL"]
    },
    "Quimerismo": {
        "perfil": "A feiticaria das ilusoes do cla Ravnos. Cria imagens, sons, odores e alucinacoes taticas capazes de enganar sentidos e causar dano.",
        "tags": ["DISTRACAO_MASCARADA", "ENGANAR_SENTIDOS", "ILUSAO_COMBATE", "ALUCINACAO"]
    },
    "Rapidez": {
        "perfil": "Velocidade reflexiva sobre-humana. Permite mover-se a velocidades imperceptiveis e realizar multiplas acoes de combate por turno.",
        "tags": ["MULTIPLOS_ATAQUES", "ESQUIVA_MAXIMA", "INICIATIVA_TURNO", "VELOCIDADE_PURA"]
    },
    "Serpentis": {
        "perfil": "Segredos ancestrais do cla Seguidores de Set. Olhos hipnoticos, lingua bifurcada, transformacao em serpente e remocao do coracao.",
        "tags": ["HIPNOSE_SANGUE", "PARALISIA_OLHAR", "MUTACAO_OFIDICA", "CORRUPCAO"]
    },
    "Taumaturgia": {
        "perfil": "A feiticaria de sangue hermetica do cla Tremere. Manipula as propriedades magicas do Vitae, invoca fogo e controla os elementos.",
        "tags": ["MAGIA_SANGUE", "BOLA_FOGO", "ROUBO_VITAE", "DEFESA_OCULTA"]
    },
    "Tenebrosidade": {
        "perfil": "Manipulacao da materia escura do Abismo (Lasombra). Controla sombras vivas, invoca tentaculos estranguladores e assume forma abissal.",
        "tags": ["ZONA_ESCURIDAO", "MEDO_SISTEMICO", "TIRAR_VISAO", "TENTACULOS_ABISMO"]
    },
    "Vicissitude": {
        "perfil": "Arte grotesca da escultura de carne e osso (Tzimisce). Altera feicoes humanas, molda ossos em armas e assume a horripilante Forma de Zulo.",
        "tags": ["MUTILACAO_FISICA", "MODIFICAR_APARENCIA", "CRIAR_MONSTROS", "ARMAS_OSSEAS"]
    }
}

class HUDDisciplinas:
    """Janela Pop-up Autonoma para Consulta Disciplinas (3a Edicao)"""

    PODERES_3ED_DETALHADO = {
        "Animalismo": [
            "N1: Linguagem Feral - (Manipulacao + Empatia c/ Animais | Dif 6)",
            "N2: Chamado de Noe - (Carisma + Sobrevivencia | Dif 6)",
            "N3: Intimidar a Besta - (Manipulacao + Intimidacao | Dif 7)",
            "N4: Cavalgar a Mente - (Carisma + Empatia c/ Animais | Dif 8)",
            "N5: Expulsando a Besta - (Manipulacao + Empatia c/ Animais | Dif 8)",
            "N6: Unidade Acelerada - (Percepcao + Empatia c/ Animais | Dif 6)"
        ],
        "Auspicios": [
            "N1: Sentidos Agucados - (Nivel de Auspicios | Depende da distancia",
            "N2: Visao da Alma - (Percepcao + Empatia | Dif 8)",
            "N3: Toque do Espirito - (Percepcao + Empatia | Dif 6)",
            "N4: Roubar Segredos - (Inteligencia + Labia | Dif Forca de Vontade do Alvo)",
            "N5: Caminhada da Anima - (Percepcao + Ocultismo | Dif 7 - Custo: 1 FV)",
            "N6: Visao Longinqua - (Percepcao + Empatia | Dif 6)"
        ],
        "Demencia": [
            "N1: Paixao do Incubo - (Carisma + Empatia | Dif Caminho)",
            "N2: Assombrar a Alma - (Manipulacao + Labia | Dif Percepcao+3)",
            "N3: Visao do Caos - (Percepcao + Ocultismo | Dif 7)",
            "N4: Confusao - (Manipulacao + Intimidacao | Dif FV do Alvo)",
            "N5: Loucura Uivante - (Manipulacao + Intimidacao | Dif FV do Alvo)",
            "N6: Beijo da Lua - (Manipulacao + Empatia | Dif FV do Alvo)"
        ],
        "Dominacao": [
            "N1: Observancia - (Manipulacao + Intimidacao | Dif FV do Alvo)",
            "N2: Murmurio - (Manipulacao + Lideranca | Dif FV do Alvo)",
            "N3: Memoria do Dissoluto - (Raciocinio + Labia | Dif FV do Alvo)",
            "N4: Isca - (Carisma + Lideranca | Dif FV do Alvo)",
            "N5: Possessao - (Carisma + Intimidacao | Dif FV do Alvo)",
            "N6: Fidelidade - (Carisma + Lideranca | Dif FV do Alvo)"
        ],
        "Fortitude": [
            "N1 a N6: Absorcao Passiva - Adiciona dados automaticos de absorcao de dano (inclusive Letal, Agravado, Fogo e Luz do Sol)."
        ],
        "Metamorfose": [
            "N1: Testemunha - (Visao Noturna Automatica)",
            "N2: Garras da Besta - (1 Ponto de Sangue | Causa Dano Agravado)",
            "N3: Enterrado com a Terra - (1 Ponto de Sangue | Fusao com o Solo)",
            "N4: Forma da Besta - (1 Ponto de Sangue | Transformacao em Lobo/Morcego)",
            "N5: Corpo Espiritual - (1 Ponto de Sangue | Transformacao em Nevoa Imaterial)",
            "N6: Sono Tranquilo - (4 Pontos de Sangue | Descanso em Forma de Nevoa)"
        ],
        "Mortis": [
            "N1: Mascara da Morte - (Vigor + Medicina | Dif 6)",
            "N2: Murchar - (Manipulacao + Medicina | Dif FV do Alvo)",
            "N3: Despertar - (Forca de Vontade | Dif 10 - Caminho)",
            "N4: Sussurros do Tumulo - (Estado de Rigor Mortis/Transe)",
            "N5: Morte Negra - (Vigor + Ocultismo | Dif FV do Alvo)",
            "N6: Vigor Mortis - (3 Sangues | Animacao de Zumbi Cadaverico)"
        ],
        "Ofuscacao": [
            "N1: Manto das Sombras - (Imobilidade Oculta Automatica)",
            "N2: Presenca Invisivel - (Raciocinio + Furtividade | Dif 6)",
            "N3: Mascara das Mil Faces - (Manipulacao + Representacao | Dif 7)",
            "N4: Desaparecimento - (Carisma + Furtividade | Dif Prontidao+Resistencia)",
            "N5: Cobrir o Grupo - (Oculta Aliados Proximos)",
            "N6: Mascara da Alma - (Disfarca a Aura contra Auspicios)"
        ],
        "Potencia": [
            "N1 a N6: Forca Brutal - Adiciona sucessos automaticos em testes de Forca e acrescimo de Dano Fisico."
        ],
        "Presenca": [
            "N1: Fascinio - (Carisma + Representacao | Dif 7)",
            "N2: Olhar Aterrador - (Carisma + Intimidacao | Dif Raciocinio+3)",
            "N3: Transe - (Aparicao + Empatia | Dif FV do Alvo)",
            "N4: Convocacao - (Carisma + Labia | Dif 5)",
            "N5: Majestade - (Incapaz de ser atacado sem teste de Coragem)",
            "N6: Paixao - (Manipulacao + Labia | Dif FV do Alvo)"
        ],
        "Quietus": [
            "N1: Silencio da Morte - (Zona de Silencio Absoluto)",
            "N2: Toque de Fraqueza - (Forca de Vontade | Dif Vigor+Fortitude do Alvo)",
            "N3: Dedo de Doenca - (3 Sangues | Teste de FV vs FV do Alvo)",
            "N4: Agonia do Sangue - (1 Sangue | Envenena Laminas para Dano Letal)",
            "N5: Essencia de Sangue - (Diablerie a Distancia)",
            "N6: Suor de Sangue - (FV vs Vigor+3 do Alvo)"
        ],
        "Quimerismo": [
            "N1: Ignis Fatuus - (1 FV | Ilusao de 1 Sentido)",
            "N2: Fata Morgana - (2 FV | Ilusao Multissensorial)",
            "N3: Aparicao - (1 Sangue | Ilusao Movel e Autonoma)",
            "N4: Cruel Realidade - (Manipulacao + Labia | Dif Percepcao+3 - Causa Dano Real)",
            "N5: Ilusao Permanente - (Torna Ilusao Duradoura)",
            "N6: Podridao da Mente - (Destroi a Sanidade do Alvo)"
        ],
        "Rapidez": [
            "N1 a N6: Velocidade Divina - Gasta Sangue para ganhar Acoes Extras por Turno e bonus de Iniciativa."
        ],
        "Serpentis": [
            "N1: Olhos da Serpente - (Forca de Vontade | Dif 9 - Paralisia pelo Olhar)",
            "N2: Lingua da Serpente - (Destreza+3 | Dif 6 - Lamina Ofidica)",
            "N3: Pele de Crocodilo - (Resistencia Escamada + Armadura)",
            "N4: Forma de Serpente - (Transformacao em Cobra Gigante)",
            "N5: Coracao das Trevas - (Remocao do Proprio Coracao para Imunidade ao Estaca)",
            "N6: Halito de Corrupcao - (Destreza + Briga | Dif 6)"
        ],
        "Taumaturgia": [
            "Trilha Principal: Rego Vitae (Trilha do Sangue) | Custo: 1 Sangue + FV (Dif Nivel+3)",
            "N1: Um Gosto por Sangue - (Determina Nivel, Cla e Vitae do Alvo)",
            "N2: Furia do Sangue - (Forca gasto forcado de Sangue no Alvo)",
            "N3: Potencia do Sangue - (Reduz temporariamente a Geracao)",
            "N4: Furto de Vitae - (Rouba Pontos de Sangue a distancia de 15m)",
            "N5: Caldeirao de Sangue - (Ferve o Sangue do Alvo causando Dano Agravado)"
        ],
        "Tenebrosidade": [
            "N1: Jogo de Sombras - (1 Sangue | Manipulacao de Sombras Visuais)",
            "N2: Noturno - (Manipulacao + Ocultismo | Dif 7 - Nuvem de Escuridao)",
            "N3: Bracos de Ahriman - (Manipulacao + Ocultismo | Dif 7 - Tentaculos Sombrios)",
            "N4: Sombras Noturnas - (Raciocinio + Ocultismo | Dif 7 - Doppelganger de Sombra)",
            "N5: Forma Tenebrosa - (3 Sangues | Transformacao em Abismo Fluido)",
            "N6: Caminhar no Abismo - (Inteligencia + Furtividade | Dif 6 - Teleporte pelas Sombras)"
        ],
        "Vicissitude": [
            "N1: Semblante Maleavel - (Destreza + Medicina | Dif 6 - Alteracao Facial)",
            "N2: Moldar Carne - (Destreza + Medicina | Dif 7 - Deformacoes Fisicas)",
            "N3: Moldar Ossos - (Destreza + Medicina | Dif 8 - Garras e Armaduras Osseas)",
            "N4: Forma de Zulo - (2 Sangues | Transforma no Monstro de Guerra +2 Atributos Fisicos)",
            "N5: Forma de Plasma - (2 Sangues | Corpo em Sangue Vivo)",
            "N6: Sopro do Dragao - (Vigor+3 | Dif 6 - Dano Agravado por Fogo Mistico)"
        ]
    }

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

