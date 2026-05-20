
import streamlit as st

# --- CONSTANTES ---
COLOR_PRINCIPAL  = "#0033A0"
COLOR_SECUNDARIO = "#007BFF"
GRIS_TEXTO       = "#4A4A4A"
GRIS_SUAVE       = "#CCCCCC"
FONDO            = "#FFFFFF"
DOSIS_FACTOR     = 0.1          # mL por kg — cambiar aquí si cambia el protocolo


# ---------------------------------------------------------------------------
# LÓGICA DE NEGOCIO (pura, sin dependencias de UI → fácil de testear)
# ---------------------------------------------------------------------------

def calcular_dosis_ml(peso_kg: float) -> float:
    """Devuelve la dosis en mL. Lanza ValueError si el peso no es válido."""
    if peso_kg <= 0:
        raise ValueError(f"El peso debe ser mayor que 0, recibido: {peso_kg}")
    return round(peso_kg * DOSIS_FACTOR, 2)


# ---------------------------------------------------------------------------
# APLICACIÓN WEB (misma estética y flujo que Tkinter, pero en Streamlit)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Calculadora vacuna antirrábica",
    layout="centered",
)

# --- Estado (equivalente al modo calcular/resultado de tu app) ---
if "modo_resultado" not in st.session_state:
    st.session_state.modo_resultado = False
if "peso_txt" not in st.session_state:
    st.session_state.peso_txt = ""
if "dosis" not in st.session_state:
    st.session_state.dosis = None

# --- CSS: mantener estética (colores, Arial, tamaños, “tarjeta”, centrado) ---
st.markdown(
    f"""
    <style>
      html, body, [class*="css"] {{
        font-family: Arial, sans-serif !important;
      }}
      .stApp {{
        background-color: {FONDO};
      }}

      /* Ancho similar al 450x450 de tu ventana */
      .main .block-container {{
        max-width: 450px;
        padding-top: 20px;
        padding-bottom: 10px;
      }}

      .titulo {{
        color: {COLOR_PRINCIPAL};
        font-size: 14pt;
        font-weight: 700;
        text-align: center;
        margin: 20px 0 10px 0;
      }}

      .card {{
        background: {FONDO};
        padding: 10px 30px 5px 30px;
      }}

      .label {{
        color: {GRIS_TEXTO};
        font-size: 11pt;
        text-align: center;
        margin: 10px 0 5px 0;
      }}

      /* Input centrado (como Entry) */
      input {{
        text-align: center !important;
        font-size: 11pt !important;
        padding: 10px !important;
      }}

      /* Botón Calcular (principal) */
      button[kind="primary"] {{
        background: {COLOR_PRINCIPAL} !important;
        color: white !important;
        border: none !important;
        padding: 12px 10px !important;
        font-weight: 700 !important;
        font-size: 11pt !important;
        width: 100% !important;
      }}
      button[kind="primary"]:hover {{
        background: {COLOR_SECUNDARIO} !important;
        color: white !important;
      }}
      button[kind="primary"][disabled] {{
        background: {GRIS_SUAVE} !important;
        color: white !important;
      }}

      /* Botón Nuevo cálculo (flat, como el tuyo) */
      button[kind="secondary"] {{
        background: {FONDO} !important;
        color: {COLOR_PRINCIPAL} !important;
        border: none !important;
        font-size: 10pt !important;
        padding: 10px 10px !important;
        width: 100% !important;
      }}
      button[kind="secondary"][disabled] {{
        color: {GRIS_SUAVE} !important;
      }}

      .resultado_texto {{
        color: {GRIS_TEXTO};
        font-size: 10pt;
        text-align: center;
        margin-top: 15px;
      }}
      .resultado_valor {{
        color: black;
        font-size: 26pt;
        font-weight: 800;
        text-align: center;
        margin: 0;
        line-height: 1.1;
      }}
      .resultado_unidad {{
        color: {GRIS_TEXTO};
        font-size: 11pt;
        text-align: center;
        margin-top: 0px;
      }}

      .footer {{
        color: {GRIS_TEXTO};
        font-size: 8pt;
        text-align: center;
        margin-top: 10px;
        padding-bottom: 10px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- UI (mismo texto) ---
st.markdown('<div class="titulo">Calculadora dosis antirrábica</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="label">Peso del paciente (kg)</div>', unsafe_allow_html=True)

# Usamos form para que ENTER funcione como “Calcular”
with st.form("form_calculo", clear_on_submit=False):
    st.session_state.peso_txt = st.text_input(
        label="",
        value=st.session_state.peso_txt,
        disabled=st.session_state.modo_resultado,
        label_visibility="collapsed",
    )
    btn_calcular = st.form_submit_button(
        "Calcular",
        type="primary",
        disabled=st.session_state.modo_resultado,
        use_container_width=True,
    )

st.markdown("</div>", unsafe_allow_html=True)  # cierre card

# Botón Nuevo cálculo (solo activo en modo resultado)
btn_reiniciar = st.button(
    "Nuevo cálculo",
    type="secondary",
    disabled=not st.session_state.modo_resultado,
    use_container_width=True,
)

# --- Eventos (mismo flujo que tu app) ---
if btn_reiniciar:
    st.session_state.modo_resultado = False
    st.session_state.peso_txt = ""
    st.session_state.dosis = None
    st.rerun()

if btn_calcular:
    try:
        peso = float(st.session_state.peso_txt)
        dosis = calcular_dosis_ml(peso)  # MISMA lógica
        st.session_state.dosis = dosis
        st.session_state.modo_resultado = True
        st.rerun()
    except ValueError:
        st.error("Ingrese un peso válido en kg.\nUse punto (.) para decimales.")

# Panel de resultado (oculto al inicio)
if st.session_state.modo_resultado and st.session_state.dosis is not None:
    st.markdown('<div class="resultado_texto">Dosis recomendada</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="resultado_valor">{st.session_state.dosis:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="resultado_unidad">mL</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Uso clínico referencial SURA® 2026</div>', unsafe_allow_html=True)
