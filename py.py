import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


smtp_server = "smtp.outlook.com"  # Exemplo: "smtp.gmail.com" para Gmail
smtp_port = 587
email_user = "email@example.com"
email_password = "senhaDoEmail"

# Destinatário e assunto
email_to = "emaildestinatario@example.com"
email_subject = "Imagem Convertida em PNG"

url = "https://mangaonline.biz/capitulo/one-piece-capitulo-1123/" 

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

container = soup.find('div', class_='content')

img_tag = container.find('img')
img_url = img_tag['src']

img_response = requests.get(img_url)
if img_response.status_code == 200:

    img_webp = Image.open(BytesIO(img_response.content))
    img_png = BytesIO()
    img_webp.convert("RGB").save(img_png, "PNG")
    img_png.seek(0)

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = email_subject
    msg.attach(MIMEText("Aqui está a imagem convertida para PNG.", "plain"))

    image_attachment = MIMEImage(img_png.read(), name="imagem_convertida.png")
    msg.attach(image_attachment)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_to, msg.as_string())
        server.quit()
        print("Email enviado")
    except Exception as err:
        print(f"Erro ao enviar email: {err}")
else:
    print("Não foi possível baixar a imagem.")
