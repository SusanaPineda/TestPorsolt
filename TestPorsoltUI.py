###################################
# FRAME1 -> Pantalla principal con las dos opciones
### FRAMES TEST AUTOMATICO ###
# FRAME2 -> Pantalla cargar video Test Automatico
# FRAME3 -> Pantalla instrucciones Test Automatico
# FRAME4 -> Pantalla reproduccion Test Automatico
# FRAME5 -> Pantalla resultados Test Automatico
### FRAMES TEST MANUAL ###
# FRAME6 -> Pantalla cargar video Test Manual
# FRAME7 -> Pantalla reproduccion Test Manual
# FRAME8 -> Pantalla resultados Test Manual
###################################
import imageio
import tkinter as tk, threading
import cv2
import click
import numpy as np 
import ctypes 
import matplotlib.pyplot as plt
import ctypes 
import pandas as pd

from matplotlib import animation
from matplotlib import style
from scipy.interpolate import InterpolatedUnivariateSpline
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from time import time
from multiprocessing import Process, Lock


### VARIABLES PARA TEST MANUAL ###
Manual_nado = 0
Manual_quieta = 0
Manual_cInit = 0
Manual_cFin = 0
Manual_inicializado = False
Manual_nadando = False
Manual_quietaB = False
stopManual = True
MutexManual = Lock()
### VARIABLES EXCEL ###
Porcentaje_Manual_Nado = 0
Porcentaje_Manual_Quieta = 0
Vector_Nado_Manual = [0]
Vector_Quieta_Manual = [0]

raiz = Tk()


### STRINGS MANUAL ###
Manual_nadoS = StringVar()
Manual_quietaS = StringVar()
Manual_Porcentaje_NadoS = StringVar()
Manual_Porcentaje_QuietaS = StringVar()

### FIN VARIABLES TEST MANUAL ###


### VARIABLES TEST AUTOMATICO ###
Automatico_video_name = ""
stopAutomatico = True
MutexAutomatico = Lock()
waitKey_fps = 15
### VARIABLES GRAFICA ###
mod = [0]
seleccion = False 
### VARIABLES CONTADOR ###
Automatico_nado = 0
Automatico_quieta = 0

### VARIABLES EXCEL ###
Porcentaje_Automatico_Nado = 0
Porcentaje_Automatico_Quieta = 0
Vector_Nado_Automatico = [0]
Vector_Quieta_Automatico = [0]

### STRINGS AUTOMATICO ###
Automatico_nadoS = StringVar()
Automatico_quietaS = StringVar()
Automatico_Porcentaje_NadoS = StringVar()
Automatico_Porcentaje_QuietaS = StringVar()
### FIN VARIABLES TEST AUTOMATICO ###
def nothing(x):
	pass

def automatico():
    frame1.pack_forget()
    frame2.pack()

def cargarVideo_Automatico():
    selectVideo_Automatico()
    frame2.pack_forget()
    frame3.pack()

def back_Automatico():
    frame2.pack_forget()
    frame1.pack()

def selectVideo_Automatico():
    global Automatico_video_name
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4","*.mp4"),("all files","*.*")))
    print(raiz.filename)
    url = raiz.filename
    Automatico_video_name = url 


def iniciar_Automatico():
    stream_Automatico(canvas1)
    frame3.pack_forget()
    frame4.pack()

def stream_Automatico(canvas1):
    global Automatico_video_name
    thread = threading.Thread(name= "hilo_testAutomatico" ,target=exec, args=(canvas1,Automatico_video_name))  
    thread.daemon = 1
    thread.start()

def seleccionar_Automatico():
    global waitKey_fps, seleccion
    waitKey_fps = 0
    seleccion = True

