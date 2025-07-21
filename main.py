import json
from flask import Flask, request
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from dotenv import load_dotenv
import traceback
load_dotenv()

app = Flask(__name__)
CORS(app)







def emailbody(user_name, jobs):
    job_blocks = ""
    for job in jobs:
        job_blocks += f"""
        <tr>
            <td style="padding: 10px 20px; color: #333; border-bottom: 1px solid #eee;">
                <h3 style="margin-bottom: 5px;">{job.get("title", "N/A")}</h3>
                <p style="margin: 0;"><strong>Empresa:</strong> {job.get("company", "N/A")}</p>
                <p style="margin: 0;"><strong>Localização:</strong> {job.get("location", "N/A")}</p>
                <p style="margin: 10px 0;">{job.get("description", "N/A")}</p>
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
    </table>
</body>
</html>
"""



def send_email(nome, email, area_interesse):
    sender_email = "mateus.silva@globaltirh.com.br"
    receiver_email = email
    password = "qemi brbt hcfz wpia"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Vagas - Global TI+RH"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    """
    
    url = "https://api.brightdata.com/datasets/v3/trigger"
 
    params = {
        "dataset_id": "gd_lpfll7v5hcqtkxl6l",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": "5",
    }

    data = [
        {"location":"Goiânia","keyword":f"\"+{area_interesse}+\"","experience_level":"Entry level","country":"","time_range":"","job_type":"","remote":"","company":"","location_radius":""},
    ]


    response = requests.post(url, headers=headers, params=params, json=data)
    response_json = response.json()
    """
    
    #snapshot_id = response_json.get("snapshot_id")
    snapshot_id = "s_md9a2om72k4gekdgw1"
    get_snapshot_infos = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    response = requests.get(get_snapshot_infos, headers=headers)
    
    job_listings = []
    jobs = [
        {
            "title": "Desenvolvedor de software",
            "company": "Conveste Serviços Financeiros",
            "location": "Goiânia, GO",
            "description": "Atuar no desenvolvimento de sistemas e aplicações.",
            "url": "https://www.linkedin.com/jobs/view/desenvolvedor-a-at-conveste-servi%C3%A7os-financeiros-4258371001?_l=en"
        },
        {
            "title": "Desenvolvedor (A) Backend Java E Android",
            "company": "Velis CRM",
            "location": "Goiânia, GO",
            "description": "Atuar no desenvolvimento de soluções backend em Java e Android.",
            "url": "https://www.linkedin.com/jobs/view/desenvolvedor-a-backend-java-e-android-at-velis-crm-4265747684?_l=en"
        },
        {
            "title": "Desenvolvedor De Back End",
            "company": "EDJ Digital",
            "location": "Goiânia, GO",
            "description": "Atuar no desenvolvimento de soluções backend.",
            "url": "https://www.linkedin.com/jobs/view/desenvolvedor-de-back-end-at-edj-digital-4261059702?_l=en"
        },
        {
            "title": "Desenvolvedor (A) Front End",
            "company": "Conveste Serviços Financeiros",
            "location": "Goiânia, GO",
            "description": "Atuar no desenvolvimento de interfaces e experiências do usuário.",
            "url": "https://www.linkedin.com/jobs/view/desenvolvedor-at-conveste-servi%C3%A7os-financeiros-4264692186?_l=en"
        },
        {
            "title": "Desenvolvedor (A) Backend Java E Android",
            "company": "Velis CRM",
            "location": "Goiânia, GO",
            "description": "Atuar no desenvolvimento de soluções backend em Java e Android.",
            "url": "https://www.linkedin.com/jobs/view/desenvolvedor-a-backend-java-e-android-at-velis-crm-4265747684?_l=en"
        }
    
    ]

    
    """
    try:
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                data = response.text
                print(data)
                data= data.replace('{"url"', ',{"url"')
                data = f"[{data}]"
                data= data.replace('[,{"url"', '[{"url"')
                # print(data)
                data = json.loads(data)
                # print(f"Resposta da API: {data}")

                # print(f"Resposta da API: {data}")  
                for job in data:
                    # print(type(job))
                    # print(f"Job: {job}")

                    job_info = {
                        "title": job.get("title", "N/A"),
                        "company": job.get("company", "N/A"),
                        "location": job.get("location", "N/A"),
                        "description": job.get("description", "N/A"),
                        "url": job.get("url", "#")
                    }
                    job_listings.append(job_info)
                    break
            else:
                print(f"Resposta não é JSON. Content-Type: {content_type}")
                print(f"Conteúdo: {response.text[:200]}...")
        else:
            print(f"Erro na API: {response.text}")

    except Exception as e:
        print(f"Erro ao processar a resposta: {e}")
        traceback.print_exc()
        return
    """
    
    
    
    


    print(response)

    body = emailbody(nome, jobs)
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()



@app.route("/send_email", methods=["POST"])
def index():

    nome = request.json.get("nome")
    email = request.json.get("email")
    telefone = request.json.get("telefone")
    area_interesse = request.json.get("area_interesse")
    
 
    send_email(nome, email, area_interesse)

    return {}, 200


if __name__ == '__main__':
    app.run(debug=False)