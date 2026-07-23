import json
import os

ARQUIVO_SALVOS = os.path.join("dados", "npcs_customizados.json")

def carregar_npcs_salvos(npcs_base_ref):
    """Carrega os NPCs do arquivo JSON e injeta no dicionario principal"""
    if os.path.exists(ARQUIVO_SALVOS):
        try:
            with open(ARQUIVO_SALVOS, "r", encoding="utf-8") as f:
                dados_salvos = json.load(f)
                if dados_salvos:
                    npcs_base_ref["Personagens Criados (Gerador)"] = dados_salvos
        except Exception as e:
            print(f"Erro ao carregar NPCs salvos: {e}")

def salvar_npc_em_disco(nome_npc, dados_npc):
    """Grava o NPC no arquivo JSON local"""
    os.makedirs("dados", exist_ok=True)
    existentes = {}
    
    if os.path.exists(ARQUIVO_SALVOS):
        try:
            with open(ARQUIVO_SALVOS, "r", encoding="utf-8") as f:
                existentes = json.load(f)
        except Exception:
            existentes = {}
            
    existentes[nome_npc] = dados_npc
    
    with open(ARQUIVO_SALVOS, "w", encoding="utf-8") as f:
        json.dump(existentes, f, ensure_ascii=False, indent=4)