import streamlit as st
import os
import json

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Gastronomía de Xi’an",
    page_icon="🍜",
    layout="centered"
)

ORDERS_FILE = "orders.json"

# ======================
# INIT ORDERS FILE (确保文件存在)
# ======================
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"1": [], "2": [], "3": []}, f, ensure_ascii=False, indent=2)

# ======================
# UTILITY FUNCTIONS: 读写文件
# ======================
def load_orders():
    """从文件读取订单"""
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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
# MENU DATA (保持不变)
# ======================
menu = {
    "🥟 包饺馍 · Entrantes": [
        {
            "es": "Rougamo de Cerdo",
            "zh": "肉夹馍",
            "desc": "Hamburguesa estilo Xi’an rellena de cerdo cocido con especias.",
            "price": 6.90,
            "img": "images/肉夹馍.jpg"
        },
        {
            "es": "Jiaozi fritos",
            "zh": "煎饺",
            "desc": "Empanadillas crujientes de cerdo y verduras.",
            "price": 8.90,
            "img": "images/煎饺.jpg"
        }
    ],
    "🍜 面类 · Tallarines": [
        {
            "es": "Tallarines Xi’an",
            "zh": "西安油泼面",
            "desc": "Fideos anchos con chile y aceite caliente.",
            "price": 8.90,
            "img": "images/西安油泼面.jpg"
        }
    ]
}

# ======================
# DISH CARD COMPONENT
# ======================
def render_dish(table, dish):
    title = f"{dish['zh']} · {dish['es']}"
    with st.expander(f"{title} — €{dish['price']}"):
        # 图片逻辑
        if os.path.exists(dish["img"]):
            st.image(dish["img"], use_container_width=True)
        else:
            st.info("📷 Imagen próximamente")
        st.write(dish["desc"])

        # 数量选择
        qty = st.number_input(
            "数量",
            min_value=1,
            max_value=10,
            value=1,
            key=f"{table}-{title}"
        )

        if st.button("➕ 加入点单", key=f"btn-{table}-{title}"):
            # 1. 读取当前最新数据
            current_orders = load_orders()
            # 2. 更新对应桌号
            current_orders.setdefault(table, []).append({
                "zh": dish["zh"],
                "es": dish["es"],
                "qty": qty,
                "price": dish["price"]
            })
            # 3. 立即保存回文件
            save_orders(current_orders)
            st.success("已加入点单！")
            st.rerun()  # 刷新页面显示最新状态

# ======================
# CUSTOMER PAGE (顾客点餐)
# ======================
if table_id:
    st.title(f"🍽️ Mesa {table_id}")
    st.caption("请点餐 · Por favor haga su pedido")
    st.markdown("---")

    # 每次进入页面都从文件读取最新数据
    orders_data = load_orders()
    my_orders = orders_data.get(table_id, [])

    for section, dishes in menu.items():
        st.subheader(section)
        for dish in dishes:
            render_dish(table_id, dish)

    st.markdown("---")
    st.subheader("🧾 当前点单")
    
    if not my_orders:
        st.info("尚未点餐")
    else:
        total = 0
        for o in my_orders:
            subtotal = o["qty"] * o["price"]
            total += subtotal
            st.write(f"- {o['zh']} {o['es']} × {o['qty']} = €{subtotal:.2f}")
        st.markdown(f"### 💰 总计 €{total:.2f}")

        if st.button("✅ 确认下单"):
            st.success("订单已提交 🙏")
            # 这里可以添加发送通知的逻辑

# ======================
# DASHBOARD (后台看板)
# ======================
else:
    st.title("📊 后台订单看板")

    # 引入自动刷新组件
    from streamlit_autorefresh import st_autorefresh

    # 每3秒自动刷新一次
    st_autorefresh(interval=3000, key="dashboard_refresh")

    # 每次刷新都从文件读取最新数据
    orders_data = load_orders()

    if not any(orders_data.values()):
        st.info("暂无订单")
    else:
        for table, orders in orders_data.items():
            st.subheader(f"🪑 Mesa {table}")

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🧹 清零", key=f"clear-{table}"):
                    # 1. 读取数据
                    current_orders = load_orders()
                    # 2. 清空该桌
                    current_orders[table] = []
                    # 3. 立即保存回文件
                    save_orders(current_orders)
                    st.rerun()  # 立即刷新界面

            if not orders:
                st.info("暂无订单")
            else:
                for o in orders:
                    st.write(f"- {o['zh']} {o['es']} × {o['qty']} (€{o['price']})")
            st.markdown("---")
