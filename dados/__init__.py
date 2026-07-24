import os
import json

from utils import CAMINHO_BASE


def carregar_npcs_base() -> dict:
    """Carrega todos os arquivos JSON da pasta de dados estaticos de NPC
    """
    base_unificada: dict = {}

    pasta_dados: str = os.path.join(CAMINHO_BASE, "dados", "npcs_base")
    if not os.path.exists(pasta_dados):
        print("Aviso: retornando pasta de NPCs vazia")
        return base_unificada

    lista_arquivos: list = [
        e 
        for e in os.listdir(pasta_dados)
        if os.path.isfile(os.path.join(pasta_dados, e))
        and e.endswith(".json")

    ]

    # Percorre todos os arquivos .json da pasta dados
    for arquivo in lista_arquivos:
        caminho_arquivo = os.path.join(pasta_dados, arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                db = json.load(f)
            
            if isinstance(db, dict):
                for cat, npcs in db.items():
                    if cat in base_unificada:
                        base_unificada[cat].update(npcs)
                    else:
                        base_unificada[cat] = npcs
        except Exception as e:
            print(f"Aviso: Não foi possível carregar 'dados/{arquivo}': {e}")

    return base_unificada


def carregar_icones(categorias:list|str|None) -> dict:
    def _carrega_arquivo(caminho:str, categorias:list|None) -> dict:
        resultado:dict = {}
        try:
            with open(caminho, 'r', encoding="utf-8") as f:
                dados = json.load(f)
                if not dados:
                    return {}
        except Exception:
            return {}
        for k, v in dados.items():
            if categorias is None or k in categorias:
                resultado[k] = v
        return resultado

    resultado: dict = {}

    if isinstance(categorias, str):
        categorias = [categorias]

    pasta_dados: str = os.path.join(CAMINHO_BASE, "dados", "icones")
    lista_arquivos:list = [
        e
        for e in os.listdir(pasta_dados)
        if e.endswith('.json')
        and os.path.isfile(os.path.join(pasta_dados, e))
    ]
    
    # carregamos primeiro os arquivos que tem _base...
    lista_prioridades:list = [
        e
        for e in lista_arquivos
        if "_base" in e
    ]
    for e in lista_prioridades:
        caminho_arquivo: str = os.path.join(pasta_dados, e)
        novos_dados: dict = _carrega_arquivo(caminho_arquivo, categorias)
        for k, v in novos_dados.items():
            if k not in resultado:
                resultado[k] = v
            else:
                resultado[k] = v

    # e agora todos os outros arquivos.
    # Assim, no futuro, podemos permitir que o usuário customize icones
    lista_customizados: list = [
        e
        for e in lista_arquivos
        if e not in lista_prioridades
    ]
    for e in lista_customizados:
        caminho_arquivo: str = os.path.join(pasta_dados, e)
        novos_dados: dict = _carrega_arquivo(caminho_arquivo, categorias)
        for k, v in novos_dados.items():
            if k not in resultado:
                resultado[k] = v
            else:
                resultado[k] = v

    return resultado


def carregar_disciplinas(categorias:list|str|None) -> dict:
    if isinstance(categorias, str):
        categorias = [categorias]

    pasta_dados: str = os.path.join(CAMINHO_BASE, "dados", "disciplinas")
    lista_arquivos:list = [
        e
        for e in os.listdir(pasta_dados)
        if e.endswith('.json')
        and os.path.isfile(os.path.join(pasta_dados, e))
    ]

    resultado:dict = {}
    for arquivo in pasta_dados:
        caminho_arquivo: str = os.path.join(pasta_dados, arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding="utf-8") as f:
                dados = json.load(f)
                if not dados:
                    return {}
        except Exception:
            continue
        for k, v in dados.items():
            if categorias is None or k in categorias:
                resultado[k] = v

    return resultado

