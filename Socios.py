from tkinter import *
import tkinter as tk
import os
from tkinter import ttk,messagebox,filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk

indexcbo =0
Nro_Socio =0 
dir= os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(dir,'socio.txt')
ruta_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)),'temp.txt')

#-------------------------------------------------------------------------------------------------------------
#Funciones
#-------------------------------------------------------------------------------------------------------------
def agregar_socios(): 
    
         # Funcion para pasar los text a la grilla
        #Nro = entry_nro_Socio.get()
    nrodoc= entry_documento.get()
    nombre =entry_nombre.get()
    domicilio=entry_domicilio.get()
    telefono=entry_telefono.get()
    mail=entry_mail.get()
    sexo=cbo_sexo.get()
    fecha=label_fecha_nac._calendar.get_date()

    if solo_numeros_entry(entry_documento) == False or solo_numeros_entry(entry_telefono) == False:
        messagebox.showwarning("Letras en numeros", "El documento o el Nro de telefono del Socio debe ser un numero")
    else: 
        #PASA LOS DATOS DE LAS CAJAS A LA GRILLA
        if (nrodoc == "") or (nombre == "") or (domicilio =="") or (telefono ==""):    
            messagebox.showwarning("Hay datos necesarios en blanco", "No se puede agregar un socio sin nombre, domicilio o telefono")
            return
        else:
            
            try:
                global Nro_Socio
                if Existe_Socio(nrodoc) == True:
                    respuesta = messagebox.askyesno("El Nro de Documento ya existe y esta asociado a un Socio","¿Desea Modificar los datos el Socio?")
                    if respuesta:
                        archivo = open(ruta_archivo, "r")                        
                        arch_temp = open(ruta_temp, "w")

                        for linea in archivo:
                            tmp = linea.split(',')
                            if tmp[1] == nrodoc:
                                arch_temp.write(f"{tmp[0]},{nrodoc},{nombre},{domicilio},{telefono},{mail},{fecha},{sexo}\n")
                            else:
                                arch_temp.write("".join(linea))

                        archivo.close()
                        arch_temp.close()
                        os.remove(ruta_archivo)
                        os.rename(ruta_temp, ruta_archivo)

                else:

                    Nro_Socio +=1
                    tree.insert("",tk.END, values=(Nro_Socio,nrodoc,nombre,domicilio,telefono,mail,sexo,fecha))
                    with open(ruta_archivo, "a") as archivo:                
                        archivo.write(f"{Nro_Socio},{nrodoc},{nombre},{domicilio},{telefono},{mail},{fecha},{sexo}\n")
                                    
                limpiar_text()
                tree.delete(*tree.get_children())
                leer_socios()
                messagebox.showinfo( "Socio Guardado","Modificacion efecuada correctamente")
                    
            except Exception as e:
                messagebox.showwarning("Se Produjo un Error - ", str(e))
            finally:
                archivo.close() 
    
#Funcion para vaicar los text y dejarlos limpios para volver a cargarlos
def limpiar_text():
    #Para limpiar los text
    entry_nro_Socio.config(state='normal')
    entry_nro_Socio.delete(0,tk.END)
    entry_nombre.delete(0,tk.END)
    entry_documento.delete(0,tk.END)
    entry_mail.delete(0,tk.END)
    entry_telefono.delete(0,tk.END)
    entry_domicilio.delete(0,tk.END)
    cbo_sexo.set("")
    entry_buscar.delete(0,tk.END)
    entry_documento.focus()
    indexcbo =0
    #self.label_fecha_nac
    
#Verifica que se ingresen datos necesarios
def validacion(documento, nombre,domicilio,telefono, mail):
    if not (documento and nombre and domicilio and telefono and mail):
        return False
    else:
        return True

#PARA PASAR DE LA GRILLA A LOS TEXT
def editar_socios():        
    limpiar_text()         #Funcion para borrar el contenido de los textbox
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Editar Socios","No se selecciono ningun socio de la grilla para editar")
        return
    
    item_id= tree.item(seleccion)["text"]
    item =tree.item(seleccion)["values"]
    entry_nro_Socio.insert(0, item[0])
    entry_nro_Socio.config(state='disabled')
    entry_documento.insert(0, item[1])
    entry_nombre.insert(0,item[2])
    entry_domicilio.insert(0,item[3])
    entry_telefono.insert(0,item[4])
    entry_mail.insert(0,item[5])
    #label_fecha_nac.set_date(item[7])
    indexcbo = item[6]
    if indexcbo == 'M':
        cbo_sexo.current(0)
    else:
        cbo_sexo.current(1)

