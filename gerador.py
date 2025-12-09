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
    print("--- INICIANDO ---")
    
    try:
        genai.configure(api_key=minha_chave)
        # Vamos usar o modelo Flash 1.5 que é mais garantido
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Sorteia temas para garantir que mude sempre
        temas_possiveis = ["Juros Simples", "Área de Círculos", "Média Ponderada", "Equação 1º Grau", "Probabilidade"]
        tema_escolhido = random.choice(temas_possiveis)

        prompt = f"""
        Gere um JSON puro com 2 questões inéditas de matemática ENEM sobre: {tema_escolhido}.
        IMPORTANTE:
        1. Responda APENAS o JSON.
        2. NÃO use Markdown (sem ```json).
        3. NÃO use LaTeX (sem barras invertidas).
        
        Formato obrigatório:
        [
            {{
                "id": 1,
                "tema": "{tema_escolhido}",
                "pergunta": "Enunciado aqui...",
                "opcoes": ["A", "B", "C", "D"],
                "correta": "A",
                "explicacao": "Resolucao..."
            }}
        ]
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza para evitar erros de JSON
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        # Tenta converter
        dados = json.loads(texto) 
        
        # Numeração
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        # Salva o arquivo novo
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        # AQUI ESTÁ A MÁGICA: O erro vira uma pergunta para você ler na tela!
        erro_na_tela = [{
            "id": 1, 
            "tema": "⚠️ ERRO ENCONTRADO", 
            "pergunta": f"O erro foi: {str(e)}", 
            "opcoes": ["Tentar de novo"], 
            "correta": "Tentar de novo", 
            "explicacao": "Tire print dessa tela e mande para o suporte."
        }]
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(erro_na_tela, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    gerar_questoes()
