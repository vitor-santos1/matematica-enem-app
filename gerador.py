import google.generativeai as genai
import json
import os
import streamlit as st
import random

# --- 1. PEGAR CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# --- 2. BACKUP ALEATÓRIO (Para não ficar repetitivo se a IA falhar) ---
def pegar_backup():
    return [
        {
            "id": 1, "tema": "Matemática (Modo Offline)", 
            "pergunta": f"Quanto é {random.randint(2,9)} x {random.randint(5,15)}?", 
            "opcoes": ["Calculando...", "Verifique na calculadora", "Resultado exato", "Erro"], 
            "correta": "Resultado exato", "explicacao": "Multiplicação simples."
        },
        {
            "id": 2, "tema": "Porcentagem (Modo Offline)", 
            "pergunta": "Quanto é 50% de 200?", 
            "opcoes": ["100", "50", "20", "150"], 
            "correta": "100", "explicacao": "Metade de 200."
        }
    ]

def gerar_questoes():
    print("--- TENTANDO IA FLASH ---")
    
    try:
        genai.configure(api_key=minha_chave)
        
        # VOLTAMOS PARA O MODELO RÁPIDO QUE FUNCIONA NA SUA CONTA
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        # Sorteia tema para obrigar a mudar
        temas = ["Geometria", "Regra de Três", "Probabilidade", "Médias", "Equações"]
        tema = random.choice(temas)
        
        prompt = f"""
        Gere um JSON puro com 3 questões de matemática ENEM sobre: {tema}.
        REGRAS:
        1. Responda APENAS o JSON.
        2. NÃO use Markdown. NÃO use LaTeX.
        3. Texto simples.
        
        Formato: [{"id":1, "tema":"{tema}", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..."}]
        """
        
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print("✅ SUCESSO! Perguntas novas geradas.")

    except Exception as e:
        print(f"⚠️ IA falhou: {e}. Usando backup.")
        # Se falhar, gera um backup
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(pegar_backup(), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    gerar_questoes()
