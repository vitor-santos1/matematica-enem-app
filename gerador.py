import google.generativeai as genai
import json
import streamlit as st
import random
import time

# --- CONFIGURAÇÃO DA CHAVE ---
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    minha_chave = "COLE_SUA_CHAVE_AQUI"

def gerar_questoes_agora():
    tentativas = 0
    # Tenta até 3 vezes se der erro
    while tentativas < 3:
        print(f"--- GERANDO LOTE (Tentativa {tentativas+1}) ---")
        try:
            genai.configure(api_key=minha_chave)
            model = genai.GenerativeModel('models/gemini-flash-latest')

            # TRUQUE DO ATACADO: Pedimos 5 questões de uma vez!
            # Isso conta como apenas 1 chamada na API.
            prompt = """
            Gere um JSON puro com 5 questões de matemática ENEM.
            
            REGRAS OBRIGATÓRIAS:
            1. Responda APENAS o JSON.
            2. NÃO use Markdown. NÃO use LaTeX.
            3. Texto simples e direto.
            4. Varie os temas: 1 de Porcentagem, 1 de Geometria, 1 de Lógica, 1 de Equação, 1 de Regra de Três.
            
            Formato: 
            [
                {"id":1, "tema":"Tema A", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..."},
                {"id":2, "tema":"Tema B", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "explicacao":"..."}
            ]
            """
            
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            if not texto: raise ValueError("Vazio")
            
            dados = json.loads(texto)
            
            # Ajusta IDs para ficarem bonitinhos (1, 2, 3, 4, 5)
            for i, q in enumerate(dados): 
                q['id'] = i + 1
            
            return dados # Retorna o pacote com 5 perguntas

        except Exception as e:
            erro = str(e).lower()
            if "429" in erro or "quota" in erro:
                print("⚠️ Cota cheia. Esperando um pouco...")
                time.sleep(5)
                tentativas += 1
            else:
                print(f"⚠️ Erro formatação: {e}")
                tentativas += 1
    
    # Se falhar tudo, entrega um pacote de emergência manual
    return [
        {"id": 1, "tema": "Backup", "pergunta": "Quanto é 10 + 10?", "opcoes":["20","30"], "correta":"20", "explicacao":"Simples."},
        {"id": 2, "tema": "Backup", "pergunta": "Quanto é 50% de 100?", "opcoes":["50","25"], "correta":"50", "explicacao":"Metade."},
        {"id": 3, "tema": "Backup", "pergunta": "3 x 3?", "opcoes":["9","6"], "correta":"9", "explicacao":"Tabuada."}
    ]
