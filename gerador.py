import google.generativeai as genai
import json
import streamlit as st
import random

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# --- BACKUP DE SEGURANÇA ---
def pegar_backup():
    return [
        {
            "id": 1, "tema": "Matemática (Backup)", 
            "pergunta": f"Quanto é {random.randint(10,50)} + {random.randint(10,50)}?", 
            "opcoes": ["Calculando...", "Resultado Correto", "Errado", "Errado"], 
            "correta": "Resultado Correto", 
            "explicacao": "Soma simples."
        },
        {
            "id": 2, "tema": "Lógica", 
            "pergunta": "Qual o próximo número: 2, 4, 8, 16...?", 
            "opcoes": ["20", "24", "32", "30"], 
            "correta": "32", 
            "explicacao": "O número sempre dobra."
        }
    ]

# Função que devolve a lista direto pra memória
def gerar_questoes_agora():
    try:
        genai.configure(api_key=minha_chave)
        # Usando o modelo latest que sua conta aceita
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        temas = ["Juros Simples", "Geometria (Áreas)", "Média e Moda", "Equação 1º Grau"]
        tema_vez = random.choice(temas)

        prompt = f"""
        Gere um JSON puro com 3 questões de matemática ENEM sobre: {tema_vez}.
        REGRAS: 
        1. Responda APENAS o JSON. Sem markdown. 
        2. Texto simples (sem LaTeX).
        Formato: [{"id":1, "tema":"{tema_vez}", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..."}]
        """
        
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        dados = json.loads(texto)
        
        # Ajusta IDs
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        return dados # Devolve as perguntas novas!

    except Exception as e:
        print(f"Erro na IA: {e}")
        return pegar_backup() # Se der erro, devolve o backup
