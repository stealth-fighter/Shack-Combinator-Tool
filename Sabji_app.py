import streamlit as st
import random

# Static in-memory storage (this resets every time the app restarts)
used_combinations = set()

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

def get_unique_menu():
    for _ in range(1000):
        shack1 = random.choice(gujarati_curries)
        shack3 = random.choice(lentil_curries)
        shack5_6 = random.sample(punjabi_curries, 2)
        combo_key = (shack1, shack3, tuple(sorted(shack5_6)))
        if combo_key not in used_combinations:
            used_combinations.add(combo_key)
            return {
                "Shack 1": shack1,
                "Shack 2": "Undhiyu",
                "Shack 3": shack3,
                "Shack 4": "Chole",
                "Shack 5": shack5_6[0],
                "Shack 6": shack5_6[1]
            }
    return None

# Streamlit App UI
st.title("🍛 Curry Shack Menu Generator")
st.write("Click the button below to get today's unique curry menu!")

if st.button("Get Today's Menu"):
    menu = get_unique_menu()
    if menu:
        for shack, item in menu.items():
            st.write(f"**{shack}**: {item}")
    else:
        st.warning("All unique combinations have been used!")
