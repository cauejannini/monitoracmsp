# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, scheduler_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app

import smtplib
import ssl
from email.message import EmailMessage

import use_cases
from datetime import datetime

# For cost control, you can set the maximum number of containers that can be
# running at the same time. This helps mitigate the impact of unexpected
# traffic spikes by instead downgrading performance. This limit is a per-function
# limit. You can override the limit for each function using the max_instances
# parameter in the decorator, e.g. @https_fn.on_request(max_instances=5).
set_global_options(max_instances=10)

initialize_app()


@https_fn.on_request()
def check_cmsp_json_on_request(req: https_fn.Request) -> https_fn.Response:
    enviar_email()
    return https_fn.Response("Email enviado!")


@scheduler_fn.on_schedule(schedule="every day 23:00")
def check_cmsp_json(event: scheduler_fn.ScheduledEvent) -> None:
    enviar_email()


def enviar_email():

    data = datetime.today().strftime('%Y-%m-%d')
    dataRead = datetime.today().strftime('%d/%m/%Y')

    movimentacoes = use_cases.get_eventos_for_date_pretty(data, show_eventos=True)

    sender_email = "monitoramentocmsp@gmail.com"
    receiver_email = "contato@cidadeape.org"
    subject = f'[{dataRead}] Movimentações na CMSP'
    message = f"Bom dia Cidadeapé! Essas são as movimentações de interesse na Câmara Municipal de SP em {dataRead}:\n\n"
    if len(movimentacoes) == 0:
        message += "Nenhuma movimentação."
    else:
        message += movimentacoes

    # Create a text/plain message
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(message)

    port = 587  # For SSL gmail requires this port
    context = ssl.create_default_context()

    smtp = smtplib.SMTP('smtp.gmail.com', port)
    smtp.starttls(context=context)
    smtp.login("monitoramentocmsp@gmail.com", "pqtu aygv raon kpsl")
    smtp.send_message(msg)


enviar_email()