def exec(canvas1, video ):
    global mod, Automatico_nado, Automatico_quieta, Vector_Nado_Automatico, Vector_Quieta_Automatico, stopAutomatico,seleccion,waitKey_fps

    ### REAJUSTE DEL FRAME4 ###
    frame4.config(width = "2100", height="1300", bg="#242424")
    TituloAutomatico = Label(frame4,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 30))
    TituloAutomatico.place(x=680, y=55)

    rec1 = Label(frame4,bg="#C4C4C4")
    rec1.config(width="105",height="5")
    rec1.place(x=126, y=478)
    
    IndicadorTxt = Label(frame4, text="Nadando", bg="#C4C4C4",font=("Helvetica", 20))
    IndicadorTxt.place(x=370,y=500)

    Indicador = Label(frame4, bg="#3847CD")
    Indicador.config(width="2", height="1")
    Indicador.place(x=520,y=510)

    rec2 = Label(frame4,bg="#C4C4C4")
    rec2.config(width="105",height="25")
    rec2.place(x=1048, y=180)

    ### Sustituir por la gráfica ###
    contNado2 = Label(frame4, text = "Tiempo nadando: ",bg="#C4C4C4",font=("Helvetica", 20))
    contNado2.place(x=1100, y=250)
    contadorNado2 = Label(frame4,bg="#C4C4C4",font=("Helvetica", 20),textvariable=Automatico_nadoS)
    contadorNado2.place(x=1400, y=250)
    contQuieta2 = Label(frame4, text = "Tiempo Quieta: ",bg="#C4C4C4",font=("Helvetica", 20))
    contQuieta2.place(x=1100, y=350)
    contadorQuieta2 = Label(frame4,bg="#C4C4C4",font=("Helvetica", 20),textvariable=Automatico_quietaS)
    contadorQuieta2.place(x=1400, y=350)
    ### Sustituir por la grafica ###
    
    btnParar = Button(frame4, text="Parar")
    btnParar.config(width="17", height="2",font=("Helvetica", 15), bg="#3F3F3F", foreground="white", command = parar_Automatico)
    btnParar.place(x=550, y=500)
    
    btnSeleccionar = Button(frame4, text="Seleccionar")
    btnSeleccionar.config(width="17", height="2",font=("Helvetica", 15), bg="#3F3F3F", foreground="white", command = seleccionar_Automatico)
    btnSeleccionar.place(x=550, y=500)
    
    ### FIN REAJUSTE DEL FRAME4 ###

    #### Inicio Variables Locales ####
    #Inicio del programa
    seleccion = False 
    seleccionado = False
    #Primer frame del video
    hsv = None 
    #Posicion del elemento que queremos seguir
    roiPos = [] 

    #Variables para el marcado de movimiento
    font = cv2.FONT_HERSHEY_SIMPLEX

    #Variables para el calculo de velocidad
    posAnterior = [0,0]
    diferencia = [0,0]
    velocidad = [0,0]
    contadorFPS = 0
    velTotal = 0
    cntX = 0
    cntY = 0
    M = [0,0]

    #variables para Camshift
    track_window = []
    term_crit =(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)

    #Variables resolucion de pantalla
    pantalla = ctypes.windll.user32
    pantalla.SetProcessDPIAware()
    ancho, alto = pantalla.GetSystemMetrics(0), pantalla.GetSystemMetrics(1)

    #Variables contador de nado
    nadandoBool = True
    quietaBool = False
    CNado = 4
    CQuieta = 4
    totContNado = 0
    totContQuieta = 0

    #VariablesGrafica
    contadorGrafica = 50
    ####Fin Variables Locales ####

    cap = cv2.VideoCapture(video)
    while(cap.isOpened()):
        MutexAutomatico.acquire()
        
        cv2.waitKey(waitKey_fps) & 0xFF

        if stopAutomatico == True:
            MutexAutomatico.release()
            #Obtenemos cada frame del video
            ret, frame_video = cap.read()
            if ret == True:
            
                frame_video = cv2.resize(frame_video,(int(ancho/2),int(alto/2)))
            
                #Pasamos de BGR a HSV
                hsv = cv2.cvtColor(frame_video,cv2.COLOR_BGR2HSV)

                #Comprobamos si estamos en el momento de seleccion
                if(seleccion):
                    #cv2.imshow("image",frame)
                    frame_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame_video,cv2.COLOR_BGR2RGB), "RGB").resize((600,300), Image.ANTIALIAS))
                    canvas1.config(image=frame_image)
                    canvas1.config(width="737",height="300")
                    canvas1.place(x=126, y=180)
                    canvas1.image =frame_image
                    roiPos = cv2.selectROI(frame_video,True)
                    track_window.append(roiPos[0])
                    track_window.append(roiPos[1])
                    track_window.append(roiPos[2])
                    track_window.append(roiPos[3])

                    roi = frame_video[roiPos[1]:roiPos[1]+roiPos[3], roiPos[0]:roiPos[0]+roiPos[2]]
                    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    mask2 = cv2.inRange(hsv_roi,np.array((0., 60., 32.,)), np.array((180.,255.,255.)))
                    roi_hist = cv2.calcHist([hsv_roi],[0],mask2,[180],[0,180])
                    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

                    M[0] = track_window[0] + float(track_window[2])/2.
                    M[1] = track_window[1] + float(track_window[3])/2.

                    posAnterior[0] = int(M[0])
                    posAnterior[1] = int(M[1])
                    btnSeleccionar.place_forget()
                    waitKey_fps = 15
                    seleccionado = True
                    seleccion = False

                if seleccionado == True :
                    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
                    ret,track_window = cv2.CamShift(dst, (track_window[0],track_window[1],track_window[2],track_window[3]), term_crit)
                    res = cv2.bitwise_and(frame_video,frame_video)

                    #Mostrar por pantalla CamShift
                    pts = cv2.boxPoints(ret)
                    pts = np.int0(pts)
                    img2 = cv2.polylines(res,[pts],True,255,2)

                    #Almacenamos la posicion del cuadrado
                    M[0] = track_window[0] + float(track_window[2])/2.
                    M[1] = track_window[1] + float(track_window[3])/2.
                    cntX = int(M[0])
                    cntY = int(M[1])

                    #Dibujamos por pantalla
                    cv2.circle(res,(cntX,cntY),5,(130,50,200),-1)
                    #cv2.putText(res,str(cntX)+','+str(cntY),(30, 60), font, 2, (130,50,200),3,cv2.LINE_AA)

                    #Calculamos la velocidad
                    if(contadorFPS == 6):
                        
                        #Obtenemos la posicion de hace 6 frames
                        x0 = posAnterior[len(posAnterior)-2]
                        y0 = posAnterior[len(posAnterior)-1]
                        #Obtenemos la posicion del frame actual
                        x1 = cntX
                        y1 = cntY
                        #Obtenemos la diferencia entre el frame1 y el frame0
                        diferencia.append(abs(x0-x1))
                        diferencia.append(abs(y0-y1))
                        #Obtenemos la velocidad tomando como tiempo un cuarto de un segundo (cada 6 frames)
                        velocidad.append(diferencia[(len(diferencia)-2)]/0.5)
                        velocidad.append(diferencia[(len(diferencia)-1)]/0.5)
                        #Obtenemos la velocidad total
                        vX = velocidad[len(velocidad)-2]
                        vY = velocidad[len(velocidad)-1]
                        velTotal = np.array([vX,vY])
                        velTotal = np.linalg.norm(velTotal)
                        mod.append(velTotal)
                        #Comprobamos la velocidad y contamos el tiempo
                        if (velTotal>17):
                            if(nadandoBool):
                               
                                Automatico_nado = Automatico_nado + 0.25
                                totContNado = totContNado + 0.25
                                Automatico_nadoS.set(str(Automatico_nado))
                                IndicadorTxt.config (text = "Nadando")
                                Indicador.config(bg = "#3847CD")
                            elif(quietaBool):
                               
                                CNado = CNado-1
                                if(CNado > 0):
                                    
                                    Automatico_quieta = Automatico_quieta + 0.25
                                    totContQuieta = totContQuieta + 0.25
                                elif(CNado == 0):
                                    
                                    CNado = 4
                                    CQuieta = 4
                                    Vector_Quieta_Automatico.append(totContQuieta)
                                    totContQuieta = 0
                                    quietaBool = False
                                    nadandoBool = True
                    
                        else:
                            if(quietaBool):
                               
                                Automatico_quieta = Automatico_quieta + 0.25
                                totContQuieta = totContQuieta + 0.25
                                Automatico_quietaS.set(str(Automatico_quieta))
                                IndicadorTxt.config(text = "Quieta")
                                Indicador.config(bg = "#6B74CA")
                            elif(nadandoBool):
                                    CQuieta = CQuieta - 1
                                    if(CQuieta>0):
                                        Automatico_nado = Automatico_nado + 0.25
                                        totContNado = totContNado + 0.25
                                    elif(CQuieta==0):
                                        CNado = 4
                                        CQuieta = 4
                                        Vector_Nado_Automatico.append(totContNado)
                                        totContNado = 0
                                        nadandoBool = False
                                        quietaBool = True

                        #Actualizamos la posicion anterior y aumentamos el contador
                        posAnterior.append(cntX)
                        posAnterior.append(cntY)
                        #Pintamos la grafica (ELIMINAR)
                            #cv2.line(graf,(contadorGrafica,(206-int(mod[len(mod)-2]))),((contadorGrafica+3),(206-int(mod[len(mod)-1]))),(0,0,0),1)
                            #contadorGrafica = contadorGrafica+3
                            #cv2.imshow("grafica",graf)
                        #Limpar contador
                        contadorFPS = 0

                    contadorFPS = contadorFPS + 1
                    #cv2.putText(res, str(mod[len(mod)-1]),(30,120),font,2, (130,50,200),3,cv2.LINE_AA)
            
                    frame_image2 = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(res,cv2.COLOR_BGR2RGB),"RGB").resize((600,300), Image.ANTIALIAS))
                    canvas1.config(image=frame_image2)
                    canvas1.config(width="737",height="300")
                    canvas1.place(x=126, y=180)
                    canvas1.image = frame_image2
                else:
                    ph = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame_video,cv2.COLOR_BGR2RGB),"RGB").resize((600,300), Image.ANTIALIAS))
                    canvas1.config(image=ph)
                    canvas1.config(width="737",height="300")
                    canvas1.place(x=126, y=180)
                    canvas1.image = ph
                
            else:
                MutexAutomatico.release()
                cap.release()
                cv2.destroyAllWindows()
                

    cap.release()
    cv2.destroyAllWindows()
            

