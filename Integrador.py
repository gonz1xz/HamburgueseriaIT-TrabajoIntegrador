import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from PIL import Image, ImageTk
import time
import sqlite3

## Creación y Conexión a la base de datos
connect = sqlite3.connect("comercio.sqlite")
cursor = connect.cursor()

try:
    cursor.execute("CREATE TABLE Ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT, fecha TEXT, combo_S INT, combo_D INT, combo_T INT, Flurby INT, total REAL)")
    cursor.execute("CREATE TABLE Registros (id INTEGER PRIMARY KEY AUTOINCREMENT, encargado TEXT, fecha TEXT, evento TEXT, caja REAL)")

except sqlite3.OperationalError:
    pass

## Inicializacion de variables globales
valorS = 5
valorD = 6
valorT = 7
valorF = 2
interfaz_principal_frame = None
img = None
entrada_nombre_encargado = None
totalVentas = 0
entrada_nombre_cliente = None

## Inicialización de la interfaz
interfaz = tk.Tk()
interfaz.resizable(0,0)
interfaz.title("Hamburgueseria IT")
interfaz.geometry("980x600")

icono = PhotoImage(file="IconBurger.png") 
interfaz.iconphoto(True, icono)


## REGISTRO DE ENTRADA Y SALIDA
def registros(accion, tiempoEnc, encargado, totalVentas):
    cursor.execute("INSERT INTO Registros (encargado, fecha, evento, caja) VALUES (?, ?, ?, ?)", (encargado, tiempoEnc, accion, totalVentas))
    connect.commit()
    

## FUNCION PARA LA FINALIZACION DEL PAGO
def realizar_pago(pago, total, cant_comboS, cant_comboD, cant_comboT, cant_comboF, nombreCliente):
    vuelto = int(pago) - int(total)
    
    etiqueta3 = ttk.Label(interfaz_principal_frame, text=f"Vuelto: {vuelto}", font=("Helvetica", 10))
    etiqueta3.grid(row=5,column=2, pady=20)
    
    etiqueta4 = ttk.Label(interfaz_principal_frame, text=f"¿Desea confirmar su compra?", font=("Helvetica", 10))
    etiqueta4.grid(row=6,column=2, pady=30)

    boton1 = ttk.Button(interfaz_principal_frame, text="Cancelar", command=mostrar_pagina_productos)
    boton1.grid(row=7, column=1, pady=(20, 0))

    boton2 = ttk.Button(interfaz_principal_frame, text="Confirmar", command=lambda: ventas(nombreCliente, cant_comboS, cant_comboD, cant_comboT, cant_comboF, total))
    boton2.grid(row=7, column=3, pady=(20, 0))


## FUNCION PARA GUARDAR NOMBRE Y REGISTRAR EL INICIO DE SESIÓN EN LA BASE DE DATOS
def guardar_nombre(nombre):
    global totalVentas, entrada_nombre_encargado
    if nombre != '':
        entrada_nombre_encargado = nombre
        totalVentas = 0
        accion = "Ingreso"
        tiempoEnc = time.asctime()
        registros(accion, tiempoEnc, nombre, totalVentas)
        mostrar_pagina_productos()
    else:
        messagebox.showerror("Error", "Porfavor ingrese su nombre.")


## REGISTRO DE VENTAS EN LA BASE DE DATOS
def ventas(ncliente, comboS, comboD,comboT,comboF,total):
    global totalVentas
    totalVentas = totalVentas + int(total)
    tiempo = time.asctime()
    cursor.execute("INSERT INTO Ventas (cliente, fecha, combo_S, combo_D, combo_T, Flurby, total) VALUES (?, ?, ?, ?, ?, ?, ?)", (ncliente, tiempo, comboS, comboD, comboT, comboF, total))
    connect.commit()
    messagebox.showinfo("Hamburguesas IT", "¡¡Gracias por su compra!!")
    mostrar_pagina_productos()

## CERRAR SESION
def cerrar_sesion(nombre):
    global totalVentas
    tiempoEnc = time.asctime()
    accion= "Egreso"
    registros(accion, tiempoEnc, nombre, totalVentas)
    mostrar_pagina_principal()


def boton_accion(abona, total, comboS, comboD, comboT, comboF, nombre_cliente):
    try:
        if (int(abona) - int(total)) >= 0:
            realizar_pago(abona, total, int(comboS), int(comboD), int(comboT), int(comboF), nombre_cliente)
        else:
            faltante = (int(abona)-int(total))*-1
            messagebox.showwarning("Pago Insuficiente", f"¡¡¡ Te faltan ${faltante} !!!")
    except ValueError:
        messagebox.showerror("Error", "No ingresaste nada o Ingresaste valores incorrectos")

