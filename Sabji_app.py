import streamlit as st
import random
import os
import pickle

# 📦 File to store used combinations
file_path = "used_combinations.pkl"

# 📥 Load from file if exists
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

# 🧠 Menu Generator
def get_unique_menu():
    for _ in range(1000):
        shack1 = random.choice(gujarati_curries)
        shack3 = random.choice(lentil_curries)
        shack5_6 = random.sample(punjabi_curries, 2)
        combo_key = (shack1, shack3, tuple(sorted(shack5_6)))

        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            # Save updated set
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

# 🎨 Web Interface
st.title("🍛 Curry Shack Menu Generator")
st.subheader("✨ Get a new unique curry menu every time!")

if st.button("Get Today’s Menu"):
    menu = get_unique_menu()
    if menu:
        for shack, item in menu.items():
            st.markdown(f"**{shack}**: {item}")
    else:
        st.error("🎉 All combinations have been used!")

# 🔁 Optional Reset Button (for admin/testing)
if st.sidebar.button("🔄 Reset Combinations"):
    used_combinations.clear()
    with open(file_path, "wb") as f:
        pickle.dump(used_combinations, f)
    st.sidebar.success("All combinations have been reset.")

