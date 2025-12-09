import google.generativeai as genai
import json
import os
import streamlit as st

# --- SEGURANÇA: PEGA A CHAVE DA NUVEM OU DO SEU PC ---
try:
    # Tenta pegar dos Segredos do Streamlit (Nuvem)
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    # Se não achar, usa a sua chave direta (Local)
    # COLE SUA CHAVE AQUI SE FOR RODAR NO PC:
    minha_chave = "AIzaSyD-ox5a1bK-san7Ki3qcNkZr-8fsPTT3KE"

genai.configure(api_key=minha_chave)

MODELO_ESCOLHIDO = 'models/gemini-flash-latest'

def gerar_questoes():
    print(f"--- FÁBRICA CLOUD (Modelo: {MODELO_ESCOLHIDO}) ---")
    model = genai.GenerativeModel(MODELO_ESCOLHIDO)
    
    prompt = """
    Gere um JSON puro com 4 questões de matemática para o ENEM.
    REGRAS: NÃO use LaTeX/Barras invertidas. Texto simples.
    Temas: Regra de Três, Porcentagem, Geometria, Estatística.
    Estrutura JSON:
    [{"id": 1, "tema": "x", "pergunta": "x", "opcoes": ["A","B"], "correta": "A", "explicacao": "x"}]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip().replace("\\", "/")
        novas_questoes = json.loads(text)
        
        for i, q in enumerate(novas_questoes):
            q['id'] = i + 1
            
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(novas_questoes, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    gerar_questoes()