def parar_Automatico():
    global Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta,stopAutomatico

    AutomaticoTotal = Automatico_nado + Automatico_quieta
    Porcentaje_Automatico_Nado = Automatico_nado / AutomaticoTotal * 100
    Porcentaje_Automatico_Quieta = Automatico_quieta / AutomaticoTotal * 100
    Automatico_Porcentaje_NadoS.set(str(round(Porcentaje_Automatico_Nado)))
    Automatico_Porcentaje_QuietaS.set(str(round(Porcentaje_Automatico_Quieta)))
    

    MutexAutomatico.acquire()
    stopAutomatico = False
    MutexAutomatico.release()
    

    frame4.pack_forget()
    ### Reajuste frame 5 ###
    #frame5 = Frame()
    frame5.config(width = "2100", height="1300", bg="#242424")
    frame5.pack()
    
    TituloAutomatico = Label(frame5,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 30))
    TituloAutomatico.place(x=680, y=55)
    
    rec1 = Label(frame5,bg="#C4C4C4")
    rec1.config(width="105",height="25")
    rec1.place(x=126, y=180)
   
    rec2 = Label(frame5,bg="#C4C4C4")
    rec2.config(width="105",height="25")
    rec2.place(x=1048, y=180)

    contNado = Label(frame5, text = "Tiempo nadando: ",bg="#C4C4C4",font=("Helvetica", 20))
    contNado.place(x=1100, y=200)
    contadorNado = Label(frame5,bg="#C4C4C4",font=("Helvetica", 20),textvariable=Automatico_nadoS)
    contadorNado.place(x=1400, y=200)
    contQuieta = Label(frame5, text = "Tiempo Quieta: ",bg="#C4C4C4",font=("Helvetica", 20))
    contQuieta.place(x=1100, y=300)
    contadorQuieta = Label(frame5,bg="#C4C4C4",font=("Helvetica", 20),textvariable=Automatico_quietaS)
    contadorQuieta.place(x=1400, y=300)
    porNado = Label(frame5, text = "Porcentaje Nadando: ",bg="#C4C4C4",font=("Helvetica", 20))
    porNado.place(x=1100, y=400)
    porcentajeNado = Label(frame5,bg="#C4C4C4",font=("Helvetica", 20),textvariable = Automatico_Porcentaje_NadoS)
    porcentajeNado.place(x=1400, y=400)
    porcQuieta = Label(frame5, text = "Porcentaje Quieta: ",bg="#C4C4C4",font=("Helvetica", 20))
    porcQuieta.place(x=1100, y=500)
    porcentajerQuieta = Label(frame5,bg="#C4C4C4",font=("Helvetica", 20),textvariable = Automatico_Porcentaje_QuietaS)
    porcentajerQuieta.place(x=1400, y=500)
    
    btnParar2 = Button(frame5, text="Exportar Datos")
    btnParar2.config(width="30", height="2",font=("Helvetica", 20), bg="#3F3F3F", foreground="white",command = exportar_Automatico)
    btnParar2.place(x=700, y=750)
    
    btnToInit2 = Button(frame5, text="Inicio")
    btnToInit2.config(width="10", height="2",font=("Helvetica", 20), bg="#3F3F3F", foreground="white", command = to_Init_Automatico)
    btnToInit2.place(x=1600, y=750)
    
    ### Fin Reajuste frame 5 ###