## PAGINA DE CONFIRMACION DE VENTA
def mostrar_ticket(cantidad_comboS, cantidad_comboD, cantidad_comboT, cantidad_comboF, entrada_nombre_cliente):
    try:
        if entrada_nombre_cliente != '':
            global interfaz_principal_frame
            comboS = int(cantidad_comboS) * valorS
            comboD = int(cantidad_comboD) * valorD
            comboT = int(cantidad_comboT) * valorT
            comboF = int(cantidad_comboF) * valorF
            total = comboS+comboD+comboT+comboF
        
            if interfaz_principal_frame != None:
                interfaz_principal_frame.destroy()
            if not(comboS == 0 and comboD == 0 and comboT==0 and comboF==0):
                interfaz_principal_frame = ttk.Frame(interfaz)
                interfaz_principal_frame.grid(row=0, column=0)

                etiqueta3 = ttk.Label(interfaz_principal_frame, text=f"Hamburguesas IT" , font=("Helvetica", 20))
                etiqueta3.grid(row=0,column=0, pady=20, padx=(10, 120))
                
                etiqueta4 = ttk.Label(interfaz_principal_frame, text=f"*TICKET*", font=("Helvetica", 10))
                etiqueta4.grid(row=0,column=4, pady=20, padx=(80, 0))

                boton2 = ttk.Button(interfaz_principal_frame, text="Anular Ticket", command=mostrar_pagina_productos)
                boton2.grid(row=0, column=5)

                etiqueta5 = ttk.Label(interfaz_principal_frame, text=f"Nombre del cliente: {str(entrada_nombre_cliente).capitalize()}", font=("Helvetica", 10))
                etiqueta5.grid(row=1,column=2, pady=20, padx=10)

                etiqueta1 = ttk.Label(interfaz_principal_frame, text=f"Total: {total}", font=("Helvetica", 10))
                etiqueta1.grid(row=2,column=2, pady=20, padx=10)

                etiqueta2 = ttk.Label(interfaz_principal_frame, text=f"Abona con:", font=("Helvetica", 10))
                etiqueta2.grid(row=3,column=2, pady=20)

                entrada_abona = ttk.Entry(interfaz_principal_frame)
                entrada_abona.grid(row=3, column=3, padx=(0, 20))

                boton = ttk.Button(interfaz_principal_frame, text="Continuar", command= lambda : boton_accion(entrada_abona.get(), total, int(cantidad_comboS), int(cantidad_comboD), int(cantidad_comboT), int(cantidad_comboF), entrada_nombre_cliente))
                boton.grid(row=4, column=2)
            else:
                mostrar_pagina_productos()
                messagebox.showerror("Error", "Porfavor ingrese cantidad")

        else:
            messagebox.showerror("Error", "Porfavor ingrese nombre del cliente")
    except ValueError:
        messagebox.showerror("Error", "No ingresaste nada o Ingresaste valores incorrectos")
    


## PAGINA PRINCIPAL
def mostrar_pagina_principal():
    global img, interfaz_principal_frame, entrada_nombre_encargado
    if interfaz_principal_frame != None:
        interfaz_principal_frame.destroy()

    interfaz_principal_frame = ttk.Frame(interfaz)
    interfaz_principal_frame.grid(row=0, column=0)

    etiqueta1 = ttk.Label(interfaz_principal_frame, text="Bienvenidx a Hamburguesas IT", font=("Helvetica", 10))
    etiqueta1.grid(row=0,column=0)

    imagen_pillow = Image.open("ItBurger.jpg")
    imagen_redimensionada = imagen_pillow.resize((1000, 500), Image.BOX)
    img = ImageTk.PhotoImage(imagen_redimensionada)
    imagen1 = ttk.Label(interfaz_principal_frame, image=img)
    imagen1.grid(row=1, column=0)
  
    etiqueta2 = ttk.Label(interfaz_principal_frame, text="Ingrese su nombre de encargado:", font=("Helvetica", 10))
    etiqueta2.grid(row=2, column=0)

    entrada_nombre_encargado = ttk.Entry(interfaz_principal_frame)
    entrada_nombre_encargado.grid(row=3, column=0, pady=5)

    boton = ttk.Button(interfaz_principal_frame, text="Ingresar", command=lambda : guardar_nombre(entrada_nombre_encargado.get()))
    boton.grid(row=4, column=0)

