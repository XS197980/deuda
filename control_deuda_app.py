
import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializar sesión
if 'deuda_inicial' not in st.session_state:
    st.session_state.deuda_inicial = 0.0
    st.session_state.pagos = []

st.title("📊 Control de Deuda Personal")

# 1️⃣ Establecer deuda inicial
st.subheader("1️⃣ Establecer deuda inicial")
deuda_input = st.number_input("Ingrese el monto de la deuda inicial (S/):", min_value=0.0, step=0.01)
if st.button("Establecer deuda"):
    st.session_state.deuda_inicial = deuda_input
    st.session_state.pagos = []
    st.success(f"Deuda inicial establecida en S/ {deuda_input:.2f}")

# 2️⃣ Registrar pagos
st.subheader("2️⃣ Registrar un pago")
pago_input = st.number_input("Ingrese el monto del pago (S/):", min_value=0.0, step=0.01)
fecha_pago = st.date_input("Fecha del pago:", value=datetime.today())
if st.button("Registrar pago"):
    if pago_input > 0:
        st.session_state.pagos.append({"Fecha": fecha_pago, "Monto": pago_input})
        st.success(f"Pago de S/ {pago_input:.2f} registrado el {fecha_pago}")
    else:
        st.error("Ingrese un monto válido para el pago.")

# 3️⃣ Saldo restante
st.subheader("3️⃣ Saldo restante")
total_pagado = sum(p['Monto'] for p in st.session_state.pagos)
saldo_restante = st.session_state.deuda_inicial - total_pagado
st.metric(label="Saldo pendiente", value=f"S/ {saldo_restante:.2f}")

# 4️⃣ Historial de pagos
st.subheader("4️⃣ Historial de pagos")
if st.session_state.pagos:
    df_pagos = pd.DataFrame(st.session_state.pagos)
    st.dataframe(df_pagos)
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
