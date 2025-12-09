import google.generativeai as genai
import json
import os
import streamlit as st

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    # Tenta pegar da Nuvem
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    # Se estiver no PC, use a manual
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# --- PERGUNTAS DE EMERGÊNCIA (Caso a IA falhe) ---
BACKUP_QUESTOES = [
    {
        "id": 1, "tema": "Porcentagem (Backup)", 
        "pergunta": "Uma camisa custa R$ 100,00 e tem 20% de desconto. Qual o valor final?", 
        "opcoes": ["R$ 80,00", "R$ 90,00", "R$ 85,00", "R$ 120,00"], 
        "correta": "R$ 80,00", "explicacao": "20% de 100 é 20. 100 - 20 = 80."
    },
    {
        "id": 2, "tema": "Geometria (Backup)", 
        "pergunta": "Qual a área de um quadrado de lado 5cm?", 
        "opcoes": ["20cm²", "25cm²", "30cm²", "10cm²"], 
        "correta": "25cm²", "explicacao": "Área = lado x lado = 5 x 5 = 25."
    },
    {
        "id": 3, "tema": "Lógica (Backup)", 
        "pergunta": "Se hoje é segunda-feira, daqui a 7 dias será?", 
        "opcoes": ["Terça", "Segunda", "Domingo", "Sábado"], 
        "correta": "Segunda", "explicacao": "A semana tem 7 dias, então o dia se repete."
    },
    {
        "id": 4, "tema": "Matemática Básica (Backup)", 
        "pergunta": "Quanto é a metade de 2 + 2?", 
        "opcoes": ["3", "2", "1", "4"], 
        "correta": "3", "explicacao": "A metade de 2 é 1. Somando com 2, temos 1 + 2 = 3. (Cuidado com a ordem!)"
    }
]

def gerar_questoes():
    print("--- INICIANDO GERADOR BLINDADO ---")
    sucesso = False
    
    # TENTATIVA 1: INTELIGÊNCIA ARTIFICIAL
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        prompt = """
        Gere um JSON puro com 4 questões de matemática ENEM.
        REGRAS: Texto simples, sem LaTeX, sem barras invertidas.
        Estrutura: [{"id":1, "tema":"x", "pergunta":"x", "opcoes":["A","B"], "correta":"A", "explicacao":"x"}]
        """
        
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip().replace("\\", "/")
        dados = json.load(text)
        
        # Ajusta IDs
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        sucesso = True
        print("✅ IA gerou com sucesso!")

    except Exception as e:
        print(f"⚠️ IA falhou ({e}). Usando backup...")
        sucesso = False

    # TENTATIVA 2: BACKUP (Se a IA falhou)
    if not sucesso:
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(BACKUP_QUESTOES, f, ensure_ascii=False, indent=2)
        print("✅ Backup salvo com sucesso!")

if __name__ == "__main__":
    gerar_questoes()