def exportar_Automatico():
    global Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta,Vector_Nado_Automatico, Vector_Quieta_Automatico
    raiz.filename = filedialog.asksaveasfilename(initialdir = "/", title = "Select directory",filetypes = (("xlsx","*.xlsx"),("all files","*.*")))
    url = raiz.filename

    if(len(Vector_Nado_Automatico)>len(Vector_Quieta_Automatico)):
        while(len(Vector_Quieta_Automatico)<len(Vector_Nado_Automatico)):
            Vector_Quieta_Automatico.append(0)
    if(len(Vector_Nado_Automatico)<len(Vector_Quieta_Automatico)):
        while(len(Vector_Nado_Automatico)<len(Vector_Quieta_Automatico)):
            Vector_Nado_Automatico.append(0)

    data = {'Tiempo total nado': round(Automatico_nado,2),
            'Tiempo total reposo': round(Automatico_quieta,2),
            'Porcentaje nado': round(Porcentaje_Automatico_Nado),
            'Porcentaje reposo': round(Porcentaje_Automatico_Quieta),
            'Tiempos nado': Vector_Nado_Automatico,
            'Tiempos reposo': Vector_Quieta_Automatico}
    df = pd.DataFrame(data,columns = ['Tiempo total nado', 'Tiempo total reposo','Porcentaje nado','Porcentaje reposo','Tiempos nado','Tiempos reposo' ])
    df.to_excel(url, sheet_name='example')

