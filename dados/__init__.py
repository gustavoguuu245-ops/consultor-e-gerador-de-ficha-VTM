import os
import importlib
import sys

def obter_caminho_base():
    """Retorna o caminho base correto seja rodando em script ou como executavel (.exe)"""
    if getattr(sys, 'frozen', False):
     
        return sys._MEIPASS
    

    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def carregar_tudo():
    base_unificada = {}
    

    if getattr(sys, 'frozen', False):
     
        pasta_atual = os.path.join(sys._MEIPASS, "dados")
    else:

        pasta_atual = os.path.dirname(__file__)

   
    if not os.path.exists(pasta_atual):
        return base_unificada

    # Percorre todos os arquivos .py da pasta dados
    for arquivo in os.listdir(pasta_atual):
        if arquivo.endswith(".py") and not arquivo.startswith("__"):
            nome_modulo = arquivo[:-3]
            try:
                mod = importlib.import_module(f"dados.{nome_modulo}")
                db = getattr(mod, 'NPCS_BASE', None)
                
                if isinstance(db, dict):
                    for cat, npcs in db.items():
                        if cat not in base_unificada:
                            base_unificada[cat] = {}
                        base_unificada[cat].update(npcs)
            except Exception as e:
                print(f"Aviso: Não foi possível carregar 'dados/{arquivo}': {e}")

    return base_unificada

NPCS_BASE = carregar_tudo()