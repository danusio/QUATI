import streamlit as st
import re

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

def main():
    st.title("QUATI")

    with open('texto_extraido - v0.txt', 'r') as file:
        text_content = file.read()

    starts = ['INSTRUÇÕES', 'A FESTA', 'O TRABALHO', 'A VIAGEM']
    ends = ['A FESTA', 'O TRABALHO', 'A VIAGEM', 'END']

    st.write(extract_substring(text_content, starts[0], ends[0]))
    
    question_number = 1
    questionario = {}
    headers = {}
    for i in range(1,len(starts)):
        content = extract_substring(text_content, starts[i], ends[i])
        list_content = content.split(' ---')

        headers[starts[i]]=list_content[0].strip()

        # Regular expression to find the questions (start with a number followed by ".")
        questions_list = re.split(r'(?m)(?=^\d{1,2}\.\s)', list_content[1].strip())
        
        questions = []
        for q in questions_list:  # Assuming 'questions_list' contains the list of questions
            if q.strip():  # Only increment if the string is not empty
                q_cleaned = q.split('.', 1)[1].strip()
                # q_cleaned = q_cleaned.replace('a -', '').replace('a-', '').strip()
                q_cleaned = re.sub(r'(?<!\w)a\s*-\s*', '', q_cleaned).strip()

                questions.append(('Q' + str(question_number), re.split(r'b\s*-\s*', q_cleaned)))
                question_number += 1

        questionario[starts[i]] = dict(questions)

    
    # Exibir questionário e capturar as respostas
    respostas = exibir_questionario(questionario, headers)

    # Botão para enviar as respostas
    if st.button("Enviar respostas"):
        st.write("Suas respostas:")
        for questao, resposta in respostas.items():
            st.write(f"{questao}: {resposta}")
        st.success("Respostas enviadas com sucesso!")
    
# Executar o aplicativo
if __name__ == "__main__":
    main()