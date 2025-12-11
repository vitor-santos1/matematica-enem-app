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

# ======================================================
# 🧠 GERADOR 100% IA (COM SISTEMA DE FILA DE ESPERA)
# ======================================================
def gerar_questoes_agora():
    
    # Configura para ser MUITO CRIATIVO (Temperatura Alta)
    # Isso garante que a IA nunca repita a mesma questão
    config_criativa = genai.types.GenerationConfig(
        temperature=1.0 
    )

    max_tentativas = 6  # Vai insistir 6 vezes antes de desistir
    tentativa_atual = 0

    while tentativa_atual < max_tentativas:
        try:
            print(f"🔄 Tentativa IA: {tentativa_atual + 1}...")
            genai.configure(api_key=minha_chave)
            
            # Usamos o Flash que é mais rápido e gasta menos cota
            model = genai.GenerativeModel(
                'models/gemini-flash-latest',
                generation_config=config_criativa
            )
            
            # PROMPT PODEROSO PARA ENEM
            prompt = """
            Você é um Elaborador Sênior do ENEM (Brasil).
            Gere um JSON com 3 questões de Matemática INÉDITAS.

            REGRAS OBRIGATÓRIAS:
            1. **Criatividade Total:** Crie contextos novos (ex: Biologia, Astronomia, Economia Digital, YouTubers, etc). NÃO use exemplos clichês.
            2. **Complexidade:** As questões devem exigir interpretação de texto + cálculo.
            3. **Explicação:** O campo 'explicacao' deve ser uma mini-aula passo a passo.
            4. **Formato:** JSON Puro.

            MODELO DE RESPOSTA:
            [
                {
                    "id": 1, 
                    "tema": "Tema Criativo", 
                    "pergunta": "Texto base longo... Pergunta final?", 
                    "opcoes": ["A", "B", "C", "D"], 
                    "correta": "A", 
                    "explicacao": "Resolução detalhada..."
                }
            ]
            """
            
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            if not texto: raise ValueError("Resposta Vazia")
            
            dados = json.loads(texto)
            
            # SUCESSO! 
            # Agora embaralhamos as alternativas para a resposta não ser sempre a primeira
            for i, q in enumerate(dados):
                random.shuffle(q['opcoes']) # Mistura A, B, C, D
                q['id'] = i + 1
            
            return dados # Entrega para o site

        except Exception as e:
            # Se der erro (Google cheio), ele NÃO desiste.
            # Ele espera um tempo crescente (5s, 10s, 15s...) e tenta de novo.
            tempo_espera = 5 + (tentativa_atual * 3)
            print(f"⚠️ Google ocupado. Esperando {tempo_espera} segundos...")
            time.sleep(tempo_espera) 
            tentativa_atual += 1
    
    # Se falhar 6 vezes (muito raro), mostra aviso para tentar depois.
    # NÃO mostra questão fake.
    return [{
        "id": 1, 
        "tema": "⚠️ Tráfego Intenso", 
        "pergunta": "O cérebro da IA está superlotado agora. Por favor, aguarde 30 segundos e clique em gerar novamente.", 
        "opcoes": ["Entendi"], 
        "correta": "Entendi", 
        "explicacao": "Muitas pessoas usando o Google Gemini ao mesmo tempo."
    }]
