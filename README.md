# 🧮 Divide tu Cuenta

Aplicación web hecha con [Streamlit](https://streamlit.io) para repartir el gasto
de una comida o una compra entre varias personas, **pagando cada una solo lo que
le corresponde** (no necesariamente a partes iguales entre todos).

Por ejemplo: si solo 3 de 5 personas piden bravas, ese gasto se reparte solo
entre esas 3, mientras que la cuenta general puede repartirse entre todos.

## ✨ Funcionalidades

- Añadir personas que participan en la cuenta.
- Añadir gastos (productos/platos) con su precio.
- Marcar cada gasto como **individual** (lo paga una sola persona) o
  **repartido** (seleccionas entre quiénes se divide).
- Cálculo automático de cuánto debe pagar cada persona en total.
- Comprobación automática de que la suma de lo que paga cada uno coincide
  con el total de la cuenta.
- Indicar quién adelantó el dinero y ver, persona a persona, cuánto debe
  transferirle cada quien.

## 📁 Estructura del proyecto

```
splitbill/
├── app.py                     # Página de inicio: gestión de personas
├── pages/
│   ├── 1_🧾_Gastos.py          # Añadir gastos y asignar participantes
│   └── 2_📊_Resumen.py         # Resumen final y reparto de transferencias
├── utils.py                   # Lógica de cálculo (pandas) y estado compartido
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Cómo ejecutarlo en local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO
   ```
2. Crea un entorno virtual (opcional pero recomendado) e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Lanza la app:
   ```bash
   streamlit run app.py
   ```
4. Se abrirá en tu navegador en `http://localhost:8501`.

## ☁️ Cómo subirlo a GitHub y desplegarlo gratis

1. Crea un repositorio nuevo en GitHub y sube este proyecto:
   ```bash
   git init
   git add .
   git commit -m "Primera versión de Divide tu Cuenta"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```
2. Ve a [share.streamlit.io](https://share.streamlit.io), conecta tu cuenta de
   GitHub y selecciona el repositorio.
3. Indica `app.py` como archivo principal y despliega. Streamlit Community
   Cloud detectará automáticamente `requirements.txt`.

## 🛠️ Tecnologías

- [Streamlit](https://streamlit.io) — interfaz web e interactividad.
- [pandas](https://pandas.pydata.org) — manejo y visualización de los datos
  de gastos y balances.
