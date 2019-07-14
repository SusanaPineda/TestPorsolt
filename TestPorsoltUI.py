###################################
# FRAME1 -> Pantalla principal con las dos opciones
# FRAME2 -> Pantalla cargar video 

### FRAMES TEST AUTOMATICO ###
# FRAME3 -> Pantalla seleccionar 
# FRAME4 -> Pantalla reproduccion Test Automatico
# FRAME5 -> Pantalla resultados y exportar

### FRAMES TEST MANUAL ###
# FRAME6 -> Pantalla seleccionar 
# FRAME7 -> Pantalla reproduccion Test Manual
# FRAME8 -> Pantalla resultados y exportar
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


### VARIABLES SELECCION AUTOMATICO-MANUAL ###
boolAutomatico = False
boolManual = False

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
Manual_video_name = ""
mod_manual = [0]
seleccion_Manual = False
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
    global boolAutomatico
    boolAutomatico = True
    frame1.pack_forget()
    frame2.pack()

def cargarVideo():
    global boolAutomatico, boolManual
    if boolAutomatico:
        frame2.pack_forget()
        frame3.pack()
        selectVideo_Automatico()
    if boolManual:
        frame2.pack_forget()
        frame6.pack()
        selectVideo_Manual()

def back():
    global boolAutomatico, boolManual
    boolAutomatico = False
    boolManual = False
    frame2.pack_forget()
    frame1.pack()

def selectVideo_Automatico():
    global Automatico_video_name
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4","*.mp4"),("MTS","*.MTS"),("all files","*.*")))
    print(raiz.filename)
    url = raiz.filename
    Automatico_video_name = url 
    stream_Automatico(canvas)


def stream_Automatico(canvas):
    global Automatico_video_name
    thread = threading.Thread(name= "hilo_testAutomatico" ,target=exec, args=(canvas,Automatico_video_name))  
    thread.daemon = 1
    thread.start()

def seleccionar():
    global waitKey_fps, seleccion, boolAutomatico, boolManual
    waitKey_fps = 0
    seleccion = True
    if boolAutomatico:
        frame3.pack_forget()
        frame4.pack()
    if boolManual:
        frame6.pack_forget()
        frame7.pack()

def reiniciar_Automatico():
    global  mod, Automatico_nado, Automatico_quieta, Vector_Nado_Automatico, Vector_Quieta_Automatico
    mod = [0]
    Automatico_nado = 0
    Automatico_quieta = 0
    Vector_Nado_Automatico = [0]
    Vector_Quieta_Automatico = [0]

