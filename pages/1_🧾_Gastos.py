import streamlit as st

from utils import init_state, items_to_dataframe

st.set_page_config(page_title="Gastos", page_icon="🧾", layout="centered")
init_state(st)

st.title("🧾 Añadir gastos")

if len(st.session_state.people) == 0:
    st.warning("Primero añade personas en la página de **Inicio**.")
    st.stop()

st.markdown("Añade cada producto o plato, su precio, y quién lo paga.")

with st.form("add_item_form", clear_on_submit=True):
    nombre = st.text_input("Concepto", placeholder="Ej: Bravas, Pizza margarita...")
    precio = st.number_input("Precio (€)", min_value=0.0, step=0.5, format="%.2f")
    tipo = st.radio(
        "¿Cómo se paga?",
        ["Repartido entre varios", "Individual (una sola persona)"],
        horizontal=True,
    )

    if tipo == "Individual (una sola persona)":
        responsable = st.selectbox("¿Quién lo paga?", st.session_state.people)
        participantes = [responsable] if responsable else []
    else:
        participantes = st.multiselect(
            "¿Entre quiénes se reparte?",
            st.session_state.people,
            default=st.session_state.people,
            help="Por ejemplo, si solo 3 de 5 comen bravas, selecciona solo esas 3 personas.",
        )

    submitted = st.form_submit_button("Añadir gasto", use_container_width=True)

    if submitted:
        if not nombre.strip():
            st.warning("Ponle un nombre al gasto.")
        elif precio <= 0:
            st.warning("El precio debe ser mayor que 0.")
        elif not participantes:
            st.warning("Selecciona al menos una persona.")
        else:
            st.session_state.items.append(
                {
                    "id": st.session_state.next_id,
                    "nombre": nombre.strip(),
                    "precio": round(precio, 2),
                    "tipo": "Individual" if tipo.startswith("Individual") else "Repartido",
                    "participantes": participantes,
                }
            )
            st.session_state.next_id += 1
            st.rerun()

st.divider()

if st.session_state.items:
    st.subheader("Gastos añadidos")
    df = items_to_dataframe(st.session_state.items)
    st.dataframe(df, use_container_width=True, hide_index=True)

    total = sum(it["precio"] for it in st.session_state.items)
    st.metric("💶 Total de la cuenta", f"{total:.2f} €")

    with st.expander("🗑️ Eliminar un gasto"):
        for it in st.session_state.items:
            c1, c2 = st.columns([5, 1])
            c1.write(
                f"**{it['nombre']}** — {it['precio']:.2f} € "
                f"({', '.join(it['participantes'])})"
            )
            if c2.button("Eliminar", key=f"del_item_{it['id']}"):
                st.session_state.items = [
                    x for x in st.session_state.items if x["id"] != it["id"]
                ]
                st.rerun()

    st.success("Cuando hayas añadido todos los gastos, ve a **Resumen** →")
else:
    st.info("Todavía no has añadido ningún gasto.")
