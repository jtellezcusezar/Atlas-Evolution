import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict, Optional

st.set_page_config(
    page_title="Dashboard 3iAtlas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# ESTILO
# =========================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #F7F9FC;
            color: #132238;
        }
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1.5rem;
            max-width: 1500px;
        }
        .dashboard-title {
            font-size: 2rem;
            font-weight: 700;
            color: #0F2744;
            margin-bottom: 0.15rem;
        }
        .dashboard-subtitle {
            font-size: 0.98rem;
            color: #4B5B70;
            margin-bottom: 1.2rem;
        }
        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #123154;
            margin-bottom: 0.5rem;
        }
        .metric-card {
            background: white;
            border: 1px solid #E3E8EF;
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: 0 2px 10px rgba(16, 24, 40, 0.04);
        }
        .timeline-card {
            background: white;
            border: 1px solid #E3E8EF;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 2px 10px rgba(16, 24, 40, 0.04);
        }
        .timeline-card-active {
            background: #EEF5FF;
            border: 1px solid #B9D4FF;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 3px 12px rgba(57, 106, 177, 0.10);
        }
        .timeline-date {
            font-size: 0.82rem;
            font-weight: 700;
            color: #3A5D8A;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .timeline-title {
            font-size: 1.12rem;
            font-weight: 700;
            color: #122B46;
            margin-top: 0.15rem;
            margin-bottom: 0.6rem;
        }
        .timeline-subhead {
            font-size: 0.9rem;
            font-weight: 700;
            color: #244567;
            margin-top: 0.55rem;
            margin-bottom: 0.2rem;
        }
        .timeline-text {
            font-size: 0.92rem;
            color: #405469;
            line-height: 1.45;
        }
        .pill {
            display: inline-block;
            background: #EFF3F8;
            color: #35506C;
            border: 1px solid #D7E0EA;
            border-radius: 999px;
            font-size: 0.78rem;
            padding: 0.22rem 0.6rem;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# CONFIGURACIÓN DE ARCHIVOS
# =========================
BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "Calibracion Atlas - copia.xlsx"

# =========================
# DATOS DE LÍNEA DE TIEMPO
# =========================
TIMELINE_EVENTS: List[Dict] = [
    {
        "event_key": "2025-10-30_lectura",
        "date_label": "30 Oct 2025",
        "anchor_date": "2025-11-15",
        "title": "Lectura",
        "short_code": "1",
        "situations": [
            "1.1 Identificación manual de actividades finalizadas, en ejecución o atrasadas."
        ],
        "solutions": [
            "1.1 Comparación de fechas con archivo CSV (Power BI) y programas en MProject, identificando actividades atrasadas y huérfanas (sin sucesoras)."
        ],
    },
    {
        "event_key": "2025-10-30_localizacion",
        "date_label": "30 Oct 2025",
        "anchor_date": "2025-11-15",
        "title": "Localización actividades",
        "short_code": "3",
        "situations": [
            "3.1 Trabajo en horas por parte de MProject.",
            "3.2 Identificación de actividades de obra.",
            "3.3 Qué hacer con actividades sucesoras de las finalizadas o en ejecución.",
            "3.4 Actividades huérfanas y en ejecución sin vínculo.",
        ],
        "solutions": [
            "3.1 Fijar las actualizaciones en 8:00 y 17:00.",
            "3.2 Concentrar la actualización en actividades que pertenecen al agrupador CONSTRUCCIÓN.",
            "3.3 Actividades finalizadas y en ejecución eliminan dependencias de sus sucesoras según lógica de programación.",
            "3.4 Anclar actividades al hito Corte.",
        ],
    },
    {
        "event_key": "2025-11-06_escritura_mp",
        "date_label": "06 Nov 2025",
        "anchor_date": "2025-11-22",
        "title": "Escritura sobre MP",
        "short_code": "2",
        "situations": [
            "2.1 Estropear programa en MProject.",
            "2.2 Cómo identificar fecha de corte.",
            "2.3 Tiempo en actualización de fechas de actividades finalizadas.",
        ],
        "solutions": [
            "2.1 Crear copia de archivo MProject.",
            "2.2 Creación KeyHito Corte.",
            "2.3 Tomar información del CSV y actualizar actividades finalizadas y en ejecución, etiquetándolas para evitar reprocesos futuros.",
        ],
    },
    {
        "event_key": "2025-11-21_configuracion_mproject",
        "date_label": "21 Nov 2025",
        "anchor_date": "2025-11-29",
        "title": "Configuración MProject",
        "short_code": "4",
        "situations": [
            "4.1 Lag de 5 horas por configuración de MProject.",
            "4.2 Identificación de atrasos y adelantos de elementos específicos.",
        ],
        "solutions": [
            "4.1 Configuración de calendarios de MProject.",
            "4.2 Guardar información de finalización de hitos de torres y ZC.",
        ],
    },
    {
        "event_key": "2025-11-14_20_atrasos_adelantos",
        "date_label": "14–20 Nov 2025",
        "anchor_date": "2025-12-13",
        "title": "Atrasos - Adelantos",
        "short_code": "5-6",
        "situations": [
            "5.1 Identificar hitos de finalización.",
            "5.2 Cálculo automático de programación en actividades.",
            "6.1 Tener en cuenta la lógica de programación (FC, CC, CF y FF).",
        ],
        "solutions": [
            "5.1 Estandarizar nombres de hitos informando fecha.",
            "5.2 Configurar actividades finalizadas y en ejecución en manual para evitar movimientos no deseados.",
            "6.1 La eliminación de dependencias en sucesoras debe seguir una lógica con condicionales.",
        ],
    },
    {
        "event_key": "2025-12-17_ruta_critica",
        "date_label": "17 Dic 2025",
        "anchor_date": "2025-12-27",
        "title": "Ruta crítica",
        "short_code": "7",
        "situations": [
            "7.1 Identificar ruta crítica individual.",
        ],
        "solutions": [
            "7.1 Algoritmo Drill-Down por hito a revisar.",
        ],
    },
    {
        "event_key": "2026-02-23_correccion_vinculacion",
        "date_label": "23 Feb 2026",
        "anchor_date": "2026-02-21",
        "title": "Corrección vinculación",
        "short_code": "8",
        "situations": [
            "8.1 Eliminación discriminada de vínculos de actividades con predecesoras finalizadas.",
        ],
        "solutions": [
            "8.1 Agrupar vínculos y, bajo los condicionales de programación, eliminar el adecuado.",
        ],
    },
    {
        "event_key": "2026-03-04_actividad_critica",
        "date_label": "04 Mar 2026",
        "anchor_date": "2026-03-07",
        "title": "Actividad crítica",
        "short_code": "9",
        "situations": [
            "9.1 Identificar primera actividad de sub-rutas críticas de cada hito.",
        ],
        "solutions": [
            "9.1 Rastrear primera actividad de las rutas críticas generadas por Drill-Down.",
        ],
    },
]

for event in TIMELINE_EVENTS:
    event["anchor_date"] = pd.to_datetime(event["anchor_date"])


# =========================
# UTILIDADES
# =========================
def normalize_numeric(value):
    if pd.isna(value):
        return None
    if value == "-":
        return None
    try:
        return float(value)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_excel_long(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=0, header=None)

    # Columnas fijas
    project_col = 1   # B
    front_col = 2     # C

    records = []
    for row_idx in range(3, len(raw)):
        project = raw.iat[row_idx, project_col]
        front = raw.iat[row_idx, front_col]

        if pd.isna(project):
            continue

        for col_idx in range(4, raw.shape[1], 3):
            date_value = raw.iat[1, col_idx]
            metric_manual = raw.iat[row_idx, col_idx]
            metric_atlas = raw.iat[row_idx, col_idx + 1] if col_idx + 1 < raw.shape[1] else None
            metric_diff = raw.iat[row_idx, col_idx + 2] if col_idx + 2 < raw.shape[1] else None

            if pd.isna(date_value):
                continue

            records.append(
                {
                    "project": str(project).strip(),
                    "front": str(front).strip() if not pd.isna(front) else "Sin frente",
                    "date": pd.to_datetime(date_value),
                    "manual_delay": normalize_numeric(metric_manual),
                    "atlas_delay": normalize_numeric(metric_atlas),
                    "reported_diff": normalize_numeric(metric_diff),
                }
            )

    df = pd.DataFrame(records)
    df = df.sort_values(["project", "front", "date"]).reset_index(drop=True)
    return df


def build_timeline_mapping(df: pd.DataFrame) -> pd.DataFrame:
    timeline_df = pd.DataFrame(TIMELINE_EVENTS)
    available_dates = sorted(df["date"].dropna().unique())

    if not available_dates:
        timeline_df["matched_date"] = pd.NaT
        return timeline_df

    matched_dates = []
    for _, row in timeline_df.iterrows():
        anchor_date = row["anchor_date"]
        nearest = min(available_dates, key=lambda d: abs(pd.Timestamp(d) - anchor_date))
        matched_dates.append(pd.to_datetime(nearest))

    timeline_df["matched_date"] = matched_dates
    return timeline_df


def nearest_timeline_event(selected_date: Optional[pd.Timestamp], timeline_df: pd.DataFrame) -> Optional[str]:
    if selected_date is None or timeline_df.empty:
        return None
    idx = (timeline_df["matched_date"] - selected_date).abs().idxmin()
    return timeline_df.loc[idx, "event_key"]


def render_timeline_cards(timeline_df: pd.DataFrame, active_event_key: Optional[str]):
    st.markdown('<div class="section-title">Línea de tiempo general</div>', unsafe_allow_html=True)

    for _, row in timeline_df.iterrows():
        card_class = "timeline-card-active" if row["event_key"] == active_event_key else "timeline-card"
        with st.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            st.markdown(f'<div class="timeline-date">{row["date_label"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="timeline-title">{row["title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="pill">Fecha vinculada: {pd.to_datetime(row["matched_date"]).strftime("%d %b %Y")}</span>', unsafe_allow_html=True)
            st.markdown('<div class="timeline-subhead">Situaciones identificadas</div>', unsafe_allow_html=True)
            for item in row["situations"]:
                st.markdown(f'<div class="timeline-text">• {item}</div>', unsafe_allow_html=True)
            st.markdown('<div class="timeline-subhead">Soluciones implementadas</div>', unsafe_allow_html=True)
            for item in row["solutions"]:
                st.markdown(f'<div class="timeline-text">• {item}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


def build_line_chart(df_filtered: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df_filtered,
        x="date",
        y="reported_diff",
        color="front",
        markers=True,
        custom_data=["front", "project"],
    )
    fig.update_traces(
        mode="lines+markers",
        line=dict(width=2),
        marker=dict(size=8),
        hovertemplate=(
            "<b>Fecha:</b> %{x|%d %b %Y}<br>"
            "<b>Frente:</b> %{customdata[0]}<br>"
            "<b>Diferencia reportada:</b> %{y}<br>"
            "<extra></extra>"
        ),
    )
    fig.update_layout(
        title="Diferencia reportada por fecha",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="Frente",
        margin=dict(l=10, r=10, t=60, b=20),
        height=430,
        hovermode="x unified",
        xaxis_title="Fecha",
        yaxis_title="Diferencia reportada",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15,39,68,0.08)", zeroline=False)
    return fig


def build_bar_chart(df_front: pd.DataFrame, selected_front: str) -> go.Figure:
    long_df = df_front.melt(
        id_vars=["date", "front", "project"],
        value_vars=["manual_delay", "atlas_delay"],
        var_name="metric",
        value_name="value",
    )
    metric_map = {
        "manual_delay": "Manual",
        "atlas_delay": "3iAtlas",
    }
    long_df["metric"] = long_df["metric"].map(metric_map)

    fig = px.bar(
        long_df,
        x="date",
        y="value",
        color="metric",
        barmode="group",
        custom_data=["front", "metric"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Fecha:</b> %{x|%d %b %Y}<br>"
            "<b>Frente:</b> %{customdata[0]}<br>"
            "<b>Serie:</b> %{customdata[1]}<br>"
            "<b>Valor:</b> %{y}<br>"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        title=f"Manual vs 3iAtlas · {selected_front}",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=60, b=20),
        height=430,
        xaxis_title="Fecha",
        yaxis_title="Días de atraso / adelanto",
        legend_title="Serie",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15,39,68,0.08)", zeroline=False)
    return fig


# =========================
# CARGA DE DATOS
# =========================
if not EXCEL_PATH.exists():
    st.error(f"No se encontró el archivo Excel en: {EXCEL_PATH}")
    st.stop()

try:
    df = load_excel_long(EXCEL_PATH)
except Exception as exc:
    st.error(f"No fue posible leer el Excel: {exc}")
    st.stop()

if df.empty:
    st.warning("No se encontraron datos válidos en el Excel.")
    st.stop()

timeline_df = build_timeline_mapping(df)

# =========================
# HEADER
# =========================
st.markdown('<div class="dashboard-title">Dashboard de calibración 3iAtlas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dashboard-subtitle">Seguimiento por proyecto, frentes y fechas con contraste entre reporte manual y 3iAtlas.</div>',
    unsafe_allow_html=True,
)

# =========================
# FILTROS
# =========================
projects = sorted(df["project"].dropna().unique().tolist())
min_date = pd.to_datetime(df["date"].min()).date()
max_date = pd.to_datetime(df["date"].max()).date()

filter_col1, filter_col2 = st.columns([1.2, 1.1])
with filter_col1:
    selected_project = st.selectbox("Proyecto", options=projects, index=0)
with filter_col2:
    selected_range = st.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if isinstance(selected_range, tuple) and len(selected_range) == 2:
    start_date, end_date = selected_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["project"] == selected_project)
    & (df["date"] >= pd.to_datetime(start_date))
    & (df["date"] <= pd.to_datetime(end_date))
].copy()

