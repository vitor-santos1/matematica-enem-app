import random
import math

# ==========================================
# 🧠 CÉREBRO DA IA SIMBÓLICA (Vitor-AI)
# ==========================================
# Esta IA não usa internet. Ela constrói conhecimento matematicamente.

def get_elemento(categoria):
    """Banco de dados criativo da IA para montar histórias."""
    db = {
        "pessoas": ["Ana", "Carlos", "Beatriz", "João", "Fernanda", "Rafael", "Mariana", "Lucas", "O gerente", "A engenheira"],
        "lugares": ["no shopping", "na construção civil", "no laboratório", "na bolsa de valores", "no supermercado", "na fazenda"],
        "objetos_caros": ["um notebook gamer", "uma geladeira smart", "um carro popular", "um drone profissional", "um smartphone"],
        "eventos": ["na Black Friday", "no Natal", "na liquidação de estoque", "durante a crise", "na alta do dólar"],
        "construcoes": ["uma piscina olímpica", "um reservatório de água", "um silo de grãos", "uma caixa d'água", "um tanque de combustível"]
    }
    return random.choice(db[categoria])

def gerar_ia_simbolica():
    questoes = []
    
    # ------------------------------------------------------------------
    # MOTOR 1: MATEMÁTICA FINANCEIRA (Histórias de Compras)
    # ------------------------------------------------------------------
    pessoa = get_elemento("pessoas")
    objeto = get_elemento("objetos_caros")
    evento = get_elemento("eventos")
    
    preco_base = random.choice([1200, 2500, 3000, 4500, 5000])
    desconto = random.choice([10, 15, 20, 25, 30, 50])
    
    valor_desconto = preco_base * (desconto / 100)
    valor_final = preco_base - valor_desconto
    
    q1 = {
        "id": 1,
        "tema": "Matemática Financeira",
        "pergunta": f"{evento}, {pessoa} encontrou {objeto} que custava originalmente R$ {preco_base},00. A loja anunciou um desconto imperdível de {desconto}% para pagamento à vista. Interessado na oferta, {pessoa} decidiu fechar negócio. Qual foi o valor final pago?",
        "opcoes": [
            f"R$ {valor_final:.2f}", 
            f"R$ {valor_final + 100:.2f}", 
            f"R$ {preco_base - 100:.2f}", 
            f"R$ {valor_desconto:.2f}"
        ],
        "correta": f"R$ {valor_final:.2f}",
        "dica_mestra": f"A palavra 'desconto' significa subtrair. Calcule {desconto}% de {preco_base} e tire esse valor do total.",
        "explicacao": f"1. Cálculo do desconto: {preco_base} x {desconto}/100 = R$ {valor_desconto:.2f}.\n2. Valor Final: {preco_base} - {valor_desconto} = R$ {valor_final:.2f}."
    }
    random.shuffle(q1['opcoes'])
    questoes.append(q1)

    # ------------------------------------------------------------------
    # MOTOR 2: GEOMETRIA ESPACIAL (Engenharia e Volume)
    # ------------------------------------------------------------------
    construcao = get_elemento("construcoes")
    raio = random.randint(3, 10)
    altura = random.randint(2, 6)
    pi = 3
    
    # Volume Cilindro = pi * r² * h
    vol_m3 = pi * (raio ** 2) * altura
    vol_litros = vol_m3 * 1000
    
    q2 = {
        "id": 2,
        "tema": "Geometria Espacial",
        "pergunta": f"Um projeto de engenharia prevê a instalação de {construcao} em formato cilíndrico para abastecer uma comunidade. As medidas do projeto indicam raio da base de {raio} metros e altura de {altura} metros. Considerando π = 3, qual a capacidade total de armazenamento em litros?",
        "opcoes": [
            f"{vol_litros} litros", 
            f"{vol_m3} litros", 
            f"{vol_litros/2} litros", 
            f"{vol_litros * 10} litros"
        ],
        "correta": f"{vol_litros} litros",
        "dica_mestra": "Primeiro calcule o volume em m³ (Área da Base x Altura). Lembre-se que 1 m³ = 1000 Litros.",
        "explicacao": f"1. Área da base (π.r²): 3 x {raio}² = {3 * raio**2} m².\n2. Volume (Base x Altura): {3 * raio**2} x {altura} = {vol_m3} m³.\n3. Conversão: {vol_m3} x 1000 = {vol_litros} litros."
    }
    random.shuffle(q2['opcoes'])
    questoes.append(q2)

    # ------------------------------------------------------------------
    # MOTOR 3: REGRA DE TRÊS (Viagens e Consumo)
    # ------------------------------------------------------------------
    km_litro = random.randint(8, 14)
    horas_viagem = random.randint(2, 5)
    velocidade = random.choice([80, 90, 100, 110])
    distancia = velocidade * horas_viagem
    # Garante que a divisão seja exata ou próxima
    litros_gastos = distancia / km_litro
    
    q3 = {
        "id": 3,
        "tema": "Grandezas Proporcionais",
        "pergunta": f"Um carro faz, em média, {km_litro} km/L de gasolina na estrada. O motorista planeja uma viagem de {horas_viagem} horas mantendo uma velocidade média constante de {velocidade} km/h. Quantos litros de combustível, aproximadamente, serão consumidos nesse trajeto?",
        "opcoes": [
            f"{litros_gastos:.1f} L", 
            f"{litros_gastos + 5:.1f} L", 
            f"{distancia} L", 
            f"{distancia / 10:.1f} L"
        ],
        "correta": f"{litros_gastos:.1f} L",
        "dica_mestra": "Primeiro descubra a distância total (Velocidade x Tempo). Depois divida pelo consumo do carro.",
        "explicacao": f"1. Distância total: {velocidade} km/h x {horas_viagem} h = {distancia} km.\n2. Consumo: {distancia} km ÷ {km_litro} km/L = {litros_gastos:.1f} litros."
    }
    random.shuffle(q3['opcoes'])
    questoes.append(q3)
    
    # ------------------------------------------------------------------
    # MOTOR 4: ANÁLISE COMBINATÓRIA (Senhas)
    # ------------------------------------------------------------------
    digitos = random.randint(3, 5)
    total_poss = 10 ** digitos
    
    q4 = {
        "id": 4,
        "tema": "Análise Combinatória",
        "pergunta": f"Um banco digital solicitou que seus clientes criassem uma nova senha numérica de {digitos} dígitos para transações via app. Sabendo que podem ser usados os algarismos de 0 a 9 e que a repetição é permitida, quantas senhas distintas podem ser formadas?",
        "opcoes": [
            f"{total_poss}", 
            f"{10 * digitos}", 
            f"{9 ** digitos}", 
            f"{total_poss * 10}"
        ],
        "correta": f"{total_poss}",
        "dica_mestra": "Use o Princípio Fundamental da Contagem. Quantas opções temos para a 1ª casa? E para a 2ª?",
        "explicacao": f"Para cada um dos {digitos} espaços, temos 10 opções de números (0-9).\nCálculo: 10 x 10... ({digitos} vezes) = 10^{digitos} = {total_poss}."
    }
    random.shuffle(q4['opcoes'])
    questoes.append(q4)

    # ------------------------------------------------------------------
    # MOTOR 5: ESTATÍSTICA (Média de Notas)
    # ------------------------------------------------------------------
    n1 = random.randint(50, 80)
    n2 = random.randint(60, 90)
    n3 = random.randint(40, 70)
    media = (n1 + n2 + n3) / 3
    
    q5 = {
        "id": 5,
        "tema": "Estatística Básica",
        "pergunta": f"Um estudante obteve as seguintes notas nas três etapas do ENEM Simulado: {n1}, {n2} e {n3}. Qual foi a média aritmética atingida por esse estudante?",
        "opcoes": [
            f"{media:.1f}", 
            f"{media + 5:.1f}", 
            f"{media - 2:.1f}", 
            f"{(n1+n2+n3)}"
        ],
        "correta": f"{media:.1f}",
        "dica_mestra": "Para achar a média, some todos os valores e divida pela quantidade de itens somados.",
        "explicacao": f"Soma: {n1} + {n2} + {n3} = {n1+n2+n3}.\nMédia: {n1+n2+n3} ÷ 3 = {media:.1f}."
    }
    random.shuffle(q5['opcoes'])
    questoes.append(q5)

    # Sorteia 3 questões dessas 5 geradas
    selecionadas = random.sample(questoes, 3)
    
    # Renumera para 1, 2, 3
    for i, q in enumerate(selecionadas):
        q['id'] = i + 1
        
    return selecionadas

# Função principal (Interface única)
def buscar_lote_questoes():
    # Não precisa mais de Google Key, nem Try/Except
    # Essa IA roda direto no processador
    return gerar_ia_simbolica()