def to_Init_Automatico():
    global Automatico_video_name, stopAutomatico, mod, Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta, Vector_Nado_Automatico, Vector_Quieta_Automatico

    Automatico_video_name = ""
    stopAutomatico = True
    mod = [0]
    Automatico_nado = 0
    Automatico_quieta = 0
    Porcentaje_Automatico_Nado = 0
    Porcentaje_Automatico_Quieta = 0
    Vector_Nado_Automatico = [0]
    Vector_Quieta_Automatico = [0]

    Automatico_nadoS.set(str(Automatico_nado))
    Automatico_quietaS.set(str(Automatico_quieta))
    Automatico_Porcentaje_NadoS.set(str(Porcentaje_Automatico_Nado))
    Automatico_Porcentaje_QuietaS.set(str(Porcentaje_Automatico_Quieta))

    frame5.pack_forget()

    frame1.config(width = "2000", height="1300", bg="#242424")
    frame1.pack()

    Cimg1.config(width="242",height="331",bg="#242424")
    Cimg1.place(x=1300, y= 200)

    Cimg2.config(width="279",height="230",bg="#242424")
    Cimg2.place(x=200, y= 600)

    btnAutomatico.config(width="30", height="2",font=("Helvetica", 20), bg="#3F3F3F", foreground="white",command = automatico)
    btnAutomatico.place(x=700, y=500)

    btnManual.config(width="30", height="2",font=("Helvetica", 20), bg="#3F3F3F", foreground="white",command = manual)
    btnManual.place(x=700, y=350)



    

def manual():
    frame1.pack_forget()
    frame6.pack()

def cargarVideo_Manual():
    selectVideo_Manual(canvas4)
    frame6.pack_forget()
    frame7.pack()
    
def back_Manual():
    frame6.pack_forget()
    frame1.pack()

def contador():
    global Manual_inicializado, Manual_nadando, Manual_quietaB, Manual_nado, Manual_quieta, Manual_cInit, Manual_cFin, Vector_Nado_Manual, Vector_Quieta_Manual

    if(Manual_inicializado == False):
        btnIniciar['text'] = 'quieta'
        Manual_inicializado = True
        Manual_nadando = True
        Manual_cInit = time()
        
        
    elif(Manual_nadando == True):
        btnIniciar['text'] = 'nadando'
        Manual_nadando = False
        Manual_quietaB = True
        Manual_cFin = time() - Manual_cInit
        Manual_nado = Manual_nado + Manual_cFin
        Vector_Nado_Manual.append(round(Manual_cFin,2))
        Manual_cInit = time()
       
        Manual_nadoS.set(str(round(Manual_nado,2)))
        

    elif(Manual_quietaB == True):
        btnIniciar['text'] = 'quieta'
        Manual_nadando = True
        Manual_quietaB = False
        Manual_cFin = time() - Manual_cInit
        Manual_quieta = Manual_quieta + Manual_cFin
        Vector_Quieta_Manual.append(round(Manual_cFin,2))
        Manual_cInit = time()
        Manual_quietaS.set(str(round(Manual_quieta,2)))

def parar_Manual():
    global Manual_nado, Manual_quieta, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta,stopManual 

    frame7.pack_forget()
    Manual_Total = Manual_nado + Manual_quieta
    Porcentaje_Manual_Nado = Manual_nado/Manual_Total*100
    Porcentaje_Manual_Quieta = Manual_quieta/Manual_Total*100
    Manual_Porcentaje_NadoS.set(str(round(Porcentaje_Manual_Nado)))
    Manual_Porcentaje_QuietaS.set(str(round(Porcentaje_Manual_Quieta)))
    MutexManual.acquire()
    stopManual = False
    MutexManual.release()
    frame8.pack()
    
