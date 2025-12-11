import google.generativeai as genai
import json
import streamlit as st
import random
import time
import math

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# ==============================================================================
# ☢️ MOTOR DE COMPLEXIDADE (FALLBACK CIENTÍFICO)
# ==============================================================================
# Este motor gera questões de alto nível (Logaritmo, Exponencial, Combinatória)
# Ele entra em ação apenas se a IA do Google estiver travada.

def gerar_complexidade_cientifica():
    questoes = []

    # --- TEMA 1: FUNÇÃO EXPONENCIAL (Crescimento de Bactérias / Meia-Vida) ---
    tipo = random.choice(["bacterias", "radioativo"])
    
    if tipo == "bacterias":
        inicial = random.choice([100, 200, 500])
        taxa = 2 # Dobra
        tempo_h = random.randint(3, 6)
        final = inicial * (taxa ** tempo_h)
        texto_base = f"Em um experimento biológico controlado, uma cultura de bactérias se reproduz de forma binária, duplicando sua população a cada hora. No início do experimento (t=0), haviam {inicial} microrganismos."
        pergunta = f"{texto_base} Considerando que as condições de temperatura e nutrientes permaneceram ideais, qual será a população exata de bactérias após {tempo_h} horas?"
        expl = f"Função Exponencial: N(t) = N0 . 2^t. \nCálculo: {inicial} . 2^{tempo_h} = {inicial} . {2**tempo_h} = {final}."
        
    else: # Radioativo
        inicial = random.choice([100, 80, 64]) # Gramas
        meia_vida = random.randint(10, 30) # Anos
        ciclos = random.randint(2, 4)
        tempo_passado = meia_vida * ciclos
        final = inicial / (2 ** ciclos)
        texto_base = f"O Césio-137 é um isótopo radioativo cuja meia-vida é de aproximadamente {meia_vida} anos. Uma amostra isolada continha inicialmente {inicial}g desse material."
        pergunta = f"{texto_base} Passados exatos {tempo_passado} anos, qual a massa restante de material radioativo nessa amostra?"
        expl = f"Meia-vida significa que a massa cai pela metade a cada ciclo. \nTempo passado: {tempo_passado} anos = {ciclos} meias-vidas. \nCálculo: {inicial} dividido por 2, {ciclos} vezes = {final}g."

    q1 = {
        "id": 1, "tema": "Função Exponencial e Biologia/Física",
        "pergunta": pergunta,
        "opcoes": [f"{final}", f"{final*2}", f"{final/2}", f"{inicial + tempo_h if tipo=='bacterias' else inicial - ciclos}"],
        "correta": f"{final}",
        "explicacao": expl
    }
    random.shuffle(q1['opcoes'])
    questoes.append(q1)

    # --- TEMA 2: LOGARITMOS (Terremotos / pH Químico) ---
    if random.choice([True, False]):
        # Escala Richter
        energia_base = 1000
        fator = random.randint(4, 8) # Potência de 10
        energia_real = energia_base * (10**fator)
        magnitude = math.log10(energia_real) - math.log10(energia_base) # Simplificado M = log(E)
        # Vamos usar a fórmula M = log10(Energia) para simplificar didaticamente
        magnitude_real = fator
        
        pergunta = f"A magnitude M de um terremoto na escala Richter pode ser calculada pelo logaritmo decimal da energia liberada E (em joules), dada pela fórmula simplificada M = log(E). Se um terremoto liberou uma energia de 10^{magnitude_real} Joules, qual foi sua magnitude?"
        res = f"{magnitude_real}"
        expl = f"Propriedade dos Logaritmos: log(10^x) = x. \nSe a energia é 10^{magnitude_real}, então log(10^{magnitude_real}) = {magnitude_real}."
    else:
        # pH Químico
        concentracao = random.choice([2, 3, 4, 5]) # 10^-x
        ph = concentracao
        pergunta = f"O potencial hidrogeniônico (pH) de uma solução é dado pela fórmula pH = -log[H+], onde [H+] é a concentração de íons de hidrogênio em mol/L. Uma análise em laboratório indicou que uma amostra de chuva ácida possui [H+] = 10^(-{ph}) mol/L. Qual o pH dessa chuva?"
        res = f"{ph}"
        expl = f"Fórmula: pH = -log(10^-{ph}). \nPela propriedade de logaritmos: log(10^x) = x. \nLogo: -(-{ph}) = {ph}."

    q2 = {
        "id": 2, "tema": "Logaritmos e Escalas",
        "pergunta": pergunta,
        "opcoes": [f"{res}", f"{int(res)+2}", f"{int(res)*2}", "10"],
        "correta": f"{res}",
        "explicacao": expl
    }
    random.shuffle(q2['opcoes'])
    questoes.append(q2)

    # --- TEMA 3: ANÁLISE COMBINATÓRIA (Senhas / Times) ---
    n = random.randint(5, 8) # Pessoas
    p = 3 # Pódio (Ouro, Prata, Bronze)
    # Arranjo: A(n,p) = n! / (n-p)!
    arranjo = math.perm(n, p)
    
    q3 = {
        "id": 3, "tema": "Análise Combinatória",
        "pergunta": f"Em uma final olímpica de natação, {n} atletas disputam as medalhas de Ouro, Prata e Bronze. Não havendo empates, de quantas maneiras diferentes o pódio pode ser formado?",
        "opcoes": [f"{arranjo}", f"{math.comb(n,p)}", f"{n*p}", f"{n**p}"],
        "correta": f"{arranjo}",
        "explicacao": f"Como a ordem importa (Ouro é diferente de Prata), usamos Arranjo. \nCálculo: {n} opções para Ouro x {n-1} para Prata x {n-2} para Bronze = {n}x{n-1}x{n-2} = {arranjo}."
    }
    random.shuffle(q3['opcoes'])
    questoes.append(q3)

    return questoes

