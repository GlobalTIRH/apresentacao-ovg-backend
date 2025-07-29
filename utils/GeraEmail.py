from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os as osBib
import smtplib
import time
from flask import json
import requests
from dotenv import load_dotenv
from utils.GerarResumo import gerar_resumo
load_dotenv()

def emailbody(user_name, jobs, resumo):
    job_blocks = ""
    for job in jobs:
        job_blocks += f"""
        <tr>
            <td style="padding: 10px 20px; color: #333; border-bottom: 1px solid #eee; text-align: justify;">
                <h3 style="margin-bottom: 5px; text-align: justify;">{job.get("title", "N/A")}</h3>
                <p style="margin: 0; text-align: justify;"><strong>Empresa:</strong> {job.get("company", "N/A")}</p>
                <p style="margin: 0; text-align: justify;"><strong>Localização:</strong> {job.get("location", "N/A")}</p>
                <p style="margin: 10px 0; text-align: justify;">{job.get("description", "N/A")}</p>
                <p><a href="{job.get("url", "#")}" style="background-color: #007bff; color: #ffffff; padding: 8px 16px; text-decoration: none; border-radius: 5px;">Ver Vaga</a></p>
            </td>
        </tr>
        """

    return f"""\
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global TIRH - Ferramenta de Vagas</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <table width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <tr>
            <td align="center" style="padding: 10px 0;">
                <img src="https://globaltirh.com.br/site/wp-content/uploads/2019/11/Global-TIRH-logo-V-small.png" alt="Logo Global TI+RH" />
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 10px 0;">
                <h2 style="color: #333;">Seja bem-vindo, {user_name}!</h2>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 20px; color: #555;">
                <h3>Resumo das vagas encontradas</h3>
                <p style="text-align: justify;">{resumo}</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 20px; color: #555;">
                <h3>Vagas que combinam com seu perfil</h3>
            </td>
        </tr>
        {job_blocks}
        <tr>
            <td align="center" style="padding: 20px 0; font-size: 14px; color: #777;">
                <p>Atenciosamente,</p>
                <p><strong>Equipe Global TI+RH</strong></p>
                <p><a href="mailto:[Contato ou Suporte da Empresa]" style="color: #007bff; text-decoration: none;">[Contato ou Suporte da Empresa]</a></p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px 0; font-size: 12px; color: #aaa;">
                <a href="https://global-ovg-apresentacao-743957276592.southamerica-east1.run.app/termo" style="color: #007bff;">Leia os termos.</a>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def emailbody_novacancy(user_name):
    return f"""\
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global TIRH - Ferramenta de Vagas</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <table width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <tr>
            <td align="center" style="padding: 10px 0;">
                <img src="https://globaltirh.com.br/site/wp-content/uploads/2019/11/Global-TIRH-logo-V-small.png" alt="Logo Global TI+RH" />
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 10px 0;">
                <h2 style="color: #333;">Seja bem-vindo, {user_name}!</h2>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 20px; color: #555;">
                <h3>Infelizmente não encontramos vagas para o seu perfil.</h3>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px 0; font-size: 14px; color: #777;">
                <p>Atenciosamente,</p>
                <p><strong>Equipe Global TI+RH</strong></p>
                <p><a href="mailto:[Contato ou Suporte da Empresa]" style="color: #007bff; text-decoration: none;">[Contato ou Suporte da Empresa]</a></p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px 0; font-size: 12px; color: #aaa;">
                <a href="https://global-ovg-apresentacao-743957276592.southamerica-east1.run.app/termo" style="color: #007bff;">Leia os termos.</a>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def send_email(nome, email, area_interesse):
    sender_email = "mateus.silva@globaltirh.com.br"
    receiver_email = email
    
    password = osBib.getenv("GOOGLE_EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Vagas - Global TI+RH"

    headers = {
        "Authorization": f"Bearer {osBib.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    url = "https://api.brightdata.com/datasets/v3/trigger"
 
    params = {
        "dataset_id": "gd_lpfll7v5hcqtkxl6l",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": "5",
    }
    area_interesse = area_interesse.lower().replace("-", " ")

    # data = {
	#     "input": [{"location":"Goiânia","keyword":f"{area_interesse}","time_range":"Past month","experience_level":"Internship","country":"BR","job_type":"","remote":"","company":"","location_radius":""}],
	#     "custom_output_fields": ["job_title","company_name","job_location","url","job_summary"],
    # }

    data = {
	    "input": [{"location":"Goiânia","keyword":f"{area_interesse}","time_range":"Past month","experience_level":"","country":"BR","job_type":"","remote":"","company":"","location_radius":""}],
	    "custom_output_fields": ["job_title","company_name","job_location","url","job_summary"],
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    response_json = response.json()

    snapshot_id = response_json.get("snapshot_id")
    get_snapshot_infos = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    response = requests.get(get_snapshot_infos, headers=headers)

    while 'Snapshot is not ready yet, try again in 30s' in response.text:
        time.sleep(5)
        response = requests.get(get_snapshot_infos, headers=headers)

    data = response.text
    
    if 'Snapshot is empty' in response.text:
        body = emailbody_novacancy(nome)
    else:

        data = data.replace("}", "},")
        data = "[" + data[:-1] + "]"
        data = data.replace("},]", "}]")

        job_listings = []
        for item in json.loads(data):
            description = item.get("job_summary", "")
            description = description.replace(" Show more Show less", ".")

            job_listings.append(
                {
                    "title": item.get("job_title"),
                    "company": item.get("company_name"),
                    "location": item.get("job_location"),
                    "description": description,
                    "url": item.get("url"),
                }
            )
        
        resumo = gerar_resumo(job_listings)
        body = emailbody(nome, job_listings, resumo)

    msg.attach(MIMEText(body, "html"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()