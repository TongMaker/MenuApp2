import streamlit as st
import os
import json
import time

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
# INIT ORDERS FILE
# ======================
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"1": [], "2": [], "3": []}, f, ensure_ascii=False, indent=2)

# ======================
# UTILITY FUNCTIONS
# ======================
def load_orders():
    """加载订单，确保每个订单项都有status字段"""
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        orders = json.load(f)
    
    # 迁移：为所有订单项添加status字段
    for table, items in orders.items():
        for item in items:
            if "status" not in item:
                item["status"] = "pending"  # 新订单默认未完成
    
    return orders

def save_orders(orders_dict):
    """保存订单到文件"""
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders_dict, f, ensure_ascii=False, indent=2)

# ======================
# GET TABLE ID FROM URL
# ======================
params = st.query_params
table_id = params.get("table", [None])[0]

# ======================
# MENU DATA (中西双语)
# ======================
menu = {
    "🥟 包饺馍 · Entrantes": [
        {
            "zh": "肉夹馍",
            "es": "Rougamo de Cerdo",
            "desc": "西安特色肉夹馍，猪肉炖煮配香料",
            "price": 6.90,
            "img": "images/肉夹馍.jpg"
        },
        {
            "zh": "煎饺",
            "es": "Jiaozi fritos",
            "desc": "外酥里嫩的猪肉蔬菜煎饺",
            "price": 8.90,
            "img": "images/煎饺.jpg"
        }
    ],
    "🍜 面类 · Tallarines": [
        {
            "zh": "西安油泼面",
            "es": "Tallarines Xi’an",
            "desc": "宽面条配热油辣椒",
            "price": 8.90,
            "img": "images/西安油泼面.jpg"
        }
    ]
}

# ======================
# CUSTOMER PAGE (顾客点餐) - 字体放大 + 中西双语
# ======================
if table_id:
    # === 顾客点单页面：字体放大1.5倍 ===
    st.markdown("""
    <style>
    body {
        font-size: 1.5rem !important;
    }
    .stMarkdown {
        font-size: 1.5rem !important;
    }
    .stButton>button {
        font-size: 1.3rem !important;
        padding: 0.8rem 1.5rem !important;
    }
    .stExpander {
        font-size: 1.4rem !important;
    }
    .stNumberInput>div>div>input {
        font-size: 1.3rem !important;
        padding: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title(f"🍽️ 桌号 {table_id}")
    st.caption("Por favor haga su pedido · 请点餐")
    st.markdown("---")

    # 初始化购物车
    cart_key = f"cart_{table_id}"
    if cart_key not in st.session_state:
        st.session_state[cart_key] = []

    cart = st.session_state[cart_key]

    # 显示菜单
    for section, dishes in menu.items():
        st.subheader(section)
        for dish in dishes:
            title = f"{dish['zh']} · {dish['es']}"
            with st.expander(f"{title} — €{dish['price']}"):
                if os.path.exists(dish["img"]):
                    st.image(dish["img"], use_container_width=True)
                else:
                    st.info("📷 Imagen próximamente")
                st.write(dish["desc"])

                qty = st.number_input(
                    "Cantidad",
                    min_value=1,
                    max_value=10,
                    value=1,
                    key=f"qty-{table_id}-{title}",
                    step=1
                )

                if st.button("➕ Añadir al carrito", key=f"add-{table_id}-{title}"):
                    cart.append({
                        "zh": dish["zh"],
                        "es": dish["es"],
                        "qty": qty,
                        "price": dish["price"],
                        "status": "pending"
                    })
                    st.session_state[cart_key] = cart
                    st.rerun()

    # 显示购物车
    st.markdown("---")
    st.subheader("🛒 Carrito")
    if not cart:
        st.info("Carrito vacío · 购物车为空")
    else:
        total = 0
        for idx, item in enumerate(cart):
            subtotal = item["qty"] * item["price"]
            total += subtotal
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{item['zh']} {item['es']} × {item['qty']} = €{subtotal:.2f}")
            with col2:
                if st.button("🗑️", key=f"del-{table_id}-{idx}"):
                    cart.pop(idx)
                    st.session_state[cart_key] = cart
                    st.rerun()
        
        st.markdown(f"### 💰 Total €{total:.2f}")
        
        if st.button("✅ Confirmar pedido", type="primary", key="confirm_order"):
            # 1. 加载当前订单
            orders = load_orders()
            # 2. 追加到该桌的订单
            orders[table_id] = orders.get(table_id, []) + cart
            # 3. 保存
            save_orders(orders)
            # 4. 清空购物车
            st.session_state[cart_key] = []
            st.success("Pedido confirmado ✅ ¡Listo para la cocina!")
            st.balloons()

# ======================
# KITCHEN DASHBOARD (厨师看板) - 200%字体 + 按钮紧贴文字
# ======================
else:
    # === 厨房看板：200%字体 + 按钮紧贴菜品文字 ===
    st.markdown("""
    <style>
    body {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-size: 2.8rem !important; /* 200%更大 (1.2 * 2.33 = 2.8) */
    }
    .stMarkdown {
        color: #ffffff !important;
        font-size: 2.8rem !important;
    }
    .stSubheader {
        font-size: 3.0rem !important;
        margin-top: 0.3rem !important;
    }
    .stHorizontalRule {
        margin: 0.3rem 0 !important;
    }
    .stButton>button {
        color: #ffffff !important;
        background-color: #333333 !important;
        font-size: 1.8rem !important; /* 按钮文字更大 */
        padding: 0.4rem 0.8rem !important; /* 按钮更小 */
        margin: 0 !important; /* 消除按钮间距 */
    }
    .stColumns {
        gap: 0 !important; /* 消除列间距，按钮紧贴文字 */
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 0.2rem !important;
        }
        .stButton>button {
            padding: 0.3rem 0.6rem !important;
            font-size: 1.6rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔥 厨房看板 - 待处理订单")
    st.caption("点击 ✅ 标记/取消标记完成（红色表示已完成）")
    st.markdown("---")

    # 自动刷新
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=3000, key="dashboard_refresh")

    orders_data = load_orders()

    # 显示所有桌子的订单
    for table, orders in orders_data.items():
        if not orders:
            continue
            
        st.subheader(f"🪑 桌号 {table}")
        
        # === 清零按钮（紧凑布局） ===
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🧹 清空", key=f"clear-{table}"):
                current_orders = load_orders()
                current_orders[table] = []  # 清空该桌所有订单
                save_orders(current_orders)
                st.rerun()
        
        # 显示该桌所有订单（已完成变红，未完成变白）
        for idx, order in enumerate(orders):
            # 根据状态设置颜色
            color = "red" if order["status"] == "done" else "white"
            
            # 使用HTML设置颜色（关键：字体2.8rem）
            styled_text = f'<span style="color:{color}">{order["zh"]} × {order["qty"]} (€{order["price"]})</span>'
            
            # === 关键修改：按钮紧贴文字 ===
            col1, col2 = st.columns([9, 1])  # 9:1比例，确保按钮紧贴文字
            with col1:
                st.markdown(styled_text, unsafe_allow_html=True)
            with col2:
                if st.button("✅", key=f"done-{table}-{idx}"):
                    # 切换状态
                    current_orders = load_orders()
                    if current_orders[table][idx]["status"] == "done":
                        current_orders[table][idx]["status"] = "pending"
                    else:
                        current_orders[table][idx]["status"] = "done"
                    save_orders(current_orders)
                    st.rerun()

        st.markdown("---")