#Doble click en la grilla para que se cierre la ventana y los datos
#pasen al formulario para ser editados
def DobleClickTree(event):
    editar_socios()

def leer_socios():

    #dir= os.path.dirname(os.path.abspath(__file__))
    #ruta_archivo = os.path.join(dir,'socio.txt')
    if os.path.exists(ruta_archivo):
        datos=[]
        with open(ruta_archivo, "r") as archivo:
        # Lee el archivo línea por línea
            for linea in archivo:
                # Inserta cada línea en el Treeview
                partes = linea.strip().split(',')
                tree.insert("", tk.END, values=(partes[0],partes[1],partes[2],partes[3],partes[4],partes[5],partes[7],partes[6]))
                global Nro_Socio
                Nro_Socio =int(partes[0])   #Guardo el Ultimo Nro

def abrir_imagen(event):
    ruta_imagen = filedialog.askopenfilename(
        initialdir=".", # Directorio inicial
        title="Seleccionar imagen",
        filetypes=(("Archivos de imagen", "*.jpg *.png *.gif"), ("Todos los archivos", "*.*"))
    )

    if ruta_imagen:
        # Cargar y mostrar la imagen
        img = Image.open(ruta_imagen)
        # Redimensionar la imagen
        img = img.resize((270, 200), Image.Resampling.LANCZOS) 
        img_tk = ImageTk.PhotoImage(img)
        # Mostrar la imagen en el label
        logo_label.config(image=img_tk)
        logo_label.image = img_tk 

def solo_numeros_entry(entry):
    res = entry.get()
    #aquí compruebas que es un número
    if res.isdigit():
        return True
    else:
        entry.delete(0, END)
        entry.focus()
        return False

def buscar_socio ():
    dato_a_buscar = entry_buscar.get()
    for iid in tree.get_children():
        valores = tree.item(iid, 'values')
        if dato_a_buscar in valores:
        # El dato fue encontrado
            tree.selection_set(iid)
            tree.focus(iid)
            return True

def Existe_Socio(dni):
    encontrado = False
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r") as archivo:
            for linea in archivo:
                if dni in linea:
                    encontrado = True                
                    break
            archivo.close()

        return encontrado

#ABRE UNA VENTANA Y MUESTRA LAS FUNCIONALIDADES DEL SISTEMA EN UN LABEL
def abrir_ventana_secundaria():
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("Ventana de Informacion de uso del Sistema")
    #ventana_secundaria.geometry("300x500")
    ventana_secundaria.state('zoomed')
    # Puedes agregar widgets a la ventana secundaria aquí
    
    texttt = tk.StringVar()
    texttt.set("Cajas de texto, N° de Documento,Nombre, Domicilio y Telefono, son datos obligatorios, si o si hay que ingresarlos o no se guardaran.\n "
"La caja telefono, solo aceptara numeros, no letras ni caracteres especiales. Ej: SI 36245896666 NO (3624-895623)\n"
"En la grilla se muestran los datos de los socios cargados. Los mismos se guardan en un txt en la ruta donde se ejecuta el script.\n"
"Si existen datos en la grilla, al hacer doble click en alguno de los registros, se cargan en las cajas de texto para modificar \n"
"\nImagen: se adjunta una archivo png llamdos socios. La misma debe estar en el directorio donde se ejecuta el script. \n"
"Al hacer doble click sobre la imagen, la misma se puede cambiar. Se abre el cuadro de dialogo para selecionar una imagen. Al cerrar \n"
"el programa la misma se borra.\n"
"\nBotones: \n"
"\nBoton Guardar: Se confirman los cambios efectuados en las cajas. \n"
"Si existe el Socio, efectua un aviso que ya existe \n" 
"un socio con el documento ingresado \n"
"Si confirma, se reemplazan los datos existentes por \n"
"los ingresados en las cajas de texto. \n"
"Si no existe el documento. Lo agrega al final. \n"
"\nBoton Limpiar: Deja las cajas de texto en blanco, disponibles para ingresar los datos.\n"
"\nBoton Modificar: Si existen datos en la grilla, al hacer doble click  en alguno de los registros,\n"
"se cargan en las cajas de texto para modificar \n"
"\nBoton Buscar: Si se ingresa algun DNI en la caja de texto 'Buscar DNI' efectua la busqueda del dni \n"
"ingresado y se posiciona en el registro encontrado \n"
"\nBoton Cerrar: Termina la Ejecucion.\n")
    tk.Label(ventana_secundaria, textvariable=texttt,font="sans 14 bold",justify='left').pack(pady=10)