## PAGINA DE MENU DE COMIDAS
def mostrar_pagina_productos():
    global interfaz_principal_frame, img1, img2, img3, img4, entrada_nombre_encargado, entrada_nombre_cliente

    entrada_nombre_cliente = None

    if interfaz_principal_frame != None:
        interfaz_principal_frame.destroy()

    interfaz_principal_frame = ttk.Frame(interfaz)
    interfaz_principal_frame.grid(row=0, column=0)

    etiqueta1 = ttk.Label(interfaz_principal_frame, text=(f"Hamburguesas IT"), font=("Helvetica", 15))
    etiqueta1.grid(row=0, column=0, pady= 30)
    etiqueta2 = ttk.Label(interfaz_principal_frame, text=(f"Encargado/a -> {str(entrada_nombre_encargado).capitalize()}"), font=("Helvetica", 10))
    etiqueta2.grid(row=0, column=2, pady= 30)

    etiqueta3 = ttk.Label(interfaz_principal_frame, text=(f"Nombre del cliente:"), font=("Helvetica", 10))
    etiqueta3.grid(row=1, column=0, pady=(0, 40))

    entrada_nombre_cliente = ttk.Entry(interfaz_principal_frame)
    entrada_nombre_cliente.grid(row=1, column=1, pady=(0, 40))

    ## COMBO S
    imagen_pillow1 = Image.open("comboS.jpg")
    imagen_redimensionada = imagen_pillow1.resize((200, 200), Image.BOX)
    img1 = ImageTk.PhotoImage(imagen_redimensionada)
    imagen1 = ttk.Label(interfaz_principal_frame, image=img1)
    imagen1.grid(row=3, column=0, padx=20)

    etiqueta_cant1 = ttk.Label(interfaz_principal_frame, text="Cantidad:", font=("Helvetica", 10))
    etiqueta_cant1.grid(row=4, column=0, pady=2)

    entrada_comboS = ttk.Entry(interfaz_principal_frame)
    entrada_comboS.grid(row=5, column=0)
    entrada_comboS.insert(0, "0")

    ## COMBO D
    imagen_pillow2 = Image.open("comboD.jpg")
    imagen_redimensionada = imagen_pillow2.resize((200, 200), Image.BOX)
    img2 = ImageTk.PhotoImage(imagen_redimensionada)
    imagen2 = ttk.Label(interfaz_principal_frame, image=img2)
    imagen2.grid(row=3, column=1, padx=20)

    etiqueta_cant2 = ttk.Label(interfaz_principal_frame, text="Cantidad:", font=("Helvetica", 10))
    etiqueta_cant2.grid(row=4, column=1, pady=2)

    entrada_comboD = ttk.Entry(interfaz_principal_frame)
    entrada_comboD.grid(row=5, column=1)
    entrada_comboD.insert(0, "0")

    ## COMBO T
    imagen_pillow3 = Image.open("comboT.jpg")
    imagen_redimensionada = imagen_pillow3.resize((200, 200), Image.BOX)
    img3 = ImageTk.PhotoImage(imagen_redimensionada)
    imagen3 = ttk.Label(interfaz_principal_frame, image=img3)
    imagen3.grid(row=3, column=2, padx=20)

    etiqueta_cant3 = ttk.Label(interfaz_principal_frame, text="Cantidad:", font=("Helvetica", 10))
    etiqueta_cant3.grid(row=4, column=2, pady=2)

    entrada_comboT = ttk.Entry(interfaz_principal_frame)
    entrada_comboT.grid(row=5, column=2)
    entrada_comboT.insert(0, "0")

    ## FLURBY
    imagen_pillow4 = Image.open("flurby.jpg")
    imagen_redimensionada = imagen_pillow4.resize((200, 200), Image.BOX)
    img4 = ImageTk.PhotoImage(imagen_redimensionada)
    imagen4 = ttk.Label(interfaz_principal_frame, image=img4)
    imagen4.grid(row=3, column=3, padx=20)

    etiqueta_cant4 = ttk.Label(interfaz_principal_frame, text="Cantidad:", font=("Helvetica", 10))
    etiqueta_cant4.grid(row=4, column=3, pady=2)

    entrada_comboF = ttk.Entry(interfaz_principal_frame)
    entrada_comboF.grid(row=5, column=3)
    entrada_comboF.insert(0, "0")

    ## FINALIZAR PEDIDO
    buton = ttk.Button(interfaz_principal_frame, text="Finalizar Pedido", command= lambda: mostrar_ticket(entrada_comboS.get(), entrada_comboD.get(), entrada_comboT.get(), entrada_comboF.get(), entrada_nombre_cliente.get()))
    buton.grid(row=6,column=3, pady=(30, 10))

    ##SALIR
    buton1 = ttk.Button(interfaz_principal_frame, text="Cerrar Sesión", command= lambda: cerrar_sesion(entrada_nombre_encargado))
    buton1.grid(row=0,column=3)

mostrar_pagina_principal()
tk.mainloop()