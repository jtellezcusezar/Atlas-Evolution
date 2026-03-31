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
            margin-top: 1.25rem;
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
        .timeline-wrapper {
            background: white;
            border: 1px solid #E3E8EF;
            border-radius: 18px;
            padding: 0.6rem 0.8rem 0.1rem 0.8rem;
            box-shadow: 0 2px 10px rgba(16, 24, 40, 0.04);
            margin-bottom: 0.6rem;
        }
        .timeline-detail-active {
            background: #EEF5FF;
            border: 1px solid #B9D4FF;
            border-radius: 18px;
            padding: 0.8rem 1rem;
            box-shadow: 0 3px 12px rgba(57, 106, 177, 0.10);
        }
            background: #EEF5FF;
            border: 1px solid #B9D4FF;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            box-shadow: 0 3px 12px rgba(57, 106, 177, 0.10);
        }
        .timeline-detail-date {
            font-size: 0.82rem;
            font-weight: 700;
            color: #3A5D8A;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .timeline-detail-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #122B46;
            margin-top: 0.1rem;
            margin-bottom: 0.65rem;
        }
        .timeline-subhead {
            font-size: 0.92rem;
            font-weight: 700;
            color: #244567;
            margin-top: 0.2rem;
            margin-bottom: 0.35rem;
        }
        .timeline-text {
            font-size: 0.92rem;
            color: #405469;
            line-height: 1.45;
            margin-bottom: 0.25rem;
        }
            font-size: 0.92rem;
            color: #405469;
            line-height: 1.45;
            margin-bottom: 0.2rem;
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
        "event_key": "hito_1",
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
        "event_key": "hito_2",
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
        "event_key": "hito_3",
        "date_label": "12 Nov 2025",
        "anchor_date": "2025-11-22",
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
        "event_key": "hito_4",
        "date_label": "14–20 Nov 2025",
        "anchor_date": "2025-11-29",
        "title": "Atrasos - Adelantos",
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
        "event_key": "hito_5",
        "date_label": "21 Nov 2025",
        "anchor_date": "2025-11-29",
        "title": "Configuración MProject",
        "short_code": "5",
        "situations": [
            "5.1 Identificar hitos de finalización.",
            "5.2 Cálculo automático de programación en actividades.",
        ],
        "solutions": [
            "5.1 Estandarizar nombres de hitos informando fecha.",
            "5.2 Configurar actividades finalizadas y en ejecución en manual para evitar movimientos no deseados.",
        ],
    },
    {
        "event_key": "hito_6",
        "date_label": "04 Dic 2025",
        "anchor_date": "2025-12-13",
        "title": "Lógica programación (FC, CC, CF, FF)",
        "short_code": "6",
        "situations": [
            "6.1 Tener en cuenta la lógica de programación (FC, CC, CF y FF).",
        ],
        "solutions": [
            "6.1 La eliminación de dependencias en sucesoras debe seguir una lógica con condicionales.",
        ],
    },
    {
        "event_key": "hito_7",
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
        "event_key": "hito_8",
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
        "event_key": "hito_9",
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

    project_col = 1  # B
    front_col = 2    # C

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


def build_line_chart(df_filtered: pd.DataFrame, show_points: bool) -> go.Figure:
    fig = px.line(
        df_filtered,
        x="date",
        y="reported_diff",
        color="front",
        markers=show_points,
        custom_data=["front", "project"],
    )

    mode_value = "lines+markers" if show_points else "lines"

    fig.update_traces(
        mode=mode_value,
        line=dict(width=2),
        marker=dict(size=8),
        hovertemplate=(
            "<b>Fecha:</b> %{x|%d %b %Y}<br>"
            "<b>Frente:</b> %{customdata[0]}<br>"
            "<b>Diferencia reportada:</b> %{y}<br>"
            "<extra></extra>"
        ),
    )

    milestone_dates = [
        pd.Timestamp("2025-10-30"),
        pd.Timestamp("2025-11-06"),
        pd.Timestamp("2025-11-12"),
        pd.Timestamp("2025-11-17"),
        pd.Timestamp("2025-11-21"),
        pd.Timestamp("2025-12-04"),
        pd.Timestamp("2025-12-17"),
        pd.Timestamp("2026-02-23"),
        pd.Timestamp("2026-03-04"),
    ]
    milestone_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    milestone_keys = [
        "hito_1", "hito_2", "hito_3", "hito_4", "hito_5", "hito_6", "hito_7", "hito_8", "hito_9"
    ]
    milestone_y = -0.5

    y_series = df_filtered["reported_diff"].dropna()
    if y_series.empty:
        y_min_data = 0.0
        y_max_data = 0.0
    else:
        y_min_data = float(y_series.min())
        y_max_data = float(y_series.max())

    y_min = min(y_min_data, milestone_y) - 0.25
    y_max = max(y_max_data, 0.0) + 0.25
    if y_max - y_min < 1.0:
        center = (y_max + y_min) / 2
        y_min = center - 0.6
        y_max = center + 0.6

    for milestone_date in milestone_dates:
        fig.add_shape(
            type="line",
            x0=milestone_date,
            x1=milestone_date,
            y0=milestone_y,
            y1=y_max,
            xref="x",
            yref="y",
            line=dict(color="rgba(229,72,77,0.8)", width=1, dash="dot"),
            layer="below",
        )

    fig.add_trace(
        go.Scatter(
            x=milestone_dates,
            y=[milestone_y] * len(milestone_dates),
            mode="lines+markers+text",
            text=milestone_labels,
            textposition="top center",
            textfont=dict(size=11, color="#A13A3F"),
            marker=dict(size=11, color="#E5484D", line=dict(color="#C9353A", width=2)),
            line=dict(color="rgba(233,167,170,0.0)", width=2, dash="dot"),
            name="",
            showlegend=False,
            hovertemplate="<b>Hito %{text}</b><br>%{x|%d %b %Y}<extra></extra>",
            customdata=[[k, "milestone"] for k in milestone_keys],
        )
    )

    fig.update_layout(
        title="Diferencia reportada por fecha",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="Frente",
        margin=dict(l=10, r=10, t=60, b=80),
        height=430,
        hovermode="x unified",
        xaxis_title="Fecha",
        yaxis_title="Diferencia reportada",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.30,
            xanchor="center",
            x=0.5,
        ),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15,39,68,0.08)", zeroline=False, range=[y_min, y_max])
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


