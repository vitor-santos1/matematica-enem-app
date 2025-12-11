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
# 🎲 GERADOR LOCAL (ESTILO ENEM + ALTERNATIVAS ALEATÓRIAS)
# ======================================================
def gerar_ia_local_variada():
    moldes = []

    # --- MOLDE 1: ANÁLISE COMBINATÓRIA (Senhas Bancárias) ---
    # Situação: Segurança da informação
    d1 = random.randint(3, 5) # Dígitos
    total = 10 ** d1
    
    q1 = {
        "id": 0, "tema": "Análise Combinatória",
        "pergunta": f"Por motivos de segurança, um aplicativo bancário exigiu que seus usuários trocassem suas senhas de acesso. A nova regra define que a senha deve ser composta exclusivamente por {d1} algarismos numéricos (0 a 9), sendo permitida a repetição de números em qualquer posição. Um especialista em segurança calculou o total de combinações possíveis para avaliar a vulnerabilidade do sistema. Esse total corresponde a:",
        "opcoes": [f"{total}", f"{total*10}", f"{10*d1}", f"{9**d1}"],
        "correta": f"{total}",
        "dica_mestra": "Pelo Princípio Fundamental da Contagem, se temos 10 opções para a primeira vaga, 10 para a segunda, e assim por diante, devemos multiplicar as possibilidades.",
        "explicacao": f"Temos {d1} posições. Cada uma aceita 10 números (0 a 9). Logo: 10 x 10... ({d1} vezes) = 10 elevado a {d1} = {total}."
    }
    random.shuffle(q1['opcoes']) # <--- O SEGREDO: Mistura as opções A,B,C,D
    moldes.append(q1)

    # --- MOLDE 2: ESCALA E CARTOGRAFIA ---
    # Situação: Arquiteto lendo planta
    escala = random.choice([50, 100, 200])
    cm_papel = random.randint(4, 12)
    m_real = (cm_papel * escala) / 100
    
    q2 = {
        "id": 0, "tema": "Razão e Proporção (Escalas)",
        "pergunta": f"Um estudante de arquitetura analisa a planta baixa de uma casa desenhada na escala 1:{escala}. Ele mede com uma régua o comprimento da sala de estar no desenho e encontra exatos {cm_papel} cm. Para comprar o piso adequado, ele precisa converter essa medida para a realidade. Qual é o comprimento real dessa sala em metros?",
        "opcoes": [f"{m_real:.2f} m", f"{m_real*10} m", f"{m_real/10} m", f"{cm_papel * escala} m"],
        "correta": f"{m_real:.2f} m",
        "dica_mestra": f"Escala 1:{escala} significa que cada 1 cm no papel vale {escala} cm na vida real. Converta o resultado final de cm para metros.",
        "explicacao": f"1. Tamanho real em cm: {cm_papel} x {escala} = {cm_papel*escala} cm. \n2. Convertendo para metros (dividir por 100): {m_real:.2f} m."
    }
    random.shuffle(q2['opcoes'])
    moldes.append(q2)

    # --- MOLDE 3: MÉDIA PONDERADA (Notas Escolares) ---
    # Situação: Cálculo de nota final
    n1 = random.randint(40, 70)
    n2 = random.randint(50, 80)
    p1, p2 = 2, 3
    media = (n1*p1 + n2*p2) / (p1+p2)
    
    q3 = {
        "id": 0, "tema": "Estatística (Média Ponderada)",
        "pergunta": f"Em um concurso público, a nota final é calculada através da média ponderada entre duas etapas. A prova objetiva tem peso {p1} e a redação tem peso {p2}. Um candidato obteve {n1} pontos na objetiva e {n2} pontos na redação. Qual foi a nota final desse candidato?",
        "opcoes": [f"{media:.1f}", f"{(n1+n2)/2:.1f}", f"{media+2:.1f}", f"{media-5:.1f}"],
        "correta": f"{media:.1f}",
        "dica_mestra": "Na média ponderada, você multiplica cada nota pelo seu peso, soma os resultados e divide pela soma dos pesos.",
        "explicacao": f"Cálculo: ({n1}x{p1} + {n2}x{p2}) / ({p1}+{p2}) = ({n1*p1} + {n2*p2}) / 5 = {media:.1f}."
    }
    random.shuffle(q3['opcoes'])
    moldes.append(q3)

    # --- MOLDE 4: GEOMETRIA ESPACIAL (Piscina) ---
    c = random.randint(5, 10)
    l = random.randint(3, 6)
    p = 2
    vol_m3 = c * l * p
    vol_litros = vol_m3 * 1000
    
    q4 = {
        "id": 0, "tema": "Geometria Espacial",
        "pergunta": f"Um clube recreativo deseja esvaziar sua piscina olímpica para manutenção. A piscina tem formato de paralelepípedo retângulo com {c}m de comprimento, {l}m de largura e {p}m de profundidade. Sabendo que 1m³ equivale a 1.000 litros, qual a capacidade total de água que deverá ser retirada?",
        "opcoes": [f"{vol_litros} litros", f"{vol_m3} litros", f"{vol_litros/2} litros", f"{vol_litros*10} litros"],
        "correta": f"{vol_litros} litros",
        "dica_mestra": "Primeiro calcule o volume em metros cúbicos (C x L x P). Depois multiplique por 1.000 para achar os litros.",
        "explicacao": f"Volume: {c} x {l} x {p} = {vol_m3} m³. \nEm litros: {vol_m3} x 1.000 = {vol_litros} litros."
    }
    random.shuffle(q4['opcoes'])
    moldes.append(q4)

    # --- MOLDE 5: PORCENTAGEM (Desconto Loja) ---
    preco = random.choice([100, 200, 500, 1000])
    desc = random.choice([10, 20, 25, 50])
    final = preco - (preco * desc / 100)
    
    q5 = {
        "id": 0, "tema": "Matemática Financeira",
        "pergunta": f"Durante a Black Friday, uma loja de eletrônicos anunciou que todos os produtos teriam {desc}% de desconto sobre o preço da etiqueta. Um cliente interessado em um fone de ouvido que custava originalmente R$ {preco},00 decidiu comprá-lo. Quanto ele pagou no caixa?",
        "opcoes": [f"R$ {final:.2f}", f"R$ {preco-10:.2f}", f"R$ {final+15:.2f}", f"R$ {preco * desc/100:.2f}"],
        "correta": f"R$ {final:.2f}",
        "dica_mestra": f"Calcule {desc}% de {preco} e subtraia esse valor do total.",
        "explicacao": f"Desconto: {preco} x {desc}/100 = {preco*desc/100}. \nPreço Final: {preco} - {preco*desc/100} = R$ {final:.2f}."
    }
    random.shuffle(q5['opcoes'])
    moldes.append(q5)

    # Sorteia 3 questões aleatórias do banco
    selecao = random.sample(moldes, 3)
    for i, q in enumerate(selecao): q['id'] = i + 1
    return selecao

# ==========================================
# 🤖 GERADOR HÍBRIDO (IA + LOCAL)
# ==========================================
def gerar_questoes_agora():
    # Tenta conectar na IA
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        prompt = """
        Atue como Elaborador do ENEM. Gere JSON com 3 questões.
        REGRAS RÍGIDAS:
        1. Contexto: Use situações reais (notícias, cotidiano).
        2. Aleatoriedade: A resposta correta NÃO pode ser sempre a primeira opção. Misture as posições.
        3. Formato: [{"id":1, "tema":"...", "pergunta":"...", "opcoes":["A","B"], "correta":"A", "dica_mestra":"...", "explicacao":"..."}]
        """
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        if not texto: raise ValueError("Vazio")
        
        dados = json.loads(texto)
        
        # GARANTIA FINAL: Mesmo que a IA mande ordenado, o Python EMBARALHA TUDO AQUI
        for q in dados:
            random.shuffle(q['opcoes'])
            q['id'] = dados.index(q) + 1
            
        return dados 

    except Exception:
        # Se a IA falhar, usa o banco local (que agora também embaralha)
        return gerar_ia_local_variada()
