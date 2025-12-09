import google.generativeai as genai
import json
import os
import streamlit as st
import random

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

def gerar_questoes():
    print("--- INICIANDO GERADOR (MODELO UNIVERSAL) ---")
    
    try:
        genai.configure(api_key=minha_chave)
        
        # MUDANÇA AQUI: Usando o nome genérico que funciona em todas as contas novas
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        temas = ["Regra de Três", "Porcentagem", "Geometria Básica", "Média Aritmética", "Equação 1º Grau"]
        tema_vez = random.choice(temas)

        prompt = f"""
        Gere um JSON puro com 2 questões de matemática ENEM sobre: {tema_vez}.
        REGRAS:
        1. Responda APENAS o JSON.
        2. NÃO use Markdown (sem ```json).
        3. NÃO use LaTeX (sem barras invertidas).
        
        Formato: [{"id":1, "tema":"{tema_vez}", "pergunta":"x", "opcoes":["A","B","C","D"], "correta":"A", "explicacao":"x"}]
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        dados = json.loads(texto) 
        
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        # Se der erro de novo, ele avisa qual foi
        erro_tela = [{
            "id": 1, 
            "tema": "⚠️ AINDA COM ERRO", 
            "pergunta": f"Erro técnico: {str(e)}", 
            "opcoes": ["Tentar"], "correta": "Tentar", "explicacao": "."
        }]
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(erro_tela, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    gerar_questoes()