def exec(canvas1, video ):
    global mod, Automatico_nado, Automatico_quieta, Vector_Nado_Automatico, Vector_Quieta_Automatico, stopAutomatico,seleccion,waitKey_fps

    ### REAJUSTE DEL FRAME4 ###
    frame4.config(width = "2100", height="1300", bg="#242424")
    TituloF4 = Label(frame4,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
    TituloF4.place(x=530, y=55)
    
    canvas = Label(frame4)
    canvas.config(width="70",height="15", bg="#242424")
    canvas.place(x=300, y=180)

    IndicadorTxt = Label(frame4, text="Nadando", bg="#242424", foreground="white",font=("Helvetica", 12))
    IndicadorTxt.place(x=580,y=450)

    Indicador = Label(frame4, bg="#3847CD")
    Indicador.config(width="2", height="1")
    Indicador.place(x=750,y=450)

    contNado2 = Label(frame4, text = "Tiempo Nado: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    contNado2.place(x=580, y=500)
    contadorNado2 = Label(frame4,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Automatico_nadoS)
    contadorNado2.place(x=750, y=500)
    contQuieta2 = Label(frame4, text = "Tiempo Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    contQuieta2.place(x=580, y=550)
    contadorQuieta2 = Label(frame4,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Automatico_quietaS)
    contadorQuieta2.place(x=750, y=550)

    btnReiniciar = Button(frame4, text="Reiniciar")
    btnReiniciar.config(width="17", height="2",font=("Helvetica", 15), bg="#3F3F3F", foreground="white", command = reiniciar_Automatico)
    btnReiniciar.place(x=120, y=550)
    
    btnParar = Button(frame4, text="Parar")
    btnParar.config(width="17", height="2",font=("Helvetica", 15), bg="#3F3F3F", foreground="white", command = parar_Automatico)
    btnParar.place(x=1000, y=550)
    
    
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
    m = cap.get(cv2.CAP_PROP_FPS)
    print("fps: "+str(m))
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
                    if(contadorFPS == 5):
                        
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
                               
                                Automatico_nado = round(Automatico_nado + 0.2 ,2)
                                totContNado = round(totContNado + 0.2,2)
                                Automatico_nadoS.set(str(Automatico_nado)+" s")
                                IndicadorTxt.config (text = "Nadando")
                                Indicador.config(bg = "#3847CD")
                            elif(quietaBool):
                               
                                CNado = CNado-1
                                if(CNado > 0):
                                    
                                    Automatico_quieta = round(Automatico_quieta + 0.2,2)
                                    totContQuieta = round(totContQuieta + 0.2,2)
                                elif(CNado == 0):
                                    
                                    CNado = 4
                                    CQuieta = 4
                                    Vector_Quieta_Automatico.append(totContQuieta)
                                    totContQuieta = 0
                                    quietaBool = False
                                    nadandoBool = True
                    
                        else:
                            if(quietaBool):
                               
                                Automatico_quieta = round(Automatico_quieta + 0.2,2)
                                totContQuieta = round(totContQuieta + 0.2,2)
                                Automatico_quietaS.set(str(Automatico_quieta)+ " s")
                                IndicadorTxt.config(text = "Quieta")
                                Indicador.config(bg = "#6B74CA")
                            elif(nadandoBool):
                                    CQuieta = CQuieta - 1
                                    if(CQuieta>0):
                                        Automatico_nado = round(Automatico_nado + 0.2,2)
                                        totContNado = round(totContNado + 0.2,2)
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
                    canvas.config(image=frame_image2)
                    canvas.config(width="737",height="300")
                    canvas.place(x=300, y=130)
                    canvas.image = frame_image2
                else:
                    ph = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame_video,cv2.COLOR_BGR2RGB),"RGB").resize((600,300), Image.ANTIALIAS))
                    canvas1.config(image=ph)
                    canvas1.config(width="737",height="300")
                    canvas1.place(x=300, y=130)
                    canvas1.image = ph
                
            else:
                MutexAutomatico.release()
                cap.release()
                cv2.destroyAllWindows()
                canvas1.place_forget()
                canvas.place_forget()
                
    canvas.place_forget()
    canvas1.place_forget()
    cap.release()
    cv2.destroyAllWindows()
            

