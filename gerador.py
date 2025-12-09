import google.generativeai as genai
import json
import os
import streamlit as st

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI" # Só usa se rodar no PC

# --- PERGUNTAS DE EMERGÊNCIA (BACKUP) ---
BACKUP_QUESTOES = [
    {
        "id": 1, "tema": "Porcentagem (Backup)", 
        "pergunta": "Uma calça de R$ 200,00 está com 50% de desconto. Qual o preço?", 
        "opcoes": ["R$ 100,00", "R$ 150,00", "R$ 50,00", "R$ 90,00"], 
        "correta": "R$ 100,00", "explicacao": "50% é a metade. Metade de 200 é 100."
    }
]

def gerar_questoes():
    print("--- INICIANDO GERADOR (CORRIGIDO) ---")
    
    try:
        genai.configure(api_key=minha_chave)
        # Mudei para o 1.5 Flash que é mais estável
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Gere um JSON puro com 4 questões de matemática ENEM.
        REGRAS CRUCIAIS:
        1. Responda APENAS o JSON. Sem '```json' e sem '```'.
        2. Não use LaTeX (barras invertidas). Use texto simples.
        
        Formato: [{"id":1, "tema":"x", "pergunta":"x", "opcoes":["A","B"], "correta":"A", "explicacao":"x"}]
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza bruta do texto para garantir que vire JSON
        texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
        
        # AQUI ESTAVA O ERRO: Agora é json.loadS (com S de String)
        dados = json.loads(texto_limpo)
        
        # Numeração
        for i, q in enumerate(dados):
            q['id'] = i + 1
            
        # Salvar
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
            
        print("✅ SUCESSO! IA gerou novas questões.")

    except Exception as e:
        print(f"❌ ERRO NA IA: {e}")
        # Se der erro, salva o backup para não ficar vazio
        with open("banco_questoes.json", "w", encoding="utf-8") as f:
            json.dump(BACKUP_QUESTOES, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    gerar_questoes()