#-------------------------------------------------------------------------------------------------------------
#VENTANA
#-------------------------------------------------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Gestor de Contactos - Informatorio Chaco - GRUPO 1")
ventana.geometry("1100x650+120+20")
ventana.config(bg="#e6f2ff")    

frame1= tk.Frame(ventana,bg="#dddddd",highlightbackground="gray",highlightthickness=1)
frame1.pack()
frame1.place(x=0,y=0,width=1100, height=100)

title =tk.Label(ventana,text="SOCIOS",bg="#dddddd",font="sans 30 bold", anchor="center")
title.pack()
title.place(x=5,y=0,width=1090,height=90)
#-----------------------------------------------------------------------------------------------------
#           EL CUERPO DE LA VENTANTA - EL OTRO CONTENEDOR Y LOS LABELS Y LAS CAJAS DE TEXTO        
frame2= tk.Frame(ventana, bg="#AB74F3",highlightbackground="gray",highlightthickness=2)
frame2.place(x=0,y=100, width=1100, height=550)

lblframe = LabelFrame(frame2,text="Informacion de los Socios", bg="#AB74F3",font="sans 16 bold")
lblframe.place(x=10,y=10,width=1070,height=520)

#NRO SOCIO
label_nro_Socio = tk.Label(lblframe,text="Nro de Socio: ",bg="#AB74F3",font="sans 12 bold")
label_nro_Socio.place(x=10,y=5)
#nro_Socio = tk.StringVar()                     # para almacenar el nro de socio
#entry_nro_Socio = tk.Entry(lblframe,textvariable=nro_Socio,state="readonly",font="sans 12 bold")
entry_nro_Socio = tk.Entry(lblframe,state='disable',font="sans 12 bold")
entry_nro_Socio.place(x=130,y=5,width=100)
#NRO DOCUMENTO
label_nrodoc =tk.Label(lblframe,text="Documento: ",bg="#AB74F3",font="sans 12 bold")
label_nrodoc.place(x=10,y=35)
entry_documento = tk.Entry(lblframe,font="sans 12 bold")
entry_documento.place(x=130,y=35,width=100)
entry_documento.focus_set()
#NOMBRE
label_nombre =tk.Label(lblframe,text="Nombre: ",bg="#AB74F3",font="sans 12 bold")
label_nombre.place(x=10,y=65)
entry_nombre = tk.Entry(lblframe,font="sans 12 bold")
entry_nombre.place(x=130,y=65,width=280)
entry_nombre.focus_set()
#DOMICILIO
label_domicilio =tk.Label(lblframe,text="Domicilio: ",bg="#AB74F3",font="sans 12 bold")
label_domicilio.place(x=10,y=95)
entry_domicilio = tk.Entry(lblframe,font="sans 12 bold")
entry_domicilio.place(x=130,y=95,width=280)
#FECHA NACIMIENTO
label_fecha_nac =tk.Label(lblframe,text="Fe Nacimiento: ",bg="#AB74F3",font="sans 12 bold")
label_fecha_nac.place(x=10,y=125)
#label_fecha_nac = tk.Entry(lblframe,font="sans 12 bold")
label_fecha_nac = DateEntry(lblframe,font="sans 12 bold",date_pattern='dd/mm/yyyy') #Que muestre dia/mes/año
label_fecha_nac.place(x=130,y=125,width=120)
#SEXO
label_sexo =tk.Label(lblframe,text="Sexo: ",bg="#AB74F3",font="sans 12 bold")
label_sexo.place(x=10,y=155)
opcionesCBO =["M","F"]
#self.cbo_sexo = ttk.Combobox(lblframe,font="sans 12 bold",values=["M", "F"])
cbo_sexo = ttk.Combobox(lblframe,font="sans 12 bold",values=opcionesCBO)
cbo_sexo.place(x=130,y=155,width=70)
#MAIL
label_mail =tk.Label(lblframe,text="E-Mail: ",bg="#AB74F3",font="sans 12 bold")
label_mail.place(x=10,y=185)
entry_mail = tk.Entry(lblframe,font="sans 12 bold")
entry_mail.place(x=130,y=185,width=280)
#TELEFONO
label_telefono =tk.Label(lblframe,text="Telefono:  ",bg="#AB74F3",font="sans 12 bold")
label_telefono.place(x=10,y=215)
entry_telefono = tk.Entry(lblframe,font="sans 12 bold")
entry_telefono.place(x=130,y=215,width=280)

