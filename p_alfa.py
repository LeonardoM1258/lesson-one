import csv
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

# Crear el archivo CSV si no existe
if not os.path.exists('almacen.csv'):
    df = pd.DataFrame(
        columns=['Tipo Muestra', 'Proyecto Muestra', 'Cantidad', 'Fecha'])
    df.to_csv('almacen.csv', index=False)
else:
    # Leer el archivo CSV inicialmente
    df = pd.read_csv('almacen.csv')


def recibir_muestra():
    def recibir_muestra_inner():
        global df
        # Agregar esta línea para acceder a la variable global df
        tipo_muestra = variable_tipo_muestra.get()
        nombre = entry_nombre.get()
        cantidad = int(entry_cantidad.get())
        fecha = entry_fecha.get()

        nueva_muestra = pd.DataFrame(
            [[tipo_muestra, nombre, cantidad, fecha]], columns=df.columns)
        df = pd.concat([df, nueva_muestra], ignore_index=True)
        df.to_csv('almacen.csv', index=False)

        label_resultado.configure(
            text="La muestra ha sido recibida y almacenada correctamente.")

    ventana_recibir_muestra = tk.Toplevel()
    ventana_recibir_muestra.title("Recibir muestra")
    ventana_recibir_muestra.geometry("350x250")

    label_tipo_muestra = tk.Label(
        ventana_recibir_muestra, text="Tipo de muestra:")
    opciones_tipo_muestra = [
        "Microbiologia", "Grasas Residuales", "Quimica General", "Analisis compuestos"]
    variable_tipo_muestra = tk.StringVar(ventana_recibir_muestra)
    variable_tipo_muestra.set(opciones_tipo_muestra[0])
    option_menu_tipo_muestra = tk.OptionMenu(
        ventana_recibir_muestra, variable_tipo_muestra, *opciones_tipo_muestra)
    label_nombre = tk.Label(ventana_recibir_muestra,
                            text="Proyecto de la muestra:")
    entry_nombre = tk.Entry(ventana_recibir_muestra)
    label_cantidad = tk.Label(ventana_recibir_muestra,
                              text="Número de muestras:")
    entry_cantidad = tk.Entry(ventana_recibir_muestra)
    label_fecha = tk.Label(ventana_recibir_muestra, text="Fecha de ingreso:")
    entry_fecha = tk.Entry(ventana_recibir_muestra)
    btn_recibir = tk.Button(
        ventana_recibir_muestra, text="Recibir muestra", command=recibir_muestra_inner)
    label_resultado = tk.Label(ventana_recibir_muestra, text="")
    btn_salir = tk.Button(ventana_recibir_muestra, text="Salir",
                          command=ventana_recibir_muestra.destroy)

    label_tipo_muestra.pack()
    option_menu_tipo_muestra.pack()
    label_nombre.pack()
    entry_nombre.pack()
    label_cantidad.pack()
    entry_cantidad.pack()
    label_fecha.pack()
    entry_fecha.pack()
    btn_recibir.pack()
    label_resultado.pack()
    btn_salir.pack()


# Crear el archivo CSV si no existe
if not os.path.exists('almacen.csv'):
    with open('almacen.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(
            ["Tipo Muestra", "Proyecto Muestra", "Cantidad", "Fecha"])

# Leer el archivo CSV inicialmente
df = pd.read_csv('almacen.csv')


