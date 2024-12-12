import cv2
from ultralytics import YOLO
import serial


# cargamos el modelo
yolo = YOLO('yolo11n.pt')

# cargamos el video 
videoCap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

marca = 0

# funcion para obtener el color de la clase
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

def mouse(evento, xm, ym, bandera, param):
    global xmo,ymo,marca
    if evento == cv2.EVENT_LBUTTONDOWN:
        xmo = xm
        ymo = ym
        marca = 1

    if evento == cv2.EVENT_LBUTTONDBLCLK :
        marca = 0


while True:
    ret, frame = videoCap.read()
    if not ret:
        continue
    frame = cv2.flip(frame,1)

    frame = cv2.resize(frame, (640,480))

    #Extraemos el ancho y el alto del pantalla
    al, an, c = frame.shape

    #Extraemos el medio de la pantalla
    centro_ancho = int(an / 2)
    centro_alto = int(al / 2)
    
    #Mostrar un punto en el centro de la pantalla 
    cv2.circle(frame, (centro_ancho, centro_alto), 20, (0, 0, 255), 2)
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    
    results = yolo.track(frame, stream=True)


    for result in results:
        # obtener el nombre de las clases
        classes_names = result.names

        # interaccion con cada cuadro
        for box in result.boxes:
            # check if confidence is greater than 40 percent
            if box.conf[0] > 0.5:

                
                # get coordinates
                [x1, y1, x2, y2] = box.xyxy[0]

                
                # convert to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                

                

                #Extraemos el punto central
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                

                
                
                # get the class
                cls = int(box.cls[0])

                # get the class name
                class_name = classes_names[cls]

                # get the respective colour
                colour = getColours(cls)
                if marca == 0:
                    # draw the rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                    #Mostrar un punto en el centro
                    cv2.circle(frame, (cx, cy), 10, (0, 0, 255), 2)

                    # put the class name and confidence on the image
                    cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)

                cv2.namedWindow('frame')
                cv2.setMouseCallback('frame', mouse)
                if marca == 1:
                    if x1 < xmo < x2 and y1 < ymo < y2:
                        cv2.circle(frame, (xmo, ymo), 20, (0, 255, 0), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)  # Dibujamos el rectangulo
                        cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f} objeto seleccionado', (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                        xmo = cx
                        ymo = cy

                        #Condiciones de eje X
                        if xmo < centro_ancho - 50:
                            # Movemos hacia la izquierda
                            print("izquierda")
                            #com.write(i.encode("ascii"))
                            #print(i)

                        if xmo > centro_ancho + 50:
                            # Movemos hacia la derecha
                            print("derecha")
                            #com.write(d.encode("ascii"))
                            #print(d)

                        

                        #Condiciones de eje Y

                        if ymo < centro_alto - 50:
                            # Movemos hacia arriva
                            print("arriba")
                            #com.write(ar.encode("ascii"))
                            #print(ar)

                        if ymo > centro_alto + 50:
                            # movemos hacia abajo
                            print("abajo")
                            #com.write(ab.encode("ascii"))
                            #print(ab)

                        if 190 <= ymo <= 290 and 270 <= xmo <= 370:
                            #paramos el servo
                            print("centro")
                            #com.write(p.encode("ascii"))
                            #print(p)


                    
                        
                

                
                    
    
    # show the image
    
    cv2.imshow('frame', frame)

    # break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# release the video capture and destroy all windows
videoCap.release()
cv2.destroyAllWindows()