def parar_Automatico():
    global Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta,stopAutomatico

    AutomaticoTotal = Automatico_nado + Automatico_quieta
    Porcentaje_Automatico_Nado = Automatico_nado / AutomaticoTotal * 100
    Porcentaje_Automatico_Quieta = Automatico_quieta / AutomaticoTotal * 100
    Automatico_Porcentaje_NadoS.set(str(round(Porcentaje_Automatico_Nado))+" %")
    Automatico_Porcentaje_QuietaS.set(str(round(Porcentaje_Automatico_Quieta))+" %")
    

    MutexAutomatico.acquire()
    stopAutomatico = False
    MutexAutomatico.release()
    

    frame4.pack_forget()
    ### Reajuste frame 5 ###
    #frame5 = Frame()
    frame5.config(width = "2100", height="1300", bg="#242424")
    frame5.pack()
    
    TituloAutomatico = Label(frame5,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
    TituloAutomatico.place(x=480, y=55)

    contNado = Label(frame5, text = "Tiempo Nado: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    contNado.place(x=550, y=200)
    contadorNado = Label(frame5,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Automatico_nadoS)
    contadorNado.place(x=720, y=200)
    contQuieta = Label(frame5, text = "Tiempo Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    contQuieta.place(x=550, y=250)
    contadorQuieta = Label(frame5,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Automatico_quietaS)
    contadorQuieta.place(x=720, y=250)
    porNado = Label(frame5, text = "Porcentaje Nado: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    porNado.place(x=550, y=300)
    porcentajeNado = Label(frame5,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable = Automatico_Porcentaje_NadoS)
    porcentajeNado.place(x=720, y=300)
    porcQuieta = Label(frame5, text = "Porcentaje Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 12))
    porcQuieta.place(x=550, y=350)
    porcentajerQuieta = Label(frame5,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable = Automatico_Porcentaje_QuietaS)
    porcentajerQuieta.place(x=720, y=350)
    
    btnExportar = Button(frame5, text="Exportar Datos")
    btnExportar.config(width="30", height="2",font=("Helvetica", 12), bg="#3F3F3F", foreground="white",command = exportar_Automatico)
    btnExportar.place(x=500, y=500)
    
    btnToInit2 = Button(frame5, text="Inicio")
    btnToInit2.config(width="10", height="2",font=("Helvetica", 12), bg="#3F3F3F", foreground="white", command = to_Init_Automatico)
    btnToInit2.place(x=1000, y=500)
    
    ### Fin Reajuste frame 5 ###

def exportar_Automatico():
    global Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta,Vector_Nado_Automatico, Vector_Quieta_Automatico
    raiz.filename = filedialog.asksaveasfilename(initialdir = "/", title = "Select directory",filetypes = (("xlsx","*.xlsx"),("all files","*.*")))
    url = raiz.filename+".xlsx"

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
    global Automatico_video_name, stopAutomatico, mod, Automatico_nado, Automatico_quieta, Porcentaje_Automatico_Nado, Porcentaje_Automatico_Quieta, Vector_Nado_Automatico, Vector_Quieta_Automatico, boolAutomatico,seleccion
    Automatico_video_name = ""
    stopAutomatico = True
    mod = [0]
    Automatico_nado = 0
    Automatico_quieta = 0
    Porcentaje_Automatico_Nado = 0
    Porcentaje_Automatico_Quieta = 0
    Vector_Nado_Automatico = [0]
    Vector_Quieta_Automatico = [0]
    boolAutomatico = False
    seleccion = False

    Automatico_nadoS.set(str(Automatico_nado) +" s")
    Automatico_quietaS.set(str(Automatico_quieta)+" s")
    Automatico_Porcentaje_NadoS.set(str(Porcentaje_Automatico_Nado)+" %")
    Automatico_Porcentaje_QuietaS.set(str(Porcentaje_Automatico_Quieta)+" %")

    frame5.pack_forget()
    frame1.pack()
   

def manual():
    global boolManual
    boolManual = True
    frame1.pack_forget()
    frame2.pack()


def contador():
    global Manual_inicializado, Manual_nadando, Manual_quietaB, Manual_nado, Manual_quieta, Manual_cInit, Manual_cFin, Vector_Nado_Manual, Vector_Quieta_Manual

    if(Manual_inicializado == False):
        btnIniciar['text'] = 'Quieta'
        Manual_inicializado = True
        Manual_nadando = True
        Manual_cInit = time()
        
        
    elif(Manual_nadando == True):
        btnIniciar['text'] = 'Nadando'
        Manual_nadando = False
        Manual_quietaB = True
        Manual_cFin = time() - Manual_cInit
        Manual_nado = Manual_nado + Manual_cFin
        Vector_Nado_Manual.append(round(Manual_cFin,2))
        Manual_cInit = time()
       
        Manual_nadoS.set(str(round(Manual_nado,2))+" s")
        

    elif(Manual_quietaB == True):
        btnIniciar['text'] = 'Quieta'
        Manual_nadando = True
        Manual_quietaB = False
        Manual_cFin = time() - Manual_cInit
        Manual_quieta = Manual_quieta + Manual_cFin
        Vector_Quieta_Manual.append(round(Manual_cFin,2))
        Manual_cInit = time()
        Manual_quietaS.set(str(round(Manual_quieta,2))+" s")

def parar_Manual():
    global Manual_nado, Manual_quieta, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta,stopManual 
    frame7.pack_forget()
    Manual_Total = Manual_nado + Manual_quieta
    Porcentaje_Manual_Nado = Manual_nado/Manual_Total*100
    Porcentaje_Manual_Quieta = Manual_quieta/Manual_Total*100
    Manual_Porcentaje_NadoS.set(str(round(Porcentaje_Manual_Nado))+ " %")
    Manual_Porcentaje_QuietaS.set(str(round(Porcentaje_Manual_Quieta))+" %")
    MutexManual.acquire()
    stopManual = False
    MutexManual.release()
    frame8.pack()
    
def exportar_Manual():
    global Manual_nado, Manual_quieta, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta,Vector_Nado_Manual, Vector_Quieta_Manual

    raiz.filename = filedialog.asksaveasfilename(initialdir = "/", title = "Select directory",filetypes = (("xlsx","*.xlsx"),("all files","*.*")))
    url = raiz.filename+".xlsx"

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

def selectVideo_Manual():
    global Manual_video_name
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4","*.mp4"),("MTS","*.MTS"),("all files","*.*")))
    print(raiz.filename)
    url = raiz.filename
    Manual_video_name = url 
    stream(canvas3)


def reiniciar_Manual():
    global  mod_manual, Manual_nado, Manual_quieta, Vector_Nado_Manual, Vector_Quieta_Manual
    mod_manual = [0]
    Manual_nado = 0
    Manual_quieta = 0
    Vector_Nado_Manual = [0]
    Vector_Quieta_Manual = [0]

def stream(canvas):
    global Manual_video_name
    thread = threading.Thread(name= "hilo_testManual" ,target=exec_manual, args=(Manual_video_name,canvas))  
    thread.daemon = 1
    thread.start()

def exec_manual(video,canvas1):
    global mod_manual, Manual_nado, Manual_quieta, Vector_Nado_Manual, Vector_Quieta_Manual, stopManual,seleccion,waitKey_fps


    ### FRAME 7 ###
    frame7.config(width = "1440", height="1024", bg="#242424")

    TituloAutomatico = Label(frame7,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
    TituloAutomatico.place(x=530, y=55)

    canvas4 = Label(frame7)
    canvas4.config(width="70",height="15",bg="#242424")
    canvas4.place(x=80, y=150)

    contNado = Label(frame7, text = "Tiempo Nado: ",bg="#242424", foreground="white",font=("Helvetica", 15))
    contNado.place(x=580, y=450)
    contadorNado = Label(frame7,bg="#242424", foreground="white",font=("Helvetica", 15),textvariable=Manual_nadoS)
    contadorNado.place(x=750, y=450)
    contQuieta = Label(frame7, text = "Tiempo Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 15))
    contQuieta.place(x=580, y=500)
    contadorQuieta = Label(frame7,bg="#242424", foreground="white",font=("Helvetica", 15),textvariable=Manual_quietaS)
    contadorQuieta.place(x=750, y=500)

    btnParar = Button(frame7, text="Parar")
    btnParar.config(width="10", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = parar_Manual)
    btnParar.place(x=1000, y=550)

    btnReiniciarF7 = Button(frame7, text="Parar")
    btnReiniciarF7.config(width="10", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = reiniciar_Manual)
    btnReiniciarF7.place(x=220, y=550)
    ### FIN FRAME 7 ###

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
    ####Fin Variables Locales ####

    cap = cv2.VideoCapture(video)
    m = cap.get(cv2.CAP_PROP_FPS)
    
    print("fps: "+str(m))
    while(cap.isOpened()):
        MutexManual.acquire()
        
        cv2.waitKey(waitKey_fps) & 0xFF
        posVideo = cap.get(cv2.CAP_PROP_POS_MSEC)
        print("fps: "+str(round(posVideo/1000,2)))
        if stopManual == True:
            MutexManual.release()
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
                    #btnSeleccionar.place_forget()
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
                    if(contadorFPS == 5):
                        
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
                        mod_manual.append(velTotal)

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
                    canvas4.config(image=frame_image2)
                    canvas4.config(width="737",height="300")
                    canvas4.place(x=300, y=130)
                    canvas4.image = frame_image2
                else:
                    ph = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame_video,cv2.COLOR_BGR2RGB),"RGB").resize((600,300), Image.ANTIALIAS))
                    canvas1.config(image=ph)
                    canvas1.config(width="737",height="300")
                    canvas1.place(x=300, y=130)
                    canvas1.image = ph
                
            else:
                MutexManual.release()
                cap.release()
                cv2.destroyAllWindows()
                

    cap.release()
    cv2.destroyAllWindows()

def to_Init_Manual():
    global Manual_video_name, seleccion,mod_manual, Manual_nado, Manual_quieta, Manual_cInit, Manual_cFin, Manual_inicializado, Manual_nadando, Manual_quietaB, stopManual, Porcentaje_Manual_Nado, Porcentaje_Manual_Quieta, Vector_Nado_Manual, Vector_Quieta_Manual,boolManual
    
    #limpar variables#
    Manual_video_name = ""
    seleccion = False
    Manual_nado = 0
    Manual_quieta = 0
    Manual_cInit = 0
    Manual_cFin = 0
    mod_manual = [0]
    Manual_inicializado = False
    Manual_nadando = False
    Manual_quietaB = False
    stopManual = True
    Porcentaje_Manual_Nado = 0
    Porcentaje_Manual_Quieta = 0
    Vector_Nado_Manual.clear()
    Vector_Quieta_Manual.clear()
    boolManual = False

    Manual_nadoS.set(str(Manual_nado)+" s")
    Manual_quietaS.set(str(Manual_quieta)+" s")
    Manual_Porcentaje_NadoS.set(str(Porcentaje_Manual_Nado)+" %")
    Manual_Porcentaje_QuietaS.set(str(Porcentaje_Manual_Quieta)+" %")

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

Titulo = Label(frame2,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
Titulo.place(x=500, y=50)

img3 = Image.open("R1.png")
img3 = img3.resize((242,331), Image.ANTIALIAS)
img3 =  ImageTk.PhotoImage(img3)
Cimg3 = Label(frame2, image = img3) 
Cimg3.config(width="242",height="331",bg="#242424")
Cimg3.place(x=1000, y= 70)

img4 = Image.open("R2.png")
img4 = img4.resize((279,230), Image.ANTIALIAS)
img4 =  ImageTk.PhotoImage(img4)
Cimg4 = Label(frame2, image = img4) 
Cimg4.config(width="279",height="230",bg="#242424")
Cimg4.place(x=70, y= 400)

btnCargarVideo = Button(frame2, text="Cargar Video")
btnCargarVideo.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = cargarVideo)
btnCargarVideo.place(x=500, y=350)

btnBack = Button(frame2, text="<")
btnBack.config(width="8", height="1",font=("Helvetica", 12), bg="#242424", foreground="white",command = back)
btnBack.place(x=80, y=50)
##FIN FRAME2##

##FRAME 3##
frame3 = Frame()
frame3.config(width = "1440", height="1024", bg="#242424")
#frame3.pack()

TituloF3 = Label(frame3,text="Test Automatico de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloF3.place(x=500, y=50)

canvas = Label(frame3)
canvas.config(width="80",height="35", bg="#242424")
canvas.place(x=1000, y=100)

Instrucciones = Label(frame3,text="Selecciona la marca del sujeto y presiona enter.",bg="#242424",foreground="white",font=("Helvetica", 12))
Instrucciones.place(x=500, y=520)

btnSeleccionarF3 = Button(frame3, text="Seleccionar")
btnSeleccionarF3.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white",command = seleccionar)
btnSeleccionarF3.place(x=500, y=600)
##FIN FRAME3##

##FRAME 4 implementado en exec()##
frame4 = Frame()
frame4.config(width = "1440", height="1024", bg="#242424")
#frame4.pack()

canvas1 = Label(frame4)
canvas1.config(width="70",height="15",bg="#242424")
canvas1.place(x=80, y=150)

##FIN FRAME4##

##FRAME 5 implementado en parar automatico##
frame5 = Frame()
##FIN FRAME5##

##FRAME6##
frame6 = Frame()
frame6.config(width = "1440", height="1024", bg="#242424")
#frame6.pack()

TituloAutomatico = Label(frame6,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=500, y=50)

canvas3 = Label(frame6)
canvas3.config(width="80",height="35",bg="#242424")
canvas3.place(x=1000, y=100)

Instrucciones = Label(frame6,text="Selecciona la marca del sujeto y presiona enter.",bg="#242424",foreground="white",font=("Helvetica", 12))
Instrucciones.place(x=500, y=520)

btnSeleccionarF6 = Button(frame6, text="Seleccionar")
btnSeleccionarF6.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = seleccionar)
btnSeleccionarF6.place(x=500, y=600)

##FIN FRAME6##

##FRAME 7 implementado en exec_manual##
frame7 = Frame()
btnIniciar = Button(frame7, text="Iniciar")
btnIniciar.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = contador)
btnIniciar.place(x=500, y=550)

##FIN FRAME7##

##FRAME8 ##
frame8 = Frame()
frame8.config(width = "1440", height="1024", bg="#242424")
#frame8.pack()

TituloAutomatico = Label(frame8,text="Test Manual de Porsolt",bg="#242424",foreground="white",font=("Helvetica", 20))
TituloAutomatico.place(x=480, y=55)

contNado = Label(frame8, text = "Tiempo Nado: ",bg="#242424", foreground="white",font=("Helvetica", 12))
contNado.place(x=550, y=200)
contadorNado = Label(frame8,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Manual_nadoS)
contadorNado.place(x=720, y=200)
contQuieta = Label(frame8, text = "Tiempo Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 12))
contQuieta.place(x=550, y=250)
contadorQuieta = Label(frame8,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable=Manual_quietaS)
contadorQuieta.place(x=720, y=250)
porNado = Label(frame8, text = "Porcentaje Nado: ",bg="#242424", foreground="white",font=("Helvetica", 12))
porNado.place(x=550, y=300)
porcentajeNado = Label(frame8,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable = Manual_Porcentaje_NadoS)
porcentajeNado.place(x=720, y=300)
porcQuieta = Label(frame8, text = "Porcentaje Reposo: ",bg="#242424", foreground="white",font=("Helvetica", 12))
porcQuieta.place(x=550, y=350)
porcentajeQuieta = Label(frame8,bg="#242424", foreground="white",font=("Helvetica", 12),textvariable = Manual_Porcentaje_QuietaS)
porcentajeQuieta.place(x=720, y=350)


btnExportarF8 = Button(frame8, text="Exportar Datos")
btnExportarF8.config(width="30", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = exportar_Manual)
btnExportarF8.place(x=500, y=500)

btnToInit = Button(frame8, text="Inicio")
btnToInit.config(width="10", height="2",font=("Helvetica", 14), bg="#3F3F3F", foreground="white", command = to_Init_Manual)
btnToInit.place(x=1000, y=500)
##FIN FRAME8##

raiz.mainloop()
