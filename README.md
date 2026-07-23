
readme_content = """# 🦇 VTM Quick Ref

> **BETA** — Banco de fichas canônicas + Gerador de NPCs para narradores de **Vampiro: A Máscara**

---

## O que é isso?

Um programinha de computador para **consulta rápida de fichas** durante as sessões de Vampiro: A Máscara.

Sabe quando seus jogadores decidem **brigar com o garçom** em vez de negociar com o Príncipe? E você fica inventando ficha no post-it?

Esse programa resolve isso em **1 segundo**.

---

## 📦 O que já funciona

| Recurso | Descrição |
|---------|-----------|
| 🔍 **Busca instantânea** | Digita "capanga", "policial", "Tremere" — acha em 1s |
| 📚 **Banco canônico unificado** | 3ª Edição · V20 · V5 · Dark Ages · Red List |
| 👹 **Criaturas sobrenaturais** | Lobisomens, magos, fadas, fantasmas, carniçais |
| 📖 **Lore integral dos livros** | Citações, modus operandi, dicas de interpretação |
| 🎲 **Gerador de NPCs** | Escolhe clã, geração, foco — gera ficha em 10s |
| 🎲 **Rolador D10 Storyteller** | Já calcula sucessos, falhas críticas e fumbles |
| 💾 **Salva NPCs customizados** | Cria seus próprios personagens e reutiliza |

---

## 🖥️ Como usar

### Opção 1: Executável (mais fácil)

1. Baixa a última release em [Releases](../../releases)
2. Descompacta
3. Clica duas vezes em `VTM_QuickRef.exe`
4. Pronto

### Opção 2: Rodar o código (se manja de Python)

```bash
# Clona o repositório
git clone https://github.com/seu-usuario/vtm-quick-ref.git
cd vtm-quick-ref

# Instala dependências
pip install -r requirements.txt

# Executa
python main_app.py
```

**Requisitos:** Python 3.8+ · Pillow

---

## 📂 Estrutura do projeto

```
vtm-quick-ref/
├── main_app.py              # Aplicação principal (interface)
├── motor/
│   ├── dice_engine.py       # Rolador D10 Storyteller
│   ├── gerador_ficha.py     # Motor de geração de fichas
│   └── savenpcsgerados.py   # Salva/carrega NPCs customizados
├── ui/
│   ├── hud_disciplina.py    # Grimório Arcano (Disciplinas 3ª Ed)
│   └── hud_gerador.py       # Interface do Gerador de Fichas
├── dados/
│   ├── __init__.py          # Unificador automático do banco
│   ├── npcsgenericos.py     # Cidadãos, policiais, criminosos
│   ├── v3ed.py              # 3ª Edição: Inquisidores, magos, fadas, fantasmas
│   ├── v20.py               # V20 & Dark Ages
│   ├── npcsv5.py            # V5: Antagonistas, animais, carniçais
│   ├── darkages.py          # Dark Ages: mortais e cainitas medievais
│   ├── redlist.py           # Red List / Anátema (most wanted)
│   ├── membrosnotaveis.py   # Príncipes, anciões, notáveis
│   └── npcs_customizados.json  # Seus NPCs salvos (gerado automaticamente)
└── assets/
    └── moldura.png          # Moldura decorativa (opcional)
```

---

## 🎮 Uso rápido na mesa

### Consultar um NPC existente

1. Digita o nome, clã ou conceito na busca
2. Seleciona na lista
3. A ficha completa aparece no painel direito
4. Clique em **"Ver Lore"** para o texto integral do livro

### Gerar um inimigo na hora

1. Clica em **"🎲 Gerador de Fichas"**
2. Escolhe: Edição → Tipo (Neófito/Ancilla/etc) → Clã → Foco
3. Clica **"GERAR FICHA"**
4. Clica **"SALVAR NA LISTA"** se quiser reutilizar depois

### Rolar dados

1. Painel esquerdo: informa quantidade de dados e dificuldade
2. Clica **"ROLAR TESTE"**
3. Resultado com sucessos, falhas críticas e fumbles já calculados

---

## 🗺️ Roadmap (se a comunidade curtir)

- [ ] Bloodlines obscuros (Baali, Salubri, Nagaraja, Samedi...)
- [ ] Exportação para Foundry VTT
- [ ] Ficha mínima de combate (só HP + reservas)
- [ ] Sistema de "Cena de Encontro" com iniciativa
- [ ] Versão web / PWA
- [ ] App mobile

---

## 🤝 Como contribuir

Quer adicionar NPCs do seu livro favorito? Corrigir uma ficha? Melhorar a interface?

1. **Fork** o repositório
2. Cria uma **branch** (`git checkout -b minha-contribuicao`)
3. Faz as alterações
4. Abre um **Pull Request**

### Adicionando NPCs ao banco

Basta editar os arquivos em `dados/` seguindo o formato existente:

```python
"Nome do NPC": {
    "edicao": "3ª Edição",           # ou "V5", "V20 / Dark Ages", etc
    "descricao": "Conceito narrativo",
    "atributos": {
        "Força": 2, "Destreza": 3, "Vigor": 2,
        "Carisma": 2, "Manipulação": 2, "Aparência": 2,
        "Percepção": 2, "Inteligência": 2, "Raciocínio": 2
    },
    "habilidades": {
        "Briga": 2, "Armas de Fogo": 3, "Esquiva": 2
    },
    "disciplinas": "Potência 2, Fortitude 1",  # opcional
    "vitalidade": 7,
    "forca_de_vontade": 5,
    "humanidade": 7,                  # opcional
    "equipamento": "Pistola 9mm",      # opcional
    "reserva_padrao": "6 dados em Briga; 5 dados em Armas de Fogo",
    "texto_livro": "Lore integral do livro..."  # opcional
}
```

O `__init__.py` carrega automaticamente todos os arquivos `.py` da pasta `dados/`.

---

## ⚠️ Avisos legais

- **Este projeto é uma ferramenta de referência para mesa.** Não substitui os livros oficiais.
- **Vampiro: A Máscara** e todo conteúdo canônico são propriedade da **Paradox Interactive**.
- Os textos de lore presentes são **citações de referência** para uso em sessões de RPG.
- Este projeto é **não-comercial** e de **código aberto**.

---

## 🧛 Créditos

- **Sistema:** Vampiro: A Máscara por Mark Rein-Hagen e White Wolf Publishing
- **Edições suportadas:** 3ª Edição · V20 · V5 · Dark Ages
- **Ferramenta:** Desenvolvida pela comunidade, para a comunidade

---

> *"A Máscara deve ser preservada. Mas as fichas dos NPCs não precisam ficar escondidas."*

🦇 **Sangue e vitae. Bom jogo, narradores.**


print("README.md criado com sucesso!")
print(f"Tamanho: {len(readme_content)} caracteres")
