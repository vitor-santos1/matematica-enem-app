import google.generativeai as genai
import json
import streamlit as st
import random

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

def gerar_questoes_agora():
    print("--- TENTANDO GERAR ---")
    try:
        genai.configure(api_key=minha_chave)
        
        # Vamos tentar o modelo flash-latest
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        temas = ["Porcentagem", "Áreas", "Média", "Equações"]
        tema_vez = random.choice(temas)

        # A CORREÇÃO ESTÁ AQUI EMBAIXO (Nas chaves duplas {{ }})
        prompt = f"""
        Gere um JSON puro com 3 questões de matemática sobre: {tema_vez}.
        REGRAS: 
        1. Responda APENAS o JSON.
        2. Texto simples (sem LaTeX).
        Formato: [{{ "id":1, "tema":"{tema_vez}", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..." }}]
        """
        
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        # Ajusta IDs
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        return dados 

    except Exception as e:
        # Mostra o erro na tela se falhar de novo
        return [{
            "id": 1, 
            "tema": "⚠️ ERRO TÉCNICO", 
            "pergunta": f"Ocorreu um erro: {str(e)}", 
            "opcoes": ["Tentar Novamente"], 
            "correta": "Tentar Novamente", 
            "explicacao": "Mande foto desse erro para o suporte."
        }]
