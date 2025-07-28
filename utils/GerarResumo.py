from cloud_functions.Gemini import call_gemini

def gerar_resumo(vagas):
    """
    Dado um conjunto de vagas em formato de array de dicionários, gera um resumo das principais habilidades e requisitos das vagas.

    Args:
        vagas (list): Lista de dicionários, onde cada dicionário representa uma vaga com suas habilidades e requisitos.
    
    Returns:
        str: Um resumo das principais habilidades e requisitos encontrados nas vagas.
    """

    prompt = "Você é um especialista em recrutamento e seleção. Sua tarefa é analisar as seguintes vagas e gerar um resumo das principais habilidades e requisitos necessários para os candidatos:\n\n"
    
    for vaga in vagas:
        
        titulos = vaga.get("title", [])
        descricoes = vaga.get("description", [])
        
        if titulos:
            prompt += f"Títulos: {', '.join(titulos)}\n"
        if descricoes:
            prompt += f"Descrições: {', '.join(descricoes)}\n"

    response = call_gemini(prompt)

    return response
