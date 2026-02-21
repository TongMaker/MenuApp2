import streamlit as st
import os
import json
from streamlit_autorefresh import st_autorefresh

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Gastronomía de Xi’an",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ORDERS_FILE = "orders.json"

# ======================
# INIT ORDERS FILE (1~30桌)
# ======================
if not os.path.exists(ORDERS_FILE):
    initial_orders = {str(i): [] for i in range(1, 31)}  # 1~30桌
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(initial_orders, f, ensure_ascii=False, indent=2)

# ======================
# UTILITY FUNCTIONS
# ======================
def load_orders():
    """加载订单，确保每个订单项都有status字段"""
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        orders = json.load(f)
    
    for table, items in orders.items():
        for item in items:
            if "status" not in item:
                item["status"] = "pending"
    
    return orders

def save_orders(orders_dict):
    """保存订单到文件"""
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders_dict, f, ensure_ascii=False, indent=2)

# ======================
# GET TABLE ID FROM URL
# ======================
params = st.query_params
table_id = params.get("table", [None])[0] # 字符串形式，保证 10~30桌正确

# ======================
# MENU DATA (中西双语)
# ======================
menu = {
    "🥟🍜🍚 套餐 · Menú": [
        {"es": "Menú A Rougamo + Sopa jiaozi + refresco", "zh": "A 肉夹馍+水饺+饮料", "desc": "", "price": "12,95 €", "img": "images/套餐1.jpg"},
        {"es": "Menú B Sopa agripicante + Arroz 3 delicia + refresco", "zh": "B 酸辣汤+三鲜炒饭+饮料", "desc": "", "price": "12,95 €", "img": "images/套餐2.jpg"},
        {"es": "Menú C Rollito prim + Tallarines Ternera + refresco", "zh": "C 春卷+牛肉面+饮料", "desc": "", "price": "14,95 €", "img": "images/套餐3.jpg"}
    ],
    "🥟 包饺馍 · Bao y empanadillas": [
        {"es": "Rougamo de Cerdo", "zh": "肉夹馍", "desc": "Hamburguesa estilo Xi’an rellena de cerdo cocido con especias.", "price": "5,95 €", "img": "images/肉夹馍.jpg"},
        {"es": "Jiaozi fritas", "zh": "煎饺", "desc": "Raviolis de cerdo y verduras, fritos o al vapor.", "price": "6,95 €", "img": "images/煎饺.jpg"},
        {"es": "Jiaozi en sopa", "zh": "汤水饺", "desc": "Jiaozi de carne y verdura en caldo caliente.", "price": "8,50 €", "img": "images/汤水饺.jpg"},
        {"es": "Empanadillas fritas", "zh": "锅贴", "desc": "Empanadillas crujientes por la base al estilo wok.", "price": "6,95 €", "img": "images/锅贴.jpg"},
        {"es": "Rollito de primavera frita", "zh": "炸春卷", "desc": "Rollito crujientes de verdura.", "price": "6,95 €", "img": "images/春卷.jpg"},
        {"es": "Pao mo", "zh": "西安泡馍", "desc": "sopa tradicional de pan desmenuzado con ternera estilo Xian", "price": "12,95 €", "img": "images/xianpaomo.jpg"}，
        {"es": "Sopa agripicante", "zh": "酸辣汤", "desc": "Sopa agripicante", "price": "5,50 €", "img": "images/酸辣汤.jpg"}
    ],
    "🍜 面类 · Tallarines": [
        {"es": "Tallarines Xi’an", "zh": "西安油泼面", "desc": "Fideos anchos con chile, cebolleta y vinagre.", "price": "8,00 €", "img": "images/西安油泼面.jpg"},
        {"es": "Tallarines Zhajiang", "zh": "炸酱面", "desc": "Fideos con salsa de soja fermentada y cerdo.", "price": "8,50 €", "img": "images/炸酱面.jpg"},
        {"es": "Tallarines 2 en 1", "zh": "二合一面", "desc": "Mezcla Xi’an + Zhajiang.", "price": "9,50 €", "img": "images/二合一面.jpg"},
        {"es": "Tallarines con ternera", "zh": "牛肉面", "desc": "En caldo casero de ternera.", "price": "9,85 €", "img": "images/牛肉面.jpg"},
        {"es": "Tallarines con ternera", "zh": "红烧排骨面", "desc": "En caldo casero de costilla.", "price": "9,50 €", "img": "images/红烧排骨面.jpg"},
        {"es": "Tallarines salteado con ternera", "zh": "牛肉炒面", "desc": "Tallarines salteado con ternera.", "price": "8,50 €", "img": "images/牛肉炒面.jpg"},
        {"es": "Tallarines salteado con verdura", "zh": "素炒面", "desc": "Tallarines salteado con verdura y huevo.", "price": "7,50 €", "img": "images/素炒面.jpg"}
    ],
    "🍚 饭类 · Arroz": [
        {"es": "Arroz tres delicias", "zh": "三鲜炒饭", "desc": "Arroz frito.", "price": "7,50 €", "img": "images/三鲜炒饭.jpg"},
        {"es": "Arroz tres delicias con gamba", "zh": "三鲜虾仁炒饭", "desc": "Arroz frito.", "price": "8,80 €", "img": "images/三鲜虾仁炒饭.jpg"},
        {"es": "Arroz con ternera", "zh": "牛肉盖饭", "desc": "Ternera salteada con cebolla y pimientos.", "price": "9,90 €", "img": "images/牛肉盖饭.jpg"},
        {"es": "Arroz Kung Pao", "zh": "宫保鸡丁饭", "desc": "Pollo picante con cacahuetes.", "price": "8,50 €", "img": "images/宫保鸡丁饭.jpg"},
        {"es": "Arroz bolas carne agridulce", "zh": "糖醋鸡丸饭", "desc": "bolas de carne de pollo a la salsa agridulce.", "price": "8,50 €", "img": "images/糖醋鸡丸饭.jpg"},
        {"es": "Arroz blanco", "zh": "米饭", "desc": "Arroz blanco al vapor.", "price": "3,00 €", "img": "images/米饭.jpg"}
    ],
    "🍚 小菜 · Aperitivos": [
        {"es": "Estofado racion pequeño(ternera, patita de pollo, callos)", "zh": "小份卤煮(牛肉, 鸡爪, 牛肚)", "desc": "Estofado chino en salsa de soja racion pequeño.", "price": "3,80 €", "img": "images/小份卤煮.jpg"},
        {"es": "Ternera estofado", "zh": "卤牛肉", "desc": "Ternera estofada chino en salsa de soja racion grande.", "price": "12,50 €", "img": "images/卤牛肉.jpg"},
        {"es": "platito aperitivo", "zh": "小凉菜", "desc": "Aperitivo verdura.", "price": "2,50 €", "img": "images/小凉菜.jpg"}
    ],
    "🥤 Bebidas": [
        {"es": "Cerveza Mahou grifo", "zh": "mahou啤酒管", "desc": "", "price": "2,80 €", "img": ""},
        {"es": "Cerveza Mahou Radley limon grifo", "zh": "mahou柠檬啤酒管", "desc": "", "price": "2,80 €", "img": ""},
        {"es": "Mahou 5 Estrellas", "zh": "mahou五星啤酒", "desc": "330 ml", "price": "2,80 €", "img": ""},
        {"es": "Mahou sin alcohol", "zh": "无酒精啤酒", "desc": "330 ml", "price": "2,80 €", "img": ""},
        {"es": "Cerveza tshindao", "zh": "青岛啤酒", "desc": "330 ml", "price": "3,50 €", "img": ""},
        {"es": "Refresco variados", "zh": "各种饮料", "desc": "cocacola, acuarius, fanta, etc", "price": "2,80 €", "img": ""},
        {"es": "Agua mineral", "zh": "矿泉水", "desc": "500 ml", "price": "2,50 €", "img": ""},
        {"es": "Café", "zh": "咖啡", "desc": "Delta", "price": "1,80 €", "img": ""},
        {"es": "Infusión", "zh": "茶", "desc": "Té verde", "price": "1,80 €", "img": ""},
        {"es": "Te chino", "zh": "中国茶", "desc": "Té verde", "price": "2,80 €", "img": ""}
    ]
}

