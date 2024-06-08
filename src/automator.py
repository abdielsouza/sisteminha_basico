"""
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
"""

import pandas as pd
import math
from sender import *
from myutil import *

"""
https://docs.google.com/spreadsheets/d/1kXotLZIM9jNbX-zcEp1BNcR8DiKNcKsnAYdGXZHj5A0/edit?usp=sharing
"""

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

class DataHolder:
    form_responses = {}
    closed_groups: list[dict] = []

def process_form_responses(sheet_link: str):

    add_out_message("Lendo planilha...")

    df = pd.read_csv(sheet_link.replace('edit?usp=sharing', 'export?format=csv'))

    add_out_message("Planilha lida com sucesso! Recolhendo dados relevantes...")

    for row in df.itertuples():
        DataHolder.form_responses[row[2]] = list(tuple(str(element).split(", ")) for element in row[3:])

    add_out_message("Dados recolhidos com sucesso!")
    add_out_message("Gerando listas de matching...")

    try:
        _get_matches_per_question()
    except Exception as e:
        add_out_message("Erro ao gerar listas! Tente novamente!")
        add_out_message(f"Descrição do erro: {e}")
        raise e
    else:
        add_out_message("Listas geradas com sucesso!")

    return DataHolder.closed_groups

def auto_send_responses(sender, password):
    sent = False
    add_out_message("Enviando respostas...")

    try:
        for group in DataHolder.closed_groups:
            recipients = []

            for email, _ in group.items():
                recipients.append(email)

            text = "Olá! Aqui vão os emails dos alunos que deram mais combinações com suas respostas no formulário:"
            
            for email in recipients:
                text += f"\n=> {email}"

            text += "\n\nObrigado pelas suas respostas!"

            send_email("Seus matchings de respostas do formulário!", text, sender, recipients, password)

    except Exception as e:
        add_out_message(f"Erro ao enviar respostas...\n\n{e}")

    if sent == True:
        add_out_message("Respostas enviadas com sucesso!")
    else:
        add_out_message("Erro ao enviar respostas!")

def _get_matches_per_question():
    caught_response = None
    next_index = 0
    for key, response in DataHolder.form_responses.items():
        caught_response = response

        if next_index > 0:
            if DataHolder.closed_groups[next_index - 1].get(key) == None:
                DataHolder.closed_groups.append({})
                DataHolder.closed_groups[next_index][key] = caught_response
            else:
                continue
        else:
            DataHolder.closed_groups.append({})
            DataHolder.closed_groups[next_index][key] = caught_response

        for another_key, another_response in DataHolder.form_responses.items():
            if caught_response is another_response:
                continue

            if _compare_response_tuples(another_response, caught_response) == True:
                DataHolder.closed_groups[next_index][another_key] = another_response

        next_index += 1

def _compare_response_tuples(response1: tuple, response2: tuple) -> bool:
    if len(response1) == 1 and len(response2) == 1:
        return True if response1[0] == response2[0] else False
    
    return True if len(response1 & response2) >= math.floor(0.80 * len(response1) + len(response2)) else False