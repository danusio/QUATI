import streamlit as st
import math
import re
import io

def exibir_questionario(questionario, headers):
    respostas = {}
    
    for enunciado, questoes in questionario.items():
        st.subheader(enunciado)
        st.write(headers[enunciado])
        for questao, opcoes in questoes.items():
            resposta = st.radio(questao, opcoes)
            respostas[questao] = resposta
    
    return respostas

def extract_substring(text, start_string, end_string):
    start_index = text.find(start_string)
    if start_index == -1:
        return "Start string not found"
    
    start_index += len(start_string)
    
    end_index = text.find(end_string, start_index)
    if end_index == -1:
        return "End string not found"
    
    return text[start_index:end_index]

def formatar_respostas(respostas, colunas=2):
    # Função auxiliar para dividir as perguntas em grupos de colunas
    def criar_matriz_perguntas(perguntas, colunas):
        # Adiciona um espaço vazio ao final se o número de perguntas não for divisível por 'colunas'
        while len(perguntas) % colunas != 0:
            perguntas.append("")  # Adiciona uma célula vazia para completar o grupo
        # Dividir a lista de perguntas em grupos de tamanho 'colunas'
        matriz = [perguntas[i:i + colunas] for i in range(0, len(perguntas), colunas)]
        return matriz

    # Função para transpor a matriz
    def transpor_matriz(matriz):
        return list(zip(*matriz))

    # Função para exibir uma categoria
    def exibir_categoria(categoria):
        perguntas = [f"{num.split('-')[1].strip()} {resposta[0]}" for num, resposta in respostas.items() if categoria in num]
        matriz = criar_matriz_perguntas(perguntas, math.ceil(len(perguntas)/4))  # ajustando para 4 linhas
        matriz_transposta = transpor_matriz(matriz)

        for linha in matriz_transposta:
            colunas_st = st.columns(len(linha))
            for idx, pergunta in enumerate(linha):
                colunas_st[idx].write(pergunta)

    col1, col2 = st.columns(2)

    with col1:
        st.header("A FESTA")
        exibir_categoria("A FESTA")
        
        st.header("A VIAGEM")
        exibir_categoria("A VIAGEM")
        
        st.header("O LAZER")
        exibir_categoria("O LAZER")

    with col2:
        st.header("O TRABALHO")
        exibir_categoria("O TRABALHO")
        
        st.header("O ESTUDO")
        exibir_categoria("O ESTUDO")
        
        st.header("PESSOAL")
        exibir_categoria("PESSOAL")

def gerar_conteudo_txt(respostas):
    conteudo = io.StringIO()
    for categoria, resposta in respostas.items():
        conteudo.write(f"{categoria}: {resposta}\n")
    return conteudo.getvalue()

def main():
    st.title("QUATI")

    with open('texto_extraido - v1.txt', 'r') as file:
        text_content = file.read()

    starts = ['INSTRUÇÕES', 'A FESTA', 'O TRABALHO', 'A VIAGEM', 'VIDA PESSOAL', 'O LAZER', 'O ESTUDO']
    ends = ['A FESTA', 'O TRABALHO', 'A VIAGEM', 'VIDA PESSOAL', 'O LAZER', 'O ESTUDO', 'END']

    st.write(extract_substring(text_content, starts[0], ends[0]))
    
    questionario = {}
    headers = {}
    for i in range(1,len(starts)):
        content = extract_substring(text_content, starts[i], ends[i])
        list_content = content.split(' ---')

        headers[starts[i]]=list_content[0].strip()

        # Regular expression to find the questions (start with a number followed by ".")
        questions_list = re.split(r'(?m)(?=^\d{1,2}\.\s)', list_content[1].strip())
        
        questions = []
        question_number = 1
        for q in questions_list:  # Assuming 'questions_list' contains the list of questions
            if q.strip():  # Only increment if the string is not empty
                q_cleaned = q.split('.', 1)[1].strip()
                q_cleaned = re.sub(r'(?<!\w)a\s*-\s*', '', q_cleaned).strip()

                options_list = re.split(r'b\s*-\s*', q_cleaned)
                options_list.append('Nenhuma ou ambas.')
                options_list = [m+opt for m,opt in zip(['a - ', 'b - ', ''], options_list)]

                questions.append((starts[i] + ' - ' + str(question_number), options_list))
                question_number += 1

        questionario[starts[i]] = dict(questions)

    # Exibir questionário e capturar as respostas
    respostas = exibir_questionario(questionario, headers)

    # Botão para enviar as respostas
    if st.button("Enviar respostas"):
        st.write("Suas respostas:")
        # for questao, resposta in respostas.items():
        #     st.write(f"{questao}: {resposta}")
        formatar_respostas(respostas, 4)
        st.success("Respostas enviadas com sucesso!")

        # Gerar o conteúdo do arquivo .txt
        conteudo_txt = gerar_conteudo_txt(respostas)
        
        # Adicionar botão para download das respostas
        st.download_button(label="Baixar respostas em TXT",
                        data=conteudo_txt,
                        file_name="respostas.txt",
                        mime="text/plain")
    
# Executar o aplicativo
if __name__ == "__main__":
    main()