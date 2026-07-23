

NPCS_BASE = {
    "Cidadãos e Trabalhadores": {
        "Garçom / Atendente": {
            "descricao": "Humano comum trabalhando em estabelecimentos noturnos ou comerciais.",
            "atributos": {"Força": 2, "Destreza": 2, "Vigor": 2, "Carisma": 2, "Manipulação": 2, "Aparência": 2, "Percepção": 2, "Inteligência": 2, "Raciocínio": 2},
            "habilidades": {"Prontidão": 1, "Lábia": 1, "Empatia": 1, "Ofícios": 1},
            "vitalidade": 7,
            "forca_de_vontade": 2,
            "reserva_padrao": "3 dados para tarefas gerais, 4 dados em sua especialidade de atendimento."
        },
        "Camponês / Trabalhador Braçal": {
            "descricao": "Trabalhador habituado a esforço físico constante.",
            "atributos": {"Força": 3, "Destreza": 2, "Vigor": 3, "Carisma": 2, "Manipulação": 1, "Aparência": 2, "Percepção": 2, "Inteligência": 2, "Raciocínio": 2},
            "habilidades": {"Atletismo": 2, "Briga": 1, "Empatia c/ Animais": 2, "Sobrevivência": 1},
            "vitalidade": 7,
            "forca_de_vontade": 3,
            "reserva_padrao": "5 dados para testes de Força/Resistência; 3 dados em combate desarmado."
        },
        "Hacker / Técnico de TI": {
            "descricao": "Especialista em redes, sistemas e invasão de dados.",
            "atributos": {"Força": 1, "Destreza": 2, "Vigor": 2, "Carisma": 1, "Manipulação": 2, "Aparência": 2, "Percepção": 3, "Inteligência": 4, "Raciocínio": 3},
            "habilidades": {"Computação": 4, "Investigação": 2, "Prontidão": 2, "Ciência": 2},
            "vitalidade": 7,
            "forca_de_vontade": 4,
            "reserva_padrao": "7 dados para invasão/sistemas; 3 dados para percepção."
        }
    },
    "Segurança e Forças da Lei": {
        "Policial de Patrulha / Guarda": {
            "descricao": "Agente da lei em patrulha urbana ou segurança de evento.",
            "atributos": {"Força": 3, "Destreza": 2, "Vigor": 3, "Carisma": 2, "Manipulação": 2, "Aparência": 2, "Percepção": 3, "Inteligência": 2, "Raciocínio": 2},
            "habilidades": {"Armas de Fogo": 2, "Briga": 2, "Esquiva": 2, "Condução": 2, "Intimidação": 2, "Prontidão": 2},
            "equipamento": "Pistola 9mm (Dano 5), Cassetete (Dano Força+1), Colete Balístico (+1 Armadura), Rádio",
            "vitalidade": 7,
            "forca_de_vontade": 4,
            "reserva_padrao": "5 dados para Atirar/Brigar; 5 dados para Prontidão/Percepção."
        },
        "Detetive / Investigador": {
            "descricao": "Investigador experiente, acostumado com interrogatórios e cenas de crime.",
            "atributos": {"Força": 2, "Destreza": 2, "Vigor": 3, "Carisma": 2, "Manipulação": 3, "Aparência": 2, "Percepção": 4, "Inteligência": 3, "Raciocínio": 3},
            "habilidades": {"Investigação": 3, "Lábia": 3, "Intimidação": 2, "Armas de Fogo": 2, "Empatia": 3, "Direito": 2},
            "equipamento": "Revolver .38 (Dano 5), Crachá, Bloco de Anotações",
            "vitalidade": 7,
            "forca_de_vontade": 5,
            "reserva_padrao": "7 dados para Investigação/Lábia; 5 dados para Interrogatório."
        },
        "Segurança Privada / Leão de Chácara": {
            "descricao": "Lutador corpulento encarregado da segurança de boates ou membros da Elite.",
            "atributos": {"Força": 4, "Destreza": 2, "Vigor": 3, "Carisma": 1, "Manipulação": 2, "Aparência": 2, "Percepção": 2, "Inteligência": 2, "Raciocínio": 2},
            "habilidades": {"Briga": 3, "Intimidação": 3, "Esquiva": 2, "Prontidão": 2},
            "equipamento": "Soco Inglês (Dano Força+1), Rádio, Algemas",
            "vitalidade": 7,
            "forca_de_vontade": 4,
            "reserva_padrao": "7 dados para Agarramentas/Socos; 5 dados para Intimidação."
        }
    },
    "Submundo e Criminalidade": {
        "Capanga / Menor de Era": {
            "descricao": "Infantaria de rua a serviço de gangues ou mafiosos locais.",
            "atributos": {"Força": 2, "Destreza": 3, "Vigor": 2, "Carisma": 2, "Manipulação": 2, "Aparência": 2, "Percepção": 2, "Inteligência": 2, "Raciocínio": 2},
            "habilidades": {"Briga": 2, "Armas Brancas": 2, "Furtividade": 2, "Manha": 3},
            "equipamento": "Canivete / Faca (Dano Força+1) ou Pistola Pequena (.22)",
            "vitalidade": 7,
            "forca_de_vontade": 3,
            "reserva_padrao": "5 dados para Furtividade/Ataque de Faca; 5 dados para Conhecimento de Rua."
        },
        "Líder de Gangue / Traficante": {
            "descricao": "Criminoso astuto com influência sobre pequenos territórios.",
            "atributos": {"Força": 3, "Destreza": 3, "Vigor": 3, "Carisma": 3, "Manipulação": 3, "Aparência": 2, "Percepção": 3, "Inteligência": 2, "Raciocínio": 3},
            "habilidades": {"Intimidação": 3, "Lábia": 3, "Armas de Fogo": 3, "Manha": 4, "Liderança": 2},
            "equipamento": "Pistola .45 (Dano 6), Celular, Dinheiro vivo",
            "vitalidade": 7,
            "forca_de_vontade": 5,
            "reserva_padrao": "6 dados para Tiro/Intimidação; 7 dados para Negociações de Rua."
        }
    },
    "Serviçais Sabujo & Ocultismo": {
        "Ghouls / Vassalo Humano": {
            "descricao": "Humano alimentado com sangue vampírico. Possui força e resiliência sobrenaturais.",
            "atributos": {"Força": 3, "Destreza": 3, "Vigor": 3, "Carisma": 2, "Manipulação": 2, "Aparência": 2, "Percepção": 3, "Inteligência": 2, "Raciocínio": 3},
            "habilidades": {"Briga": 3, "Armas de Fogo": 2, "Furtividade": 2, "Prontidão": 3, "Lequi": 2},
            "disciplinas": "Potência 1 ou Fortitude 1",
            "vitalidade": 7,
            "forca_de_vontade": 5,
            "pontos_de_sangue": "1/1 (Sangue Vampírico)",
            "reserva_padrao": "6 dados em Combate; Pode gastar sangue para +1 em Atributo Físico."
        }
    }
}