def retirar_muestra():
    def retirar_muestra_inner():
        proyecto_muestra = entry_proyecto_muestra.get()
        cantidad_retirar = int(entry_cantidad_retirar.get())

        # Leer el archivo CSV
        df = pd.read_csv('almacen.csv')

        # Buscar la muestra por proyecto de la muestra
        muestra_encontrada = df.loc[df['Proyecto Muestra'] == proyecto_muestra]

        if muestra_encontrada.empty:
            label_resultado.configure(
                text="No se encontró la muestra con el proyecto especificado.")
            return

        cantidad_actual = muestra_encontrada['Cantidad'].item()

        if cantidad_retirar > cantidad_actual:
            label_resultado.configure(
                text="No hay suficientes muestras disponibles para retirar esa cantidad.")
            return

        # Actualizar la cantidad de muestra retirada
        df.loc[df['Proyecto Muestra'] == proyecto_muestra,
               'Cantidad'] = cantidad_actual - cantidad_retirar

        # Guardar los cambios en el archivo CSV
        df.to_csv('almacen.csv', index=False)

        label_resultado.configure(
            text="Se ha retirado la muestra correctamente.")

    ventana_retirar_muestra = tk.Toplevel()
    ventana_retirar_muestra.title("Retirar muestra")
    ventana_retirar_muestra.geometry("350x200")

    label_proyecto_muestra = tk.Label(
        ventana_retirar_muestra, text="Proyecto de la muestra:")
    entry_proyecto_muestra = tk.Entry(ventana_retirar_muestra)
    label_cantidad_retirar = tk.Label(
        ventana_retirar_muestra, text="Cantidad a retirar:")
    entry_cantidad_retirar = tk.Entry(ventana_retirar_muestra)
    btn_retirar = tk.Button(
        ventana_retirar_muestra, text="Retirar muestra", command=retirar_muestra_inner)
    label_resultado = tk.Label(ventana_retirar_muestra, text="")
    btn_salir = tk.Button(ventana_retirar_muestra, text="Salir",
                          command=ventana_retirar_muestra.destroy)

    label_proyecto_muestra.pack()
    entry_proyecto_muestra.pack()
    label_cantidad_retirar.pack()
    entry_cantidad_retirar.pack()
    btn_retirar.pack()
    label_resultado.pack()
    btn_salir.pack()


def ver_inventario():
    def cerrar_ventana_inventario():
        ventana_inventario.destroy()

    ventana_inventario = tk.Toplevel()
    ventana_inventario.title("Inventario")
    ventana_inventario.geometry("550x300")

    # Leer el archivo CSV
    df = pd.read_csv('almacen.csv')

    tabla = ttk.Treeview(ventana_inventario)
    tabla["columns"] = ("tipo_muestra", "nombre", "cantidad", "fecha")
    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("tipo_muestra", anchor=tk.W, width=100)
    tabla.column("nombre", anchor=tk.W, width=150)
    tabla.column("cantidad", anchor=tk.W, width=100)
    tabla.column("fecha", anchor=tk.W, width=100)

    tabla.heading("#0", text="")
    tabla.heading("tipo_muestra", text="Tipo Muestra")
    tabla.heading("nombre", text="Proyecto Muestra")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("fecha", text="Fecha")

    for _, row in df.iterrows():
        tabla.insert(parent='', index='end', iid=row.name, text="", values=(
            row['Tipo Muestra'], row['Proyecto Muestra'], row['Cantidad'], row['Fecha']))

    tabla.pack()

    btn_cerrar = tk.Button(ventana_inventario, text="Cerrar",
                           command=cerrar_ventana_inventario)
    btn_cerrar.pack()


# Crear el archivo CSV si no existe
if not os.path.exists('almacen.csv'):
    df = pd.DataFrame(
        columns=['Tipo Muestra', 'Proyecto Muestra', 'Cantidad', 'Fecha'])
    df.to_csv('almacen.csv', index=False)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de almacenamiento de muestras")
ventana.geometry("520x200")

# posicionamiento de los botones en la ventana principal
btn_recibir_muestra = tk.Button(
    ventana, text="Recibir muestra", command=recibir_muestra)
btn_recibir_muestra.grid(row=0, column=1, padx=10, pady=3)

btn_retirar_muestra = tk.Button(
    ventana, text="Retirar muestra", command=retirar_muestra)
btn_retirar_muestra.grid(row=0, column=2, padx=10, pady=3)

btn_ver_inventario = tk.Button(
    ventana, text="Ver inventario", command=ver_inventario)
btn_ver_inventario.grid(row=0, column=3, padx=1, pady=1)


ruta_actual = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa de la imagen
ruta_imagen = os.path.join(ruta_actual, "logo.png")

# Abrir la imagen
imagen = Image.open(ruta_imagen)

# Modificar el tamaño de la imagen
nuevo_tamano = (200, 200)  # Especifica el nuevo tamaño deseado
imagen = imagen.resize(nuevo_tamano)
# Convertir la imagen a PhotoImage
imagen_tk = ImageTk.PhotoImage(imagen)

# Crear un Label para mostrar la imagen
label_imagen = tk.Label(ventana, image=imagen_tk)
label_imagen.grid(row=0, column=0)

ventana.mainloop()
