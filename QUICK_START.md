# 🚀 QUICK START GUIDE - Xi'an Gastronomía 2.0

## Installation (30 seconds)

```bash
# 1. Navigate to project folder
cd /Users/tongzhou/Desktop/VScode/MenuApp2-main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

**✅ Done!** The app opens automatically in your browser.

---

## Running the App

### 🔗 URLs to Access

#### **FOR CUSTOMERS** (Replace `5` with any table number 1-30)
```
http://localhost:8501/?table=5
```

#### **FOR KITCHEN** (No table number needed)
```
http://localhost:8501/
```

---

## 👤 Customer Experience

### Step-by-Step

1. **See Menu**
   - Categories displayed with 🔥 emojis
   - Each listed with bilingual names

2. **Search (Optional)** 
   - Top search bar: Type "肉" or "cerdo" to find beef/pork items
   - Real-time results

3. **Filter Spicy (Optional)**
   - Check "🌶️ Solo picantes" for spicy dishes only

4. **View Dish Details**
   - Click dish to expand
   - See image, description, price
   - See if dish is spicy

5. **Select Quantity**
   - Number selector (1-20 items)
   - Default is 1

6. **Add Special Notes (Optional)**
   - "Sin cilantro" = No cilantro
   - "Extra picante" = Very spicy
   - "Alergia: cacahuetes" = Allergy warning

7. **Add to Cart**
   - Green ➕ button adds item
   - Success message appears

8. **Review Cart**
   - See all items with prices
   - See subtotals for each item
   - Edit notes if needed
   - Delete items with 🗑️

9. **Checkout**
   - Big green **CONFIRMAR PEDIDO** button
   - Order appears instantly in kitchen
   - 🎉 Celebration effect!

---

## 👨‍🍳 Kitchen Staff Experience

### Real-Time Dashboard

1. **See Statistics**
   - 📋 **Mesas** = Number of tables with orders
   - 🍽️ **Items** = Total items to prepare
   - ⏳ **Pendientes** = Items still cooking
   - ⏰ **Hora** = Current time

2. **View Orders by Table**
   - Click on table section
   - See all items for that table
   - See item quantities and prices

3. **See Customer Notes**
   - 📝 Special requests shown below each item
   - Allergies, preferences, customizations
   - Example: "Sin cilantro, muy picante"

4. **Mark Items Ready**
   - ✅ button = Mark as ready
   - Item goes from **red** (pending) to **green** (done)
   - Customer can see it's ready

5. **Revert if Needed**
   - ↩️ button = Change back to pending
   - If item needs more time or was marked by mistake

6. **Clear Table**
   - 🧹 button = Clear all items for that table
   - Use when customer has received everything

7. **Auto-Refresh**
   - Dashboard updates every 2 seconds automatically
   - No manual refresh needed
   - Always current view of all tables

---

## 🎨 UI Elements Explained

### Colors & Meanings

| Color | Meaning |
|-------|---------|
| **Red (#FF4444)** | Primary action, pending status, alerts |
| **Gold (#FFB800)** | Secondary actions, prices, accents |
| **Green** | Completed orders, success |
| **Dark Gray** | Background and cards |

### Icons & Their Use

| Icon | Usage |
|------|-------|
| 🔥 | App logo / hot dishes |
| 🍽️ | Table/dish reference |
| 🔍 | Search function |
| 🌶️ | Spicy filter / spicy indicator |
| ➕ | Add to cart |
| 🛒 | Shopping cart |
| 💰 | Total price |
| ✅ | Mark as done / confirm |
| 🗑️ | Delete item |
| 🧹 | Clear table |
| 📝 | Special notes |
| ⏳ | Pending status |

---

## ⚡ Pro Tips

### For Customers
- **Search first** if you're looking for something specific
- **Filter by spicy** if you want to customize preferences
- **Add notes** for dietary restrictions or allergies - kitchen will see them!
- **Review cart** before ordering to catch mistakes

### For Kitchen Staff  
- **Check stats first** to see workload at a glance
- **Scroll tables** with most pending items first (prioritize)
- **Read notes carefully** - customer requests matter!
- **Toggle items** when doubting - you can revert easily
- **Clear tables** only when customer has left

---

## 🔧 Customization

### Change Table Count
Edit line ~200 in `app.py`:
```python
initial_orders = {str(i): [] for i in range(1, 51)}  # Change 31 to 51 for 50 tables
```

### Add New Dish
Edit the `menu` dictionary (line ~130):
```python
menu = {
    "🍕 YOUR CATEGORY": [
        {
            "es": "Spanish name",
            "zh": "中文名字",
            "desc": "Description",
            "price": "9,99 €",
            "img": "images/yourimage.jpg",
            "spicy": False
        }
    ]
}
```

### Change Refresh Rate (Kitchen)
Edit line ~350:
```python
st_autorefresh(interval=3000, key="kitchen_refresh")  # 3000ms = 3 seconds
```

---

## 📊 File Structure

```
MenuApp2-main/
├── app.py                    ← Main application (RUN THIS!)
├── app_old.py               ← Backup of old version
├── orders.json              ← Order data (auto-created)
├── requirements.txt         ← Dependencies to install
├── README_MODERNIZED.md     ← Full documentation
├── IMPROVEMENTS.md          ← What changed in v2.0
├── BEFORE_AFTER.md         ← Feature comparison
├── QUICK_START.md          ← This file!
└── images/                 ← Menu dish images
    ├── 肉夹馍.jpg
    ├── 煎饺.jpg
    └── ... (other images)
