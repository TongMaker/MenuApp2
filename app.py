import streamlit as st
import os
import json
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import time

# ======================
# CONFIG & STYLING
# ======================
st.set_page_config(
    page_title="🔥 Xi'an Gastronomía - Kitchen Hub",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items=None
)

ORDERS_FILE = "orders.json"

# Modern Mobile-First Dark Theme CSS
MODERN_THEME = """
<style>
:root {
    --primary: #FF4444;
    --secondary: #FFB800;
    --dark-bg: #080808;
    --card-bg: #141414;
    --text-primary: #FFFFFF;
    --text-secondary: #9CA3AF;
    --success: #10B981;
    --border: rgba(255, 255, 255, 0.06);
    --border-accent: rgba(255, 68, 68, 0.3);
}

html, body, [data-testid="stApp"] {
    background: var(--dark-bg) !important;
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Hide Streamlit chrome */
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer {
    display: none !important;
    visibility: hidden !important;
}

/* Block container — centered, desktop-friendly max-width */
.block-container {
    padding: 0 10px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 28px !important;
}

.main, .main > div {
    overflow: visible !important;
}

/* View mode helpers */
body:has(.kitchen-mode) {
    height: 100vh;
    overflow: hidden;
}

body:has(.kitchen-mode) [data-testid="stAppViewContainer"],
body:has(.kitchen-mode) [data-testid="stApp"] {
    height: 100vh;
}

body:has(.kitchen-mode) .block-container {
    height: 100vh;
    padding-bottom: 0 !important;
}

body:has(.kitchen-mode) .main {
    height: 100vh;
    overflow: hidden;
}

body:has(.kitchen-mode) div[data-testid="column"]:has(.kitchen-scroll-marker) {
    height: calc(100vh - 250px);
    overflow-y: auto;
    padding-right: 6px;
    padding-bottom: 12px;
}

body:has(.customer-mode) div[data-testid="column"]:has(.cart-sticky-marker) {
    position: sticky;
    top: 10px;
    align-self: flex-start;
    max-height: calc(100vh - 20px);
    overflow-y: auto;
    padding-bottom: 14px;
}

@media (max-width: 900px) {
    body:has(.customer-mode) div[data-testid="column"]:has(.cart-sticky-marker) {
        position: static;
        max-height: none;
        overflow: visible;
    }
}

h1, h2, h3, h4 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}

.customer-mode,
.kitchen-mode,
.cart-sticky-marker,
.kitchen-scroll-marker {
    display: none;
}

/* ── RESTAURANT HEADER ── */
.restaurant-header {
    background: linear-gradient(160deg, #1C0909 0%, #100606 100%);
    border-bottom: 1px solid rgba(255, 68, 68, 0.2);
    padding: 22px 16px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.restaurant-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(255, 68, 68, 0.12) 0%, transparent 65%);
    pointer-events: none;
}

.restaurant-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #FF4444 25%, #FFB800 75%, transparent 100%);
}

.restaurant-name {
    font-size: 1.55rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FF6666 0%, #FFB800 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.3px;
    line-height: 1.2;
    margin: 0;
    position: relative;
}

.table-badge {
    display: inline-block;
    background: rgba(255, 68, 68, 0.1);
    border: 1px solid rgba(255, 68, 68, 0.25);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.82rem;
    font-weight: 700;
    color: #FF9999;
    margin-top: 10px;
    letter-spacing: 0.5px;
    position: relative;
}

/* ── KITCHEN HEADER ── */
.kitchen-header {
    background: linear-gradient(160deg, #110A00 0%, #0C0800 100%);
    border-bottom: 1px solid rgba(255, 184, 0, 0.2);
    padding: 22px 16px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.kitchen-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(255, 184, 0, 0.1) 0%, transparent 65%);
    pointer-events: none;
}

.kitchen-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #FFB800 25%, #FF4444 75%, transparent 100%);
}

.kitchen-title {
    font-size: 1.45rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FFB800 0%, #FF6644 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.3px;
    margin: 0;
    position: relative;
}

.kitchen-subtitle {
    color: rgba(255, 255, 255, 0.4);
    font-size: 0.78rem;
    margin-top: 8px;
    position: relative;
}

/* ── STICKY TABS ── */
[data-testid="stTabs"] {
    position: sticky !important;
    top: 0 !important;
    z-index: 999 !important;
    background: #0D0D0D !important;
    padding: 8px 8px 0 !important;
    margin: 0 !important;
    border-bottom: 1px solid var(--border) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
}

[data-testid="stTabs"] button[role="tab"] {
    flex: 1 !important;
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    color: rgba(255, 255, 255, 0.45) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 10px 6px !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    min-height: 40px !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, rgba(255, 68, 68, 0.1) 0%, rgba(255, 68, 68, 0.03) 100%) !important;
    color: #FF7777 !important;
    border-color: rgba(255, 68, 68, 0.25) !important;
    border-bottom-color: #0D0D0D !important;
}

[data-testid="stTabsContent"] {
    padding: 12px 12px 0 !important;
    background: transparent !important;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-size: 0.72rem;
    font-weight: 800;
    color: #FFB800;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 10px 2px 6px;
    border-bottom: 1px solid rgba(255, 184, 0, 0.12);
    margin-bottom: 6px;
}

/* ── EXPANDER / MENU ITEMS ── */
[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin: 3px 0 !important;
    overflow: hidden !important;
    transition: border-color 0.15s ease !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(255, 68, 68, 0.2) !important;
}

details summary {
    background: var(--card-bg) !important;
    padding: 9px 12px !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    cursor: pointer !important;
    line-height: 1.4 !important;
}

details[open] > summary {
    border-bottom: 1px solid var(--border) !important;
    background: #181818 !important;
}

details > div {
    background: #0E0E0E !important;
    padding: 10px !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #FF4444, #DD1111) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 10px 12px !important;
    min-height: 40px !important;
    font-size: 0.86rem !important;
    box-shadow: 0 2px 10px rgba(255, 68, 68, 0.25) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    width: 100% !important;
    letter-spacing: 0.2px !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(255, 68, 68, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Primary confirm button */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #10B981, #047857) !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35) !important;
    font-size: 1.02rem !important;
    font-weight: 800 !important;
    padding: 14px 18px !important;
    border-radius: 14px !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 10px 24px rgba(16, 185, 129, 0.5) !important;
    transform: translateY(-2px) !important;
}

.stButton > button[kind="primary"]:active,
.stButton > button[data-testid="baseButton-primary"]:active {
    transform: translateY(1px) !important;
}

/* Add-to-cart button (last column → green) */
.stColumns > div[data-testid="column"]:last-child .stButton > button {
    background: linear-gradient(135deg, #10B981, #047857) !important;
    box-shadow: 0 3px 12px rgba(16, 185, 129, 0.28) !important;
    font-size: 1.3rem !important;
    font-weight: 900 !important;
    padding: 8px 8px !important;
    min-height: 44px !important;
    border-radius: 10px !important;
}

.stColumns > div[data-testid="column"]:last-child .stButton > button:hover {
    box-shadow: 0 5px 18px rgba(16, 185, 129, 0.45) !important;
}

/* ── NUMBER INPUT ── */
.stNumberInput {
    margin: 0 !important;
}

.stNumberInput > div,
.stNumberInput > div > div {
    margin: 0 !important;
}

.stNumberInput > div > div > input {
    background: #1C1C1C !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    font-size: 0.85rem !important;
    text-align: center !important;
    height: 34px !important;
    font-weight: 600 !important;
}

.stNumberInput > div > div > input:focus {
    border-color: rgba(255, 68, 68, 0.4) !important;
    outline: none !important;
    box-shadow: none !important;
}

/* ── TEXT INPUT ── */
.stTextInput > div > div > input {
    background: #1C1C1C !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    font-size: 0.82rem !important;
    height: 34px !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.22) !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(255, 68, 68, 0.4) !important;
    box-shadow: 0 0 0 2px rgba(255, 68, 68, 0.06) !important;
}

.stTextInput label,
.stNumberInput label {
    color: rgba(255, 255, 255, 0.35) !important;
    font-size: 0.7rem !important;
    margin-bottom: 1px !important;
}

/* ── CART ITEMS ── */
.cart-item-box {
    background: rgba(255, 68, 68, 0.04);
    border: 1px solid rgba(255, 68, 68, 0.15);
    border-left: 3px solid #FF4444;
    border-radius: 10px;
    padding: 8px 10px;
    margin: 4px 0;
    font-size: 0.82rem;
    line-height: 1.4;
}

.cart-item-ordered {
    background: rgba(16, 185, 129, 0.04);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-left: 3px solid #10B981;
    border-radius: 10px;
    padding: 8px 10px;
    margin: 4px 0;
    opacity: 0.72;
    font-size: 0.82rem;
    line-height: 1.4;
}

/* ── PRICE BADGE ── */
.price-badge {
    background: linear-gradient(135deg, #FFB800, #E07000);
    color: white;
    padding: 2px 9px;
    border-radius: 12px;
    font-weight: 800;
    font-size: 0.84rem;
    display: inline-block;
    vertical-align: middle;
    box-shadow: 0 2px 5px rgba(200, 100, 0, 0.25);
}

/* ── TOTAL BOX ── */
.total-box {
    background: linear-gradient(135deg, #FF4444, #CC0000);
    color: white;
    padding: 12px 14px;
    border-radius: 12px;
    text-align: center;
    font-size: 1.3rem;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(255, 68, 68, 0.3);
    margin: 10px 0;
    letter-spacing: -1px;
}

/* ── KITCHEN CARD ── */
.kitchen-card {
    background: #141414;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 6px 0;
}

.kitchen-card h3 {
    margin: 0 0 2px 0 !important;
    font-size: 0.92rem !important;
    color: #FFB800 !important;
    font-weight: 800 !important;
}

.kitchen-card small {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.45);
}

/* ── STATUS BADGES ── */
.order-status-badge {
    display: inline-block;
    padding: 1px 6px;
    border-radius: 12px;
    font-size: 0.65rem;
    font-weight: 700;
    vertical-align: middle;
    margin-left: 4px;
    letter-spacing: 0.3px;
}

.status-pending {
    background: rgba(255, 68, 68, 0.1);
    color: #FF8080;
    border: 1px solid rgba(255, 68, 68, 0.18);
}

.status-done {
    background: rgba(16, 185, 129, 0.1);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.18);
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: #141414 !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    padding: 10px 8px !important;
    text-align: center !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
}

[data-testid="stMetricLabel"] {
    color: rgba(255, 255, 255, 0.4) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── ALERTS ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
}

/* ── DIVIDERS ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
    margin: 8px 0 !important;
}

/* ── COLUMNS ── */
[data-testid="stHorizontalBlock"] {
    gap: 4px !important;
    align-items: center !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 68, 68, 0.25); border-radius: 3px; }

/* ── MOBILE BREAKPOINTS ── */
@media (max-width: 480px) {
    .restaurant-name { font-size: 1.3rem; }
    .kitchen-title { font-size: 1.2rem; }
    .total-box { font-size: 1.2rem; padding: 12px 12px; }
    details summary { font-size: 0.8rem !important; padding: 8px 10px !important; }
    [data-testid="stTabsContent"] { padding: 8px !important; }
    .cart-item-box, .cart-item-ordered { padding: 8px 10px; }
}

@media (max-width: 360px) {
    .restaurant-name { font-size: 1.1rem; }
    [data-testid="stTabs"] button[role="tab"] {
        font-size: 0.75rem !important;
        padding: 8px 4px !important;
    }
    .total-box { font-size: 1.3rem; }
}
</style>
"""

