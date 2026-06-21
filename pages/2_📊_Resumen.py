import streamlit as st

from utils import init_state, compute_balances, total_bill, balances_to_dataframe

st.set_page_config(page_title="Resumen", page_icon="📊", layout="centered")
init_state(st)

st.title("📊 Resumen final")

if not st.session_state.people:
    st.warning("Primero añade personas en la página de **Inicio**.")
    st.stop()
if not st.session_state.gastos:
    st.warning("Todavía no has añadido ningún gasto en la página de **Gastos**.")
    st.stop()

balances = compute_balances(st.session_state.people, st.session_state.gastos)
total = total_bill(st.session_state.gastos)
suma_individual = sum(balances.values())

st.subheader("💰 Cuánto debe pagar cada persona")
df = balances_to_dataframe(balances)
st.dataframe(df, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)
col1.metric("Total de la cuenta", f"{total:.2f} €")
col2.metric("Suma de lo que paga cada uno", f"{suma_individual:.2f} €")

if abs(total - suma_individual) < 0.01:
    st.success("✅ Las cuentas cuadran. Todo el importe está repartido correctamente.")
else:
    diferencia = total - suma_individual
    st.error(
        f"⚠️ Hay un descuadre de {diferencia:.2f} €. "
        "Revisa que todos los gastos tengan al menos un participante asignado."
    )

st.divider()
st.subheader("💸 ¿Quién pagó la cuenta?")
st.markdown(
    "Indica quién adelantó el dinero (pagó en caja o en el restaurante) "
    "para calcular quién debe transferirle a quién."
)

pagador = st.selectbox(
    "Persona que pagó la cuenta completa",
    ["-- Selecciona --"] + st.session_state.people,
)

if pagador != "-- Selecciona --":
    st.session_state.pagador = pagador
    st.subheader(f"📤 Transferencias a {pagador}")

    hay_transferencias = False
    for p, v in balances.items():
        if p == pagador:
            continue
        if v > 0.005:
            hay_transferencias = True
            st.write(f"**{p}** → debe pagar **{v:.2f} €** a **{pagador}**")

    if not hay_transferencias:
        st.info("Nadie más tiene que pagar nada.")

    propio = balances.get(pagador, 0.0)
    st.caption(
        f"{pagador} ya cubrió su propia parte ({propio:.2f} €) al pagar la cuenta entera."
    )

st.divider()
if st.button("🔄 Empezar de nuevo (borrar todo)"):
    st.session_state.people = []
    st.session_state.gastos = []
    st.session_state.next_id = 1
    st.session_state.pagador = None
    st.rerun()