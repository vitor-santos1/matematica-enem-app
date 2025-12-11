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

# ======================================================
# 🧠 MOTOR MATEMÁTICO (Gera Questões + Explicações)
# ======================================================
def gerar_offline_complexo():
    questoes = []

    # --- MOLDE 1: LOGARITMOS (Terremotos/Escala Richter) ---
    energia = random.choice([1000, 10000, 100000, 1000000])
    # Richter R = log10(E) - C (Simplificado para R = log10(E))
    magnitude = int(math.log10(energia))
    
    q1 = {
        "id": 0, "tema": "Logaritmos e Escalas",
        "pergunta": f"A magnitude de um terremoto pode ser medida pela escala Richter, que é baseada em logaritmos. Suponha que a energia liberada E seja dada por {energia} unidades e a magnitude M seja dada pela fórmula M = log(E) (na base 10). Qual foi a magnitude desse terremoto?",
        "opcoes": [f"{magnitude}", f"{magnitude*2}", f"{magnitude+1}", f"{magnitude-2}"],
        "correta": f"{magnitude}",
        "explicacao": f"A fórmula é M = log10({energia}). \nSabemos que {energia} é igual a 10 elevado a {magnitude}. \nLogo, o logaritmo na base 10 é {magnitude}."
    }
    random.shuffle(q1['opcoes'])
    questoes.append(q1)

    # --- MOLDE 2: ANÁLISE COMBINATÓRIA (Placas de Carro) ---
    letras = 3
    numeros = 4
    # Placa antiga: LLL-NNNN (26^3 * 10^4)
    total = (26**3) * (10**4)
    
    q2 = {
        "id": 0, "tema": "Análise Combinatória",
        "pergunta": f"Um sistema de emplacamento antigo utilizava 3 letras (de um alfabeto de 26) seguidas de 4 algarismos (0 a 9). O número total de placas possíveis que podiam ser formadas nesse sistema é dado por:",
        "opcoes": [
            "26³ x 10⁴", 
            "26 x 10", 
            "26⁴ x 10³", 
            "26 + 10"
        ],
        "correta": "26³ x 10⁴",
        "explicacao": f"Temos 3 posições para letras (26 opções cada) e 4 para números (10 opções cada). \nPelo Princípio Multiplicativo: 26x26x26 x 10x10x10x10 = 26³ x 10⁴."
    }
    random.shuffle(q2['opcoes'])
    questoes.append(q2)

    # --- MOLDE 3: MATRIZES (Custo de Produção) ---
    a11 = random.randint(2, 5) # Peças A na fábrica 1
    a12 = random.randint(2, 5) # Peças B na fábrica 1
    custo_a = 10
    custo_b = 20
    custo_total = (a11 * custo_a) + (a12 * custo_b)
    
    q3 = {
        "id": 0, "tema": "Matrizes e Custos",
        "pergunta": f"Uma fábrica possui uma matriz de produção onde a primeira linha [ {a11}  {a12} ] representa a quantidade de produtos do tipo A e B produzidos no dia. Se o custo do produto A é R$ 10,00 e do produto B é R$ 20,00 (vetor custo C = [10, 20]), qual o custo total dessa produção (Produto da Matriz pelo Vetor)?",
        "opcoes": [f"R$ {custo_total},00", f"R$ {custo_total+50},00", f"R$ {custo_total-20},00", f"R$ {custo_total*2},00"],
        "correta": f"R$ {custo_total},00",
        "explicacao": f"Multiplicação de matrizes: ({a11} x 10) + ({a12} x 20) \n= {a11*10} + {a12*20} \n= R$ {custo_total},00."
    }
    random.shuffle(q3['opcoes'])
    questoes.append(q3)

    # --- MOLDE 4: JUROS COMPOSTOS (Investimento) ---
    capital = 1000
    taxa = 10
    tempo = 2
    # Mês 1 = 1100. Mês 2 = 1210.
    montante = 1210 
    
    q4 = {
        "id": 0, "tema": "Matemática Financeira",
        "pergunta": f"Um capital de R$ 1000,00 é aplicado a juros compostos de 10% ao mês por 2 meses. Qual o montante final?",
        "opcoes": ["R$ 1210,00", "R$ 1200,00", "R$ 1100,00", "R$ 1300,00"],
        "correta": "R$ 1210,00",
        "explicacao": "Mês 1: 1000 + 10% = 1100. \nMês 2: 1100 + 10% (que é 110) = 1210. \nNota: Se fosse juros simples, seria 1200."
    }
    random.shuffle(q4['opcoes'])
    questoes.append(q4)

    return questoes

# ==========================================
# 🚀 GERADOR HÍBRIDO (Nunca Falha)
# ==========================================
def gerar_questoes_agora():
    # Tenta IA (Google) - Apenas 1 tentativa rápida
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        prompt = """
        Gere JSON com 3 questões de matemática ENEM.
        Obrigatório ter campo "explicacao".
        Formato: [{"id":1, "tema":"x", "pergunta":"x", "opcoes":["A"], "correta":"A", "explicacao":"Resolução detalhada..."}]
        """
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        # Embaralha e numera
        for i, q in enumerate(dados):
            random.shuffle(q['opcoes'])
            q['id'] = i + 1
            # Garante que explicação existe
            if "explicacao" not in q: q["explicacao"] = "Resolução calculada passo a passo."
            
        return dados 

    except Exception:
        # Se der erro de cota ou internet, usa o motor local
        # O usuário nem percebe a diferença
        return gerar_offline_complexo()
