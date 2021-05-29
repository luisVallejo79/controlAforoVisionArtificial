import cv2
import funciones as fun
import mediapipe as mp


#""" importamos md ahora la utilizado para la deteccion del rostro  """
mp_face_detection = mp.solutions.face_detection

#""" solucion para visualizar el triangulo que rodea el rostro, y los puntos de ref """
mp_drawing = mp.solutions.drawing_utils

# """ inicializar la camara """
cap = cv2.VideoCapture(0)
sendMail = False
aforoAula201=1
#timedOut = 0
verify=0
alertaEnviada = 0
with mp_face_detection.FaceDetection(
	#valor minimo de confianza para que sea considerada exitos  
    min_detection_confidence=0.5) as face_detection:  
	while cap.isOpened():
		#leemos lo que viene en el video y guardamos en dos variables
		ret, frame = cap.read()
		if ret == False: break

		#convertir el frame de bgr a rgb OpenCV es compatible con el modelo BGR - "área" menos significativa
		frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

		#guardamos el resultado de la deteccion en la variables results
		results = face_detection.process(frame)

		#condicional para iniciar con el dibujado del rectangulo que delimita el rostro
		counter = 0
		if results.detections:
			for detection in results.detections:
				mp_drawing.draw_detection(frame, detection)

				# podemos editar la forma en que se dibujan los puntos detectados
				#mp_drawing.DrawingSpec(color= (0, 255, 255), circle_radius=3))

				#dibujado por defecto de mediaPipe
				mp_drawing.draw_detection(frame, detection)
				#conteo para confrontar con el del aforo
				counter=counter+1


		#dibujar el rectangulo donde se va a mostrar el texto y conteo	
		cv2.rectangle(frame,(0,0),(frame.shape[1],30),(0,0,0),-2)


		#argumentos para el visualizar el texto "Conteo actual"
		color = (0, 255, 255)
		mensaje = "Conteo actual"
		font = cv2.FONT_HERSHEY_SIMPLEX
		
	
		#para visualizar el anterior texto se utiliza la funcion cv.putTex() 
		cv2.putText(frame, mensaje, (5,25), font, 1, color, 2)
		#mostrando el contador convirtiendo a entero para realizar operaciones
		cv2.putText(frame, str(counter), (240,25), font, 1, color, 2)

		#mostrar el video de la camara
		cv2.imshow('Control de Aforo Umanizales', frame)

		#inician las verificaciones de aforo y conteo
		if counter>aforoAula201:
			# si sobrepasa se inicia un contador de verificacion
			verify=verify+1
		else:
			verify=0

		# primer vez que el conteo sobrepasa el aforo, y el conteo de verificacion llego a 50
		if counter>aforoAula201 and sendMail == False and verify>50:
			fun.alerta()
			sendMail=True
			#fun.wait()
			verify=0
			alertaEnviada=alertaEnviada+1

		# Entra en este condicional solo si ya entro al anterior y luego de 20seg continua el contado mayor al aforo
		if counter>aforoAula201 and alertaEnviada == 1 and verify>50:
			fun.alerta()
			verify=0
			alertaEnviada=alertaEnviada+1
			
		print('verify', verify);
		if cv2.waitKey(80) & 0xFF == ord('q'):
			break

cap.release()
#salida.release()
cv2.destroyAllWindows()

