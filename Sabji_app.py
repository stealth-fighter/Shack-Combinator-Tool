import streamlit as st
import random
import os
import pickle
import pandas as pd

# 🔄 File for used combinations
file_path = "used_combinations.pkl"
if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        used_combinations = pickle.load(f)
else:
    used_combinations = set()

# 🥗 Your Gujarati curries (J for Jain-safe only)
gujarati_curries = [
    "Bhindi Capsicums",
    "Bhindi Potato Masala",
    "Bhindi Masala",
    "Cauliflower Peas Potato",
    "Cauliflower Peas Tomato",
    "Cauliflower Potato Tomato",
    "Eggplant Lilva/Eggplant Toover",
    "Eggplant Potato",
    "Eggplant Potato Raviya",
    "Potato Rasa",
    "Potato Tomato",
    "Tindora Potato",
    "Tindora Masala",
    "Tindora Dry (J)",
    "Turiya Patra (J)"
]

# ✅ Your unchanged Punjabi and Lentil curries
punjabi_curries = [
    "Baingan Bharta", "Dum Aloo", "Dal Makhani", "Dal Fry", "Tadka Dal",
    "Malai Kofta", "Methi Mutter Malai", "Vegetable Korma", "Kaju Corn",
    "Kaju Khoya", "Shahi Paneer", "Palak Paneer", "Kadai Paneer", "Mutter Paneer",
    "Paneer Tikka", "Paneer Angara", "Paneer Chettinad", "Paneer Bhurji", "Paneer Pasanda"
]

lentil_curries = [
    "Vaal/Lima Beans", "Mix Kathod", "Moong Rasa", "Sprouted Moong",
    "Rajma", "Black Chana", "Red Chori", "White Chori"
]

# 🔍 Filter Gujarati for Jain days only
def filter_gujarati(diet_type):
    if diet_type == "Jain":
        return [dish for dish in gujarati_curries if "(J)" in dish]
    else:
        return gujarati_curries

# 🎲 Menu generator with Gujarati filtering
def get_unique_menu(diet_type):
    filtered_gujarati = filter_gujarati(diet_type)
    for _ in range(1000):
        if len(filtered_gujarati) < 1 or len(punjabi_curries) < 2 or len(lentil_curries) < 1:
            return None
        shack1 = random.choice(filtered_gujarati)
        shack3 = random.choice(lentil_curries)
        shack5_6 = random.sample(punjabi_curries, 2)
        combo_key = (shack1, shack3, tuple(sorted(shack5_6)))
        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            with open(file_path, "wb") as f:
                pickle.dump(used_combinations, f)
            return {
                "Gujarati Type": diet_type,
                "Shack 1": shack1,
                "Shack 2": "Undhiyu",
                "Shack 3": shack3,
                "Shack 4": "Chole",
                "Shack 5": shack5_6[0],
                "Shack 6": shack5_6[1]
            }
    return None

# 🖥️ Streamlit UI
st.set_page_config(page_title="Shack Menu Generator", page_icon="🍛", layout="centered")
st.title("🍛 Shack Menu Generator")

tab1, tab2 = st.tabs(["📅 Single Day", "📆 Weekly Planner"])

# ---------------------------
# 📅 SINGLE DAY MENU
# ---------------------------
with tab1:
    st.header("🎲 Generate Today's Menu")
    diet_type = st.radio("Gujarati Dish Type:", ["None", "Jain"])
    if st.button("Generate Menu"):
        menu = get_unique_menu(diet_type)
        if menu:
            for shack, item in menu.items():
                if shack != "Gujarati Type":
                    st.markdown(f"**{shack}**: {item}")
            st.success(f"Gujarati Filter Applied: {menu['Gujarati Type']}")
        else:
            st.error("No valid combinations found.")

# ---------------------------
# 📆 WEEKLY MENU PLANNER
# ---------------------------
with tab2:
    st.header("📆 Weekly Menu Planner")

    jain_days = st.number_input("Days with Jain Gujarati Dish", min_value=0, max_value=7, value=0)
    none_days = 7 - jain_days
    st.markdown(f"📝 Remaining {none_days} day(s) will use full Gujarati list.")

    menu_plan = []
    day_number = 1

    for _ in range(jain_days):
        menu = get_unique_menu("Jain")
        if menu:
            menu["Day"] = f"Day {day_number}"
            menu_plan.append(menu)
            day_number += 1
    for _ in range(none_days):
        menu = get_unique_menu("None")
        if menu:
            menu["Day"] = f"Day {day_number}"
            menu_plan.append(menu)
            day_number += 1

    if menu_plan:
        df = pd.DataFrame(menu_plan)[["Day", "Gujarati Type", "Shack 1", "Shack 2", "Shack 3", "Shack 4", "Shack 5", "Shack 6"]]
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Weekly Menu (CSV)", csv, "weekly_shack_menu.csv", "text/csv")
    else:
        st.warning("No menus could be generated.")

# ---------------------------
# 🛠️ ADMIN SIDEBAR
# ---------------------------
with st.sidebar:
    st.header("🛠️ Admin")
    if st.button("🔄 Reset All Used Combinations"):
        used_combinations.clear()
        with open(file_path, "wb") as f:
            pickle.dump(used_combinations, f)
        st.success("All combinations have been reset.")