st.markdown(MODERN_THEME, unsafe_allow_html=True)

# ======================
# INITIALIZE DATA
# ======================
if not os.path.exists(ORDERS_FILE):
    initial_orders = {str(i): [] for i in range(1, 31)}
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(initial_orders, f, ensure_ascii=False, indent=2)

# ======================
# UTILITY FUNCTIONS
# ======================
def load_orders():
    """Load orders from file with proper status handling"""
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        orders = json.load(f)
    
    for table, items in orders.items():
        for item in items:
            if "status" not in item:
                item["status"] = "pending"
            if "timestamp" not in item:
                item["timestamp"] = datetime.now().isoformat()
            if "notes" not in item:
                item["notes"] = ""
    
    return orders

def save_orders(orders_dict):
    """Save orders to file"""
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders_dict, f, ensure_ascii=False, indent=2)

def parse_price(price_str):
    """Convert price string to float"""
    return float(str(price_str).replace("€", "").replace(",", ".").strip())

def get_all_dishes():
    """Get flat list of all dishes for searching"""
    all_dishes = []
    for section, dishes in menu.items():
        for dish in dishes:
            dish['section'] = section
            all_dishes.append(dish)
    return all_dishes

def search_dishes(query, dishes_list):
    """Search dishes by name or description"""
    if not query:
        return dishes_list
    
    query = query.lower()
    return [d for d in dishes_list if 
            query in d['zh'].lower() or 
            query in d['es'].lower() or 
            query in d['desc'].lower()]

