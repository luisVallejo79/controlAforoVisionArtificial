import smtplib
import time 

def alerta():
	mensajeAlerta = "El aula sobrepasa el aforo maximo permitido"
	asunto = "Mensaje alerta aforo"

	mensajeAlerta = "Subject: {}\n\n{}".format(asunto, mensajeAlerta)

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("lfvallejo61922@umanizales.edu.co", "supervideos1")

	server.sendmail("lfvallejo61922@umanizales.edu.co", "lkrios62840@umanizales.edu.co", mensajeAlerta)

	server.quit()

	print("Correo de alerta enviado exitosamente")



def wait():
	print("Temporizador iniciado")
	time.sleep(10)
	print("Temporizador Finalizado")
    
