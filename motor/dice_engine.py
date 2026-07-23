import random
       # aqui simulamos as rolagens de dados
def rolar_dados(quantidade, dificuldade=6):
  
    if quantidade <= 0:
        return {"resultados": [], "sucessos": 0, "mensagem": "Sem dados na reserva!"}
    
    resultados = [random.randint(1, 10) for _ in range(quantidade)]
    sucessos = 0
    uns = 0
    
    for dado in resultados:
        if dado >= dificuldade:
            sucessos += 1
        if dado == 1:
            uns += 1
            
    sucessos_finais = sucessos - uns
    
    if sucessos_finais < 0:
        if uns > 0 and sucessos == 0:
            resultado_txt = "FALHA CRÍTICA (FUMBLE)!"
        else:
            resultado_txt = "Falha"
    elif sucessos_finais == 0:
        resultado_txt = "Falha Simples"
    else:
        resultado_txt = f"{sucessos_finais} Sucesso(s)!"

    return {
        "resultados": sorted(resultados, reverse=True),
        "sucessos": sucessos_finais,
        "mensagem": resultado_txt
    }
