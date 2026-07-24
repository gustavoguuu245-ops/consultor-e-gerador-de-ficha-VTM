import sys
import os


def obter_caminho_base() -> str:
    """Retorna o caminho base correto seja rodando em script ou
    como executável (.exe)"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.getcwd()