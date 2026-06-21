"""
Funciones de utilidad compartidas por todas las páginas de la app.

Centralizamos aquí:
- La inicialización del estado de sesión (st.session_state).
- La conversión de los gastos a un DataFrame de pandas para mostrarlos.
- El cálculo del reparto: cuánto debe pagar cada persona.
"""

import pandas as pd


def init_state(st):
    """Inicializa las claves necesarias en st.session_state si no existen."""
    if "people" not in st.session_state:
        st.session_state.people = []
    if "gastos" not in st.session_state:
        st.session_state.gastos = []  # lista de dicts, ver estructura abajo
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1
    if "pagador" not in st.session_state:
        st.session_state.pagador = None


# Estructura de cada elemento en st.session_state.gastos:
# {
#     "id": int,
#     "nombre": str,
#     "precio": float,
#     "tipo": "Individual" | "Repartido",
#     "participantes": [str, ...],  # quienes pagan ese gasto
# }


def items_to_dataframe(items: list[dict]) -> pd.DataFrame:
    """Convierte la lista de gastos en un DataFrame legible para mostrar en pantalla."""
    rows = []
    for it in items:
        rows.append(
            {
                "Concepto": it["nombre"],
                "Precio (€)": round(it["precio"], 2),
                "Tipo": it["tipo"],
                "Participantes": ", ".join(it["participantes"]),
            }
        )
    return pd.DataFrame(rows)


def compute_balances(people: list[str], items: list[dict]) -> dict[str, float]:
    """
    Calcula cuánto debe pagar cada persona en total.

    Cada gasto se divide a partes iguales entre sus participantes
    (si solo hay un participante, esa persona paga el 100%).
    """
    balances = {p: 0.0 for p in people}
    for it in items:
        participantes = it["participantes"]
        if not participantes:
            continue
        share = it["precio"] / len(participantes)
        for p in participantes:
            if p in balances:
                balances[p] += share
    return balances


def total_bill(items: list[dict]) -> float:
    """Suma el precio de todos los gastos: el total de la cuenta."""
    return sum(it["precio"] for it in items)


def balances_to_dataframe(balances: dict[str, float]) -> pd.DataFrame:
    """Convierte el diccionario de balances en un DataFrame ordenado de mayor a menor."""
    df = pd.DataFrame(
        [{"Persona": p, "Debe pagar (€)": round(v, 2)} for p, v in balances.items()]
    )
    return df.sort_values("Debe pagar (€)", ascending=False).reset_index(drop=True)