if filtered.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()

fronts = sorted(filtered["front"].dropna().unique().tolist())
default_front = fronts[0] if fronts else None

# selector auxiliar discreto para el gráfico de barras
selector_col1, selector_col2, selector_col3 = st.columns([1, 1, 2.3])
with selector_col1:
    selected_front = st.selectbox("Frente destacado", options=fronts, index=0)
with selector_col2:
    show_points = st.toggle("Mostrar marcadores", value=True)
with selector_col3:
    st.markdown(
        '<div style="padding-top: 1.9rem; color:#5A6B7E; font-size:0.9rem;">'
        'La gráfica de línea muestra todos los frentes. La gráfica de barras profundiza en el frente seleccionado.'
        '</div>',
        unsafe_allow_html=True,
    )

front_df = filtered[filtered["front"] == selected_front].copy()

# =========================
# KPIS
# =========================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown('<div class="metric-card"><b>Proyecto</b><br>' + selected_project + '</div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="metric-card"><b>Frentes visibles</b><br>' + str(filtered["front"].nunique()) + '</div>', unsafe_allow_html=True)
with kpi3:
    avg_diff = filtered["reported_diff"].dropna().mean()
    avg_diff_txt = f"{avg_diff:.2f}" if pd.notna(avg_diff) else "N/D"
    st.markdown('<div class="metric-card"><b>Diferencia promedio</b><br>' + avg_diff_txt + '</div>', unsafe_allow_html=True)
