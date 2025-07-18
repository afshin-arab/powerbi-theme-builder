# app.py
import streamlit as st
import json
import pandas as pd
import altair as alt

st.set_page_config(page_title="Power BI Theme Builder", layout="wide")

# Utility Functions
def load_json(file):
    try:
        return json.load(file)
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return {}

def generate_sample_data():
    return pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Value": [100, 250, 175, 300]
    })

def render_bar_chart(data, colors, font):
    chart = alt.Chart(data).mark_bar().encode(
        x='Category',
        y='Value',
        color=alt.Color('Category', scale=alt.Scale(range=colors))
    ).properties(width=300, height=250).configure_axis(
        labelFont=font,
        titleFont=font
    ).configure_legend(labelFont=font, titleFont=font)
    st.altair_chart(chart)

def render_kpi_card(value, label, color, font):
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:20px; border-radius:10px; color:white; text-align:center; font-family:{font}">
            <h2 style="margin:0;">{value}</h2>
            <p style="margin:0;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_matrix_table(data, font, text_color):
    st.markdown(f"<h4 style='font-family:{font}; color:{text_color}'>Matrix Preview</h4>", unsafe_allow_html=True)
    st.dataframe(data.style.set_properties(**{
        'font-family': font,
        'color': text_color
    }))

# Sidebar - Load or New Theme
st.sidebar.title("🧩 Theme Controls")
load_option = st.sidebar.radio("Start From", ["New Theme", "Upload Theme"])
theme = {}
if load_option == "Upload Theme":
    uploaded = st.sidebar.file_uploader("Upload JSON Theme", type="json")
    if uploaded:
        theme = load_json(uploaded)

# Theme Builder UI
st.title("🎨 Power BI Theme Builder")
theme["name"] = st.text_input("Theme Name", theme.get("name", "My Power BI Theme"))

st.subheader("1. Base Colors")
bg = st.color_picker("Page Background", theme.get("background", "#FFFFFF"))
fg = st.color_picker("Text Color (Foreground)", theme.get("foreground", "#000000"))
accent = st.color_picker("Table Accent Color", theme.get("tableAccent", "#0078D7"))

st.subheader("2. Data Colors")
data_colors = theme.get("dataColors", ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7"])
new_data_colors = []
cols = st.columns(4)
for i in range(8):
    with cols[i % 4]:
        color = st.color_picker(f"Color {i+1}", data_colors[i] if i < len(data_colors) else "#CCCCCC")
        new_data_colors.append(color)

st.subheader("3. Diverging & Sentiment Colors")
min_color = st.color_picker("Minimum (Negative)", theme.get("minimum", "#FF0000"))
center_color = st.color_picker("Center (Neutral)", theme.get("center", "#FFFF00"))
max_color = st.color_picker("Maximum (Positive)", theme.get("maximum", "#00B050"))

kpi_good = st.color_picker("KPI Good", theme.get("kpi", {}).get("*", {}).get("goodColor", "#00B050"))
kpi_neutral = st.color_picker("KPI Neutral", theme.get("kpi", {}).get("*", {}).get("neutralColor", "#FFD700"))
kpi_bad = st.color_picker("KPI Bad", theme.get("kpi", {}).get("*", {}).get("badColor", "#FF0000"))

st.subheader("4. Font Settings")
powerbi_fonts = ["Segoe UI", "DIN", "Arial", "Calibri", "Verdana"]
font = st.selectbox("Font Family", powerbi_fonts, index=powerbi_fonts.index(theme.get("text", {}).get("fontFamily", "Segoe UI")))
title_size = st.slider("Title Font Size", 10, 32, theme.get("textClasses", {}).get("title", {}).get("fontSize", 16))
label_size = st.slider("Label Font Size", 8, 24, theme.get("textClasses", {}).get("label", {}).get("fontSize", 12))

st.subheader("5. UI & Visual Settings")
border = st.checkbox("Enable Borders", theme.get("visualDefaults", {}).get("border", True))
shadow = st.checkbox("Enable Shadows", theme.get("visualDefaults", {}).get("shadow", False))
border_radius = st.slider("Border Radius", 0, 10, theme.get("visualDefaults", {}).get("borderRadius", 0))
slicer_style = st.selectbox("Slicer Style", ["Dropdown", "Tile", "Between"], index=0)

st.subheader("6. Label & Format Settings")
currency_symbol = st.text_input("Currency Symbol", theme.get("numberFormat", {}).get("currency", "$"))
currency_format = st.text_input("Currency Format", theme.get("numberFormat", {}).get("currencyFormat", "$#,0.00"))
percent_format = st.text_input("Percent Format", theme.get("numberFormat", {}).get("percentFormat", "#,0.00%"))
decimal_places = st.slider("Decimal Places", 0, 6, theme.get("numberFormat", {}).get("decimalPlaces", 2))

# Build JSON Object
theme = {
    "name": theme["name"],
    "dataColors": new_data_colors,
    "background": bg,
    "foreground": fg,
    "tableAccent": accent,
    "minimum": min_color,
    "center": center_color,
    "maximum": max_color,
    "text": {"fontFamily": font},
    "visualDefaults": {
        "border": border,
        "shadow": shadow,
        "borderRadius": border_radius
    },
    "textClasses": {
        "title": {"fontSize": title_size, "fontFace": font, "color": fg},
        "label": {"fontSize": label_size, "fontFace": font, "color": fg}
    },
    "slicer": {"style": slicer_style},
    "numberFormat": {
        "currency": currency_symbol,
        "currencyFormat": currency_format,
        "percentFormat": percent_format,
        "decimalPlaces": decimal_places
    },
    "kpi": {
        "*": {
            "goodColor": kpi_good,
            "neutralColor": kpi_neutral,
            "badColor": kpi_bad
        }
    }
}

# Preview Section
st.markdown("---")
st.header("🔍 Live Preview")
data = generate_sample_data()
preview_cols = st.columns(3)
with preview_cols[0]:
    st.markdown(f"<h4 style='font-family:{font}; color:{fg}'>Bar Chart</h4>", unsafe_allow_html=True)
    render_bar_chart(data, new_data_colors, font)
with preview_cols[1]:
    st.markdown(f"<h4 style='font-family:{font}; color:{fg}'>KPI Card</h4>", unsafe_allow_html=True)
    render_kpi_card("92%", "Uptime", new_data_colors[0], font)
with preview_cols[2]:
    render_matrix_table(data, font, fg)

# Download JSON
st.markdown("---")
st.header("📄 Theme JSON Output")
st.json(theme)
st.download_button(
    label="📥 Download JSON Theme",
    data=json.dumps(theme, indent=2),
    file_name=f"{theme['name'].replace(' ', '_').lower()}_theme.json",
    mime="application/json"
)
