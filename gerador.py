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
    # Tenta 3 vezes para garantir
    while tentativas < 3:
        try:
            genai.configure(api_key=minha_chave)
            # Usando o modelo flash (rápido e inteligente)
            model = genai.GenerativeModel('models/gemini-flash-latest')

            # --- O SEGREDO DO NÍVEL 2 ---
            # Pedimos para a IA agir como um Mentor do ENEM
            prompt = """
            Atue como um Professor de Matemática Especialista no ENEM.
            Gere um JSON com 3 questões de nível médio/difícil.

            REGRAS DE PEDAGOGIA:
            1. **Contexto:** Crie uma situação problema (loja, construção, viagem, economia).
            2. **Dica:** Crie uma "dica_mestra" que ajude o aluno a começar a pensar, sem dar a resposta.
            3. **Resolução:** Explique o passo a passo lógico no campo "explicacao".

            FORMATO JSON OBRIGATÓRIO:
            [
                {
                    "id": 1,
                    "tema": "Matemática Financeira",
                    "pergunta": "Joana quer comprar um carro de R$ 40.000... [texto longo]... Qual o valor final?",
                    "opcoes": ["R$ 42.000", "R$ 45.000", "R$ 48.000", "R$ 50.000"],
                    "correta": "R$ 45.000",
                    "dica_mestra": "Lembre-se que o juro composto é calculado sobre o montante do mês anterior, não sobre o inicial.",
                    "explicacao": "Mês 1: 40.000 + 10% = 44.000. Mês 2: 44.000 + ..."
                }
            ]
            """
            
            response = model.generate_content(prompt)
            texto = response.text.replace("```json", "").replace("```", "").strip()
            dados = json.loads(texto)
            
            # Numeração e retorno
            for i, q in enumerate(dados): q['id'] = i + 1
            return dados

        except Exception as e:
            # Se der erro de cota, espera um pouco
            time.sleep(4)
            tentativas += 1
            
    # Backup se a IA falhar muito
    return [{
        "id": 1, "tema": "Erro na IA", 
        "pergunta": "A IA está sobrecarregada. Tente gerar novamente em 1 minuto.", 
        "opcoes": ["Ok"], "correta": "Ok", "dica_mestra": "Sem dica", "explicacao": "..."
    }]
