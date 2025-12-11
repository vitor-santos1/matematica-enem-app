import random
import math

# ==============================================================================
# 🧠 VITOR-AI 2.0: GERADOR PROCEDURAL DIVERSIFICADO
# ==============================================================================

def get_texto(tipo):
    """Banco de dados criativo para montar frases dinâmicas."""
    db = {
        "profissoes": ["Um engenheiro civil", "Uma arquiteta", "Um mestre de obras", "Um analista de dados", "Um gerente de projetos"],
        "locais": ["no canteiro de obras", "em um projeto urbano", "na análise trimestral", "no planejamento estratégico"],
        "verbos": ["precisa calcular", "está projetando", "analisou os dados de", "deve estimar"],
        "estruturas": ["uma rampa de acessibilidade", "uma escada de segurança", "o telhado de um galpão", "uma torre de transmissão"],
        "conectivos": ["Sabendo que", "Considerando que", "Tendo em vista que", "De acordo com as normas,"],
    }
    return random.choice(db[tipo])

def gerar_ia_propria():
    questoes = []

    # ------------------------------------------------------------------
    # MOTOR 1: TRIGONOMETRIA / PITÁGORAS (Construção Civil)
    # ------------------------------------------------------------------
    # Usa Trios Pitagóricos para dar conta exata: (3,4,5), (6,8,10), (5,12,13)
    trio = random.choice([(3,4,5), (6,8,10), (5,12,13), (8,15,17)])
    cateto1, cateto2, hipotenusa = trio
    
    # Contexto: Escada ou Rampa
    sujeito = get_texto("profissoes")
    estrutura = get_texto("estruturas")
    
    if random.choice(["escada", "sombra"]):
        pergunta = f"{sujeito} {get_texto('verbos')} o comprimento de {estrutura}. A base da estrutura está apoiada no chão a {cateto1} metros de distância da parede, e o topo atinge uma altura de {cateto2} metros. Qual deve ser o comprimento total dessa estrutura (hipotenusa)?"
        dica = "Isso forma um Triângulo Retângulo. Use o Teorema de Pitágoras: a² = b² + c²."
        expl = f"Cateto 1 (b) = {cateto1}m. Cateto 2 (c) = {cateto2}m.\nHipotenusa² = {cateto1}² + {cateto2}²\nH² = {cateto1*cateto1} + {cateto2*cateto2} = {hipotenusa*hipotenusa}\nH = Raiz de {hipotenusa*hipotenusa} = {hipotenusa} metros."
        resp = f"{hipotenusa} metros"
    else:
        pergunta = f"Durante uma reforma, {sujeito} instalou uma viga de {hipotenusa} metros na diagonal. Se a altura da parede é de {cateto2} metros, a que distância da parede a viga foi fixada no chão?"
        dica = "Você tem a Hipotenusa e um Cateto. Use Pitágoras para achar o outro lado."
        expl = f"Hipotenusa = {hipotenusa}. Cateto Conhecido = {cateto2}.\n{hipotenusa}² = {cateto2}² + x²\n{hipotenusa*hipotenusa} = {cateto2*cateto2} + x²\nx² = {hipotenusa*hipotenusa} - {cateto2*cateto2} = {cateto1*cateto1}\nx = {cateto1} metros."
        resp = f"{cateto1} metros"

    q_trig = {
        "id": 1, "tema": "Geometria (Teorema de Pitágoras)",
        "pergunta": pergunta,
        "opcoes": [resp, f"{hipotenusa + 2} metros", f"{cateto1 + cateto2} metros", f"{int((cateto1+cateto2)/2)} metros"],
        "correta": resp, "dica_mestra": dica, "explicacao": expl
    }
    random.shuffle(q_trig['opcoes'])
    questoes.append(q_trig)

    # ------------------------------------------------------------------
    # MOTOR 2: ESTATÍSTICA (Média e Moda)
    # ------------------------------------------------------------------
    # Gera uma lista de números aleatórios (ex: notas, gols, idades)
    lista = [random.randint(1, 10) for _ in range(5)]
    # Garante que tenha uma moda (um número que repete)
    repetido = random.choice(lista)
    lista.append(repetido)
    random.shuffle(lista)
    
    soma = sum(lista)
    media = soma / len(lista)
    lista_str = ", ".join(map(str, lista))
    
    contexto_stat = random.choice(["as notas de um aluno", "o número de vendas diárias", "os gols marcados no campeonato"])
    
    q_stat = {
        "id": 2, "tema": "Estatística Básica",
        "pergunta": f"Um analista registrou {contexto_stat} nos últimos 6 eventos: {{ {lista_str} }}. Qual é, respectivamente, a Média Aritmética e a Moda desse conjunto de dados?",
        "opcoes": [
            f"Média {media:.1f} e Moda {repetido}", 
            f"Média {media+1:.1f} e Moda {repetido}", 
            f"Média {repetido} e Moda {media:.1f}", 
            f"Média {soma} e Moda {repetido}"
        ],
        "correta": f"Média {media:.1f} e Moda {repetido}",
        "dica_mestra": "Média = Soma tudo e divide pela quantidade. Moda = O número que mais aparece.",
        "explicacao": f"1. Soma: {soma}. Quantidade: 6. Média = {soma}/6 = {media:.1f}.\n2. O número que mais se repete na lista é {repetido} (Moda)."
    }
    random.shuffle(q_stat['opcoes'])
    questoes.append(q_stat)

    # ------------------------------------------------------------------
    # MOTOR 3: PROGRESSÃO ARITMÉTICA (Metas e Treinos)
    # ------------------------------------------------------------------
    # An = A1 + (n-1)r
    a1 = random.choice([5, 10, 100, 500]) # Começo
    razao = random.randint(2, 50) # Aumento diário
    n = random.randint(5, 20) # Dias/Meses
    an = a1 + (n - 1) * razao
    
    tipo_pa = random.choice(["treino", "economia"])
    if tipo_pa == "treino":
        texto_pa = f"Um atleta correu {a1} km no primeiro dia de treino e decidiu aumentar sua meta em {razao} km todos os dias."
        pergunta_pa = f"Seguindo esse cronograma, quantos quilômetros ele correrá exatamente no {n}º dia?"
    else:
        texto_pa = f"Para comprar um carro, João guardou R$ {a1},00 no primeiro mês e decidiu aumentar o depósito em R$ {razao},00 a cada mês subsequente."
        pergunta_pa = f"Qual será o valor depositado no {n}º mês?"

    q_pa = {
        "id": 3, "tema": "Progressão Aritmética (PA)",
        "pergunta": f"{texto_pa} {pergunta_pa}",
        "opcoes": [f"{an}", f"{an + razao}", f"{a1 * n}", f"{an - 10}"],
        "correta": f"{an}",
        "dica_mestra": "Use a fórmula do Termo Geral da PA: An = A1 + (n-1).r",
        "explicacao": f"Dados: A1={a1}, Razão(r)={razao}, n={n}.\nCálculo: An = {a1} + ({n}-1)x{razao}\nAn = {a1} + {n-1}x{razao}\nAn = {a1} + {(n-1)*razao} = {an}."
    }
    random.shuffle(q_pa['opcoes'])
    questoes.append(q_pa)

    # ------------------------------------------------------------------
    # MOTOR 4: FUNÇÃO DE 1º GRAU (Uber / Táxi)
    # ------------------------------------------------------------------
    # f(x) = ax + b
    bandeirada = random.choice([4.00, 5.50, 6.00, 10.00])
    km_rodado = random.choice([2.50, 3.00, 4.00])
    distancia = random.randint(8, 25)
    total = bandeirada + (km_rodado * distancia)
    
    q_fun = {
        "id": 4, "tema": "Função Afim (1º Grau)",
        "pergunta": f"Em uma cidade, o serviço de táxi cobra um valor fixo de R$ {bandeirada:.2f} (bandeirada) mais R$ {km_rodado:.2f} por quilômetro rodado. Um passageiro solicitou uma corrida de {distancia} km. Qual o valor final a pagar?",
        "opcoes": [f"R$ {total:.2f}", f"R$ {bandeirada + distancia:.2f}", f"R$ {km_rodado * distancia:.2f}", f"R$ {total+5:.2f}"],
        "correta": f"R$ {total:.2f}",
        "dica_mestra": "Monte a função: Preço = Fixo + (Preço_Km x Distância).",
        "explicacao": f"Função: f(x) = {km_rodado}x + {bandeirada}.\nSubstituindo x por {distancia}: ({km_rodado} * {distancia}) + {bandeirada} = {km_rodado*distancia} + {bandeirada} = R$ {total:.2f}."
    }
    random.shuffle(q_fun['opcoes'])
    questoes.append(q_fun)

    # ------------------------------------------------------------------
    # MOTOR 5: PROBABILIDADE (Urnas e Sorteios)
    # ------------------------------------------------------------------
    vencedores = random.randint(1, 5)
    total_participantes = random.choice([50, 100, 200, 500])
    # Simplificando a fração se possível (didático)
    prob_pct = (vencedores / total_participantes) * 100
    
    q_prob = {
        "id": 5, "tema": "Probabilidade",
        "pergunta": f"Em uma rifa beneficente, foram vendidos {total_participantes} bilhetes numerados. João comprou {vencedores} bilhetes. Supondo que o sorteio seja honesto, qual a probabilidade (em porcentagem) de João ganhar o prêmio?",
        "opcoes": [f"{prob_pct:.1f}%", f"{prob_pct*2:.1f}%", f"{100-prob_pct:.1f}%", "50.0%"],
        "correta": f"{prob_pct:.1f}%",
        "dica_mestra": "Probabilidade = (O que eu quero) dividido pelo (Total Possível). Depois multiplique por 100.",
        "explicacao": f"Favoráveis: {vencedores}. Total: {total_participantes}.\nDivisão: {vencedores} ÷ {total_participantes} = {vencedores/total_participantes}.\nEm porcentagem: {vencedores/total_participantes} x 100 = {prob_pct:.1f}%."
    }
    random.shuffle(q_prob['opcoes'])
    questoes.append(q_prob)

    return questoes

def gerar_questoes_agora():
    return gerar_ia_propria()
