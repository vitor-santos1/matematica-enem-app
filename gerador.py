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
# 🎲 BANCO DE MOLDES (Sorteia histórias diferentes)
# ======================================================
def gerar_ia_local_variada():
    moldes = []

    # --- MOLDE 1: ANÁLISE COMBINATÓRIA (Senhas) ---
    chars = random.randint(3, 5)
    total_senhas = 10 ** chars
    moldes.append({
        "id": 0, "tema": "Análise Combinatória",
        "pergunta": f"Um banco decidiu atualizar seu sistema de segurança e solicitou que todos os clientes criassem novas senhas numéricas formadas por exatamente {chars} algarismos (0 a 9), sendo permitida a repetição de números. Qual o total de senhas possíveis que podem ser criadas nesse novo padrão?",
        "opcoes": [f"{total_senhas}", f"{total_senhas*10}", f"{10*chars}", f"{9**chars}"],
        "correta": f"{total_senhas}",
        "dica_mestra": "Pelo Princípio Fundamental da Contagem, multiplique as possibilidades de cada posição. Temos 10 opções (0-9) para cada vaga.",
        "explicacao": f"São {chars} posições. Cada uma tem 10 opções. Logo: 10 x 10... ({chars} vezes) = 10^{chars} = {total_senhas}."
    })

    # --- MOLDE 2: ESCALA (Mapas) ---
    escala_cm = random.choice([100, 200, 500, 1000]) # 1:100 etc
    dist_mapa = random.randint(5, 20) # cm
    dist_real_cm = dist_mapa * escala_cm
    dist_real_m = dist_real_cm / 100
    moldes.append({
        "id": 0, "tema": "Razão e Proporção (Escala)",
        "pergunta": f"Em um mapa arquitetônico desenhado na escala 1:{escala_cm}, a medida do comprimento de uma sala é de {dist_mapa} cm. Qual é a medida real, em metros, desse comprimento?",
        "opcoes": [f"{dist_real_m} m", f"{dist_real_cm} m", f"{dist_real_m/10} m", f"{dist_real_m*10} m"],
        "correta": f"{dist_real_m} m",
        "dica_mestra": f"A escala 1:{escala_cm} significa que 1 cm no papel vale {escala_cm} cm na vida real. Converta para metros no final.",
        "explicacao": f"1. Distância em cm: {dist_mapa} x {escala_cm} = {dist_real_cm} cm. \n2. Converter para metros (dividir por 100): {dist_real_m} metros."
    })

    # --- MOLDE 3: ESTATÍSTICA (Média de Gols/Notas) ---
    valores = [random.randint(0, 5) for _ in range(5)]
    soma = sum(valores)
    media = soma / 5
    moldes.append({
        "id": 0, "tema": "Estatística (Média)",
        "pergunta": f"Um time de futebol marcou a seguinte quantidade de gols nos seus últimos 5 jogos: {valores}. Qual foi a média de gols por partida desse time?",
        "opcoes": [f"{media:.1f}", f"{media+1:.1f}", f"{soma}", f"{media/2:.1f}"],
        "correta": f"{media:.1f}",
        "dica_mestra": "Para calcular a Média Aritmética Simples, some todos os valores e divida pela quantidade de jogos (5).",
        "explicacao": f"Soma: {valores[0]}+{valores[1]}+{valores[2]}+{valores[3]}+{valores[4]} = {soma}. \nMédia: {soma} ÷ 5 = {media:.1f}."
    })

    # --- MOLDE 4: PROBABILIDADE (Urna) ---
    vermelhas = random.randint(3, 10)
    azuis = random.randint(3, 10)
    total = vermelhas + azuis
    prob_azul_pct = int((azuis / total) * 100)
    moldes.append({
        "id": 0, "tema": "Probabilidade",
        "pergunta": f"Em uma urna opaca existem {vermelhas} bolas vermelhas e {azuis} bolas azuis, todas idênticas ao tato. Ao retirar uma bola ao acaso, qual a probabilidade aproximada (em porcentagem) de ela ser AZUL?",
        "opcoes": [f"{prob_azul_pct}%", f"{100 - prob_azul_pct}%", "50%", f"{int(prob_azul_pct/2)}%"],
        "correta": f"{prob_azul_pct}%",
        "dica_mestra": "Probabilidade = (Casos Favoráveis / Casos Totais). Multiplique por 100 para achar a porcentagem.",
        "explicacao": f"Total de bolas: {total}. Bolas azuis: {azuis}. \nCálculo: {azuis}/{total} = {azuis/total:.2f} = {prob_azul_pct}%."
    })

    # --- MOLDE 5: FUNÇÃO DE 1º GRAU (Salário Vendedor) ---
    fixo = random.choice([1000, 1200, 1500])
    comissao = random.choice([20, 50, 100])
    vendas = random.randint(5, 15)
    salario = fixo + (comissao * vendas)
    moldes.append({
        "id": 0, "tema": "Funções (Salário)",
        "pergunta": f"Um vendedor recebe um salário mensal fixo de R$ {fixo},00 mais uma comissão de R$ {comissao},00 por produto vendido. Em um mês onde ele vendeu {vendas} produtos, qual foi seu salário total?",
        "opcoes": [f"R$ {salario},00", f"R$ {fixo + vendas},00", f"R$ {comissao * vendas},00", f"R$ {salario + 200},00"],
        "correta": f"R$ {salario},00",
        "dica_mestra": "A função é Salário = Fixo + (Comissão x Quantidade).",
        "explicacao": f"Conta: {fixo} + ({comissao} x {vendas}) \n= {fixo} + {comissao*vendas} \n= R$ {salario},00."
    })
    
    # --- MOLDE 6: GEOMETRIA (Área Piso) ---
    lado1 = random.randint(3, 8)
    lado2 = random.randint(4, 10)
    area = lado1 * lado2
    custo = random.randint(20, 60)
    total_piso = area * custo
    moldes.append({
        "id": 0, "tema": "Geometria e Orçamento",
        "pergunta": f"Deseja-se trocar o piso de uma sala retangular de {lado1}m por {lado2}m. O pedreiro cobra R$ {custo},00 por metro quadrado (m²) instalado. Qual será o custo total da mão de obra?",
        "opcoes": [f"R$ {total_piso},00", f"R$ {area * 10},00", f"R$ {total_piso/2},00", f"R$ {custo * 10},00"],
        "correta": f"R$ {total_piso},00",
        "dica_mestra": "Calcule a área da sala (Base x Altura) e multiplique pelo preço do m².",
        "explicacao": f"Área: {lado1} x {lado2} = {area} m². \nCusto: {area} x {custo} = R$ {total_piso},00."
    })

    # --- SORTEIO ALEATÓRIO ---
    # Aqui está o segredo: Pegamos 3 moldes aleatórios dessa lista de 6
    selecionadas = random.sample(moldes, 3)
    
    # Arruma os IDs (1, 2, 3)
    for i, q in enumerate(selecionadas):
        q['id'] = i + 1
        
    return selecionadas

# ==========================================
# 🤖 GERADOR HÍBRIDO
# ==========================================
def gerar_questoes_agora():
    # Tenta usar a IA do Google (1 tentativa rápida)
    try:
        genai.configure(api_key=minha_chave)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        
        prompt = """
        Atue como Elaborador do ENEM. Gere JSON com 3 questões DIFÍCEIS e VARIADAS.
        REGRAS: Texto longo, contexto interdisciplinar.
        FORMATO: [{"id":1, "tema":"...", "pergunta":"...", "opcoes":["A"], "correta":"A", "dica_mestra":"...", "explicacao":"..."}]
        """
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        if not texto: raise ValueError("Vazio")
        
        dados = json.loads(texto)
        for i, q in enumerate(dados): q['id'] = i + 1
        return dados 

    except Exception:
        # SE A IA FALHAR, USA O NOVO BANCO VARIADO
        return gerar_ia_local_variada()
