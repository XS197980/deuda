
import streamlit as st
import pandas as pd
from datetime import datetime
import csv

# Inicializar sesin
if 'deuda_inicial' not in st.session_state:
    st.session_state.deuda_inicial = 0.0
    st.session_state.pagos = []

# Funcin para guardar pagos en CSV
def guardar_pago_csv(fecha, monto):
    with open("pagos.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([fecha, monto])

st.title(" Control de Deuda Personal")

# 1 Establecer deuda inicial
st.subheader("1 Establecer deuda inicial")
deuda_input = st.number_input("Ingrese el monto de la deuda inicial (S/):", min_value=0.0, step=0.01)
if st.button("Establecer deuda"):
    st.session_state.deuda_inicial = deuda_input
    st.session_state.pagos = []
    st.success(f"Deuda inicial establecida en S/ {deuda_input:.2f}")

# 2 Registrar pagos
st.subheader("2 Registrar un pago")
pago_input = st.number_input("Ingrese el monto del pago (S/):", min_value=0.0, step=0.01)
fecha_pago = st.date_input("Fecha del pago:", value=datetime.today())
if st.button("Registrar pago"):
    if pago_input > 0:
        st.session_state.pagos.append({"Fecha": fecha_pago, "Monto": pago_input})
        guardar_pago_csv(fecha_pago, pago_input)
        st.success(f"Pago de S/ {pago_input:.2f} registrado el {fecha_pago}")
    else:
        st.error("Ingrese un monto v1lido para el pago.")

# 3 Monto restante
st.subheader("3 Monto restante")
total_pagado = sum(p['Monto'] for p in st.session_state.pagos)
monto_restante = st.session_state.deuda_inicial - total_pagado
st.metric(label="Monto pendiente por pagar", value=f"S/ {monto_restante:.2f}")

# 4 Historial de pagos
st.subheader("4 Historial de pagos")
if st.session_state.pagos:
    df_pagos = pd.DataFrame(st.session_state.pagos)
    st.dataframe(df_pagos)
else:
    st.info("No hay pagos registrados afn.")

# 5 Reporte mensual de pagos
st.subheader("5 Reporte mensual de pagos")
if st.session_state.pagos:
    df_pagos['Mes'] = pd.to_datetime(df_pagos['Fecha']).dt.to_period('M')
    reporte_mensual = df_pagos.groupby('Mes')['Monto'].sum().reset_index()
    reporte_mensual.columns = ['Mes', 'Total Pagado']
    st.bar_chart(reporte_mensual.set_index('Mes'))
else:
    st.info("No hay datos suficientes para generar el reporte mensual.")


