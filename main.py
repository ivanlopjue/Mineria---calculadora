import pandas as pd
import tkinter as tk

# =========================
# CONFIGURACIÓN GENERAL
# =========================
VELOCIDAD_ESCRITURA = 10  # milisegundos por carácter
RUTA_EXCEL = "./listado/listado.xlsx"

# =========================
# CARGAR EXCEL
# =========================
try:
    df = pd.read_excel(RUTA_EXCEL)
except Exception as e:
    print("Error leyendo el Excel:", e)
    exit()

# =========================
# COLA DE RESULTADOS PARA ESCRITURA
# =========================
cola_resultados = []  # lista global que mantiene resultados pendientes

# =========================
# EFECTO MÁQUINA DE ESCRIBIR
# =========================
def escribir_lento(texto, index=0):
    if index < len(texto):
        salida_texto.insert(tk.END, texto[index])
        salida_texto.see(tk.END)
        ventana.after(VELOCIDAD_ESCRITURA, escribir_lento, texto, index + 1)
    else:
        # Terminado este texto, sacar de la cola y escribir siguiente si hay más
        cola_resultados.pop(0)
        if cola_resultados:
            escribir_lento(cola_resultados[0])

# =========================
# MOSTRAR RESULTADO FORMATEADO
# =========================
def mostrar_resultado(item, unidades, vehiculo):
    salida = (
        "-" * 51 + "\n"
        f"Material: {item:<20} Unidades: {unidades}\n\n"
        f"Tipo de minado: {vehiculo}\n"
        + "-" * 51 + "\n\n"
    )
    cola_resultados.append(salida)
    # Si no hay animación en curso, iniciar escritura
    if len(cola_resultados) == 1:
        escribir_lento(cola_resultados[0])

# =========================
# PROCESAR NÚMERO
# =========================
def procesar_numero(event=None):  # event para ENTER
    salida_texto.delete("1.0", tk.END)

    valor = entrada_numero.get().strip()  # Quitar espacios

    if not valor:
        cola_resultados.clear()
        mostrar_error("Introduce un número.\n")
        entrada_numero.delete(0, tk.END)
        entrada_numero.focus()
        return

    try:
        numero = int(valor)
    except ValueError:
        cola_resultados.clear()
        mostrar_error("Debes introducir un número entero válido.\n")
        entrada_numero.delete(0, tk.END)
        entrada_numero.focus()
        return

    # Limpiar campo y devolver foco
    entrada_numero.delete(0, tk.END)
    entrada_numero.focus()

    encontrado = False

    for _, fila in df.iterrows():
        codigo = fila["codigo"]
        item = fila["item"]
        vehiculo = fila["vehiculo"]

        if numero % codigo == 0:
            unidades = numero // codigo
            mostrar_resultado(item, unidades, vehiculo)
            encontrado = True

    if not encontrado:
        mostrar_error("El código no corresponde a ningún material conocido.\n")

# =========================
# FUNCION AUXILIAR PARA ERRORES
# =========================
def mostrar_error(mensaje):
    cola_resultados.append(mensaje)
    if len(cola_resultados) == 1:
        escribir_lento(cola_resultados[0])

# =========================
# INTERFAZ GRÁFICA
# =========================
ventana = tk.Tk()
ventana.title("Minerales - Calculadora")
ventana.geometry("650x400")

# ---- Campo de entrada ----
frame_superior = tk.Frame(ventana)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Introduce un número:").pack(side=tk.LEFT, padx=5)

entrada_numero = tk.Entry(frame_superior, width=25)
entrada_numero.pack(side=tk.LEFT, padx=5)

# Ejecutar al pulsar ENTER
entrada_numero.bind("<Return>", procesar_numero)
entrada_numero.focus()

# ---- Salida ----
salida_texto = tk.Text(
    ventana,
    height=18,
    width=75,
    font=("Consolas", 10)
)
salida_texto.pack(padx=10, pady=10)

# =========================
# EJECUCIÓN
# =========================
ventana.mainloop()
