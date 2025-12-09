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

def gerar_questoes_agora():
    # Tenta até 3 vezes se der erro de "Cota Excedida"
    tentativas = 0
    max_tentativas = 3
    
    genai.configure(api_key=minha_chave)
    # Usando o modelo flash-latest que é o mais rápido
    model = genai.GenerativeModel('models/gemini-flash-latest')

    while tentativas < max_tentativas:
        print(f"--- TENTATIVA IA {tentativas+1}/{max_tentativas} ---")
        try:
            # Sorteia tema para não ficar repetitivo
            temas = [
                "Porcentagem com descontos", 
                "Geometria (Área e Perímetro)", 
                "Média Aritmética de notas", 
                "Regra de Três simples", 
                "Equação de 1º Grau no cotidiano"
            ]
            tema_vez = random.choice(temas)

            prompt = f"""
            Gere um JSON puro com 3 questões de matemática estilo ENEM sobre: {tema_vez}.
            
            REGRAS OBRIGATÓRIAS:
            1. Responda APENAS o JSON. Nada de texto antes ou depois.
            2. NÃO use Markdown (não use ```json).
            3. NÃO use LaTeX ou barras invertidas. Escreva por extenso.
            4. Crie enunciados criativos e diferentes.
            
            Formato: [{{ "id":1, "tema":"{tema_vez}", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..." }}]
            """
            
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            # Se vier vazio ou errado, força erro pra tentar de novo
            if not texto: raise ValueError("Resposta vazia")
            
            dados = json.loads(texto)
            
            # Ajusta IDs e retorna (SUCESSO!)
            for i, q in enumerate(dados): q['id'] = i + 1
            return dados 

        except Exception as e:
            # Se o erro for de COTA (429), espera e tenta de novo
            erro_str = str(e).lower()
            if "429" in erro_str or "quota" in erro_str:
                print("⚠️ Cota cheia. Esperando 5 segundos...")
                time.sleep(5) # Espera a IA "esfriar"
                tentativas += 1
            else:
                # Se for outro erro (ex: JSON inválido), tenta de novo imediatamente
                print(f"⚠️ Erro de formato: {e}")
                tentativas += 1
    
    # Se falhar 3 vezes seguidas, aí sim mostra aviso de erro (pra não travar o site)
    return [{
        "id": 1, 
        "tema": "⚠️ IA Ocupada", 
        "pergunta": "O Google Gemini está superlotado agora. Espere 30 segundos e tente de novo.", 
        "opcoes": ["Tentar Novamente"], 
        "correta": "Tentar Novamente", 
        "explicacao": "Muitas requisições ao mesmo tempo."
    }]
