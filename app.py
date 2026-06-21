import streamlit as st

from utils import init_state

st.set_page_config(page_title="Divide tu Cuenta", page_icon="🧮", layout="centered")
init_state(st)

st.title("🧮 Divide tu Cuenta")
st.markdown(
    """
    Reparte el gasto de una comida o una compra entre varias personas,
    de forma que **cada quien pague solo lo que le corresponde**
    (y no a partes iguales si no es necesario).

    **Cómo funciona:**
    1. 👥 Añade aquí a las personas que participan.
    2. 🧾 En la página **Gastos** (menú lateral), añade cada producto o
       plato, su precio, y quién lo paga: todos, algunos, o uno solo.
    3. 📊 En la página **Resumen**, verás cuánto debe pagar cada persona
       y, si quieres, quién le debe transferir dinero a quién.
    """
)

st.divider()
st.subheader("👥 Personas")

with st.form("add_person_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        nombre = st.text_input(
            "Nombre de la persona",
            label_visibility="collapsed",
            placeholder="Ej: Adam",
        )
    with col2:
        submitted = st.form_submit_button("Añadir", use_container_width=True)

    if submitted:
        nombre = nombre.strip()
        if not nombre:
            st.warning("Escribe un nombre antes de añadir.")
        elif nombre in st.session_state.people:
            st.warning(f"'{nombre}' ya está en la lista.")
        else:
            st.session_state.people.append(nombre)
            st.rerun()

if st.session_state.people:
    st.write("Personas añadidas:")
    for i, persona in enumerate(st.session_state.people):
        c1, c2 = st.columns([5, 1])
        c1.write(f"• {persona}")
        if c2.button("🗑️", key=f"del_person_{i}"):
            st.session_state.people.remove(persona)
            # Si la quitamos, también la quitamos de los gastos donde participaba
            for it in st.session_state.gastos:
                if persona in it["participantes"]:
                    it["participantes"].remove(persona)
            if st.session_state.pagador == persona:
                st.session_state.pagador = None
            st.rerun()

    st.success(
        f"{len(st.session_state.people)} persona(s) lista(s). "
        "Ve a la página **Gastos** en el menú lateral →"
    )
else:
    st.info("Añade al menos 2 personas para empezar.")