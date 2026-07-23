# motor/gerador_ficha.py
"""
Motor de Geração de Fichas para Vampiro: A Máscara
Suporta: 3ª Edição, Dark Ages, Humanos e Carniçais
"""
import random

# ============================================================
# REGRAS DE CRIAÇÃO POR TIPO DE PERSONAGEM


REGRAS = {
    "neofito_3a": {
        "nome": "Neófito (3ª Edição)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 7, "secundario": 5, "terciario": 3},
        "habilidades": {"primario": 13, "secundario": 9, "terciario": 5},
        "disciplinas": 3,
        "antecedentes": 5,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "ancilla_3a": {
        "nome": "Ancilla (3ª Edição, 50-100 anos)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 8, "secundario": 6, "terciario": 4},
        "habilidades": {"primario": 15, "secundario": 10, "terciario": 6},
        "disciplinas": 5,
        "antecedentes": 6,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "anciao_3a": {
        "nome": "Ancião (3ª Edição, 100-200 anos)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 9, "secundario": 6, "terciario": 4},
        "habilidades": {"primario": 16, "secundario": 11, "terciario": 7},
        "disciplinas": 6,
        "antecedentes": 8,
        "virtudes": 7,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "matusalem_3a": {
        "nome": "Metusalém (3ª Edição, 1000+ anos)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 12, "secundario": 8, "terciario": 5},
        "habilidades": {"primario": 20, "secundario": 14, "terciario": 10},
        "disciplinas": 10,
        "antecedentes": 12,
        "virtudes": 7,
        "pontos_bonus": 30,
        "habilidade_max": 6,

        #========================================
        # Começo da DarkAges
    },
    "neofito_da": {
        "nome": "Neófito (Dark Ages)",
        "edicao": "dark_ages",
        "atributos": {"primario": 7, "secundario": 5, "terciario": 3},
        "habilidades": {"primario": 13, "secundario": 9, "terciario": 5},
        "disciplinas": 4,  # Dark Ages: 4 pontos em disciplinas
        "antecedentes": 5,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "ancilla_da": {
        "nome": "Ancilla (Dark Ages, 50-100 anos)",
        "edicao": "dark_ages",
        "atributos": {"primario": 8, "secundario": 6, "terciario": 4},
        "habilidades": {"primario": 15, "secundario": 10, "terciario": 6},
        "disciplinas": 6,
        "antecedentes": 6,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "anciao_da": {
        "nome": "Ancião (Dark Ages, 100-200 anos)",
        "edicao": "dark_ages",
        "atributos": {"primario": 9, "secundario": 6, "terciario": 4},
        "habilidades": {"primario": 16, "secundario": 11, "terciario": 7},
        "disciplinas": 8,
        "antecedentes": 8,
        "virtudes": 7,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "matusalem_da": {
        "nome": "Metusalém (Dark Ages, 1000+ anos)",
        "edicao": "dark_ages",
        "atributos": {"primario": 12, "secundario": 8, "terciario": 5},
        "habilidades": {"primario": 20, "secundario": 14, "terciario": 10},
        "disciplinas": 12,
        "antecedentes": 12,
        "virtudes": 7,
        "pontos_bonus": 30,
        "habilidade_max": 6,
    },
    "humano_3a": {
        "nome": "Humano (3ª Edição)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 7, "secundario": 5, "terciario": 3},
        "habilidades": {"primario": 13, "secundario": 9, "terciario": 5},
        "disciplinas": 0,
        "antecedentes": 5,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "carnical_3a": {
        "nome": "Carniçal (3ª Edição)",
        "edicao": "3a_edicao",
        "atributos": {"primario": 6, "secundario": 4, "terciario": 3},
        "habilidades": {"primario": 11, "secundario": 7, "terciario": 4},
        "disciplinas": 2,  # Potência 1 + 1 do clã do criador
        "antecedentes": 5,
        "virtudes": 7,  # ou 5 para Sabá
        "pontos_bonus": 0,  # Carniçais não têm pontos de bônus
        "habilidade_max": 3,
    },
    "humano_da": {
        "nome": "Humano (Dark Ages)",
        "edicao": "dark_ages",
        "atributos": {"primario": 7, "secundario": 5, "terciario": 3},
        "habilidades": {"primario": 13, "secundario": 9, "terciario": 5},
        "disciplinas": 0,
        "antecedentes": 5,
        "virtudes": 8,
        "pontos_bonus": 15,
        "habilidade_max": 5,
    },
    "carnical_da": {
        "nome": "Carniçal (Dark Ages)",
        "edicao": "dark_ages",
        "atributos": {"primario": 6, "secundario": 4, "terciario": 3},
        "habilidades": {"primario": 11, "secundario": 7, "terciario": 4},
        "disciplinas": 2,
        "antecedentes": 5,
        "virtudes": 7,
        "pontos_bonus": 0,
        "habilidade_max": 3,
    },
}

# ============================================================
# ESTRUTURAS DE DADOS POR EDIÇÃO
# ============================================================

EDICOES = {
    "3a_edicao": {
        "nome": "3ª Edição",
        "atributos_fisicos": ["Força", "Destreza", "Vigor"],
        "atributos_sociais": ["Carisma", "Manipulação", "Aparência"],
        "atributos_mentais": ["Percepção", "Inteligência", "Raciocínio"],
        "talentos": ["Prontidão", "Esportes", "Briga", "Esquiva", "Empatia", "Expressão", "Intimidação", "Liderança", "Manha", "Lábia"],
        "pericias": ["Empatia c/Animais", "Ofícios", "Condução", "Etiqueta", "Armas de Fogo", "Armas Brancas", "Performance", "Segurança", "Furtividade", "Sobrevivência"],
        "conhecimentos": ["Acadêmicos", "Computador", "Finanças", "Investigação", "Direito", "Linguística", "Medicina", "Ocultismo", "Política", "Ciência"],
        "virtudes": ["Consciência", "Autocontrole", "Coragem"],
        "antecedentes": ["Aliados", "Contatos", "Fama", "Influência", "Mentor", "Rebanho", "Recursos", "Status", "Criados", "Domínio", "Geração", "Lacaios"],
    },
    "dark_ages": {
        "nome": "Dark Ages",
        "atributos_fisicos": ["Força", "Destreza", "Vigor"],
        "atributos_sociais": ["Carisma", "Manipulação", "Aparência"],
        "atributos_mentais": ["Percepção", "Inteligência", "Raciocínio"],
        "talentos": ["Prontidão", "Esportes", "Briga", "Esquiva", "Empatia", "Expressão", "Intimidação", "Liderança", "Manha", "Lábia"],
        "pericias": ["Empatia c/Animais", "Ofícios", "Condução", "Etiqueta", "Armas de Fogo", "Armas Brancas", "Performance", "Segurança", "Furtividade", "Sobrevivência", "Cavalgar", "Herborismo", "Arqueirismo", "Artesanato", "Música"],
        "conhecimentos": ["Acadêmicos", "Instrução", "Investigação", "Direito", "Linguística", "Medicina", "Ocultismo", "Política", "Ciência", "Senescalia", "Sabedoria Popular", "Teologia"],
        "virtudes": ["Consciência", "Autocontrole", "Coragem"],
        "antecedentes": ["Aliados", "Contatos", "Fama", "Influência", "Mentor", "Rebanho", "Recursos", "Status", "Criados", "Domínio", "Geração"],
    }
}

# ============================================================
# CLÃS E DISCIPLINAS
# ============================================================

CLAS = {
    "3a_edicao": {
        "Brujah": {"disciplinas": ["Rapidez", "Potência", "Presença"], "foco": "fisico"},
        "Gangrel": {"disciplinas": ["Animalismo", "Fortitude", "Metamorfose"], "foco": "fisico"},
        "Malkaviano": {"disciplinas": ["Auspícios", "Demência", "Ofuscação"], "foco": "mental"},
        "Nosferatu": {"disciplinas": ["Animalismo", "Ofuscação", "Potência"], "foco": "mental"},
        "Toreador": {"disciplinas": ["Auspícios", "Rapidez", "Presença"], "foco": "social"},
        "Tremere": {"disciplinas": ["Auspícios", "Dominação", "Taumaturgia"], "foco": "mental"},
        "Ventrue": {"disciplinas": ["Dominação", "Fortitude", "Presença"], "foco": "social"},
        "Lasombra": {"disciplinas": ["Dominação", "Potência", "Tenebrosidade"], "foco": "social"},
        "Tzimisce": {"disciplinas": ["Animalismo", "Auspícios", "Vicissitude"], "foco": "mental"},
        "Assamita": {"disciplinas": ["Ofuscação", "Quietus", "Rapidez"], "foco": "fisico"},
        "Ravnos": {"disciplinas": ["Animalismo", "Ofuscação", "Quimerismo"], "foco": "social"},
        "Setita": {"disciplinas": ["Ofuscação", "Presença", "Serpentis"], "foco": "social"},
        "Giovanni": {"disciplinas": ["Dominação", "Potência", "Mortis"], "foco": "social"},
        "Cappadocio": {"disciplinas": ["Auspícios", "Fortitude", "Mortis"], "foco": "mental"},
    },
    "dark_ages": {
        "Brujah": {"disciplinas": ["Rapidez", "Potência", "Presença"], "foco": "fisico"},
        "Gangrel": {"disciplinas": ["Animalismo", "Fortitude", "Metamorfose"], "foco": "fisico"},
        "Malkaviano": {"disciplinas": ["Auspícios", "Demência", "Ofuscação"], "foco": "mental"},
        "Nosferatu": {"disciplinas": ["Animalismo", "Ofuscação", "Potência"], "foco": "mental"},
        "Toreador": {"disciplinas": ["Auspícios", "Rapidez", "Presença"], "foco": "social"},
        "Tremere": {"disciplinas": ["Auspícios", "Dominação", "Taumaturgia"], "foco": "mental"},
        "Ventrue": {"disciplinas": ["Dominação", "Fortitude", "Presença"], "foco": "social"},
        "Lasombra": {"disciplinas": ["Dominação", "Potência", "Tenebrosidade"], "foco": "social"},
        "Tzimisce": {"disciplinas": ["Animalismo", "Auspícios", "Vicissitude"], "foco": "mental"},
        "Assamita": {"disciplinas": ["Ofuscação", "Quietus", "Rapidez"], "foco": "fisico"},
        "Ravnos": {"disciplinas": ["Animalismo", "Ofuscação", "Quimerismo"], "foco": "social"},
        "Setita": {"disciplinas": ["Ofuscação", "Presença", "Serpentis"], "foco": "social"},
        "Giovanni": {"disciplinas": ["Dominação", "Potência", "Mortis"], "foco": "social"},
        "Cappadocio": {"disciplinas": ["Auspícios", "Fortitude", "Mortis"], "foco": "mental"},
        "Salubri": {"disciplinas": ["Auspícios", "Fortitude", "Dominação"], "foco": "mental"},
    }
}

# Disciplinas extras disponíveis (para pontos de bônus e anciões)
DISCIPLINAS_EXTRAS = [
    "Animalismo", "Auspícios", "Demência", "Dominação", "Fortitude",
    "Metamorfose", "Mortis", "Ofuscação", "Potência", "Presença",
    "Quietus", "Quimerismo", "Rapidez", "Serpentis", "Taumaturgia",
    "Tenebrosidade", "Vicissitude"
]

# Naturezas/Comportamentos
NATUREZAS = [
    "Arquiteto", "Autocrata", "Bon Vivant", "Cavalheiro",
    "Competidor", "Conformista", "Diretor",
    "Fanático", "Galante", "Inovador", "Malandro",
    "Juiz", "Caçador de Emoções", "Mártir","Pedagogo", "Penitente", "Perfeccionista", "Rebelde",
    "Sobrevivencialista", "Solitário", "Tradicionalista", "Celebrante", "Criança", "Monstro", "Solitario"
]

CONCEITOS = {
    "Brujah": ["Ativista", "Batedor de Carteiras", "Criminosa", "Motoqueiro", "Político", "Revolucionário", "Vândalo"],
    "Gangrel": ["Caçador", "Cigano", "Druida Urbano", "Hobo", "Sobrevivencialista", "Vagabundo"],
    "Malkaviano": ["Artista Louco", "Conspiracionista", "Estudante", "Fanático Religioso", "Profeta", "Serial Killer"],
    "Nosferatu": ["Espião", "Informante", "Investigador", "Ladrão", "Rato de Esgoto", "Sabujo"],
    "Toreador": ["Ator", "Dandy", "Estilista", "Músico", "Poeta", "Socialite", "Viciado em Adrenalina"],
    "Tremere": ["Acadêmico", "Alquimista", "Feiticeiro", "Ocultista", "Pesquisador", "Sacerdote Negro"],
    "Ventrue": ["Banqueiro", "Empresário", "Líder Político", "Mafioso", "Militar", "Nobre"],
    "Lasombra": ["Bispo", "Capitão de Navio", "Inquisidor", "Pirata", "Tirano"],
    "Tzimisce": ["Alquimista", "Cirurgião", "Monstro", "Necromante", "Torturador"],
    "Assamita": ["Assassino", "Bodyguard", "Caçador de Recompensas", "Mercenário", "Sicário"],
    "Ravnos": ["Charlatão", "Ladrão", "Místico", "Trapaceiro", "Vendedor de Curas"],
    "Setita": ["Cultista", "Guru", "Político Corrupto", "Sacerdote", "Traficante"],
    "Giovanni": ["Banqueiro", "Criminosa", "Necromante", "Negociante", "Ocultista"],
    "Cappadocio": ["Eremita", "Monge", "Necromante", "Pesquisador", "Sacerdote"],
    "Salubri": ["Cavaleiro", "Curandeiro", "Mártir", "Paladino", "Visionário"],
}

# ============================================================
# FUNÇÕES DISTRIBUIÇÃO DE PONTOS


def _distribuir_pontos_atributos(categorias, pontos_por_prioridade, foco_escolhido, cla_foco):
   
    # Determinar ordem das categorias baseada no foco
    if foco_escolhido == "aleatorio":
        foco = random.choice(["fisico", "social", "mental"])
    else:
        foco = foco_escolhido
    
    # Mapear foco para categoria
    mapa_foco = {
        "fisico": "fisicos",
        "social": "sociais", 
        "mental": "mentais"
    }
    
    categorias_nomes = ["fisicos", "sociais", "mentais"]
    foco_cat = mapa_foco.get(foco, "fisicos")
    outras = [c for c in categorias_nomes if c != foco_cat]
    ordem_categorias = [foco_cat] + outras
    
    # Pontos para cada prioridade
    pontos = [pontos_por_prioridade["primario"], 
              pontos_por_prioridade["secundario"], 
              pontos_por_prioridade["terciario"]]
    
    atributos_finais = {}
    
    for i, cat_nome in enumerate(ordem_categorias):
        atributos_cat = categorias[cat_nome]
        pts = pontos[i]
        # Todos começam com 1 (ponto automático)
        valores = {attr: 1 for attr in atributos_cat}
        
        # Distribuir pontos restantes aleatoriamente, com tendência para o foco
        while pts > 0:
            # Preferir atributos que fazem sentido para o clã
            attr = random.choice(atributos_cat)
            if valores[attr] < 5:  # Máximo 5 para neófitos
                valores[attr] += 1
                pts -= 1
        
        atributos_finais.update(valores)
    
    return atributos_finais

        #Habilidades parte da distribuição

def _distribuir_pontos_habilidades(todas_habilidades, pontos_por_prioridade, habilidade_max=5, foco=None):
    
    # Separar em grupos
    talentos = todas_habilidades["talentos"]
    pericias = todas_habilidades["pericias"]
    conhecimentos = todas_habilidades["conhecimentos"]
    
    # Determinar prioridade baseada no foco
    if foco == "fisico":
        ordem = [pericias, talentos, conhecimentos]
    elif foco == "social":
        ordem = [talentos, pericias, conhecimentos]
    elif foco == "mental":
        ordem = [conhecimentos, talentos, pericias]
    else:
        # Aleatório
        grupos = [talentos, pericias, conhecimentos]
        random.shuffle(grupos)
        ordem = grupos
    
    pontos = [pontos_por_prioridade["primario"], 
              pontos_por_prioridade["secundario"], 
              pontos_por_prioridade["terciario"]]
    
    habilidades_finais = {}
    
    for i, grupo in enumerate(ordem):
        pts = pontos[i]
        # Selecionar  habilidades para este grupo
        num_habs = min(len(grupo), max(3, pts // 2))
        habs_selecionadas = random.sample(grupo, num_habs)
        
        valores = {h: 0 for h in habs_selecionadas}
        
        while pts > 0:
            h = random.choice(habs_selecionadas)
            if valores[h] < habilidade_max:
                valores[h] += 1
                pts -= 1
        
        habilidades_finais.update(valores)
    
    # Remover zeros
    habilidades_finais = {k: v for k, v in habilidades_finais.items() if v > 0}
    
    return habilidades_finais

def _distribuir_disciplinas(disciplinas_cla, pontos, habilidade_max=5, tipo="vampiro"):
 
    if tipo in ["humano", "humano_da"]:
        return {}
    
    if tipo == "carnical":
        disc = {"Potência": 1}
        if disciplinas_cla:
            disc[random.choice(disciplinas_cla)] = 1
        return disc
    
    disciplinas_finais = {}
    
    # 1. Definir uma distribuição de pontos dinâmica baseada no total de pontos
    # Para 3 pontos (Neófito): Pode ser (3), (2, 1) ou (1, 1, 1)
    # Para mais pontos (Anciões/Ancillas): Monta blocos de investimento
    if pontos == 3:
        # Padrões reais de fichas de VTM:
        # 50% chance de focar (2, 1) | 30% chance de espalhar (1, 1, 1) | 20% chance de focar total (3)
        padrao = random.choices(
            [[2, 1], [1, 1, 1], [3]], 
            weights=[50, 30, 20]
        )[0]
    else:
        # Para mais de 3 pontos, distribui em 'fatias' 
        padrao = []
        pts_restantes = pontos
        while pts_restantes > 0:
            fatia = min(random.randint(1, 3), pts_restantes)
            padrao.append(fatia)
            pts_restantes -= fatia

    # 2. Atribuir os blocos sorteados às disciplinas
    for qtd_pontos in padrao:
        # 80% de chance de pegar uma disciplina do Clã / 20% de pegar de Fora
        if random.random() < 0.8 and disciplinas_cla:
            # Escolhe uma disciplina do clã que ainda não atingiu o limite max
            candidatas = [d for d in disciplinas_cla if disciplinas_finais.get(d, 0) + qtd_pontos <= habilidade_max]
            if not candidatas:
                candidatas = disciplinas_cla
            d = random.choice(candidatas)
        else:
            d = random.choice(DISCIPLINAS_EXTRAS)

        # Adiciona a pontuação sorteada
        atual = disciplinas_finais.get(d, 0)
        novo_valor = min(atual + qtd_pontos, habilidade_max)
        disciplinas_finais[d] = novo_valor

    return disciplinas_finais

def _distribuir_virtudes(pontos, edicao="3a_edicao"):
    """
    Distribui pontos em virtudes.
    """
    virtudes_nomes = EDICOES[edicao]["virtudes"]
    
    # Consciência/Convicção e Autocontrole/Instinto começam com 1
    # Coragem começa com 1
    valores = {v: 1 for v in virtudes_nomes}
    pontos -= 3  # 3 pontos já gastos nos 1s automáticos
    
    while pontos > 0:
        v = random.choice(virtudes_nomes)
        if valores[v] < 5:
            valores[v] += 1
            pontos -= 1
    
    return valores

def _distribuir_antecedentes(pontos, edicao="3a_edicao"):

    ants = EDICOES[edicao]["antecedentes"]
    valores = {}
    
    while pontos > 0:
        a = random.choice(ants)
        atual = valores.get(a, 0)
        if atual < 5:
            valores[a] = atual + 1
            pontos -= 1
    
    return valores

# ============================================================
# FUNÇÃO PRINCIPAL DE GERAÇÃO


def gerar_ficha(tipo_personagem, nome, cla=None, foco="aleatorio", 
                natureza=None, comportamento=None, conceito=None,
                jogador="", cronica="", nacionalidade="", idade_mortal="",
                sexo="", senhor="", geracao=""):
     
    if tipo_personagem not in REGRAS:
        raise ValueError(f"Tipo de personagem desconhecido: {tipo_personagem}")
    
    regra = REGRAS[tipo_personagem]
    edicao_key = regra["edicao"]
    edicao = EDICOES[edicao_key]
    
    # Determinar clã e foco
    if cla and edicao_key in CLAS and cla in CLAS[edicao_key]:
        info_cla = CLAS[edicao_key][cla]
        disciplinas_cla = info_cla["disciplinas"]
        cla_foco = info_cla["foco"]
    else:
        cla = None
        info_cla = None
        disciplinas_cla = []
        cla_foco = "fisico"
    
    # Se foco aleatório, usar foco do clã ou sortear
    if foco == "aleatorio":
        foco = cla_foco if cla_foco else random.choice(["fisico", "social", "mental"])
    
    # Gerar dados narrativos se não fornecidos
    if not natureza:
        natureza = random.choice(NATUREZAS)
    if not comportamento:
        comportamento = random.choice(NATUREZAS)
    if not conceito and cla and cla in CONCEITOS:
        conceito = random.choice(CONCEITOS[cla])
    elif not conceito:
        conceito = "Desconhecido"
    
    # ============================================================
    # DISTRIBUIR ATRIBUTOS
   
    
    categorias = {
        "fisicos": edicao["atributos_fisicos"],
        "sociais": edicao["atributos_sociais"],
        "mentais": edicao["atributos_mentais"]
    }
    
    atributos = _distribuir_pontos_atributos(
        categorias, regra["atributos"], foco, cla_foco
    )
    
    # ============================================================
    # DISTRIBUIR HABILIDADES
  
    
    todas_habs = {
        "talentos": edicao["talentos"],
        "pericias": edicao["pericias"],
        "conhecimentos": edicao["conhecimentos"]
    }
    
    habilidades = _distribuir_pontos_habilidades(
        todas_habs, regra["habilidades"], regra.get("habilidade_max", 5), foco
    )
    
    # ============================================================
    # DISTRIBUIR DISCIPLINAS
   
    
    tipo_criatura = "vampiro"
    if "humano" in tipo_personagem:
        tipo_criatura = "humano"
    elif "carnical" in tipo_personagem:
        tipo_criatura = "carnical"
    
    disciplinas = _distribuir_disciplinas(
        disciplinas_cla, regra["disciplinas"], 
        regra.get("habilidade_max", 5), tipo_criatura
    )
    
    # ============================================================
    # DISTRIBUIR VIRTUDES E ANTECEDENTES

    
    virtudes = _distribuir_virtudes(regra["virtudes"], edicao_key)
    antecedentes = _distribuir_antecedentes(regra["antecedentes"], edicao_key)
    
    # ============================================================
    # CALCULAR DERIVADOS

    
    # Vitalidade = Vigor + 7 (base)
    vigor = atributos.get("Vigor", 1)
    vitalidade = vigor + 7
    
    # Força de Vontade = Coragem (para 3a ed) ou base
    coragem = virtudes.get("Coragem", 1)
    forca_vontade = coragem
    
    # Humanidade/Trilha
    humanidade = regra.get("humanidade_padrao", 7)
    
    # Geração
    if not geracao:
        if "matusalem" in tipo_personagem:
            geracao = random.choice(["4ª", "5ª"])
        elif "anciao" in tipo_personagem:
            geracao = random.choice(["6ª", "7ª", "8ª"])
        elif "ancilla" in tipo_personagem:
            geracao = random.choice(["8ª", "9ª", "10ª"])
        else:
            geracao = random.choice(["10ª", "11ª", "12ª", "13ª"])
    
    # Pontos de sangue (baseado na geração)
    pontos_sangue = _calcular_sangue(geracao)
    
    # ============================================================
    # MONTAR FICHA FINAL

    
    ficha = {
        "nome": nome,
        "jogador": jogador,
        "cronica": cronica,
        "natureza": natureza,
        "comportamento": comportamento,
        "nacionalidade": nacionalidade,
        "idade_mortal": idade_mortal,
        "sexo": sexo,
        "senhor": senhor,
        "cla": cla if cla else "Nenhum",
        "conceito": conceito,
        "geracao": geracao,
        "edicao": edicao_key,
        "tipo": regra["nome"],
        
        "atributos": atributos,
        "habilidades": habilidades,
        "disciplinas": disciplinas,
        "virtudes": virtudes,
        "antecedentes": antecedentes,
        
        "vitalidade": vitalidade,
        "forca_vontade": forca_vontade,
        "humanidade": humanidade,
        "pontos_sangue": pontos_sangue,
        "pontos_sangue_max": pontos_sangue,
    }
    
    return ficha

def _calcular_sangue(geracao):
    """Calcula pontos de sangue máximo baseado na geração."""
    mapa = {
        "3ª": 50, "4ª": 40, "5ª": 30, "6ª": 20, "7ª": 15,
        "8ª": 10, "9ª": 10, "10ª": 10, "11ª": 8, "12ª": 6,
        "13ª": 4, "14ª": 3, "15ª": 2
    }
    return mapa.get(geracao, 10)

def formatar_ficha_texto(ficha):
    """Formata a ficha alinhada no padrão oficial Storyteller."""
    linhas = []
    ed_key = ficha.get('edicao', '3a_edicao')
    ed_info = EDICOES.get(ed_key, EDICOES['3a_edicao'])
    
    # Cabeçalho
    linhas.append("=" * 78)
    linhas.append(f"  FICHA DE PERSONAGEM - {ficha['tipo'].upper()}")
    linhas.append("=" * 78)
    linhas.append("")
    
    # Dados básicos
    linhas.append(f"Nome:         {ficha['nome']:<25} Clã:          {ficha['cla']}")
    linhas.append(f"Jogador:      {ficha['jogador']:<25} Conceito:     {ficha['conceito']}")
    linhas.append(f"Crônica:      {ficha['cronica']:<25} Geração:      {ficha['geracao']}")
    linhas.append(f"Natureza:     {ficha['natureza']:<25} Senhor:       {ficha['senhor']}")
    linhas.append(f"Comportamento:{ficha['comportamento']:<25} Idade Mortal: {ficha['idade_mortal']}")
    linhas.append("")
    
    # ============================================================
    # ATRIBUTOS (FÍSICOS / SOCIAIS / MENTAIS)
    
    linhas.append("-" * 65)
    linhas.append("ATRIBUTOS")
    linhas.append("-" * 65)
    
    atrs = ficha['atributos']
    fisicos = ["Força", "Destreza", "Vigor"]
    sociais = ["Carisma", "Manipulação", "Aparência"]
    mentais = ["Percepção", "Inteligência", "Raciocínio"]
    
    for i in range(3):
        f_nom, s_nom, m_nom = fisicos[i], sociais[i], mentais[i]
        f_v = atrs.get(f_nom, 1)
        s_v = atrs.get(s_nom, 1)
        m_v = atrs.get(m_nom, 1)
        
        # Formatação enxuta de 20 caracteres por coluna
        f_str = f"{f_nom[:8]:<8} {'●'*f_v}{'○'*(5-f_v)} ({f_v})"
        s_str = f"{s_nom[:8]:<8} {'●'*s_v}{'○'*(5-s_v)} ({s_v})"
        m_str = f"{m_nom[:8]:<8} {'●'*m_v}{'○'*(5-m_v)} ({m_v})"
        
        linhas.append(f"{f_str:<21} {s_str:<21} {m_str:<21}")
    linhas.append("")

    # ============================================================
    # HABILIDADES (TALENTOS / PERÍCIAS / CONHECIMENTOS)
    
    linhas.append("-" * 65)
    linhas.append("HABILIDADES")
    linhas.append("-" * 65)
    
    habs_pessoais = ficha['habilidades']
    
    # 1. TALENTOS
    linhas.append("  [ TALENTOS ]")
    for t_nom in ed_info["talentos"]:
        val = habs_pessoais.get(t_nom, 0)
        dots = "●" * val + "○" * (5 - val)
        linhas.append(f"    • {t_nom:<18}: {dots} ({val})")
    linhas.append("")

    # 2. PERÍCIAS
    linhas.append("  [ PERÍCIAS ]")
    for p_nom in ed_info["pericias"]:
        val = habs_pessoais.get(p_nom, 0)
        dots = "●" * val + "○" * (5 - val)
        linhas.append(f"    • {p_nom:<18}: {dots} ({val})")
    linhas.append("")

    # 3. CONHECIMENTOS
    linhas.append("  [ CONHECIMENTOS ]")
    for c_nom in ed_info["conhecimentos"]:
        val = habs_pessoais.get(c_nom, 0)
        dots = "●" * val + "○" * (5 - val)
        linhas.append(f"    • {c_nom:<18}: {dots} ({val})")
    linhas.append("")

    # ============================================================
    # DISCIPLINAS E VANTAGENS
    
    if ficha.get('disciplinas'):
        linhas.append("-" * 78)
        linhas.append("DISCIPLINAS")
        linhas.append("-" * 78)
        for d_nom, d_v in sorted(ficha['disciplinas'].items()):
            dots = "●" * d_v + "○" * (5 - d_v) if d_v <= 5 else "●" * d_v
            linhas.append(f"  • {d_nom:<20}: {dots} ({d_v})")
        linhas.append("")

    # Virtudes
    linhas.append("-" * 78)
    linhas.append("VIRTUDES / DERIVADOS")
    linhas.append("-" * 78)
    for v_nom, v_v in ficha['virtudes'].items():
        linhas.append(f"  • {v_nom:<15}: {'●'*v_v}{'○'*(5-v_v)} ({v_v})")
    
    linhas.append(f"\n  Vitalidade:        {ficha['vitalidade']} Níveis")
    linhas.append(f"  Força de Vontade:  {ficha['forca_vontade']}")
    linhas.append(f"  Humanidade/Trilha: {ficha['humanidade']}")
    if ficha.get('pontos_sangue'):
        linhas.append(f"  Reserva de Sangue: {ficha['pontos_sangue']}/{ficha['pontos_sangue_max']}")
    linhas.append("")

    linhas.append("=" * 78)
    return "\n".join(linhas)
