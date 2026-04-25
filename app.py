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
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

ORDERS_FILE = "orders.json"

# Modern Dark Theme CSS
MODERN_THEME = """
<style>
:root {
    --primary: #FF4444;
    --secondary: #FFB800;
    --dark-bg: #0F0F0F;
    --card-bg: #1A1A1A;
    --text-primary: #FFFFFF;
    --text-secondary: #A0A0A0;
    --success: #00D084;
    --warning: #FF6B6B;
    --light-border: rgba(255, 68, 68, 0.15);
}

* {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

html, body {
    background: linear-gradient(135deg, #0F0F0F 0%, #1A1A1A 100%);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
}

.main {
    background: transparent;
}

/* Headers */
h1, h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}

h1 { font-size: 2.5em !important; letter-spacing: -1px; }
h2 { font-size: 2em !important; margin-top: 30px !important; }

/* Cards */
.stCard, .modern-card {
    background: var(--card-bg) !important;
    border-radius: 12px !important;
    border: 1px solid var(--light-border) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}

.modern-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(255, 68, 68, 0.2);
    border: 1px solid rgba(255, 68, 68, 0.3);
}

/* Menu Item Cards */
.menu-item-card {
    background: var(--card-bg);
    border-radius: 10px;
    border-left: 4px solid var(--primary);
    padding: 14px;
    margin: 10px 0;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item-card:hover {
    background: rgba(255, 68, 68, 0.08);
    transform: translateX(4px);
    border-left: 4px solid var(--secondary);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), #FF6666) !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3) !important;
    transition: all 0.3s ease !important;
    font-size: 1.05em !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 68, 68, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary buttons */
.stButton > button[kind="secondary"] {
    background: rgba(255, 184, 0, 0.2) !important;
    border: 2px solid var(--secondary) !important;
    color: var(--secondary) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    background: rgba(255, 184, 0, 0.3) !important;
}

/* Input Fields */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stSelectbox > div > div > select {
    background: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--light-border) !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
    font-size: 1.1em !important;
}

/* Align quantity input with menu line */
.stNumberInput {
    margin-bottom: 0 !important;
    margin-top: 0 !important;
}

.stNumberInput > div {
    margin: 0 !important;
}

.stNumberInput > div > div {
    margin: 0 !important;
    align-items: center !important;
    display: flex !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus {
    border: 2px solid var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(255, 68, 68, 0.1) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--card-bg) !important;
    border: 1px solid var(--light-border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 68, 68, 0.08) !important;
    border: 1px solid rgba(255, 68, 68, 0.3) !important;
}

/* Cart Items */
.cart-item-box {
    background: rgba(255, 68, 68, 0.05);
    border: 1px solid rgba(255, 68, 68, 0.2);
    border-left: 4px solid var(--primary);
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    transition: all 0.2s ease;
}

.cart-item-box:hover {
    background: rgba(255, 68, 68, 0.1);
}

/* Ordered items - greyed out */
.cart-item-ordered {
    background: rgba(0, 208, 132, 0.08);
    border: 1px solid rgba(0, 208, 132, 0.3);
    border-left: 4px solid #00D084;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    opacity: 0.7;
    transition: all 0.2s ease;
}

/* Price Badge */
.price-badge {
    background: linear-gradient(135deg, var(--secondary), #FFA500);
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.95em;
    display: inline-block;
}

/* Total Amount */
.total-box {
    background: linear-gradient(135deg, var(--primary), #FF6666);
    color: white;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    font-size: 2.2em;
    font-weight: 800;
    box-shadow: 0 8px 24px rgba(255, 68, 68, 0.4);
    margin: 20px 0;
    letter-spacing: -1px;
}

/* Kitchen Dashboard */
.kitchen-card {
    background: var(--card-bg);
    border: 2px solid var(--light-border);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    transition: all 0.3s ease;
}

.kitchen-card.completed {
    opacity: 0.5;
    border: 2px solid rgba(0, 208, 132, 0.3);
}

.order-status-badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.85em;
    font-weight: 700;
    margin-right: 8px;
}

.status-pending {
    background: rgba(255, 107, 107, 0.2);
    color: var(--warning);
}

.status-done {
    background: rgba(0, 208, 132, 0.2);
    color: var(--success);
}

/* Section Title */
.section-header {
    color: var(--primary);
    font-size: 1.8em;
    font-weight: 800;
    margin: 30px 0 15px 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 3px solid var(--primary);
    padding-bottom: 10px;
}

/* Divider */
.stDivider {
    border: 1px solid var(--light-border) !important;
    opacity: 0.3 !important;
}

/* Success/Info boxes */
.stSuccess, .stInfo, .stWarning {
    background: rgba(0, 208, 132, 0.1) !important;
    border: 1px solid rgba(0, 208, 132, 0.3) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

.stError {
    background: rgba(255, 107, 107, 0.1) !important;
    border: 1px solid rgba(255, 107, 107, 0.3) !important;
    border-radius: 8px !important;
}

/* Table selector */
.table-selector {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 10px;
    margin: 20px 0;
}

/* Responsive */
@media (max-width: 768px) {
    h1 { font-size: 1.8em !important; }
    h2 { font-size: 1.5em !important; }
    .total-box { font-size: 1.8em; padding: 18px; }
    .section-header { font-size: 1.4em; }
}

/* Inline layout for quantity and button - same line */
.stColumns {
    gap: 8px !important;
}

.stColumns > div[data-testid="column"] {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    height: auto !important;
}

/* Quantity input column */
.stColumns > div[data-testid="column"] .stNumberInput {
    margin: 0 !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
}

.stColumns > div[data-testid="column"] .stNumberInput > div {
    width: 100% !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
}

.stColumns > div[data-testid="column"] .stNumberInput input {
    padding: 8px 10px !important;
    font-size: 0.95rem !important;
    height: 40px !important;
    width: 100% !important;
}

/* Button column - right aligned */
.stColumns > div[data-testid="column"]:last-child {
    justify-content: flex-end !important;
}

.stColumns > div[data-testid="column"]:last-child .stButton {
    width: auto !important;
}

.stColumns > div[data-testid="column"]:last-child .stButton > button {
    padding: 8px 14px !important;
    font-size: 1.3rem !important;
    height: 40px !important;
    min-width: 50px !important;
}

/* Mobile-first responsive layout */
@media (max-width: 640px) {
    .stColumns > div[data-testid="column"] .stNumberInput input {
        padding: 6px 8px !important;
        font-size: 0.9rem !important;
        height: 36px !important;
    }
    
    .stColumns > div[data-testid="column"]:last-child .stButton > button {
        padding: 6px 12px !important;
        font-size: 1.2rem !important;
        height: 36px !important;
    }
}

/* Make tick mark button weightier and prominent */
.stColumns > div[data-testid="column"]:last-child .stButton > button {
    font-size: 1.4em !important;
    font-weight: 900 !important;
    padding: 14px 20px !important;
    background: linear-gradient(135deg, #00D084, #00B875) !important;
    border: 3px solid #00D084 !important;
    box-shadow: 0 6px 16px rgba(0, 208, 132, 0.4) !important;
    border-radius: 10px !important;
    min-height: 50px !important;
}

.stColumns > div[data-testid="column"]:last-child .stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(0, 208, 132, 0.6) !important;
    background: linear-gradient(135deg, #00B875, #00D084) !important;
}

/* Sticky tabs at the top */
[data-testid="stTabs"] {
    position: sticky !important;
    top: 0 !important;
    z-index: 1000 !important;
    background: linear-gradient(135deg, #0F0F0F 0%, #1A1A1A 100%) !important;
    padding: 12px 20px 0 20px !important;
    margin: 0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
    border-bottom: 1px solid rgba(255, 68, 68, 0.2) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
}

[data-testid="stTabs"] > button {
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 12px 20px !important;
    margin-bottom: 0 !important;
}

@media (max-width: 768px) {
    [data-testid="stTabs"] {
        padding: 8px 15px 0 15px !important;
    }

    [data-testid="stTabs"] > button {
        font-size: 0.95rem !important;
        padding: 10px 16px !important;
    }
}

/* Ensure parent containers allow sticky positioning */
.main, .main > div, .block-container {
    overflow: visible !important;
}

/* Remove the fixed padding since we're using sticky */
.main .block-container {
    padding-top: 0 !important;
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
        {"es": "Arroz pollo teriyaki a la plancha", "zh": "照烧鸡排饭", "desc": "Pollo teriyaki a la plancha", "price": "9,50 €", "img": "images/照烧鸡排饭.jpg", "spicy": True},  
        {"es": "Arroz con cerdo estofado", "zh": "卤肉饭", "desc": "cerdo estofado dulce en salsa de soja", "price": "9,95 €", "img": "images/卤肉饭.jpg", "spicy": True},
        {"es": "Arroz al curry con pollo", "zh": "咖喱鸡饭", "desc": "Pollo tierno en salsa de curry", "price": "9,95 €", "img": "images/咖喱鸡饭.jpg", "spicy": True},
        {"es": "Arroz bolas carne agridulce", "zh": "糖醋鸡丸饭", "desc": "Bolas de pollo en salsa agridulce", "price": "8,50 €", "img": "images/糖醋鸡丸饭.jpg", "spicy": False},
        {"es": "Arroz con pato asado", "zh": "烧鸭饭", "desc": "Bolas de pollo en salsa agridulce", "price": "9,95 €", "img": "images/烧鸭饭.jpg", "spicy": False},
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
    st.title(f"🍽️ MESA {table_id}")
    
    # Initialize cart for tab count
    cart_key = f"cart_{table_id}"
    if cart_key not in st.session_state:
        st.session_state[cart_key] = []
    
    cart = st.session_state[cart_key]
    pending_count = len([item for item in cart if item.get("status") == "pending"])
    
    # Create STICKY TABS at the top
    tab_menu, tab_cart = st.tabs([f"📋 MENÚ", f"🛒 CARRITO ({pending_count})"])
    
    # ==================
    # MENU TAB
    # ==================
    with tab_menu:
        st.markdown("*Haz tu pedido / 請點餐*")
        st.divider()
        
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
                st.markdown(f"### {section}", help="Click to expand menu items")
            
            for dish in grouped[section]:
                with st.container():
                    col_main, col_action = st.columns([4, 1])
                    
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
                        col_qty, col_btn = st.columns([2, 1])
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
    with tab_cart:
        # Separate ordered and pending items
        ordered_items = [item for item in cart if item.get("status") == "ordered"]
        pending_items = [item for item in cart if item.get("status") == "pending"]
        
        if not cart:
            st.info("📭 Carrito vacío - ¡Selecciona algunos platos! (Carrito vacío)")
        else:
            # Display pending items (new orders)
            if pending_items:
                st.markdown("### 📝 PEDIDO ACTUAL")
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
                    if st.button("✅ CONFIRMAR PEDIDO", use_container_width=True, key="confirm_cart"):
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
                st.markdown("### ✅ PEDIDOS CONFIRMADOS")
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
    st.title("🔥 COCINA - PANEL DE CONTROL")
    st.markdown("*Haz clic en ✅ para marcar como listo / 再点恢复*")
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
    
    # Display tables with orders
    for table_num in sorted(orders_data.keys(), key=lambda x: int(x)):
        orders = orders_data[table_num]
        if not orders:
            continue
        
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