def exportar_Manual():
    global Manual_nado, Manual_quieta, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta,Vector_Nado_Manual, Vector_Quieta_Manual

    raiz.filename = filedialog.asksaveasfilename(initialdir = "/", title = "Select directory",filetypes = (("xlsx","*.xlsx"),("all files","*.*")))
    url = raiz.filename

    if(len(Vector_Nado_Manual)>len(Vector_Quieta_Manual)):
        while(len(Vector_Quieta_Manual)<len(Vector_Nado_Manual)):
            Vector_Quieta_Manual.append(0)
    if(len(Vector_Nado_Manual)<len(Vector_Quieta_Manual)):
        while(len(Vector_Nado_Manual)<len(Vector_Quieta_Manual)):
            Vector_Nado_Manual.append(0)

    data = {'Tiempo total nado': round(Manual_nado,2),
            'Tiempo total reposo': round(Manual_quieta,2),
            'Porcentaje nado': round(Porcentaje_Manual_Nado),
            'Porcentaje reposo': round(Porcentaje_Manual_Quieta),
            'Tiempos nado': Vector_Nado_Manual,
            'Tiempos reposo': Vector_Quieta_Manual}
    df = pd.DataFrame(data,columns = ['Tiempo total nado', 'Tiempo total reposo','Porcentaje nado','Porcentaje reposo','Tiempos nado','Tiempos reposo' ])
    df.to_excel(url, sheet_name='example')

def selectVideo_Manual(canvas4):
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4","*.mp4"),("all files","*.*")))
    url = raiz.filename
    video_name = url 
    video = imageio.get_reader(video_name)
    thread = threading.Thread(target=stream, args=(video,canvas4))
    thread.daemon = 1
    thread.start()

def stream(video,canvas4):
    global stopManual
    for image in video.iter_data():
        MutexManual.acquire()
        if(stopManual):
            MutexManual.release()
            frame_image = ImageTk.PhotoImage((Image.fromarray(image)).resize((496,276), Image.ANTIALIAS))
            canvas4.config(image=frame_image)
            canvas4.config(width="492",height="272")
            canvas4.place(x=80, y=150)
            canvas4.image = frame_image
            k = cv2.waitKey(5) & 0xFF
        else:
            MutexManual.release()
            break

def to_Init_Manual():
    global Manual_nado, Manual_quieta, Manual_cInit, Manual_cFin, Manual_inicializado, Manual_nadando, Manual_quietaB, stopManual, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta, Vector_Nado_Manual, Vector_Quieta_Manual
    
    #limpar variables#
    Manual_nado = 0
    Manual_quieta = 0
    Manual_cInit = 0
    Manual_cFin = 0
    Manual_inicializado = False
    Manual_nadando = False
    Manual_quietaB = False
    stopManual = True
    Porcentaje_Manual_Nado = 0
    Porcentaje_Manual_Quieta = 0
    Vector_Nado_Manual.clear()
    Vector_Quieta_Manual.clear()

    Manual_nadoS.set(str(Manual_nado))
    Manual_quietaS.set(str(Manual_quieta))
    Manual_Porcentaje_NadoS.set(str(Porcentaje_Manual_Nado))
    Manual_Porcentaje_QuietaS.set(str(Porcentaje_Manual_Quieta))

    frame8.pack_forget()
    frame1.pack()

##FRAME1##
frame1 = Frame()
frame1.config(width = "1440", height="1024", bg="#242424")
frame1.pack()

img1 = Image.open("R1.png")
img1 = img1.resize((242,331), Image.ANTIALIAS)
img1 =  ImageTk.PhotoImage(img1)
Cimg1 = Label(frame1, image = img1) 
Cimg1.config(width="242",height="331",bg="#242424")
Cimg1.place(x=1000, y= 70)

img2 = Image.open("R2.png")
img2 = img2.resize((279,230), Image.ANTIALIAS)
img2 =  ImageTk.PhotoImage(img2)
Cimg2 = Label(frame1, image = img2) 
Cimg2.config(width="279",height="230",bg="#242424")
Cimg2.place(x=70, y= 400)

btnAutomatico = Button(frame1, text="Test Automatico")
btnAutomatico.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = automatico)
btnAutomatico.place(x=500, y=400)

btnManual = Button(frame1, text="Test Manual")
btnManual.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = manual)
btnManual.place(x=500, y=250)
##FIN FRAME1##

##FRAME2##
frame2 = Frame()
frame2.config(width = "1440", height="1024", bg="#242424")
#frame2.pack()

