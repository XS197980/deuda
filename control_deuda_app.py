
import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os

# Función para cargar deuda desde CSV
def cargar_deuda_csv():
    if os.path.exists("deuda.csv"):
        with open("deuda.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            try:
                monto = next(reader)[0]
                return float(monto)
            except:
                return 0.0
    return 0.0

# Función para cargar pagos desde CSV
def cargar_pagos_csv():
    pagos = []
    if os.path.exists("pagos.csv"):
        with open("pagos.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                try:
                    fecha = datetime.strptime(row[0], "%Y-%m-%d").date()
                    monto = float(row[1])
                    pagos.append({"Fecha": fecha, "Monto": monto})
                except:
                    continue
    return pagos

# Inicializar sesión
if 'deuda_inicial' not in st.session_state:
    st.session_state.deuda_inicial = cargar_deuda_csv()

if 'pagos' not in st.session_state:
    st.session_state.pagos = cargar_pagos_csv()

# Función para guardar pagos en CSV
def guardar_pago_csv(fecha, monto):
    pagos_existentes = cargar_pagos_csv()
    pagos_existentes.append({"Fecha": fecha, "Monto": monto})
    with open("pagos.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Monto"])
        for pago in pagos_existentes:
            writer.writerow([pago["Fecha"], pago["Monto"]])

# Función para guardar deuda en CSV
def guardar_deuda_csv(monto):
    with open("deuda.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Deuda"])
        writer.writerow([monto])

st.title("📊 Control de Deuda Personal")

# 🔄 Resetear deuda y pagos
st.subheader("🔄 Resetear deuda y pagos")
if st.button("Resetear todo"):
    st.session_state.deuda_inicial = 0.0
    st.session_state.pagos = []
    guardar_deuda_csv(0.0)
    with open("pagos.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Monto"])
    st.success("La deuda y el historial de pagos han sido reiniciados.")

# 1️⃣ Añadir nueva deuda
st.subheader("1️⃣ Añadir nueva deuda")
deuda_input = st.number_input("Ingrese el monto de la nueva deuda (S/):", min_value=0.0, step=0.01)
if st.button("Añadir deuda"):
    st.session_state.deuda_inicial += deuda_input
    guardar_deuda_csv(st.session_state.deuda_inicial)
    st.success(f"Se ha añadido S/ {deuda_input:.2f} a la deuda. Total actual: S/ {st.session_state.deuda_inicial:.2f}")

# 2️⃣ Registrar pagos
st.subheader("2️⃣ Registrar un pago")
pago_input = st.number_input("Ingrese el monto del pago (S/):", min_value=0.0, step=0.01)
fecha_pago = st.date_input("Fecha del pago:", value=datetime.today())
if st.button("Registrar pago"):
    if pago_input > 0:
        st.session_state.pagos.append({"Fecha": fecha_pago, "Monto": pago_input})
        guardar_pago_csv(fecha_pago, pago_input)
        st.success(f"Pago de S/ {pago_input:.2f} registrado el {fecha_pago}")
    else:
        st.error("Ingrese un monto válido para el pago.")

# 3️⃣ Saldo restante
st.subheader("3️⃣ Saldo restante")
total_pagado = sum(p['Monto'] for p in st.session_state.pagos)
saldo_restante = st.session_state.deuda_inicial - total_pagado
st.metric(label="Saldo pendiente", value=f"S/ {saldo_restante:.2f}")
st.metric(label="Total pagado", value=f"S/ {total_pagado:.2f}")

# 4️⃣ Historial de pagos
st.subheader("4️⃣ Historial de pagos")
if st.session_state.pagos:
    df_pagos = pd.DataFrame(st.session_state.pagos)
    df_pagos = df_pagos.sort_values(by="Fecha")
    df_pagos["Fecha"] = df_pagos["Fecha"].astype(str)
    st.dataframe(df_pagos)
    csv = df_pagos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar historial de pagos (CSV)",
        data=csv,
        file_name='historial_pagos.csv',
        mime='text/csv'
    )
else:
    st.info("No hay pagos registrados aún.")

# 5️⃣ Reporte mensual de pagos
st.subheader("5️⃣ Reporte mensual de pagos")
if st.session_state.pagos:
    df_pagos['Mes'] = pd.to_datetime(df_pagos['Fecha']).dt.to_period('M')
    reporte_mensual = df_pagos.groupby('Mes')['Monto'].sum().reset_index()
    reporte_mensual.columns = ['Mes', 'Total Pagado']
    st.bar_chart(reporte_mensual.set_index('Mes'))
else:
    st.info("No hay datos suficientes para generar el reporte mensual.")
