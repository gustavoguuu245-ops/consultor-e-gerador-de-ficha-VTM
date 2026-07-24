import json
import os


PASTA_ARQUIVO_SALVOS = os.path.join("dados", "npcs_customizados")

def carregar_npcs_salvos() -> dict:
    """Carrega os NPCs do arquivo JSON"""
    if not os.path.exists(PASTA_ARQUIVO_SALVOS):
        return {}

    lista_arquivos: list = [
        e
        for e in os.listdir(PASTA_ARQUIVO_SALVOS)
        if e.endswith('.json')
        and os.path.isfile(os.path.join(PASTA_ARQUIVO_SALVOS, e))
    ]
    dados_carregados: dict = {}
    for arquivo in lista_arquivos:
        caminho_arquivo = os.path.join(PASTA_ARQUIVO_SALVOS, arquivo)
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                if dados_salvos:
                    #  TODO: modificar a chave em `dados carregados` para poder
                    # carregar mais de um arquivo salvo
                    dados_carregados["Personagens Criados (Gerador)"] = dados_salvos
        except Exception as e:
            print(f"Erro ao carregar NPCs salvos: {e}")
    return dados_carregados

def salvar_npc_em_disco(nome_npc: str, dados_npc: dict, nome_arquivo:str|None) -> str:
    """Grava o NPC no arquivo JSON local. Se um arquivo já existir no destino,
    o atualiza com os dados recebidos

    Args:
        nome_npc (str): nome do NPC a ser salvo
        dados_npc (dict): dados do NPC a ser salvo
        nome_arquivo (str | None): nome do arquivo onde salvar os dados.
            Padrão: npcs_customizados.json

    Returns:
        str: caminho do arquivo salvo.
    """
    if nome_arquivo is None:
        nome_arquivo = 'npcs_customizados.json'
    caminho_arquivo: str = os.path.join(PASTA_ARQUIVO_SALVOS, nome_arquivo)
    
    existentes:dict = {}
    if os.path.exists(caminho_arquivo) and os.path.isfile(caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                existentes = json.load(f)
        except Exception:
            pass
            
    existentes[nome_npc] = dados_npc
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(existentes, f, ensure_ascii=False, indent=4)

    return caminho_arquivo