# ==============================================================================
# 🧠 CÉREBRO PRINCIPAL (IA GEMINI COM INSISTÊNCIA)
# ==============================================================================
def gerar_questoes_agora():
    
    # 1. TENTA A IA (GOOGLE) - 3 TENTATIVAS AGRESSIVAS
    # Usamos temperatura alta para criatividade máxima
    config_criativa = genai.types.GenerationConfig(temperature=1.0)
    
    for tentativa in range(3):
        try:
            genai.configure(api_key=minha_chave)
            model = genai.GenerativeModel('models/gemini-flash-latest', generation_config=config_criativa)
            
            prompt = """
            Aja como o Banco Nacional de Itens do INEP (ENEM).
            Gere um JSON com 3 questões de matemática NÍVEL DIFÍCIL.
            
            REGRAS OBRIGATÓRIAS:
            1. **Interdisciplinaridade:** Contexto longo (Biologia, Geografia, Economia).
            2. **Complexidade:** Exija raciocínio lógico, não apenas conta.
            3. **Formato:** JSON puro.
            
            FORMATO:
            [{"id":1, "tema":"Tema", "pergunta":"Texto longo...", "opcoes":["A","B"], "correta":"A", "explicacao":"Passo a passo..."}]
            """
            
            # Timeout curto para não travar
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            if not texto: raise ValueError("Vazio")
            
            dados = json.loads(texto)
            
            # Embaralha e retorna se deu certo
            for i, q in enumerate(dados):
                random.shuffle(q['opcoes'])
                q['id'] = i + 1
            return dados

        except Exception as e:
            # Se deu erro, espera 1 segundo e tenta de novo
            time.sleep(1)
            continue

    # 2. SE A IA FALHAR NAS 3 TENTATIVAS, ATIVA O MOTOR CIENTÍFICO
    # Isso garante que SEMPRE haverá questão complexa, nunca "erro".
    return gerar_complexidade_cientifica()
