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

# --- 1. GERADOR INFINITO (BACKUP INTELIGENTE) ---
# Este gerador cria questões completas (com dicas e explicações) se a IA falhar.
def gerar_backup_infinito():
    questoes = []
    
    # Questão 1: Porcentagem
    total = random.choice([100, 200, 500, 1000])
    perc = random.choice([10, 20, 25, 50])
    res_p = int(total * (perc/100))
    questoes.append({
        "id": 1, 
        "tema": "Matemática Financeira (Modo Offline)",
        "pergunta": f"Uma loja está oferecendo {perc}% de desconto em um produto que custa R$ {total},00. Qual o valor do desconto?",
        "opcoes": [f"R$ {res_p},00", f"R$ {res_p+10},00", f"R$ {res_p*2},00", f"R$ {int(res_p/2)},00"],
        "correta": f"R$ {res_p},00", 
        "dica_mestra": f"Lembre-se que {perc}% é a mesma coisa que dividir por {int(100/perc)} (ou multiplicar por 0,{perc}).",
        "explicacao": f"O cálculo é: {total} x {perc}/100 = {res_p}. O desconto é de R$ {res_p},00."
    })

    # Questão 2: Geometria
    lado = random.randint(4, 12)
    area = lado * lado
    questoes.append({
        "id": 2, 
        "tema": "Geometria Plana (Modo Offline)",
        "pergunta": f"Um arquiteto projetou uma sala quadrada com {lado} metros de lado. Quantos metros quadrados de piso serão necessários?",
        "opcoes": [f"{area} m²", f"{area+5} m²", f"{lado*4} m²", f"{area*2} m²"],
        "correta": f"{area} m²", 
        "dica_mestra": "A área de um quadrado é calculada multiplicando a medida do lado por ela mesma (L x L).",
        "explicacao": f"Como o lado é {lado}, fazemos {lado} x {lado} = {area} m²."
    })

    # Questão 3: Cálculo Básico
    n1 = random.randint(20, 100)
    n2 = random.randint(10, 90)
    soma = n1 + n2
    questoes.append({
        "id": 3, 
        "tema": "Cálculo Mental (Modo Offline)",
        "pergunta": f"Para conferir o troco, você precisa somar rapidamente R$ {n1},00 com R$ {n2},00. Qual o total?",
        "opcoes": [f"R$ {soma},00", f"R$ {soma+10},00", f"R$ {soma-5},00", f"R$ {soma-10},00"],
        "correta": f"R$ {soma},00", 
        "dica_mestra": "Tente somar primeiro as dezenas e depois as unidades.",
        "explicacao": f"A soma exata é {n1} + {n2} = {soma}."
    })

    return questoes

# --- 2. GERADOR PRINCIPAL (IA) ---
def gerar_questoes_agora():
    tentativas = 0
    # Tenta conectar na IA 3 vezes
    while tentativas < 3:
        try:
            genai.configure(api_key=minha_chave)
            # Trocamos para o modelo 'flash' que é mais rápido
            model = genai.GenerativeModel('models/gemini-flash-latest')

            prompt = """
            Atue como um Professor de Matemática Especialista no ENEM.
            Gere um JSON com 3 questões de nível médio.

            REGRAS DE PEDAGOGIA:
            1. Contexto: Situações reais (compras, construção, viagens).
            2. Dica: Crie uma "dica_mestra" útil.
            3. Explicação: Passo a passo detalhado.
            4. APENAS JSON, sem markdown.

            FORMATO:
            [
                {
                    "id": 1, "tema": "...", "pergunta": "...", "opcoes": ["A", "B"], 
                    "correta": "A", "dica_mestra": "...", "explicacao": "..."
                }
            ]
            """
            
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            # Se vier vazio, força erro pra cair no retry
            if not texto: raise ValueError("Vazio")

            dados = json.loads(texto)
            for i, q in enumerate(dados): q['id'] = i + 1
            return dados

        except Exception:
            # Se der erro, espera um pouco e tenta de novo
            time.sleep(2)
            tentativas += 1
            
    # --- SE A IA FALHAR TUDO, CHAMA O BACKUP INFINITO ---
    # Aqui é a mudança: em vez de mostrar erro, ele calcula matemática nova!
    print("⚠️ IA falhou. Usando modo offline.")
    return gerar_backup_infinito()
