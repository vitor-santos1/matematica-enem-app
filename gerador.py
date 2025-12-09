import google.generativeai as genai
import json
import streamlit as st
import random

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

# --- BANCO DE EMERGÊNCIA (Caso a IA esteja sem cota) ---
def pegar_backup():
    questoes_reserva = [
        {
            "id": 1, "tema": "Porcentagem", 
            "pergunta": "Uma camiseta custa R$ 50,00. Com 10% de desconto, quanto fica?", 
            "opcoes": ["R$ 45,00", "R$ 40,00", "R$ 48,00", "R$ 35,00"], 
            "correta": "R$ 45,00", "explicacao": "10% de 50 é 5. 50 - 5 = 45."
        },
        {
            "id": 2, "tema": "Geometria", 
            "pergunta": "Qual a área de um retângulo de base 4cm e altura 3cm?", 
            "opcoes": ["12cm²", "7cm²", "14cm²", "10cm²"], 
            "correta": "12cm²", "explicacao": "Área = Base x Altura (4 x 3 = 12)."
        },
        {
            "id": 3, "tema": "Matemática Básica", 
            "pergunta": "O dobro de um número mais 5 é igual a 15. Que número é esse?", 
            "opcoes": ["5", "10", "2", "8"], 
            "correta": "5", "explicacao": "2x + 5 = 15 -> 2x = 10 -> x = 5."
        },
        {
            "id": 4, "tema": "Lógica", 
            "pergunta": "Se 3 gatos caçam 3 ratos em 3 minutos, quanto tempo 100 gatos levam para caçar 100 ratos?", 
            "opcoes": ["3 minutos", "100 minutos", "1 minuto", "300 minutos"], 
            "correta": "3 minutos", "explicacao": "Cada gato leva 3 minutos para caçar seu rato. O tempo é simultâneo."
        },
        {
            "id": 5, "tema": "Conversão", 
            "pergunta": "Quantos minutos têm em 1 hora e meia?", 
            "opcoes": ["90", "100", "80", "60"], 
            "correta": "90", "explicacao": "60 min (1h) + 30 min (meia) = 90 min."
        }
    ]
    # Embaralha e pega 3 aleatórias
    return random.sample(questoes_reserva, 3)

def gerar_questoes_agora():
    print("--- TENTANDO GERAR ---")
    try:
        genai.configure(api_key=minha_chave)
        
        # MUDANÇA: Tentando o modelo 2.0 que talvez você ainda tenha cota
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        temas = ["Juros Simples", "Regra de Três", "Média", "Equações"]
        tema_vez = random.choice(temas)

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
        
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        return dados 

    except Exception as e:
        print(f"⚠️ Erro na IA ({e}). Usando Backup.")
        # SE DER ERRO (QUOTA OU OUTRO), ELE USA O BACKUP SILENCIOSAMENTE
        # Assim o usuário sempre vê perguntas, nunca erros.
        return pegar_backup()
