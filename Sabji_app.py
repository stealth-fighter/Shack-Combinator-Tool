import streamlit as st
import random
import os
import pickle
import pandas as pd
from io import StringIO

# 📁 File to store used combinations
file_path = "used_combinations.pkl"

# 🔄 Load from file if exists
if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        used_combinations = pickle.load(f)
else:
    used_combinations = set()

# 🥗 Curry Lists
gujarati_curries = [
    "Bhindi Capsicums", "Bhindi Potato Masala", "Bhindi Masala",
    "Cauliflower Peas Potato", "Cauliflower Peas Tomato", "Cauliflower Potato Tomato",
    "Eggplant Lilva/Eggplant Toover", "Eggplant Potato", "Eggplant Potato Raviya",
    "Potato Rasa", "Potato Tomato", "Tindora Potato", "Tindora Masala", "Tindora Dry",
    "Turiya Patra"
]

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

# 🔀 Menu Generator
def get_unique_menu():
    for _ in range(1000):
        shack1 = random.choice(gujarati_curries)
        shack3 = random.choice(lentil_curries)
        shack5_6 = random.sample(punjabi_curries, 2)
        combo_key = (shack1, shack3, tuple(sorted(shack5_6)))

        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            with open(file_path, "wb") as f:
                pickle.dump(used_combinations, f)
            return {
                "Shack 1": shack1,
                "Shack 2": "Undhiyu",
                "Shack 3": shack3,
                "Shack 4": "Chole",
                "Shack 5": shack5_6[0],
                "Shack 6": shack5_6[1]
            }
    return None

# 🌟 Streamlit UI
st.set_page_config(page_title="Curry Shack Menu", page_icon="🍛", layout="centered")

st.title("🍛 Curry Shack Menu Generator")
st.markdown("Plan your meals with unique curry combinations! Choose an option below:")

# 🔘 Tabs for One-Day or Weekly View
tab1, tab2 = st.tabs(["📅 Single Day", "📆 Weekly Planner"])

with tab1:
    st.header("🍽️ Get Today's Menu")
    if st.button("🎲 Generate Today's Shack Menu"):
        menu = get_unique_menu()
        if menu:
            with st.container():
                for shack, item in menu.items():
                    st.markdown(f"**{shack}**: {item}")
        else:
            st.error("🎉 All combinations have been used!")

with tab2:
    st.header("🗓️ Weekly Shack Menu Planner")
    weekly_menus = []
    for day in range(1, 8):
        menu = get_unique_menu()
        if menu:
            menu["Day"] = f"Day {day}"
            weekly_menus.append(menu)
        else:
            st.warning(f"Only {day-1} days generated. All combinations used.")
            break

    if weekly_menus:
        df = pd.DataFrame(weekly_menus)[["Day", "Shack 1", "Shack 2", "Shack 3", "Shack 4", "Shack 5", "Shack 6"]]
        st.dataframe(df, use_container_width=True)

        # ⬇️ Download CSV
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Weekly Menu (CSV)", csv, "weekly_curry_menu.csv", "text/csv")

# ⚙️ Optional Sidebar Reset
with st.sidebar:
    if st.button("🔄 Reset All Used Combinations"):
        used_combinations.clear()
        with open(file_path, "wb") as f:
            pickle.dump(used_combinations, f)
        st.success("All combinations have been reset.")