TituloAutomatico = Label(frame2,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

rec1 = Label(frame2,bg="#C4C4C4")
rec1.config(width="70",height="18")
rec1.place(x=80, y=150)

img6 = Image.open("R3.png")
img6 = img6.resize((98,152), Image.ANTIALIAS)
img6 =  ImageTk.PhotoImage(img6)
Cimg6 = Label(frame2, image = img6) 
Cimg6.config(width="98",height="152",bg="#C4C4C4")
Cimg6.place(x=400, y= 250)

rec2 = Label(frame2,bg="#C4C4C4")
rec2.config(width="70",height="18")
rec2.place(x=710, y=150)

img7 = Image.open("R4.png")
img7 = img7.resize((68,102), Image.ANTIALIAS)
img7 =  ImageTk.PhotoImage(img7)
Cimg7 = Label(frame2, image = img7) 
Cimg7.config(width="68",height="102",bg="#C4C4C4")
Cimg7.place(x=1100, y= 300)

btnCargarVideo = Button(frame2, text="Cargar Video")
btnCargarVideo.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = cargarVideo_Automatico)
btnCargarVideo.place(x=470, y=500)

btnBack = Button(frame2, text="Back")
btnBack.config(width="8", height="1",font=("Helvetica", 12), bg="#3F3F3F", foreground="white",command = back_Automatico)
btnBack.place(x=80, y=50)
##FIN FRAME2##

##FRAME 3##
frame3 = Frame()
frame3.config(width = "1440", height="1024", bg="#242424")
#frame3.pack()

TituloAutomatico = Label(frame3,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

rec1 = Label(frame3,bg="#C4C4C4")
rec1.config(width="70",height="18")
rec1.place(x=80, y=150)
canvas = Label(frame3)
canvas.config(width="70",height="15", bg="#C4C4C4")
canvas.place(x=80, y=150)

img9 = Image.open("R3.png")
img9 = img9.resize((98,152), Image.ANTIALIAS)
img9 =  ImageTk.PhotoImage(img9)
Cimg9 = Label(frame3, image = img9) 
Cimg9.config(width="98",height="152",bg="#C4C4C4")
Cimg9.place(x=400, y= 250)

rec2 = Label(frame3,bg="#C4C4C4")
rec2.config(width="70",height="18")
rec2.place(x=710, y=150)

img8 = Image.open("R4.png")
img8 = img8.resize((68,102), Image.ANTIALIAS)
img8 =  ImageTk.PhotoImage(img8)
Cimg8 = Label(frame3, image = img8) 
Cimg8.config(width="68",height="102",bg="#C4C4C4")
Cimg8.place(x=1100, y= 300)

Instrucciones = Label(frame3,text="Al presionar el botón seleccionar aparecerá \n una nueva ventana en la cual habrá que \n seleccionar la marca del sujeto \n y presionar enter.",bg="#C4C4C4",font=("Helvetica", 15))
Instrucciones.place(x=750, y=200)

btnIniciar = Button(frame3, text="Iniciar")
btnIniciar.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = iniciar_Automatico)
btnIniciar.place(x=470, y=500)
##FIN FRAME3##

##FRAME 4##
frame4 = Frame()
frame4.config(width = "1440", height="1024", bg="#242424")
#frame4.pack()

canvas1 = Label(frame4)
canvas1.config(width="70",height="15",bg="#C4C4C4")
canvas1.place(x=80, y=150)

##FIN FRAME4##

##FRAME 5##
frame5 = Frame()

##FIN FRAME5##

##FRAME6##
frame6 = Frame()
frame6.config(width = "1440", height="1024", bg="#242424")
#frame6.pack()

TituloAutomatico = Label(frame6,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

rec1 = Label(frame6,bg="#C4C4C4")
rec1.config(width="70",height="18")
rec1.place(x=80, y=150)
canvas3 = Label(frame6)
canvas3.config(width="70",height="15",bg="#C4C4C4")
canvas3.place(x=80, y=150)

img3 = Image.open("R3.png")
img3 = img3.resize((98,152), Image.ANTIALIAS)
img3 =  ImageTk.PhotoImage(img3)
Cimg3 = Label(frame6, image = img3) 
Cimg3.config(width="98",height="152",bg="#C4C4C4")
Cimg3.place(x=400, y= 250)

rec2 = Label(frame6,bg="#C4C4C4")
rec2.config(width="70",height="18")
rec2.place(x=710, y=150)

img4 = Image.open("R4.png")
img4 = img4.resize((68,102), Image.ANTIALIAS)
img4 =  ImageTk.PhotoImage(img4)
Cimg4 = Label(frame6, image = img4) 
Cimg4.config(width="68",height="102",bg="#C4C4C4")
Cimg4.place(x=1100, y= 300)

btnCargarVideo = Button(frame6, text="Cargar Video")
btnCargarVideo.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = cargarVideo_Manual)
btnCargarVideo.place(x=470, y=500)

