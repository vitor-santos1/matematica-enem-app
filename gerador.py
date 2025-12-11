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

def buscar_lote_questoes():
    """
    Busca um pacote de 5 questões de uma vez para criar um 'estoque'.
    Isso evita ficar chamando a IA toda hora e travando o site.
    """
    try:
        genai.configure(api_key=minha_chave)
        
        # --- A PERSONALIDADE DA SUA IA ---
        # Aqui definimos que ela é uma Especialista no ENEM
        config_ia = genai.types.GenerationConfig(
            temperature=0.8 # Alta criatividade para não repetir
        )
        
        system_instruction = """
        Você é o 'MathTutor', uma IA especialista em preparar alunos para o ENEM.
        Seu objetivo é criar questões desafiadoras, interdisciplinares e com pegadinhas inteligentes.
        Nunca crie perguntas óbvias. Sempre use um texto base.
        """

        model = genai.GenerativeModel(
            'models/gemini-flash-latest',
            generation_config=config_ia,
            system_instruction=system_instruction
        )

        # Pedimos 5 questões de uma vez (Lote)
        prompt = """
        Gere um JSON puro com 5 questões de Matemática Estilo ENEM.
        
        REGRAS DE OURO:
        1. **Contexto:** Use temas variados (Astronomia, Economia, Biologia, Cotidiano).
        2. **Nível:** Médio/Difícil.
        3. **Estrutura:** Texto base + Pergunta + 4 Alternativas.
        4. **Feedback:** O campo 'explicacao' deve ser uma aula completa.
        
        Formato JSON:
        [
            {
                "tema": "Título do Tema",
                "pergunta": "Texto longo... Pergunta final?",
                "opcoes": ["A", "B", "C", "D"],
                "correta": "A",
                "dica_mestra": "Dica para desbloquear o raciocínio...",
                "explicacao": "Passo 1... Passo 2... Conclusão..."
            }
        ]
        """
        
        print("⚡ Solicitando lote de questões para a IA...")
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        dados = json.loads(texto)
        
        # Tratamento final: Embaralha as alternativas de TODAS as questões
        for q in dados:
            random.shuffle(q['opcoes'])
            
        return dados # Retorna a lista com 5 questões

    except Exception as e:
        print(f"Erro na IA: {e}")
        # Se der erro, retorna VAZIO (o app.py vai saber lidar com isso)
        return None