#BOTON DE INFORMACION DE LAS FUNCIONALIDADES DEL SISTEMA
btn_info = tk.Button(lblframe,text="Info ",bg="lightgrey",font="sans 12 bold", command=abrir_ventana_secundaria)
btn_info.place(x=980,y=5, width=70,height=30)

#Buscar
lbl1 =tk.Label(lblframe,text="Buscar DNI : ",bg="#AB74F3",font="sans 12 bold")
lbl1.place(x=550,y=215)

entry_buscar = tk.Entry(lblframe,font="sans 12 bold")
entry_buscar.place(x=655,y=215,width=270)   

#FRAME DE LA GRILLA
treeframe = tk.Frame(frame2,bg="#AB74F3")
treeframe.place(x=30,y=290,width=1030,height=150)

scrol_y= ttk.Scrollbar(treeframe,orient=VERTICAL)
scrol_y.pack(side=RIGHT,fill=Y)

scrol_x= ttk.Scrollbar(treeframe,orient=HORIZONTAL)
scrol_x.pack(side=BOTTOM,fill=X)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#           GRILLA 
tree = ttk.Treeview(treeframe,columns=("Socio","Documento","Nombre","Domicilio","Telefono","Mail","Sexo","Fecha"), show="headings",height=10,yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set)
scrol_y.config(command=tree.yview)
scrol_x.config(command=tree.xview)

#Encabezados de la GRILLA
tree.heading("#1",text="Socio")
tree.heading("#2",text="Documento")
tree.heading("#3",text="Nombre")
tree.heading("#4",text="Domicilio")
tree.heading("#5",text="Telefono")
tree.heading("#6",text="Mail")
tree.heading("#7",text="Sexo")
tree.heading("#8",text="Fecha")

#Columnas
tree.column("Socio", anchor="center")
tree.column("Documento", anchor="center")
tree.column("Nombre", anchor="center")
tree.column("Domicilio", anchor="center")
tree.column("Telefono", anchor="center")
tree.column("Mail", anchor="center")
tree.column("Sexo", anchor="center")
tree.column("Fecha", anchor="center")

tree.pack(expand=True,fill="both")     #Arma la grilla y la muestra con el metodo pack
tree.bind("<Double-1>", DobleClickTree)

#Barra de opciones abajo
lblframe1 = LabelFrame(frame2,text="Opciones", bg="#AB74F3",font="sans 12 bold")
lblframe1.place(x=30,y=450,width=1030,height=70)

#BOTONES
btn_agregar = tk.Button(lblframe1,text="Guardar ",bg="lightgrey",font="sans 12 bold", command=agregar_socios)
btn_agregar.place(x=10,y=5, width=150,height=30)

btn_baja = tk.Button(lblframe1,text="Limpiar ",bg="lightgrey",font="sans 12 bold",command=limpiar_text)
btn_baja.place(x=170,y=5, width=150,height=30)

btn_modificar = tk.Button(lblframe1,text="Modificar ",bg="lightgrey",font="sans 12 bold",command=editar_socios)
btn_modificar.place(x=335,y=5, width=150,height=30)

btn_buscar = tk.Button(lblframe1,text="Buscar ",bg="lightgrey",font="sans 12 bold", command=buscar_socio)
btn_buscar.place(x=500,y=5, width=150,height=30)

btn_cerrar = tk.Button(lblframe1,text="Cerrar ",bg="lightgrey",font="sans 12 bold",command=ventana.destroy)
btn_cerrar.place(x=835,y=5, width=150,height=30)

#IMAGEN DE LOS SOCIOS
dir= os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(dir,'socios.png')
logo_image = Image.open(ruta_imagen)
logo_image = logo_image.resize((270,200))
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(frame2, image=logo_image, bg="#AB74F3") 
logo_label.place(x=665,y=40)
logo_label.bind("<Double-Button-1>", abrir_imagen)

entry_documento.focus_set()
leer_socios()
ventana.mainloop()  
#-------------------------------------------------------------------------------------------------------------