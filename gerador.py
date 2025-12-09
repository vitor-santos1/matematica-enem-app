import google.generativeai as genai
import json
import streamlit as st
import random
import time

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# --- GERADOR MATEMÁTICO (Caso a IA falhe, ele cria matemática na hora) ---
def gerar_backup_infinito():
    questoes = []
    
    # 1. SOMA/SUBTRAÇÃO ALEATÓRIA
    n1 = random.randint(10, 200)
    n2 = random.randint(5, 100)
    op = random.choice(['+', '-'])
    res = n1 + n2 if op == '+' else n1 - n2
    questoes.append({
        "id": 1, "tema": "Cálculo Rápido (Modo Infinito)",
        "pergunta": f"Quanto é {n1} {op} {n2}?",
        "opcoes": [str(res), str(res+5), str(res-2), str(res+10)],
        "correta": str(res), "explicacao": "Cálculo básico."
    })

    # 2. PORCENTAGEM ALEATÓRIA
    total = random.choice([50, 100, 200, 400, 500, 1000])
    perc = random.choice([10, 20, 25, 50])
    res_p = int(total * (perc/100))
    questoes.append({
        "id": 2, "tema": "Porcentagem (Modo Infinito)",
        "pergunta": f"Quanto é {perc}% de {total}?",
        "opcoes": [str(res_p), str(res_p+10), str(res_p*2), str(int(res_p/2))],
        "correta": str(res_p), "explicacao": f"{perc}% de {total} é {res_p}."
    })

    # 3. GEOMETRIA ALEATÓRIA
    lado = random.randint(3, 12)
    area = lado * lado
    questoes.append({
        "id": 3, "tema": "Geometria (Modo Infinito)",
        "pergunta": f"Qual a área de um quadrado de lado {lado}m?",
        "opcoes": [f"{area}m²", f"{area+5}m²", f"{area*2}m²", f"{lado*4}m²"],
        "correta": f"{area}m²", "explicacao": f"Área = Lado x Lado ({lado} x {lado})."
    })

    # 4. REGRA DE TRÊS
    qtd = random.randint(2, 5)
    preco_un = random.randint(2, 10)
    total_re = qtd * preco_un
    questoes.append({
        "id": 4, "tema": "Regra de Três (Modo Infinito)",
        "pergunta": f"Se 1 caneta custa R$ {preco_un}, quanto custam {qtd} canetas?",
        "opcoes": [f"R$ {total_re}", f"R$ {total_re+2}", f"R$ {total_re-1}", f"R$ {total_re*2}"],
        "correta": f"R$ {total_re}", "explicacao": "Multiplicação simples."
    })

    return questoes

def gerar_questoes_agora():
    # Tenta usar a IA primeiro
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')

        prompt = """
        Gere um JSON puro com 4 questões de matemática ENEM variadas.
        REGRAS: 
        1. APENAS JSON. Sem markdown. 
        2. Texto simples.
        Formato: [{"id":1, "tema":"x", "pergunta":"x", "opcoes":["A","B"], "correta":"A", "explicacao":"x"}]
        """
        
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        for i, q in enumerate(dados): q['id'] = i + 1
        return dados 

    except Exception as e:
        print(f"⚠️ IA falhou: {e}. Gerando matemática aleatória.")
        # SE A IA FALHAR, ELE CHAMA O GERADOR INFINITO (NUNCA REPETE)
        return gerar_backup_infinito()
