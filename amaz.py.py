import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Amazonas · Investigación de Mercados cuantitativa",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS mínimo solo para fondo y fuente — sin tocar el DOM de React ───────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;}
.stApp{background:linear-gradient(160deg,#0D1F15 0%,#091510 100%)!important;}
[data-testid="stSidebar"]{background:#0f2118!important;border-right:1px solid #1e4228!important;}
[data-testid="stSidebar"] *{color:#c8e6d0!important;}
h1,h2,h3{color:#7DC896!important;}
p,li{color:#c8e6d0!important;}
.stMetric label{color:#9DC4AA!important;}
.stMetric [data-testid="metric-container"] > div{color:#7DC896!important;}
div[data-testid="stMetricValue"] > div{color:#7DC896!important;font-size:2rem!important;}
</style>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for path in [
        os.path.join(script_dir, 'amazonas1__2_.xlsx'),
        os.path.join(script_dir, 'amazonas1 (2).xlsx'),
        'amazonas1__2_.xlsx',
    ]:
        if os.path.exists(path):
            break
    else:
        st.error("No se encontró el archivo Excel. Ponlo en la misma carpeta que app.py")
        st.stop()

    df = pd.read_excel(path)
    df = df[df['edad'] <= 100].copy()
    costos_cols    = ['pre_costo_comparativo_inv','pre_duda_paquete_inv','pre_falta_transparencia_inv']
    miedos_cols    = ['miedo_seguridad_general_inv','miedo_animales_inve','miedo_insectos_inv',
                      'miedo_salud_enfermedad_inv','miedo_ermegencia_medica_inv']
    confort_cols   = ['serv_higene_hotel_inv','serv_seguridad_alimentaria_inv','serv_conectividad_inv']
    marketing_cols = ['comu_poca_info_turismo_inv','comu_nunca_info_guias_locales_inv',
                      'comu_infor_guia_confianza','comu_tourtradi_suficiente']
    intencion_cols = ['inten_decision_infor_clara','inten_guia_experto','inten_reonexion_paz',
                      'inten_lista_destinos','inten_proximo_principales','inten_viaje_24meses']
    df['score_costos']    = df[costos_cols].mean(axis=1)
    df['score_miedos']    = df[miedos_cols].mean(axis=1)
    df['score_confort']   = df[confort_cols].mean(axis=1)
    df['score_marketing'] = df[marketing_cols].mean(axis=1)
    df['score_intencion'] = df[intencion_cols].mean(axis=1)
    return df

df = load()

# ── Plotly helpers ────────────────────────────────────────────────────────────
BG  = 'rgba(0,0,0,0)'
PBG = 'rgba(15,33,24,0.7)'
FC  = '#B2DFC0'
GC  = 'rgba(58,125,68,0.2)'
PAL = ['#52A96D','#C9A84C','#7DC896','#3A7D44','#E8C97A','#B2DFC0','#235430']

def layout(h=360, **kw):
    d = dict(paper_bgcolor=BG, plot_bgcolor=PBG,
             font=dict(family='DM Sans', color=FC, size=12),
             margin=dict(l=45, r=25, t=50, b=45),
             height=h,
             legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=FC, size=11)))
    d.update(kw)
    return d

def ax(**kw):
    return dict(gridcolor=GC, linecolor='rgba(58,125,68,.3)',
                tickcolor='rgba(58,125,68,.3)', zerolinecolor=GC,
                tickfont=dict(color=FC), **kw)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌿 Amazonas")
    st.caption("Investigación de Mercados II · 2026-1")
    st.divider()
    page = st.radio("Navegación", [
        "🌍  ¿Quiénes respondieron?",
        "🔬  Instrumento (α y ω)",
        "📊  Estadísticos descriptivos",
        "🔗  Correlaciones de Pearson",
        "📐  ANOVA",
        "✅  Hipótesis & Chi²",
        "🎯  Conclusiones",
    ], label_visibility="collapsed")
    st.divider()
    st.caption("Paula Ríos · Caterine Quevedo · Samir Neme\nUniversidad Santo Tomás")

# ── Title always shown ────────────────────────────────────────────────────────
st.title("🌿 Percepción y Decisión de Viaje al Amazonas Colombiano")
st.caption("Influencia de costos, miedos y confort en la intención de compra · Bogotá D.C. · n = 114")
st.divider()

# ═══════════════════════════════════════════════════════════
# 1 — ¿QUIÉNES RESPONDIERON?
# ═══════════════════════════════════════════════════════════
if "Quiénes" in page:
    st.subheader("👥 Perfil de los 114 encuestados")
    st.caption("Tablas de frecuencia · Caracterización sociodemográfica")

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total encuestados", "114")
    k2.metric("Género femenino", "66.4 %", "75 personas")
    k3.metric("Estrato dominante", "Estrato 3", "53.1 %")
    k4.metric("Edad promedio", "29.9 años", "mediana 25")

    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = go.Figure(go.Pie(
            labels=['Femenino', 'Masculino'], values=[75, 39],
            hole=.55,
            marker=dict(colors=['#52A96D','#C9A84C'],
                        line=dict(color='#091510', width=2)),
            textfont=dict(color='#E8F5EC', size=13),
            hovertemplate='%{label}: %{value} (%{percent})<extra></extra>'
        ))
        fig.update_layout(**layout(h=290,
            title=dict(text='Distribución por sexo', font=dict(size=13, color=FC), x=.5),
            annotations=[dict(text='n=114', x=.5, y=.5,
                              font=dict(size=13, color='#7DC896'), showarrow=False)]
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure(go.Bar(
            x=[f'E{i}' for i in range(1, 6)],
            y=[2, 20, 60, 29, 2],
            marker=dict(color=PAL, line=dict(color='rgba(0,0,0,.3)', width=1)),
            text=['1.8%','17.7%','53.1%','25.7%','1.8%'],
            textposition='outside', textfont=dict(color=FC, size=11),
            hovertemplate='Estrato %{x}: %{y} personas<extra></extra>'
        ))
        fig.update_layout(**layout(h=290,
            title=dict(text='Estrato socioeconómico', font=dict(size=13, color=FC), x=.5),
            xaxis=ax(), yaxis=ax(title='Frecuencia')
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        ing_lbl = ['< 1 SMMLV','1–2','2–3','3–4','> 4']
        ing_n   = [df[df['nivel_de_ingresos']==g].shape[0]
                   for g in ['menos de 1 smmlv','entre 1-2 smmlv','entre 2-3 smmlv',
                              'entre 3-4 smmlv','mas de 4 smmlv']]
        fig = go.Figure(go.Bar(
            x=ing_n, y=ing_lbl, orientation='h',
            marker=dict(color=PAL, line=dict(color='rgba(0,0,0,.3)', width=1)),
            text=ing_n, textposition='outside', textfont=dict(color=FC, size=11),
            hovertemplate='%{y}: %{x} personas<extra></extra>'
        ))
        fig.update_layout(**layout(h=290,
            title=dict(text='Nivel de ingresos', font=dict(size=13, color=FC), x=.5),
            xaxis=ax(title='Frecuencia'), yaxis=ax()
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.info("📌 **Perfil dominante:** Mujer (66.4 %), estrato 3 (53.1 %), entre 22–36 años, ingresos 1–3 SMMLV. Clase media bogotana con acceso digital y capacidad real de consumo turístico.")

    st.divider()
    st.caption("Tabla de frecuencias — Sexo y Estrato")
    freq_df = pd.DataFrame({
        'Variable': ['Femenino','Masculino','Estrato 1','Estrato 2','Estrato 3','Estrato 4','Estrato 5'],
        'n':        [75, 39, 2, 20, 60, 29, 2],
        '%':        [66.4, 33.6, 1.8, 17.7, 53.1, 25.7, 1.8],
    })
    st.dataframe(freq_df, use_container_width=True, hide_index=True, height=285)

# ═══════════════════════════════════════════════════════════
# 2 — INSTRUMENTO
# ═══════════════════════════════════════════════════════════
elif "Instrumento" in page:
    st.subheader("🔬 Confiabilidad del instrumento")
    st.caption("α de Cronbach · ω de McDonald · Umbral aceptable ≥ 0.70")

    st.write("El cuestionario tiene **5 dimensiones** en escala Likert 1–7. Verificamos que cada bloque sea internamente consistente antes de usarlo en el análisis.")

    rel = [
        ('Costos percibidos',    0.594, 0.597, '#E8C97A', 'Moderada'),
        ('Miedos percibidos',    0.806, 0.809, '#52A96D', 'Alta ✓'),
        ('Nivel de confort',     0.521, 0.524, '#E8C97A', 'Moderada'),
        ('Marketing',           -0.019,-0.016, '#E07B54', 'Baja ✗'),
        ('Intención de compra',  0.746, 0.749, '#52A96D', 'Alta ✓'),
    ]
    dims_r   = [r[0] for r in rel]
    alphas   = [r[1] for r in rel]
    omegas   = [r[2] for r in rel]
    colors_r = [r[3] for r in rel]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='α Cronbach', x=dims_r, y=alphas,
        marker=dict(color=colors_r, opacity=.85,
                    line=dict(color='rgba(0,0,0,.3)', width=1)),
        text=[f'{v:.3f}' for v in alphas],
        textposition='outside', textfont=dict(color=FC, size=12)
    ))
    fig.add_trace(go.Scatter(
        name='ω McDonald', x=dims_r, y=omegas,
        mode='markers',
        marker=dict(color='white', size=10, symbol='diamond',
                    line=dict(color='#C9A84C', width=2))
    ))
    fig.add_hline(y=0.70, line_dash='dot', line_color='rgba(255,255,255,.5)',
                  annotation_text='Umbral 0.70',
                  annotation_font=dict(color=FC, size=11),
                  annotation_position='top right')
    fig.update_layout(**layout(h=400,
        title=dict(text='α de Cronbach y ω de McDonald por dimensión',
                   font=dict(size=13, color=FC), x=.5),
        xaxis=ax(), yaxis=ax(title='Coeficiente', range=[-0.2, 1.05]),
        barmode='group'
    ))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.success("**Miedos (α=0.806)** y **Intención (α=0.746)** superan 0.70 — dimensiones centrales del análisis.")
    c2.warning("**Costos (0.594)** y **Confort (0.521)** son moderados. Resultados orientativos.")
    c3.error("**Marketing (α=−0.019):** sin consistencia. El Amazonas no tiene mensaje unificado.")

    st.divider()
    df_rel = pd.DataFrame({
        'Dimensión':       dims_r,
        'α Cronbach':      alphas,
        'ω McDonald':      omegas,
        'Interpretación':  [r[4] for r in rel],
    })
    st.dataframe(df_rel, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════
# 3 — ESTADÍSTICOS DESCRIPTIVOS
# ═══════════════════════════════════════════════════════════
elif "Estadísticos" in page:
    st.subheader("📊 ¿Cómo perciben los encuestados cada dimensión?")
    st.caption("Media · Mediana · D.E. · Varianza · Escala 1–7")

    labels  = ['Costos percibidos','Miedos percibidos','Nivel de confort','Marketing','Intención de compra']
    means   = [3.850, 2.993, 3.643, 4.288, 5.295]
    medians = [3.667, 3.000, 3.667, 4.250, 5.333]
    sds     = [1.277, 1.418, 1.279, 0.880, 1.122]
    variances=[1.631, 2.011, 1.636, 0.775, 1.260]

    # Metrics row
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, lbl, m in zip([m1,m2,m3,m4,m5], labels, means):
        col.metric(lbl.split()[0], f"{m:.2f}", f"D.E. {sds[labels.index(lbl)]:.2f}")

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        # Radar
        lc = labels + [labels[0]]
        mc = means  + [means[0]]
        fig = go.Figure(go.Scatterpolar(
            r=mc, theta=lc, fill='toself',
            fillcolor='rgba(58,125,68,0.2)',
            line=dict(color='#52A96D', width=2.5),
            marker=dict(color='#7DC896', size=8)
        ))
        fig.update_layout(**layout(h=370,
            polar=dict(
                bgcolor='rgba(15,33,24,.6)',
                radialaxis=dict(visible=True, range=[0,7],
                                tickfont=dict(color=FC, size=9),
                                gridcolor=GC, linecolor=GC),
                angularaxis=dict(tickfont=dict(color=FC, size=11),
                                 linecolor=GC, gridcolor=GC)
            ),
            title=dict(text='Perfil de medias (1–7)', font=dict(size=13, color=FC), x=.5)
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Tabla descriptiva
        df_desc = pd.DataFrame({
            'Dimensión':  labels,
            'Media':      means,
            'Mediana':    medians,
            'D.E.':       sds,
            'Varianza':   variances,
        })
        st.dataframe(df_desc, use_container_width=True, hide_index=True, height=215)
        st.info("📌 **Intención de compra** es la dimensión más alta (M=5.30). **Miedos** tienen la mayor varianza (2.01): la percepción de riesgo es muy heterogénea entre encuestados.")

    # Gráfica de medias con error bars
    fig2 = go.Figure(go.Bar(
        x=labels, y=means,
        error_y=dict(type='data', array=sds, visible=True,
                     color='rgba(255,255,255,.5)', thickness=1.5, width=6),
        marker=dict(color=['#C9A84C','#E07B54','#C9A84C','#7DC896','#52A96D'],
                    line=dict(color='rgba(0,0,0,.3)', width=1)),
        text=[f'{m:.2f}' for m in means],
        textposition='outside', textfont=dict(color=FC, size=12),
        hovertemplate='%{x}<br>Media: %{y:.3f}<extra></extra>'
    ))
    fig2.add_hline(y=4, line_dash='dot', line_color='rgba(255,255,255,.3)',
                   annotation_text='Punto neutro (4)',
                   annotation_font=dict(color=FC, size=11),
                   annotation_position='top left')
    fig2.update_layout(**layout(h=330,
        title=dict(text='Media ± D.E. por dimensión', font=dict(size=13, color=FC), x=.5),
        xaxis=ax(), yaxis=ax(title='Media (1–7)', range=[0, 7.5])
    ))
    st.plotly_chart(fig2, use_container_width=True)
    st.warning("Solo **Marketing** e **Intención** superan el punto neutro (4). Costos, Miedos y Confort están por debajo — son las barreras activas que frenan la decisión de viaje.")

# ═══════════════════════════════════════════════════════════
# 4 — CORRELACIONES
# ═══════════════════════════════════════════════════════════
elif "Correlaciones" in page:
    st.subheader("🔗 ¿Qué variables se relacionan con la intención de compra?")
    st.caption("Correlación r de Pearson · α = 0.05")

    st.write("Medimos la fuerza y dirección de la relación lineal entre cada dimensión y la **intención de compra**. Un r negativo significa que a mayor percepción negativa, *menor* intención.")

    corr_data = [
        ('Costos percibidos',  -0.1712, 0.0698),
        ('Miedos percibidos',  -0.2517, 0.0072),
        ('Nivel de confort',   -0.1537, 0.1041),
        ('Marketing',           0.0188, 0.8434),
    ]
    lbs     = [c[0] for c in corr_data]
    rs      = [c[1] for c in corr_data]
    ps      = [c[2] for c in corr_data]
    bar_clr = ['#52A96D' if p < 0.05 else '#2a4a33' for p in ps]

    fig = go.Figure(go.Bar(
        x=lbs, y=rs,
        marker=dict(color=bar_clr, line=dict(color='rgba(0,0,0,.3)', width=1)),
        text=[f'r={r:.3f}  p={p:.3f}' for r, p in zip(rs, ps)],
        textposition='outside', textfont=dict(color=FC, size=12),
        hovertemplate='%{x}<br>r = %{y:.4f}<extra></extra>'
    ))
    fig.add_hline(y=0, line_color='rgba(255,255,255,.2)')
    fig.update_layout(**layout(h=370,
        title=dict(text='Correlación con Intención de Compra  (verde = significativa, p < 0.05)',
                   font=dict(size=12, color=FC), x=.5),
        xaxis=ax(), yaxis=ax(title='r de Pearson', range=[-0.45, 0.18])
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Scatter miedos vs intención
    x_ = df['score_miedos'].dropna()
    y_ = df.loc[x_.index, 'score_intencion']
    m_, b_, r_, _, _ = stats.linregress(x_, y_)
    xline = np.linspace(x_.min(), x_.max(), 80)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=x_, y=y_, mode='markers',
        marker=dict(color='#E07B54', opacity=.65, size=7,
                    line=dict(color='white', width=.5)),
        name='Encuestados',
        hovertemplate='Miedo: %{x:.2f}<br>Intención: %{y:.2f}<extra></extra>'
    ))
    fig2.add_trace(go.Scatter(
        x=xline, y=m_*xline + b_, mode='lines',
        line=dict(color='white', width=2, dash='dash'),
        name='r = −0.252  p = 0.007'
    ))
    fig2.update_layout(**layout(h=320,
        title=dict(text='Miedos percibidos vs Intención de compra',
                   font=dict(size=13, color=FC), x=.5),
        xaxis=ax(title='Miedos percibidos'),
        yaxis=ax(title='Intención de compra')
    ))
    st.plotly_chart(fig2, use_container_width=True)

    st.success("⭐ **Única correlación significativa:** Miedos → Intención (r = −0.252, p = 0.007). A más miedo, menos intención. Las demás variables no alcanzan p < 0.05.")

    st.divider()
    df_corr = pd.DataFrame({
        'Variable':   lbs,
        'r Pearson':  [f'{r:.4f}' for r in rs],
        'p-valor':    [f'{p:.4f}' for p in ps],
        'Sig. (α=0.05)': ['✓ Sí' if p < 0.05 else '✗ No' for p in ps],
    })
    st.dataframe(df_corr, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════
# 5 — ANOVA
# ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════
# 5 — ANOVA (CORREGIDO Y ESTILIZADO)
# ═══════════════════════════════════════════════════════════
elif "ANOVA" in page:
    st.subheader("📐 ¿Varía la intención según el perfil del encuestado?")
    st.caption("ANOVA de un factor · Nivel de significancia α = 0.05")

    st.markdown("""
    <div style="background-color: #f0fdf4; padding: 18px; border-radius: 8px; border-left: 5px solid #10b981; margin-bottom: 20px;">
        <span style="color: #166534; font-weight: bold;">🏛️ Storytelling de Datos: Bogotá como Mercado Homogéneo</span><br>
        <span style="color: #1f2937; font-size: 14px;">
            Para evaluar si el nivel adquisitivo o los hábitos de viaje fragmentan el mercado, analizamos las variaciones de medias. Al ejecutar el análisis de varianza (<b>ANOVA</b>), observamos que todos los p-valores son superiores a 0.05. En términos gerenciales, esto demuestra que <b>no existen diferencias significativas entre grupos</b>. La intención de viaje es igual de sólida sin importar el estrato o los ingresos.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 1. Tabla de resultados ANOVA matemáticos de la tesis
    anova_rows = [
        ('Estrato socioeconómico', '5 Grupos', '1.0813', '0.3695', '✗ No significativo'),
        ('Nivel de ingresos', '5 Grupos', '1.7156', '0.1518', '✗ No significativo'),
        ('Frecuencia de viaje', '5 Grupos', '0.9191', '0.4557', '✗ No significativo'),
    ]
    
    df_tabla_anova = pd.DataFrame(anova_rows, columns=['Variable Demográfica', 'Grupos Comparados', 'Estadístico F', 'p-valor', 'Resultado'])
    
    st.markdown("<p style='font-weight:600; color:#B2DFC0; margin-bottom:8px;'>Matriz de Contraste de Hipótesis (ANOVA)</p>", unsafe_allow_html=True)
    st.dataframe(df_tabla_anova, use_container_width=True, hide_index=True)

    st.divider()

    # 2. Gráfico de Medias por Frecuencia de Viaje
    col_izq, col_der = st.columns([1.2, 0.8])
    
    with col_izq:
        freq_lbl  = ['Nunca', '1 vez/año', '2–3 veces', '3–4 veces', '> 4 veces']
        freq_mean = [4.222, 5.387, 5.207, 5.456, 5.444]
        freq_n    = [3, 47, 45, 15, 3]

        fig_anova = go.Figure(go.Bar(
            x=freq_lbl, y=freq_mean,
            marker=dict(
                color=freq_mean,
                colorscale=[[0, '#1A3D24'], [0.5, '#3A7D44'], [1, '#7DC896']],
                line=dict(color='rgba(0,0,0,.3)', width=1)
            ),
            text=[f'{m:.2f} (n={n})' for m, n in zip(freq_mean, freq_n)],
            textposition='outside', textfont=dict(color=FC, size=11),
            hovertemplate='Frecuencia: %{x}<br>Media Intención: %{y:.3f}'
        ))
        
        fig_anova.add_hline(y=5.295, line_dash='dot', line_color='rgba(255,255,255,.5)',
                             annotation_text='Media global (5.30)',
                             annotation_font=dict(color=FC, size=11),
                             annotation_position='top right')
        
        fig_anova.update_layout(**layout(h=340,
            title=dict(text='Estabilidad de la Intención de Compra por Frecuencia de Viaje', font=dict(size=13, color=FC), x=.5),
            xaxis=ax(), yaxis=ax(title='Media Intención (1-7)', range=[0, 7])
        ))
        st.plotly_chart(fig_anova, use_container_width=True)

    with col_der:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("💡 **Conclusión Estratégica:** Al confirmarse que el p-valor (0.46) es mayor a 0.05, el comportamiento del consumidor es **transversal**. No gastes presupuesto segmentando campañas publicitarias en Bogotá por niveles demográficos; el mercado reacciona como una sola masa homogénea.")
# ═══════════════════════════════════════════════════════════
# 6 — HIPÓTESIS & CHI²
# ═══════════════════════════════════════════════════════════
elif "Hipótesis" in page:
    st.subheader("✅ Pruebas de hipótesis")
    st.caption("Pearson · Chi² · p-valor · α = 0.05")

    # Hipótesis correlacionales
    st.write("**Hipótesis correlacionales (r de Pearson)**")

    hyps = [
        ('H1a', 'Costos percibidos → Intención de compra',   -0.1712, 0.0698, False),
        ('H1b', 'Miedos percibidos → Intención de compra',   -0.2517, 0.0072, True),
        ('H1c', 'Nivel de confort → Intención de compra',    -0.1537, 0.1041, False),
        ('H1d', 'Marketing → Intención de compra',            0.0188, 0.8434, False),
    ]

    df_hyp = pd.DataFrame({
        'ID':       [h[0] for h in hyps],
        'Hipótesis':[h[1] for h in hyps],
        'r':        [f'{h[2]:.4f}' for h in hyps],
        'p-valor':  [f'{h[3]:.4f}' for h in hyps],
        'Decisión': ['✓ Se acepta' if h[4] else '✗ No se acepta' for h in hyps],
    })
    st.dataframe(df_hyp, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    c1.success("**H1b aceptada:** Los miedos tienen relación significativa negativa con la intención de compra (r=−0.252, p=0.007).")
    c2.error("**H1a, H1c, H1d rechazadas:** Costos, confort y marketing no alcanzan significancia estadística en esta muestra.")

    st.divider()

    # Chi-cuadrado
    st.write("**Estadística inferencial — Chi² de Pearson**")
    st.write("¿Descartar el viaje por miedo depende del sexo o del estrato?")

    chi_data = [
        ('Descarte del viaje × Sexo',    0.0184, 1, 0.8920, '✗ Sin asociación'),
        ('Descarte del viaje × Estrato', 1.5381, 4, 0.8199, '✗ Sin asociación'),
    ]
    df_chi = pd.DataFrame({
        'Prueba':     [c[0] for c in chi_data],
        'χ²':         [f'{c[1]:.4f}' for c in chi_data],
        'gl':         [c[2] for c in chi_data],
        'p-valor':    [f'{c[3]:.4f}' for c in chi_data],
        'Decisión':   [c[4] for c in chi_data],
    })
    st.dataframe(df_chi, use_container_width=True, hide_index=True)

    col1, col2 = st.columns([1, 1.3])

    with col1:
        fig = go.Figure(go.Pie(
            labels=['Sí descartó el viaje', 'No descartó'],
            values=[59, 54],
            hole=.58,
            marker=dict(colors=['#E07B54','#52A96D'],
                        line=dict(color='#091510', width=2)),
            textfont=dict(color='#E8F5EC', size=13),
            hovertemplate='%{label}: %{value} (%{percent})<extra></extra>'
        ))
        fig.update_layout(**layout(h=300,
            title=dict(text='¿Descartó viajar al Amazonas por miedo?',
                       font=dict(size=12, color=FC), x=.5),
            annotations=[dict(text='52.2%<br>sí descartó',
                               x=.5, y=.5,
                               font=dict(size=12, color='#E07B54'),
                               showarrow=False)]
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("")
        st.write("")
        st.error("**52.2 % descartó el viaje por miedo** — pero ese descarte no varía según sexo (p=0.89) ni estrato (p=0.82).")
        st.info("**El miedo actúa igual en todos los grupos:** es una barrera cultural, no demográfica.")
        st.success("**Resumen:** Solo se acepta **H1b**. La hipótesis nula (H0) se rechaza únicamente para la dimensión de miedos.")

# ═══════════════════════════════════════════════════════════
# 7 — CONCLUSIONES (CORREGIDO Y SEGURO)
# ═══════════════════════════════════════════════════════════
elif "Conclusiones" in page:
    st.subheader("🎯 ¿Qué encontramos y qué recomendamos?")

    # KPIs resumen
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Intención de compra", "5.30 / 7", "La más alta")
    k2.metric("Descartaron por miedo", "52.2 %", "59 personas")
    k3.metric("Única correlación sig.", "Miedos r=−0.25", "p = 0.007")
    k4.metric("Hipótesis aceptada", "Solo H1b", "De 4 planteadas")

    st.divider()

    # Gráfica resumen — la paradoja
    paradox_lbl = ['Intención alta\n(M=5.30)', '52% descartó\npor miedo', 'Miedos tienen\nefecto real (p<0.05)', 'Costos/Confort\nno significativos']
    paradox_val = [5.30, 3.80, 3.20, 1.80]
    paradox_clr = ['#52A96D', '#E8C97A', '#E07B54', '#2a4a33']

    fig = go.Figure(go.Bar(
        x=paradox_val, y=paradox_lbl, orientation='h',
        marker=dict(color=paradox_clr, line=dict(color='rgba(0,0,0,.3)', width=1)),
        text=['M = 5.30', '52.2 % descartó', 'r=−0.25, p=0.007', 'p > 0.05'],
        textposition='outside', textfont=dict(color=FC, size=12),
        hovertemplate='%{y}: %{x}'
    ))
    
    # CORRECCIÓN AQUÍ: Evitamos duplicar 'tickfont' pasando la configuración limpia
    config_yaxis = ax()
    config_yaxis['tickfont'] = dict(color=FC, size=12) # Fusionamos de forma segura tamaño y color

    fig.update_layout(**layout(h=300,
        title=dict(text='La paradoja del Amazonas', font=dict(size=14, color=FC), x=.5),
        xaxis=ax(range=[0, 9], showticklabels=False),
        yaxis=config_yaxis
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.warning("**La paradoja:** Los bogotanos *quieren* ir al Amazonas (intención alta, M=5.30) pero *no van* (52% lo descartó). No es un problema de precio ni infraestructura — es una barrera de percepción construida culturalmente.")

    st.divider()
    st.write("**5 recomendaciones concretas**")

    recos = [
        ("🎯 Campaña anti-miedo",
         "Contenido que desmitifique fauna, enfermedades y seguridad con evidencia real: videos de guías locales, estadísticas, testimonios de viajeros."),
        ("🌐 Visibilidad de guías nativos",
         "Crear perfiles digitales verificados para guías locales. Su conocimiento ancestral es el diferencial que las agencias tradicionales no pueden replicar."),
        ("💵 Transparencia de precios",
         "Publicar comparativos claros (transporte + hospedaje + alimentación). Eliminar la incertidumbre que genera percepción de riesgo económico."),
        ("🏛️ Alianzas con ProColombia / Fontur",
         "Campañas de educación y sentido de pertenencia nacional. El Amazonas como orgullo colombiano, no solo destino de lujo."),
        ("📱 Presencia digital constante",
         "Cartagena y San Andrés tienen campañas permanentes. El Amazonas necesita recordación de marca sostenida para competir."),
    ]
    for ico_tit, desc in recos:
        with st.expander(ico_tit):
            st.write(desc)

    st.divider()
    st.markdown("> *\"El Amazonas no se viene a conocer, se viene a vivir.\"*")
    st.caption("— Guías locales del Amazonas colombiano")