with kpi4:
    max_date_txt = pd.to_datetime(filtered["date"].max()).strftime("%d %b %Y")
    st.markdown('<div class="metric-card"><b>Última fecha visible</b><br>' + max_date_txt + '</div>', unsafe_allow_html=True)

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# =========================
# GRÁFICOS SUPERIORES
# =========================
left_col, right_col = st.columns(2)

with left_col:
    line_df = filtered.copy()
    line_fig = build_line_chart(line_df)
    if not show_points:
        line_fig.update_traces(mode="lines", marker=dict(size=0))
    selected_line = st.plotly_chart(
        line_fig,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
    )

with right_col:
    bar_fig = build_bar_chart(front_df, selected_front)
    selected_bar = st.plotly_chart(
        bar_fig,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
    )

# =========================
# INTERACCIÓN FECHA -> TIMELINE
# =========================
selected_date = None

if selected_line and selected_line.selection and selected_line.selection.get("points"):
    first_point = selected_line.selection["points"][0]
    x_value = first_point.get("x")
    if x_value is not None:
        selected_date = pd.to_datetime(x_value)

if selected_date is None and selected_bar and selected_bar.selection and selected_bar.selection.get("points"):
    first_point = selected_bar.selection["points"][0]
    x_value = first_point.get("x")
    if x_value is not None:
        selected_date = pd.to_datetime(x_value)

active_event_key = nearest_timeline_event(selected_date, timeline_df)

# =========================
# TABLA RESUMEN
# =========================
with st.expander("Ver tabla de detalle filtrada", expanded=False):
    detail = filtered.copy()
    detail["date"] = detail["date"].dt.strftime("%Y-%m-%d")
    detail = detail.rename(
        columns={
            "project": "Proyecto",
            "front": "Frente",
            "date": "Fecha",
            "manual_delay": "Manual",
            "atlas_delay": "3iAtlas",
            "reported_diff": "Diferencia reportada",
        }
    )
    st.dataframe(detail, use_container_width=True, hide_index=True)

# =========================
# LÍNEA DE TIEMPO
# =========================
render_timeline_cards(timeline_df, active_event_key)
