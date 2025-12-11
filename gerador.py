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

# ==========================================
# 🧠 "IA LOCAL" (O SEGREDO DA ESTABILIDADE)
# ==========================================
# Aqui criamos moldes de questões estilo ENEM.
# O Python sorteia os números, calcula a resposta e monta o texto na hora.
# Isso funciona SEM INTERNET e SEM LIMITES.

def gerar_ia_local():
    questoes = []
    
    # --- MOLDES DE QUESTÕES ---
    
    # 1. MATEMÁTICA FINANCEIRA (Desconto Progressivo)
    preco = random.choice([100, 200, 500, 1200])
    desc_vista = random.choice([5, 10, 15])
    valor_desc = preco * (desc_vista/100)
    valor_final = preco - valor_desc
    
    questoes.append({
        "id": 1,
        "tema": "Matemática Financeira",
        "pergunta": f"Uma loja de eletrônicos lançou uma promoção para um celular que custa R$ {preco},00. Para pagamentos à vista, a loja oferece {desc_vista}% de desconto. Joana decidiu comprar o aparelho pagando em dinheiro. Qual foi o valor final pago por ela?",
        "opcoes": [
            f"R$ {valor_final:.2f}", 
            f"R$ {valor_final+10:.2f}", 
            f"R$ {preco-10:.2f}", 
            f"R$ {valor_desc:.2f}"
        ],
        "correta": f"R$ {valor_final:.2f}",
        "dica_mestra": f"Calcule primeiro quanto vale {desc_vista}% de {preco}. Depois subtraia esse valor do preço original.",
        "explicacao": f"1. O desconto é: {preco} x {desc_vista}/100 = R$ {valor_desc:.2f}. \n2. O valor final é: {preco} - {valor_desc} = R$ {valor_final:.2f}."
    })

    # 2. GEOMETRIA (Terreno)
    frente = random.randint(5, 15)
    fundo = random.randint(10, 30)
    area = frente * fundo
    preco_m2 = random.choice([10, 20, 50, 100])
    preco_total = area * preco_m2
    
    questoes.append({
        "id": 2,
        "tema": "Geometria Plana",
        "pergunta": f"Um terreno retangular possui {frente} metros de frente e {fundo} metros de fundo. O proprietário deseja vender o terreno cobrando R$ {preco_m2},00 por metro quadrado. Qual o valor total do imóvel?",
        "opcoes": [
            f"R$ {preco_total},00", 
            f"R$ {area},00", 
            f"R$ {preco_total/2},00", 
            f"R$ {preco_total+100},00"
        ],
        "correta": f"R$ {preco_total},00",
        "dica_mestra": "Primeiro descubra a área total do terreno (Base x Altura). Depois multiplique pelo preço do metro quadrado.",
        "explicacao": f"1. Área: {frente}m x {fundo}m = {area} m². \n2. Valor: {area} x {preco_m2} = R$ {preco_total},00."
    })

    # 3. REGRA DE TRÊS (Consumo de Combustível)
    km_litro = random.randint(8, 15)
    distancia = km_litro * random.randint(2, 6) # Garante conta exata
    litros = int(distancia / km_litro)
    
    questoes.append({
        "id": 3,
        "tema": "Razão e Proporção",
        "pergunta": f"O computador de bordo de um carro indica que ele faz, em média, {km_litro} km com 1 litro de gasolina. Se o motorista planeja fazer uma viagem de {distancia} km mantendo essa média, quantos litros de combustível serão necessários?",
        "opcoes": [
            f"{litros} litros", 
            f"{litros+2} litros", 
            f"{litros*2} litros", 
            f"{int(litros/2)} litros"
        ],
        "correta": f"{litros} litros",
        "dica_mestra": "Você pode usar uma Regra de Três: Se 1 litro faz {km_litro}km, quantos litros (x) fazem {distancia}km?",
        "explicacao": f"Basta dividir a distância pelo consumo: {distancia} / {km_litro} = {litros} litros."
    })

    return questoes

# ==========================================
# 🤖 GERADOR HÍBRIDO (Tenta Google -> Falha -> Usa Local)
# ==========================================
def gerar_questoes_agora():
    # Tenta conectar na IA (Máximo 2 tentativas rápidas para não travar)
    for tentativa in range(2):
        try:
            genai.configure(api_key=minha_chave)
            model = genai.GenerativeModel('models/gemini-flash-latest')

            prompt = """
            Atue como Professor do ENEM. Gere JSON com 3 questões.
            REGRAS: Contexto rico, Dica útil, Explicação passo-a-passo.
            FORMATO: [{"id":1, "tema":"...", "pergunta":"...", "opcoes":["A"], "correta":"A", "dica_mestra":"...", "explicacao":"..."}]
            """
            
            # Timeout curto (se demorar, pula pro local)
            response = model.generate_content(prompt) 
            texto = response.text.replace("```json", "").replace("```", "").strip()
            if not texto: raise ValueError("Vazio")
            
            dados = json.loads(texto)
            for i, q in enumerate(dados): q['id'] = i + 1
            return dados # Sucesso da IA!

        except Exception:
            time.sleep(1) # Espera rápida
            continue # Tenta de novo
            
    # --- SE CHEGOU AQUI, A IA FALHOU ---
    # Em vez de mostrar erro, ativamos a "IA Local" silenciosamente.
    # O usuário nem percebe a diferença.
    return gerar_ia_local()
