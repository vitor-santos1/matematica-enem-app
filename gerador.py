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
# 🧱 CONSTRUTOR SEMÂNTICO (LEGO DE TEXTO OFFLINE)
# ======================================================
# Aqui o Python monta frases palavra por palavra para nunca repetir.

def get_elemento(tipo):
    """Retorna uma palavra aleatória baseada no tipo pedido"""
    banco = {
        "lojas": ["Uma grande loja de departamentos", "Um site de e-commerce", "Uma boutique exclusiva", "Um supermercado atacadista", "Uma livraria online"],
        "acoes_desc": ["anunciou uma promoção de", "decidiu liquidar o estoque com", "ofereceu um cupom de", "aplicou um desconto relâmpago de"],
        "produtos": ["um notebook gamer", "uma geladeira inox", "um par de tênis de corrida", "um smartphone de última geração", "uma coleção de livros"],
        "nomes": ["Ana", "Carlos", "Beatriz", "João", "Fernanda", "Rafael", "Mariana", "Lucas"],
        "construcoes": ["uma piscina olímpica", "um reservatório cilíndrico", "uma caixa d'água cúbica", "um silo de grãos", "um aquário gigante"],
        "investimentos": ["na poupança", "em um fundo imobiliário", "em ações de tecnologia", "no Tesouro Direto", "em criptomoedas"],
        "periodos": ["um semestre", "um trimestre", "dois anos", "cinco meses"]
    }
    return random.choice(banco[tipo])

def gerar_ia_local_criativa():
    questoes = []
    
    # --- CENÁRIO 1: MATEMÁTICA FINANCEIRA (História Dinâmica) ---
    preco = random.choice([1200, 2500, 3000, 4500])
    desc = random.choice([10, 15, 20, 25, 30])
    valor_desc = preco * (desc/100)
    final = preco - valor_desc
    
    # Monta a frase peça por peça
    loja = get_elemento("lojas")
    acao = get_elemento("acoes_desc")
    prod = get_elemento("produtos")
    
    q1 = {
        "id": 0, "tema": "Matemática Financeira",
        "pergunta": f"{loja} {acao} {desc}% para quem comprasse {prod}. O preço original da etiqueta era de R$ {preco},00. Um cliente atento aproveitou a oportunidade. Quanto ele pagou no final?",
        "opcoes": [f"R$ {final:.2f}", f"R$ {preco-100:.2f}", f"R$ {final+50:.2f}", f"R$ {valor_desc:.2f}"],
        "correta": f"R$ {final:.2f}",
        "dica_mestra": f"Calcule {desc}% de {preco} e depois subtraia esse valor do total.",
        "explicacao": f"Desconto: {desc}% de {preco} = R$ {valor_desc:.2f}. \nPreço Final: {preco} - {valor_desc} = R$ {final:.2f}."
    }
    random.shuffle(q1['opcoes'])
    questoes.append(q1)

    # --- CENÁRIO 2: GEOMETRIA ESPACIAL (Construção Variável) ---
    obj = get_elemento("construcoes")
    medida1 = random.randint(4, 10) # Lado ou Raio
    altura = random.randint(2, 5)
    
    if "cilíndrico" in obj or "silo" in obj:
        # Cilindro
        pi = 3
        vol = pi * (medida1**2) * altura
        texto_medidas = f"com raio de {medida1}m e altura de {altura}m"
        texto_expl = f"Volume Cilindro = pi . r² . h = 3 . {medida1}² . {altura} = {vol} m³."
    else:
        # Prisma/Cubo
        vol = (medida1**2) * altura
        texto_medidas = f"com base quadrada de lado {medida1}m e profundidade de {altura}m"
        texto_expl = f"Volume Prisma = Área base . altura = ({medida1}x{medida1}) . {altura} = {vol} m³."
    
    litros = vol * 1000

    q2 = {
        "id": 0, "tema": "Geometria Espacial",
        "pergunta": f"Um engenheiro foi contratado para projetar {obj} {texto_medidas}. Para testar a estrutura, foi necessário enchê-la totalmente com água. Considerando que 1m³ = 1000 litros (e pi=3 se necessário), qual a capacidade total?",
        "opcoes": [f"{litros} L", f"{vol} L", f"{litros/2} L", f"{litros*10} L"],
        "correta": f"{litros} L",
        "dica_mestra": "Calcule primeiro o volume em m³. Depois multiplique por 1000 para achar em litros.",
        "explicacao": f"{texto_expl} \nEm litros: {vol} x 1000 = {litros} litros."
    }
    random.shuffle(q2['opcoes'])
    questoes.append(q2)

    # --- CENÁRIO 3: JUROS E INVESTIMENTOS (Personagens Variados) ---
    nome = get_elemento("nomes")
    onde = get_elemento("investimentos")
    capital = random.choice([1000, 5000, 10000])
    taxa = random.randint(1, 5)
    tempo = random.randint(2, 6)
    juros = capital * (taxa/100) * tempo
    montante = capital + juros
    
    q3 = {
        "id": 0, "tema": "Juros Simples",
        "pergunta": f"{nome} recebeu uma herança e decidiu aplicar R$ {capital},00 {onde}. A corretora prometeu um rendimento de {taxa}% ao mês em regime de juros simples. Após {tempo} meses, qual será o valor total (montante) disponível para saque?",
        "opcoes": [f"R$ {montante:.2f}", f"R$ {juros:.2f}", f"R$ {capital + 100:.2f}", f"R$ {montante*2:.2f}"],
        "correta": f"R$ {montante:.2f}",
        "dica_mestra": "Juros Simples: J = Capital x Taxa x Tempo. O Montante é o Capital + Juros.",
        "explicacao": f"Juros: {capital} x {taxa/100} x {tempo} = R$ {juros:.2f}. \nMontante Final: {capital} + {juros} = R$ {montante:.2f}."
    }
    random.shuffle(q3['opcoes'])
    questoes.append(q3)

    return questoes

# ==========================================
# 🧠 GERADOR HÍBRIDO COM ALTA TEMPERATURA
# ==========================================
def gerar_questoes_agora():
    try:
        genai.configure(api_key=minha_chave)
        
        # CONFIGURAÇÃO DE CRIATIVIDADE (Temperatura Alta)
        configuracao_criativa = genai.types.GenerationConfig(
            temperature=1.0 # <--- 1.0 Deixa a IA muito mais criativa e menos repetitiva
        )
        
        model = genai.GenerativeModel(
            'models/gemini-flash-latest',
            generation_config=configuracao_criativa
        )
        
        prompt = """
        Atue como Elaborador Sênior do ENEM. Gere JSON com 3 questões.
        REGRAS CRUCIAIS DE VARIEDADE:
        1. NUNCA repita temas da última rodada.
        2. Crie histórias inusitadas (ex: biologia de bactérias, órbita de satélites, economia de um país fictício).
        3. Formato: [{"id":1, "tema":"...", "pergunta":"...", "opcoes":["A"], "correta":"A", "dica_mestra":"...", "explicacao":"..."}]
        """
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        if not texto: raise ValueError("Vazio")
        
        dados = json.loads(texto)
        
        # Embaralha alternativas da IA também
        for q in dados:
            random.shuffle(q['opcoes'])
            q['id'] = dados.index(q) + 1
            
        return dados 

    except Exception:
        # Se a IA falhar, usa o LEGO de texto (que cria frases novas toda vez)
        return gerar_ia_local_criativa()