```

---

## 🐛 Troubleshooting

### App doesn't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep streamlit  # Should show streamlit installed

# Try installing again
pip install -r requirements.txt --upgrade
```

### Images not showing
- Check `images/` folder exists
- Verify filenames match exactly in menu
- Restart app: `Ctrl+C` then `streamlit run app.py`

### Cart doesn't update
- Refresh browser (Ctrl+R)
- Clear browser cache: Cmd+Shift+Delete
- Check browser console for errors (F12)

### Kitchen dashboard not auto-refreshing
- Manually refresh: Cmd+R
- Check internet connection
- Restart Streamlit

### Orders not saving
- Check file permissions on `orders.json`
- Verify app.py can write to project folder
- Check disk space available

---

## 📞 Support

Running into an issue? Here's how to debug:

1. **Check logs** - Terminal shows error messages
2. **Read README_MODERNIZED.md** - Comprehensive docs
3. **Review code comments** - Well-commented sections
4. **Try sample data** - Delete orders.json and restart (creates fresh)

---

## 🎯 Common Tasks

### Reset all orders
```bash
rm orders.json
# App will recreate it when you restart
streamlit run app.py
```

### Backup orders
```bash
cp orders.json orders_backup_$(date +%Y%m%d_%H%M%S).json
```

### Test with specific table
```
http://localhost:8501/?table=1
http://localhost:8501/?table=15
http://localhost:8501/?table=30
```

### Access from another computer on same network
Replace `localhost` with your IP:
```
http://YOUR_IP:8501/?table=5
http://YOUR_IP:8501/  (kitchen)
```

---

## 📱 Mobile Testing

Open on phone:
- Find your computer's IP: `ifconfig` (Mac) or `ipconfig` (Windows)
- Open: `http://YOUR_IP:8501/?table=5` on phone
- App automatically adapts to mobile screen size

---

## ✨ What Makes v2.0 Special

✅ **Modern dark theme** - Professional restaurant vibe  
✅ **Search & filtering** - Find dishes instantly  
✅ **Special requests** - Reduce kitchen errors  
✅ **Real-time dashboard** - Kitchen efficiency  
✅ **Mobile-first design** - Works everywhere  
✅ **Smooth animations** - Premium feel  
✅ **Auto-refresh** - No manual updates  

---

**Ready? Start the app:**

```bash
streamlit run app.py
```

**Then visit:**
- Customer: `http://localhost:8501/?table=1`
- Kitchen: `http://localhost:8501/`

**🎉 Enjoy your modern restaurant ordering system!**

---

*Last updated: April 2026 | Version: 2.0*
