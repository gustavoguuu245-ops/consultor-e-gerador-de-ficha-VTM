"""Modulo para simulação de rolagens de dados
"""
import random
from copy import copy


def rolar_dados(quantidade:int, dificuldade:int=6, explodir:bool=False) -> dict:
    """Simula a rolagem de dados de Vampiro 3a Ed/V20

    Args:
        quantidade (int): Número de dados na parada
        dificuldade (int, optional): Dificuldade da rolagem. Padrão: 6.
        explodir (bool, optional): Se colocado como True, resultados 10 explodem.

    Returns:
        dict: _description_
    """
    resposta: dict = {
        "resultados": [],
        "sucessos": 0,
        "uns": 0,
        "dez": 0,
        "mensagem": "Sem dados na reserva!"
    }
    if quantidade <= 0:
        return resposta
    if dificuldade < 2:
        raise ValueError('Dificuldade nunca pode ser menor do que 2')

    pool: int = copy(quantidade)
    while pool > 0:
        resultados = [random.randint(1, 10) for _ in range(pool)]
        sucessos = 0
        uns = 0
        dez = 0
        pool = 0  # impede que fiquemos num loop infinito
    
        for dado in resultados:
            if dado >= dificuldade:
                sucessos += 1
            elif dado == 1:
                uns += 1
            if dado == 10 and explodir is True:
                pool += 1

        resposta['resultados'] += resultados
        resposta['sucessos'] += sucessos
        resposta['uns'] += uns
        resposta['dez'] += dez
            
    sucessos_finais = sucessos - uns
    if sucessos_finais < 0:
        if uns > 0 and sucessos == 0:
            resposta['mensagem'] = "FALHA CRÍTICA (FUMBLE)!"
        else:
            resposta['mensagem'] = "Falha"
    elif sucessos_finais == 0:
        resposta['mensagem'] = "Falha Simples"
    else:
        resposta['mensagem'] = f"{sucessos_finais} Sucesso(s)!"

    return resposta
