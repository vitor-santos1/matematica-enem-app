import random
import math

# ==============================================================================
# 🧠 VITOR-AI: MOTOR DE GERAÇÃO PROCEDURAL (SEM INTERNET)
# ==============================================================================
# Esta "IA" constrói questões frase por frase usando bancos de dados semânticos.
# Resultado: Questões infinitas, complexas e sempre diferentes.

def get_texto(tipo):
    """Banco de dados criativo para montar frases dinâmicas."""
    db = {
        "cientistas": ["Um engenheiro nuclear", "Uma bióloga marinha", "Um pesquisador da USP", "Um químico industrial", "Um geólogo"],
        "locais": ["em um laboratório de alta tecnologia", "em uma expedição na Antártida", "durante uma análise de campo", "no centro de controle"],
        "verbos_crescimento": ["observou um crescimento acelerado", "notou uma multiplicação exponencial", "registrou um aumento progressivo"],
        "verbos_queda": ["detectou um decaimento radioativo", "mediu a desvalorização do ativo", "analisou a redução da concentração"],
        "microorganismos": ["de uma colônia de bactérias", "de uma cultura de vírus", "de algas microscópicas", "de células-tronco"],
        "elementos_quimicos": ["do Isótopo Césio-137", "de uma amostra de Urânio", "de um composto instável", "de Carbono-14"],
        "conectivos_dica": ["Lembre-se que", "Note que", "Considere o fato de que", "Atenção à regra:"],
    }
    return random.choice(db[tipo])