# ======================
# MENU DATA (Bilingual)
# ======================
menu = {
    "🥟🍜🍚 MENÚS DEL DÍA · 今日套餐": [
        {"es": "Menú A: Rougamo + Sopa jiaozi + Refresco", "zh": "A 肉夹馍+水饺汤+饮料", "desc": "Disponible de martes a sábado", "price": "12,95 €", "img": "images/套餐1.jpg", "spicy": False},
        {"es": "Menú B: Sopa agripicante + Arroz 3 delicias + Refresco", "zh": "B 酸辣汤+三鲜炒饭+饮料", "desc": "Disponible de martes a sábado", "price": "12,95 €", "img": "images/套餐2.jpg", "spicy": True},
        {"es": "Menú C: Rollito prim. + Tallarines Ternera + Refresco", "zh": "C 春卷+牛肉面+饮料", "desc": "Disponible de martes a sábado", "price": "14,95 €", "img": "images/套餐3.jpg", "spicy": False}
    ],
    "🥟 EMPANADILLAS & BOAS · 包饺馍": [
        {"es": "Rougamo de Cerdo", "zh": "肉夹馍", "desc": "Hamburguesa estilo Xi'an rellena de cerdo cocido con especias", "price": "5,95 €", "img": "images/肉夹馍.jpg", "spicy": False},
        {"es": "Jiaozi fritas", "zh": "煎饺", "desc": "Raviolis de cerdo y verduras, fritos crocantes", "price": "6,95 €", "img": "images/煎饺.jpg", "spicy": False},
        {"es": "Jiaozi en sopa", "zh": "汤水饺", "desc": "Jiaozi de carne y verdura en caldo caliente casero", "price": "8,50 €", "img": "images/汤水饺.jpg", "spicy": False},
        {"es": "Empanadillas fritas", "zh": "锅贴", "desc": "Empanadillas crujientes por la base al estilo wok", "price": "6,95 €", "img": "images/锅贴.jpg", "spicy": False},
        {"es": "Rollito de primavera frita", "zh": "炸春卷", "desc": "Rollos crujientes de verdura", "price": "6,95 €", "img": "images/春卷.jpg", "spicy": False},
        {"es": "Pao mo (Sopa tradicional)", "zh": "西安泡馍", "desc": "Sopa de pan desmenuzado con ternera estilo Xi'an (plato completo)", "price": "12,95 €", "img": "images/xianpaomo.jpg", "spicy": True},
        {"es": "Sopa agripicante", "zh": "酸辣汤", "desc": "Sopa picante y ácida - especialidad de Xi'an", "price": "5,50 €", "img": "images/酸辣汤.jpg", "spicy": True}
    ],
    "🍜 TALLARINES · 面类": [
        {"es": "Tallarines Xi'an (Oil-Splash Noodles)", "zh": "西安油泼面", "desc": "Fideos anchos con chile, cebolleta y vinagre - plato icónico", "price": "8,00 €", "img": "images/西安油泼面.jpg", "spicy": True},
        {"es": "Tallarines Zhajiang", "zh": "炸酱面", "desc": "Fideos con salsa de soja fermentada y cerdo molido", "price": "8,50 €", "img": "images/炸酱面.jpg", "spicy": False},
        {"es": "Tallarines 2 en 1", "zh": "二合一面", "desc": "Mezcla Xi'an + Zhajiang - lo mejor de ambos mundos", "price": "9,50 €", "img": "images/二合一面.jpg", "spicy": True},
        {"es": "Tallarines con ternera", "zh": "牛肉面", "desc": "En caldo casero de ternera - receta tradicional", "price": "9,85 €", "img": "images/牛肉面.jpg", "spicy": False},
        {"es": "Tallarines con costilla", "zh": "红烧排骨面", "desc": "En caldo casero de costilla de cerdo", "price": "9,50 €", "img": "images/红烧排骨面.jpg", "spicy": False},
        {"es": "Tallarines salteado con ternera", "zh": "牛肉炒面", "desc": "Tallarines wok con ternera jugosa", "price": "8,50 €", "img": "images/牛肉炒面.jpg", "spicy": False},
        {"es": "Tallarines salteado con verdura", "zh": "素炒面", "desc": "Tallarines wok con verdura y huevo - opción vegetariana", "price": "7,50 €", "img": "images/素炒面.jpg", "spicy": False}
    ],
    "🍚 ARROCES · 饭类": [
        {"es": "Arroz tres delicias", "zh": "三鲜炒饭", "desc": "Arroz frito con jamón, huevo y guisantes", "price": "7,50 €", "img": "images/三鲜炒饭.jpg", "spicy": False},
        {"es": "Arroz con gamba", "zh": "三鲜虾仁炒饭", "desc": "Arroz frito con gamba, jamón y huevo", "price": "8,80 €", "img": "images/三鲜虾仁炒饭.jpg", "spicy": False},
        {"es": "Arroz con ternera", "zh": "牛肉盖饭", "desc": "Ternera salteada wok con cebolla y pimientos", "price": "9,90 €", "img": "images/牛肉盖饭.jpg", "spicy": False},
        {"es": "Arroz Kung Pao", "zh": "宫保鸡丁饭", "desc": "Pollo con salsa picante y cacahuetes", "price": "8,50 €", "img": "images/宫保鸡丁饭.jpg", "spicy": True},
        {"es": "Arroz pollo teriyaki a la plancha", "zh": "照烧鸡排饭", "desc": "Pollo teriyaki a la plancha", "price": "9,95 €", "img": "images/照烧鸡排饭.jpg", "spicy": True},  
        {"es": "Arroz con cerdo estofado", "zh": "卤肉饭", "desc": "cerdo estofado dulce en salsa de soja", "price": "9,95 €", "img": "images/卤肉饭.jpg", "spicy": True},
        {"es": "Arroz al curry con pollo", "zh": "咖喱鸡饭", "desc": "Pollo tierno en salsa de curry", "price": "9,95 €", "img": "images/咖喱鸡饭.jpg", "spicy": True},
        {"es": "Arroz bolas carne agridulce", "zh": "糖醋鸡丸饭", "desc": "Bolas de pollo en salsa agridulce", "price": "8,50 €", "img": "images/糖醋鸡丸饭.jpg", "spicy": False},
        {"es": "Arroz con pato asado", "zh": "烧鸭饭", "desc": "Bolas de pollo en salsa agridulce", "price": "10,90 €", "img": "images/烧鸭饭.jpg", "spicy": False},
        {"es": "Arroz blanco", "zh": "米饭", "desc": "Arroz blanco al vapor", "price": "3,00 €", "img": "images/米饭.jpg", "spicy": False}
    ],
    "🍲 APERITIVOS & PEQUEÑOS · 小菜": [
        {"es": "Estofado pequeño (ternera)", "zh": "小份卤煮(牛肉)", "desc": "Estofado chino en salsa de soja - ración pequeña", "price": "3,80 €", "img": "images/小份卤煮.jpg", "spicy": False},
        {"es": "Estofado pequeño (patita de pollo)", "zh": "小份卤煮(鸡爪)", "desc": "Patitas de pollo estofadas en salsa de soja - ración pequeña", "price": "3,80 €", "img": "images/小份卤煮.jpg", "spicy": False},
        {"es": "Estofado pequeño (callos)", "zh": "小份卤煮(牛肚)", "desc": "Callos estofados en salsa de soja - ración pequeña", "price": "3,80 €", "img": "images/小份卤煮.jpg", "spicy": False},
        {"es": "Ternera estofado (ración grande)", "zh": "卤牛肉", "desc": "Ternera estofada chino en salsa de soja - ración grande", "price": "12,50 €", "img": "images/卤牛肉.jpg", "spicy": False},
        {"es": "Platito aperitivo verdura", "zh": "小凉菜", "desc": "Mix de verduras cocinadas a la manera tradicional china", "price": "2,50 €", "img": "images/小凉菜.jpg", "spicy": False}
    ],
    "🍰 POSTRES · 甜点": [
        {"es": "Mochi Mango", "zh": "Mochi 芒果", "desc": "Postre tipo mochi relleno de crema de mango - una delicia", "price": "2,95 €", "img": "images/mochimango.jpg", "spicy": False},
        {"es": "Mochi Coco", "zh": "Mochi 椰子", "desc": "Postre tipo mochi relleno de crema de coco tropical", "price": "2,95 €", "img": "images/mochicoco.jpg", "spicy": False}
    ],
    "🍻 CERVEZAS & BEBIDAS · 啤酒": [
        {"es": "Cerveza Mahou (grifo)", "zh": "Mahou扎啤", "desc": "Cerveza española clásica", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Cerveza Mahou Limón (grifo)", "zh": "Mahou柠檬扎啤", "desc": "Fresca y refrescante", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Mahou 5 Estrellas", "zh": "Mahou五星啤酒", "desc": "330 ml", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Heineken", "zh": "Heineken", "desc": "330 ml", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Cerveza Tsingtao", "zh": "青岛啤酒", "desc": "330 ml - cerveza china clásica", "price": "3,50 €", "img": "", "spicy": False},
        {"es": "Mahou sin alcohol", "zh": "无酒精啤酒", "desc": "330 ml", "price": "2,80 €", "img": "", "spicy": False}
    ],
    "🥤 BEBIDAS VARIADAS · 饮料": [
        {"es": "Coca-Cola", "zh": "可乐", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Coca-Cola Zero", "zh": "Zero可乐", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Sprite", "zh": "雪碧", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Acuarius", "zh": "Acuarius", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Nestea Limón", "zh": "Nestea柠檬茶", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Zumo COMPAL", "zh": "COMPAL果汁", "desc": "Piña, Naranja, Melocotón, Tomate", "price": "2,50 €", "img": "", "spicy": False},
        {"es": "Fanta Naranja", "zh": "橙子芬达", "desc": "", "price": "2,80 €", "img": "", "spicy": False},
        {"es": "Agua mineral", "zh": "矿泉水", "desc": "500 ml", "price": "2,50 €", "img": "", "spicy": False},
        {"es": "Café", "zh": "咖啡", "desc": "Delta", "price": "1,80 €", "img": "", "spicy": False},
        {"es": "Infusión de té verde", "zh": "茶", "desc": "Té verde", "price": "1,80 €", "img": "", "spicy": False},
        {"es": "Té chino", "zh": "中国茶", "desc": "Té verde", "price": "2,80 €", "img": "", "spicy": False}
    ]
}

# ======================
# MAIN APP LOGIC
# ======================
params = st.query_params
table_id = params.get("table", [None])[0]

# ==================
# CUSTOMER PAGE
# ==================
if table_id:
    st.markdown(f"""
    <div class="restaurant-header">
        <div class="restaurant-name">🔥 XI'AN GASTRONOMÍA</div>
        <div class="table-badge">🪑 Mesa {table_id}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="customer-mode"></div>', unsafe_allow_html=True)
    
    # Initialize cart for tab count
    cart_key = f"cart_{table_id}"
    if cart_key not in st.session_state:
        st.session_state[cart_key] = []
    
    cart = st.session_state[cart_key]
    pending_count = len([item for item in cart if item.get("status") == "pending"])
    
    col_menu, col_cart = st.columns([3, 1], gap="large")
    
    # ==================
    # MENU TAB
    # ==================
    with col_menu:
        st.markdown('<div class="section-header">📋 MENÚ</div>', unsafe_allow_html=True)
        # Display menu
        all_dishes = get_all_dishes()
        filtered_dishes = all_dishes
    
        # Group by section
        from collections import defaultdict
        grouped = defaultdict(list)
        for dish in filtered_dishes:
            grouped[dish['section']].append(dish)
        
        for section in menu.keys():
            if section in grouped and grouped[section]:
                st.markdown(f'<div class="section-header">{section}</div>', unsafe_allow_html=True)
            
            for dish in grouped[section]:
                with st.container():
                    col_main, col_action = st.columns([3, 2])
                    
                    with col_main:
                        title = f"{dish['zh']} • {dish['es']}"
                        expander = st.expander(f"**{title}** — {dish['price']}", expanded=False)
                        
                        with expander:
                            col_img, col_info = st.columns([1, 2])
                            
                            with col_img:
                                if dish["img"] and os.path.exists(dish["img"]):
                                    st.image(dish["img"], use_container_width=True)
                                else:
                                    st.info("📷 Imagen próximamente")
                            
                            with col_info:
                                st.write(f"**📝 {dish['desc']}**")
                    
                    with col_action:
                        col_qty, col_btn = st.columns([3, 2])
                        with col_qty:
                            qty = st.number_input(
                                "",
                                min_value=1, max_value=20, value=1,
                                key=f"qty-{table_id}-{dish['zh']}", step=1
                            )
                        with col_btn:
                            if st.button("✓", key=f"add-{table_id}-{dish['zh']}", help="Añadir al carrito"):
                                cart.append({
                                    "zh": dish["zh"],
                                    "es": dish["es"],
                                    "qty": qty,
                                    "price": dish["price"],
                                    "status": "pending",
                                    "notes": "",
                                    "timestamp": datetime.now().isoformat(),
                                    "order_group": datetime.now().isoformat()
                                })
                                st.session_state[cart_key] = cart
                                st.success(f"✅ {dish['zh']} añadido!", icon="✨")
                                time.sleep(0.5)
                                st.rerun()
    
    # ==================
    # CART TAB
    # ==================
    with col_cart:
        st.markdown('<div class="cart-sticky-marker"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">🛒 CARRITO ({pending_count})</div>', unsafe_allow_html=True)
        # Separate ordered and pending items
        ordered_items = [item for item in cart if item.get("status") == "ordered"]
        pending_items = [item for item in cart if item.get("status") == "pending"]
        
        if not cart:
            st.info("📭 Carrito vacío - ¡Selecciona algunos platos! (Carrito vacío)")
        else:
            # Display pending items (new orders)
            if pending_items:
                st.markdown('<div class="section-header">📝 Pedido actual</div>', unsafe_allow_html=True)
                pending_total = 0
                for idx, item in enumerate(pending_items):
                    price_value = parse_price(item["price"])
                    subtotal = price_value * item["qty"]
                    pending_total += subtotal
                    
                    st.markdown(f"""
                    <div class="cart-item-box">
                        <strong>{item['zh']} • {item['es']}</strong> × {item['qty']} = <span class="price-badge">{subtotal:.2f}€</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_info, col_delete = st.columns([4, 1])
                    with col_info:
                        notes = st.text_input(
                            "Notas especiales (opcional) / 特殊说明",
                            value=item.get("notes", ""),
                            key=f"notes-cart-{idx}",
                            placeholder="Ej: Sin cilantro / Sin picante..."
                        )
                        item["notes"] = notes
                    
                    with col_delete:
                        cart_idx = cart.index(item)
                        if st.button("🗑️", key=f"del-cart-{table_id}-{idx}"):
                            cart.pop(cart_idx)
                            st.session_state[cart_key] = cart
                            st.rerun()
                
                # Pending total and confirmation
                st.markdown(f'<div class="total-box">💰 SUBTOTAL: {pending_total:.2f}€</div>', unsafe_allow_html=True)
                
                col_clear, col_confirm = st.columns([1, 1])
                with col_clear:
                    if st.button("🔄 Vaciar pedido actual", use_container_width=True, key="clear_cart"):
                        cart[:] = ordered_items
                        st.session_state[cart_key] = cart
                        st.rerun()
                
                with col_confirm:
                    if st.button("✅ CONFIRMAR PEDIDO", use_container_width=True, key="confirm_cart", type="primary"):
                        # Mark pending items as ordered
                        for item in pending_items:
                            item["status"] = "ordered"
                        
                        # Save to orders file
                        orders = load_orders()
                        for item in pending_items:
                            if table_id not in orders:
                                orders[table_id] = []
                            orders[table_id].append(item)
                        save_orders(orders)
                        
                        # Update cart in session
                        st.session_state[cart_key] = cart
                        st.success("🎉 ¡Pedido confirmado! Aquí para la cocina ¡Listo!", icon="✨")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
            
            # Display ordered items (history)
            if ordered_items:
                st.divider()
                st.markdown('<div class="section-header">✅ Pedidos confirmados</div>', unsafe_allow_html=True)
                ordered_total = 0
                for idx, item in enumerate(ordered_items):
                    price_value = parse_price(item["price"])
                    subtotal = price_value * item["qty"]
                    ordered_total += subtotal
                    
                    st.markdown(f"""
                    <div style="background: rgba(0, 208, 132, 0.08); border: 1px solid rgba(0, 208, 132, 0.3); border-left: 4px solid #00D084; border-radius: 8px; padding: 12px; margin: 8px 0; opacity: 0.8;">
                        <strong>{item['zh']} • {item['es']}</strong> × {item['qty']} = <span class="price-badge">{subtotal:.2f}€</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f'<div class="total-box" style="opacity: 0.7;">💰 CONFIRMADOS: {ordered_total:.2f}€</div>', unsafe_allow_html=True)

# ==================
# KITCHEN DASHBOARD
# ==================
else:
    st.markdown("""
    <div class="kitchen-header">
        <div class="kitchen-title">🔥 COCINA — PANEL DE CONTROL</div>
        <div class="kitchen-subtitle">Haz clic en ✅ para marcar como listo / 再点恢复</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="kitchen-mode"></div>', unsafe_allow_html=True)
    st.divider()
    
    # Auto-refresh
    st_autorefresh(interval=2000, key="kitchen_refresh")
    
    # Load orders
    orders_data = load_orders()
    
    # Kitchen stats
    total_orders = sum(1 for orders in orders_data.values() if orders)
    total_items = sum(len(orders) for orders in orders_data.values())
    pending_items = sum(1 for orders in orders_data.values() for item in orders if item.get("status") == "pending")
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Mesas", total_orders, delta=None)
    with col2:
        st.metric("🍽️ Items", total_items, delta=None)
    with col3:
        st.metric("⏳ Pendientes", pending_items, delta=None)
    with col4:
        st.metric("⏰ Hora", datetime.now().strftime("%H:%M"), delta=None)
    
    st.divider()
    
    tables_with_orders = [
        (table_num, orders_data[table_num])
        for table_num in sorted(orders_data.keys(), key=lambda x: int(x))
        if orders_data[table_num]
    ]

    if not tables_with_orders:
        st.info("📭 Sin pedidos por ahora.")
    else:
        left_tables = tables_with_orders[::2]
        right_tables = tables_with_orders[1::2]
        col_left, col_right = st.columns(2)

        for col, tables in zip([col_left, col_right], [left_tables, right_tables]):
            with col:
                st.markdown('<div class="kitchen-scroll-marker"></div>', unsafe_allow_html=True)
                for table_num, orders in tables:
                    pending_count = sum(1 for o in orders if o.get("status") == "pending")
                    done_count = sum(1 for o in orders if o.get("status") == "done")

                    st.markdown(f"""
                    <div class="kitchen-card">
                        <h3>🪑 MESA {table_num}</h3>
                        <small>⏳ Pendientes: {pending_count} | ✅ Listos: {done_count}</small>
                    </div>
                    """, unsafe_allow_html=True)

                    col_clear, col_expand = st.columns([1, 5])
                    with col_clear:
                        if st.button("🧹", key=f"clear-{table_num}", help="Limpiar mesa"):
                            orders_data[table_num] = []
                            save_orders(orders_data)
                            st.rerun()

                    # Display items
                    for idx, order in enumerate(orders):
                        status = order.get("status", "pending")
                        status_class = "status-done" if status == "done" else "status-pending"
                        status_text = "✅ LISTO" if status == "done" else "⏳ PREPARANDO"

                        strike = "text-decoration: line-through;" if status == "done" else ""

                        col_btn, col_item, col_notes = st.columns([1, 3, 2])

                        with col_btn:
                            if st.button(
                                "✅" if status == "pending" else "↩️",
                                key=f"toggle-{table_num}-{idx}",
                                help="Marcar/desmarcar como listo"
                            ):
                                order["status"] = "done" if status == "pending" else "pending"
                                save_orders(orders_data)
                                st.rerun()

                        with col_item:
                            st.markdown(f"""
                            <div style="{strike} opacity: {'0.6' if status == 'done' else '1'};">
                                <strong>{order['zh']}</strong> × {order['qty']} ({order['price']})
                                <span class="order-status-badge {status_class}">{status_text}</span>
                            </div>
                            """, unsafe_allow_html=True)

                        with col_notes:
                            if order.get("notes"):
                                st.caption(f"📝 {order['notes']}")

                    st.markdown("---")
