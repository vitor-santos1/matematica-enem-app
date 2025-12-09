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

# --- 2. PERGUNTAS DE SEGURANÇA (BACKUP) ---
# Estas perguntas são salvas ANTES de tentar a IA.
BACKUP_FIXO = [
    {
        "id": 1, "tema": "Matemática (Modo Offline)", 
        "pergunta": "Se um carro anda a 80km/h, quanto ele anda em 2 horas?", 
        "opcoes": ["100km", "160km", "140km", "120km"], 
        "correta": "160km", "explicacao": "Distância = Velocidade x Tempo. 80 x 2 = 160."
    },
    {
        "id": 2, "tema": "Porcentagem (Modo Offline)", 
        "pergunta": "Quanto é 10% de 500?", 
        "opcoes": ["50", "5", "100", "25"], 
        "correta": "50", "explicacao": "10% é dividir por 10. 500/10 = 50."
    }
]

def gerar_questoes():
    print("--- INICIANDO ---")
    
    # 3. SALVAR BACKUP PRIMEIRO (Para garantir que algo apareça)
    with open("banco_questoes.json", "w", encoding="utf-8") as f:
        json.dump(BACKUP_FIXO, f, ensure_ascii=False, indent=2)
    print("✅ Perguntas de backup salvas (Garantia).")

    # 4. TENTAR IA (Se der certo, substitui o backup)
    try:
        genai.configure(api_key=minha_chave)
        
        # Tentando o modelo mais clássico que existe
        model = genai.GenerativeModel('models/gemini-pro')
        
        prompt = """
        Gere um JSON puro com 2 questões de matemática ENEM.
        REGRAS: Responda APENAS o JSON. Sem markdown. Sem LaTeX.
        Formato: [{"id":1, "tema":"x", "pergunta":"x", "opcoes":["A","B"], "correta":"A", "explicacao":"x"}]
        """
        
        print("⏳ Chamando IA...")
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        # SOBRESCREVE O ARQUIVO COM AS NOVAS
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print("✅ SUCESSO! IA substituiu o backup.")

    except Exception as e:
        print(f"⚠️ Falha na IA: {e}. Mantendo o backup.")
        # Se der erro, não faz nada (o backup já foi salvo lá em cima!)

if __name__ == "__main__":
    gerar_questoes()