def build_timeline_chart(timeline_df: pd.DataFrame, active_event_key: Optional[str]) -> go.Figure:
    plot_df = timeline_df.copy().reset_index(drop=True)
    plot_df["x_pos"] = list(range(1, len(plot_df) + 1))
    plot_df["y_pos"] = 1
    plot_df["is_active"] = plot_df["event_key"] == active_event_key
    plot_df["marker_color"] = plot_df["is_active"].map({True: "#E5484D", False: "#B9D9F7"})
    plot_df["marker_line"] = plot_df["is_active"].map({True: "#C9353A", False: "#7EB8E6"})
    plot_df["marker_size"] = plot_df["is_active"].map({True: 22, False: 20})
    plot_df["date_text"] = plot_df["date_label"]
    plot_df["title_text"] = plot_df["title"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot_df["x_pos"],
            y=plot_df["y_pos"],
            mode="lines",
            line=dict(color="#B9D9F7", width=6),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_df["x_pos"],
            y=plot_df["y_pos"],
            mode="markers",
            marker=dict(
                size=plot_df["marker_size"],
                color=plot_df["marker_color"],
                line=dict(color=plot_df["marker_line"], width=3),
            ),
            customdata=plot_df[["event_key", "date_label", "title"]].values,
            hovertemplate=(
                "<b>%{customdata[1]}</b><br>"
                "%{customdata[2]}<br>"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_df["x_pos"],
            y=[0.955] * len(plot_df),
            mode="text",
            text=plot_df["date_text"],
            textposition="middle center",
            textfont=dict(size=12, color="#163A63"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_df["x_pos"],
            y=[0.915] * len(plot_df),
            mode="text",
            text=plot_df["title_text"],
            textposition="middle center",
            textfont=dict(size=12, color="#163A63"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=140,
        margin=dict(l=15, r=15, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True,
            range=[0.88, 1.06],
        ),
        dragmode=False,
        clickmode="event+select",
    )
    return fig


def render_timeline_detail(timeline_df: pd.DataFrame, active_event_key: Optional[str]):
    if active_event_key is None:
        row = timeline_df.iloc[0]
    else:
        row = timeline_df[timeline_df["event_key"] == active_event_key].iloc[0]

    st.markdown('<div class="section-title">Detalle del hito seleccionado</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="timeline-detail-date">{row["date_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="timeline-detail-title">{row["title"]}</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="timeline-subhead">Situaciones identificadas</div>', unsafe_allow_html=True)
        for item in row["situations"]:
            st.markdown(f'<div class="timeline-text">• {item}</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="timeline-subhead">Soluciones implementadas</div>', unsafe_allow_html=True)
        for item in row["solutions"]:
            st.markdown(f'<div class="timeline-text">• {item}</div>', unsafe_allow_html=True)


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
header_col1, header_col2 = st.columns([1.7, 1.7])
with header_col1:
    st.markdown('<div class="dashboard-title">Dashboard de calibración 3iAtlas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-subtitle">Seguimiento por proyecto, frentes y fechas con contraste entre reporte manual y 3iAtlas.</div>',
        unsafe_allow_html=True,
    )
with header_col2:
    st.markdown(
        '''
        <div style="display:flex; gap:10px; justify-content:flex-end; align-items:flex-start; flex-wrap:nowrap; margin-top:1.1rem;">
            <div style="background:white; border:1px solid #E3E8EF; border-radius:14px; padding:0.5rem 0.75rem; box-shadow:0 2px 10px rgba(16,24,40,0.04); font-size:0.84rem; color:#17324F; min-width:210px;">
                <b>En prueba</b><br>Manual: 28% &nbsp;|&nbsp; 3iAtlas: 72%
            </div>
            <div style="background:white; border:1px solid #E3E8EF; border-radius:14px; padding:0.5rem 0.75rem; box-shadow:0 2px 10px rgba(16,24,40,0.04); font-size:0.84rem; color:#17324F; min-width:250px;">
                <b>Calibrados</b><br>Manual/no calibrados: 33% &nbsp;|&nbsp; 3iAtlas/calibrados: 67%
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

# =========================
# FILTROS
# =========================
projects = sorted(df["project"].dropna().unique().tolist())
filter_col1, filter_col2, filter_col3 = st.columns([1.3, 1.2, 1.1])
with filter_col1:
    selected_project = st.selectbox("Proyecto", options=projects, index=0)

filtered = df[df["project"] == selected_project].copy()

if filtered.empty:
    st.warning("No hay datos para el proyecto seleccionado.")
    st.stop()

fronts = sorted(filtered["front"].dropna().unique().tolist())

with filter_col2:
    selected_front = st.selectbox("Frente destacado", options=fronts, index=0)
with filter_col3:
    show_points = st.toggle("Mostrar marcadores", value=True)

front_df = filtered[filtered["front"] == selected_front].copy()

st.markdown("<div style='height:0.2rem'></div>", unsafe_allow_html=True)

# =========================
# GRÁFICOS SUPERIORES
# =========================
left_col, right_col = st.columns(2)

with left_col:
    line_fig = build_line_chart(filtered.copy(), show_points)
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
selected_event_key = None

if selected_line and selected_line.selection and selected_line.selection.get("points"):
    point = selected_line.selection["points"][0]
    customdata = point.get("customdata")
    x_value = point.get("x")

    if customdata and len(customdata) >= 2 and customdata[1] == "milestone":
        selected_event_key = customdata[0]
    elif x_value is not None:
        selected_date = pd.to_datetime(x_value)

if selected_event_key is None and selected_bar and selected_bar.selection and selected_bar.selection.get("points"):
    first_point = selected_bar.selection["points"][0]
    x_value = first_point.get("x")
    if x_value is not None:
        selected_date = pd.to_datetime(x_value)

auto_event_key = selected_event_key if selected_event_key is not None else nearest_timeline_event(selected_date, timeline_df)

timeline_keys = timeline_df["event_key"].tolist()

if "timeline_selected_key" not in st.session_state:
    st.session_state["timeline_selected_key"] = timeline_keys[0]

if auto_event_key is not None:
    st.session_state["timeline_selected_key"] = auto_event_key

st.markdown('<div class="section-title">Línea de tiempo general</div>', unsafe_allow_html=True)
timeline_fig = build_timeline_chart(timeline_df, st.session_state["timeline_selected_key"])
timeline_selection = st.plotly_chart(
    timeline_fig,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points",
)

if timeline_selection and timeline_selection.selection and timeline_selection.selection.get("points"):
    point = timeline_selection.selection["points"][0]
    customdata = point.get("customdata")
    if customdata and len(customdata) > 0:
        st.session_state["timeline_selected_key"] = customdata[0]

render_timeline_detail(timeline_df, st.session_state["timeline_selected_key"])

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