btnBack2 = Button(frame6, text="Back")
btnBack2.config(width="8", height="1",font=("Helvetica", 12), bg="#3F3F3F", foreground="white",command = back_Manual)
btnBack2.place(x=80, y=50)
##FIN FRAME6##

##FRAME 7##
frame7 = Frame()
frame7.config(width = "1440", height="1024", bg="#242424")
#frame7.pack()

TituloAutomatico = Label(frame7,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

rec1 = Label(frame7,bg="#C4C4C4")
rec1.config(width="70",height="18")
rec1.place(x=80, y=150)
canvas4 = Label(frame7)
canvas4.config(width="70",height="15")
canvas4.place(x=80, y=150)

rec2 = Label(frame7,bg="#C4C4C4")
rec2.config(width="70",height="18")
rec2.place(x=710, y=150)

img5 = Image.open("R4.png")
img5 = img5.resize((68,102), Image.ANTIALIAS)
img5 =  ImageTk.PhotoImage(img5)
Cimg5 = Label(frame7, image = img5) 
Cimg5.config(width="68",height="102",bg="#C4C4C4")
Cimg5.place(x=1100, y= 300)

contNado = Label(frame7, text = "Tiempo nadando: ",bg="#C4C4C4",font=("Helvetica", 15))
contNado.place(x=750, y=200)
contadorNado = Label(frame7,bg="#C4C4C4",font=("Helvetica", 15),textvariable=Manual_nadoS)
contadorNado.place(x=950, y=200)
contQuieta = Label(frame7, text = "Tiempo Quieta: ",bg="#C4C4C4",font=("Helvetica", 15))
contQuieta.place(x=750, y=250)
contadorQuieta = Label(frame7,bg="#C4C4C4",font=("Helvetica", 15),textvariable=Manual_quietaS)
contadorQuieta.place(x=950, y=250)

btnIniciar = Button(frame7, text="Iniciar")
btnIniciar.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = contador)
btnIniciar.place(x=470, y=500)

btnParar = Button(frame7, text="Parar")
btnParar.config(width="10", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = parar_Manual)
btnParar.place(x=1085, y=500)
##FIN FRAME7##

##FRAME8 ##
frame8 = Frame()
frame8.config(width = "1440", height="1024", bg="#242424")
#frame8.pack()

TituloAutomatico = Label(frame8,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

rec1 = Label(frame8,bg="#C4C4C4")
rec1.config(width="70",height="18")
rec1.place(x=80, y=150)
canvas5 = Label(frame8)
canvas5.config(width="70",height="15",bg="#C4C4C4")
canvas5.place(x=80, y=150)

rec2 = Label(frame8,bg="#C4C4C4")
rec2.config(width="70",height="18")
rec2.place(x=710, y=150)

contNado = Label(frame8, text = "Tiempo nadando: ",bg="#C4C4C4",font=("Helvetica", 15))
contNado.place(x=750, y=200)
contadorNado = Label(frame8,bg="#C4C4C4",font=("Helvetica", 15),textvariable=Manual_nadoS)
contadorNado.place(x=950, y=200)
contQuieta = Label(frame8, text = "Tiempo Quieta: ",bg="#C4C4C4",font=("Helvetica", 15))
contQuieta.place(x=750, y=250)
contadorQuieta = Label(frame8,bg="#C4C4C4",font=("Helvetica", 15),textvariable=Manual_quietaS)
contadorQuieta.place(x=950, y=250)
porNado = Label(frame8, text = "Porcentaje Nadando: ",bg="#C4C4C4",font=("Helvetica", 15))
porNado.place(x=750, y=300)
porcentajeNado = Label(frame8,bg="#C4C4C4",font=("Helvetica", 15),textvariable = Manual_Porcentaje_NadoS)
porcentajeNado.place(x=950, y=300)
porcQuieta = Label(frame8, text = "Porcentaje Quieta: ",bg="#C4C4C4",font=("Helvetica", 15))
porcQuieta.place(x=750, y=350)
porcentajeQuieta = Label(frame8,bg="#C4C4C4",font=("Helvetica", 15),textvariable = Manual_Porcentaje_QuietaS)
porcentajeQuieta.place(x=950, y=350)


btnParar = Button(frame8, text="Exportar Datos")
btnParar.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = exportar_Manual)
btnParar.place(x=470, y=500)

btnToInit = Button(frame8, text="Inicio")
btnToInit.config(width="10", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = to_Init_Manual)
btnToInit.place(x=1085, y=500)
##FIN FRAME8##

raiz.mainloop()