def gerar_ia_propria():
    questoes = []

    # ------------------------------------------------------------------
    # MOTOR 1: FUNÇÃO EXPONENCIAL (Crescimento/Decaimento)
    # ------------------------------------------------------------------
    # A IA decide na hora se é uma questão de Biologia (Crescer) ou Física (Cair)
    modo = random.choice(["biologia", "fisica"])
    
    if modo == "biologia":
        sujeito = get_texto("cientistas")
        local = get_texto("locais")
        verbo = get_texto("verbos_crescimento")
        objeto = get_texto("microorganismos")
        
        inicial = random.choice([100, 200, 500, 1000])
        tempo = random.randint(3, 8) # horas
        base = 2 # dobra
        final = inicial * (base ** tempo)
        
        pergunta = f"{sujeito}, trabalhando {local}, {verbo} {objeto}. No início do experimento, haviam exatos {inicial} organismos. Sabendo que essa população dobra a cada hora, qual será a quantidade total após {tempo} horas?"
        dica = f"{get_texto('conectivos_dica')} uma duplicação a cada hora é uma Função Exponencial de base 2."
        expl = f"Fórmula: N(t) = N0 . 2^t\nCálculo: {inicial} . 2^{tempo} = {inicial} . {2**tempo} = {final} organismos."
    
    else: # Fisica (Radioatividade)
        sujeito = get_texto("cientistas")
        objeto = get_texto("elementos_quimicos")
        verbo = get_texto("verbos_queda")
        
        inicial = random.choice([100, 80, 64, 128]) # gramas
        meia_vida = random.randint(10, 30) # anos
        ciclos = random.randint(2, 4)
        tempo_total = meia_vida * ciclos
        final = inicial / (2 ** ciclos)
        
        pergunta = f"{sujeito} {verbo} {objeto}. A amostra inicial tinha {inicial}g. Sabendo que a meia-vida desse material é de {meia_vida} anos, qual será a massa restante após {tempo_total} anos?"
        dica = f"{get_texto('conectivos_dica')} a cada 'meia-vida', a massa é dividida por 2."
        expl = f"Tempo passado: {tempo_total} anos. Isso equivale a {ciclos} meias-vidas ({tempo_total}/{meia_vida}).\nCálculo: {inicial} dividido por 2, {ciclos} vezes = {final}g."

    q1 = {
        "id": 1, "tema": f"Função Exponencial ({modo.capitalize()})",
        "pergunta": pergunta,
        "opcoes": [f"{final}", f"{final*2}", f"{inicial}", f"{final/2}"],
        "correta": f"{final}", "dica_mestra": dica, "explicacao": expl
    }
    random.shuffle(q1['opcoes'])
    questoes.append(q1)

    # ------------------------------------------------------------------
    # MOTOR 2: MATEMÁTICA FINANCEIRA (Histórias de Fraude/Lucro)
    # ------------------------------------------------------------------
    # Contexto: Investimento ou Dívida
    tipo_fin = random.choice(["investimento", "divida"])
    capital = random.choice([1000, 2000, 5000, 10000])
    taxa = random.choice([5, 10, 20])
    meses = 2
    
    if tipo_fin == "investimento":
        contexto = f"Um jovem empreendedor decidiu aplicar R$ {capital},00 em uma startup de tecnologia."
        acao = "O contrato prometia um retorno de"
        final_simples = capital + (capital * (taxa/100) * meses)
        # Juros compostos simulados na mao
        m1 = capital * (1 + taxa/100)
        m2 = m1 * (1 + taxa/100)
        final_composto = int(m2)
        pergunta_fim = f"Se o regime for de Juros Compostos, qual o montante após {meses} meses?"
        
    else: # Divida
        contexto = f"Devido a um imprevisto médico, uma família precisou pegar um empréstimo de R$ {capital},00 no banco."
        acao = "A taxa cobrada pelo banco foi de"
        m1 = capital * (1 + taxa/100)
        m2 = m1 * (1 + taxa/100)
        final_composto = int(m2)
        pergunta_fim = f"Considerando Juros Compostos, qual o valor total da dívida após {meses} meses?"

    q2 = {
        "id": 2, "tema": "Matemática Financeira",
        "pergunta": f"{contexto} {acao} {taxa}% ao mês. {pergunta_fim}",
        "opcoes": [f"R$ {final_composto},00", f"R$ {capital},00", f"R$ {int(capital * 2)},00", f"R$ {int(final_composto * 1.5)},00"],
        "correta": f"R$ {final_composto},00",
        "dica_mestra": "Juros Compostos é 'Juro sobre Juro'. Calcule mês a mês.",
        "explicacao": f"Mês 1: {capital} + {taxa}% = {int(m1)}. \nMês 2: {int(m1)} + {taxa}% = {final_composto}."
    }
    random.shuffle(q2['opcoes'])
    questoes.append(q2)

    # ------------------------------------------------------------------
    # MOTOR 3: ANÁLISE COMBINATÓRIA (Situações de Risco)
    # ------------------------------------------------------------------
    # Contexto: Senhas ou Cofres
    digitos = random.randint(3, 5)
    total = 10 ** digitos
    cenario = random.choice([
        f"O cofre de segurança máxima de um banco possui uma senha digital de {digitos} dígitos.",
        f"Para desbloquear um smartphone apreendido, a perícia precisa descobrir um código de {digitos} dígitos."
    ])
    
    q3 = {
        "id": 3, "tema": "Análise Combinatória",
        "pergunta": f"{cenario} Sabendo que os dígitos podem ser quaisquer números de 0 a 9 e que podem se repetir, quantas tentativas no máximo seriam necessárias para descobrir o código na força bruta?",
        "opcoes": [f"{total}", f"{10*digitos}", f"{9**digitos}", f"{total*10}"],
        "correta": f"{total}",
        "dica_mestra": "Princípio Fundamental da Contagem: 10 opções para a primeira casa, 10 para a segunda...",
        "explicacao": f"Temos {digitos} posições. Cada uma tem 10 possibilidades.\nConta: 10 elevado a {digitos} = {total} combinações."
    }
    random.shuffle(q3['opcoes'])
    questoes.append(q3)

    return questoes

# Função que o app.py vai chamar (Nome deve ser igual ao do app.py)
def gerar_questoes_agora():
    return gerar_ia_propria()