# ======================
# CUSTOMER PAGE (顾客点餐)
# ======================
if table_id:
    # 字体放大
    st.markdown("""
    <style>
    body { font-size:1.5rem !important; }
    .stMarkdown { font-size:1.5rem !important; }
    .stButton>button { font-size:1.3rem !important; padding:0.8rem 1.5rem !important; }
    .stExpander { font-size:1.4rem !important; }
    .stNumberInput>div>div>input { font-size:1.3rem !important; padding:0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"🍽️ 桌号 {table_id}")
    st.caption("Por favor haga su pedido · 请点餐")
    st.markdown("---")

    cart_key = f"cart_{table_id}"
    if cart_key not in st.session_state:
        st.session_state[cart_key] = []

    cart = st.session_state[cart_key]

    # 菜品列表
    for section, dishes in menu.items():
        st.subheader(section)
        for dish in dishes:
            title = f"{dish['zh']} · {dish['es']}"
            with st.expander(f"{title} — {dish['price']}"):
                if dish["img"] and os.path.exists(dish["img"]):
                    st.image(dish["img"], use_container_width=True)
                else:
                    st.info("📷 Imagen próximamente")
                st.write(dish["desc"])
                qty = st.number_input(
                    "Cantidad",
                    min_value=1, max_value=10, value=1,
                    key=f"qty-{table_id}-{title}", step=1
                )
                if st.button("➕ Añadir al carrito", key=f"add-{table_id}-{title}"):
                    cart.append({"zh": dish["zh"], "es": dish["es"], "qty": qty,
                                 "price": dish["price"], "status": "pending"})
                    st.session_state[cart_key] = cart
                    st.rerun()

    # 购物车
    st.markdown("---")
    st.subheader("🛒 Carrito")
    if not cart:
        st.info("Carrito vacío · 购物车为空")
    else:
        total = 0
        for idx, item in enumerate(cart):
            subtotal = float(str(item["price"]).replace("€","").replace(",",".")) * item["qty"]
            total += subtotal
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"{item['zh']} {item['es']} × {item['qty']} = €{subtotal:.2f}")
            with col2:
                if st.button("🗑️", key=f"del-{table_id}-{idx}"):
                    cart.pop(idx)
                    st.session_state[cart_key] = cart
                    st.rerun()
        st.markdown(f"### 💰 Total €{total:.2f}")

        if st.button("✅ Confirmar pedido", key=f"confirm_order_{table_id}"):
            orders = load_orders()
            orders[table_id] = orders.get(table_id, []) + cart
            save_orders(orders)
            st.session_state[cart_key] = []
            st.success("Pedido confirmado ✅ ¡Listo para la cocina!")
            st.balloons()

# ======================
# KITCHEN DASHBOARD
# ======================
else:
    st.markdown("""
    <style>
    .kitchen { font-size: 2rem; color: white; }
    div.stButton>button { font-size:2rem; padding:0; height:4.5rem; line-height:4.5rem; background:transparent !important; border:none !important; box-shadow:none !important; outline:none !important; cursor:pointer !important; color:white !important;}
    div.stButton>button:hover {color:#ff5555 !important;}
    div.stButton>button:active, div.stButton>button:focus {background:transparent !important; box-shadow:none !important; outline:none !important;}
    </style>
    """, unsafe_allow_html=True)

    st.title("🔥 厨房看板")
    st.caption("点击 ✅ 标记完成 / 再点恢复")
    st.divider()
    st_autorefresh(interval=3000, key="refresh")

    orders_data = load_orders()
    for table, orders in orders_data.items():
        if not orders: continue
        st.subheader(f"🪑 桌号 {table}")

        # 清空按钮
        if st.button("🧹 清空本桌", key=f"clear-{table}"):
            orders_data[table] = []
            save_orders(orders_data)
            st.rerun()

        # 菜品列表
        for idx, order in enumerate(orders):
            col_btn, col_text = st.columns([1,9])
            with col_btn:
                if st.button("✅", key=f"done-{table}-{idx}"):
                    order["status"] = "pending" if order["status"]=="done" else "done"
                    save_orders(orders_data)
                    st.rerun()
            with col_text:
                color = "red" if order["status"]=="done" else "white"
                deco = "line-through" if order["status"]=="done" else "none"
                st.markdown(
                    f'<div class="kitchen" style="color:{color}; text-decoration:{deco}; line-height:4.5rem;">{order["zh"]} × {order["qty"]} ({order["price"]})</div>',
                    unsafe_allow_html=True
                )
        st.divider()
