import streamlit as st
import random
import os
import pickle
import pandas as pd
from datetime import datetime, date, timedelta
from streamlit_calendar import calendar
import pytz

# Set timezone for Los Angeles
LA_TZ = pytz.timezone("America/Los_Angeles")

# File paths
used_combo_file = "used_combinations.pkl"
daily_log_file = "daily_menu_log.csv"

# Load used combinations
if os.path.exists(used_combo_file):
    with open(used_combo_file, "rb") as f:
        used_combinations = pickle.load(f)
else:
    used_combinations = set()

# Dishes

gujarati_curries = [
    "Bhindi Potato", " Stuffed Bhindi (J)", "Bhindi Masala (J)", "Cauliflower Peas Potato",
    "Cauliflower Peas Tomato (J)", "Cauliflower Potato Tomato", "Eggplant Lilva/Eggplant Toover", 
    "Eggplant Potato", "Eggplant Potato Raviya", "Potato Rasa", "Potato Tomato", "Tindora Potato Rasa", 
    "Tindora Masala (J)", "Tindora Ravaiya (J)", "Tindora Rasa", "Turiya Patra (J)"
]

punjabi_curries = [
    "Baigan Bharta", "Dum Aloo", "Dal Makhani", "Dal Fry", "Tadka Dal", "Malai Kofta", 
    "Methi Mutter Malai", "Vegetable Korma", "Vegetable Jelfrazi", "Navratan Korma", "Kaju Corn",
    "Kaju Khoya", "Shahi Paneer", "Palak Paneer", "Kadai Paneer", "Mutter Paneer",
    "Paneer Tikka", "Paneer Angara", "Paneer Chettinad", "Paneer Bhurji", "Paneer Pasanda"
]

lentil_curries = [
    "Vaal/Lima Beans", "Mix Kathod", "Moong Rasa", "Sprouted Moong",
    "Rajma", "Black Chana", "Red Chori", "White Chori"
]

def filter_gujarati(diet_type):
    return [dish for dish in gujarati_curries if "(J)" in dish] if diet_type == "Jain" else gujarati_curries

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
            with open(used_combo_file, "wb") as f:
                pickle.dump(used_combinations, f)
            return {
                "Date": datetime.now(LA_TZ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                "Gujarati Type": diet_type,
                "Shack 1": shack1,
                "Shack 2": "Undhiyu",
                "Shack 3": shack3,
                "Shack 4": "Chole",
                "Shack 5": shack5_6[0],
                "Shack 6": shack5_6[1]
            }
    return None

def save_menu_to_log(menu):
    df = pd.read_csv(daily_log_file) if os.path.exists(daily_log_file) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([menu])], ignore_index=True)
    df.to_csv(daily_log_file, index=False)

def get_calendar_events(df):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    events = []
    for d in df["Date"].dt.date.unique():
        events.append({
            "title": "✔ Menu Saved",
            "start": d.strftime("%Y-%m-%d"),
            "allDay": True,
            "color": "#22c55e"
        })
    return events

# --- UI Begins ---
st.set_page_config(page_title="SABJI MENU GENERATOR", page_icon="📋", layout="wide")

st.markdown("""
    <div style='background-color:#1f2937; padding:15px 10px; border-radius:10px; text-align:center; border: 1px solid #f97316;'>
        <h2 style='color:#f97316; margin:0;'>📋 SABJI MENU GENERATOR</h2>
        <p style='font-size:15px; color:#f3f4f6;'>Your Daily Sabji Planner!</p>
    </div>
    <br>
""", unsafe_allow_html=True)

menu_option = st.sidebar.radio("Choose View", ["Daily Menu", "Weekly Planner", "Admin"])

# --- Daily Menu ---
if menu_option == "Daily Menu":
    st.header("🎲 Generate Today's Menu")
    with st.expander("🔐 Lock/Unlock Today's Menu"):
        if "menu_locked" not in st.session_state:
            st.session_state.menu_locked = False
            st.session_state.locked_menu = None

        if not st.session_state.menu_locked:
            diet_type = st.radio("Gujarati Dish Type:", ["None", "Jain"])
            if st.button("Generate Menu"):
                menu = get_unique_menu(diet_type)
                if menu:
                    st.session_state.locked_menu = menu
                    st.session_state.menu_locked = True
                    save_menu_to_log(menu)
                else:
                    st.error("No valid combinations found.")
        else:
            menu = st.session_state.locked_menu
            if menu:
                st.markdown(f"<div style='background-color:#2d3748;padding:10px;border-radius:5px;margin-bottom:10px;color:#f3f4f6;'>Gujarati Type: <b>{menu['Gujarati Type']}</b></div>", unsafe_allow_html=True)
              for i in range(1, 7):
    ...
    st.markdown(f"""
        <div style='background-color:#facc15;padding:10px 15px;border-radius:8px;margin-bottom:5px;'>
        <b>{label}:</b> {dish}
        </div>
    """, unsafe_allow_html=True)
            if st.button("🔓 Unlock & Regenerate"):
                st.session_state.menu_locked = False
                st.session_state.locked_menu = None

# --- Weekly Planner ---
elif menu_option == "Weekly Planner":
    st.header("📆 Weekly Menu Planner")
    today = date.today()
    weekdays = [(today + timedelta(days=i)).strftime("%A") for i in range(7)]
    jain_days_selected = st.multiselect("Pick Days for Jain Gujarati Dish", weekdays)

    menu_plan = []
    for i, day in enumerate(weekdays):
        diet_type = "Jain" if day in jain_days_selected else "None"
        menu = get_unique_menu(diet_type)
        if menu:
            menu["Day"] = day
            menu_plan.append(menu)

    if menu_plan:
        df = pd.DataFrame(menu_plan)
        def highlight_jain(val):
            return 'background-color: #eafaf1; font-weight: bold; color: #1e4620' if val == "Jain" else ''
        styled_df = df[["Day", "Gujarati Type", "Shack 1", "Shack 2", "Shack 3", "Shack 4", "Shack 5", "Shack 6"]].style.applymap(
            highlight_jain, subset=["Gujarati Type"]
        )
        with st.expander("📋 View Weekly Plan"):
            st.dataframe(styled_df, use_container_width=True)
        st.download_button("⬇️ Download Weekly Menu (CSV)", df.to_csv(index=False), "weekly_shack_menu.csv")

# --- Admin Panel ---
elif menu_option == "Admin":
    st.header("🛠️ Admin Panel")
    if os.path.exists(daily_log_file):
        log_df = pd.read_csv(daily_log_file)
        log_df["Date"] = pd.to_datetime(log_df["Date"], errors="coerce")
        min_date = log_df["Date"].min()
        max_date = log_df["Date"].max()

        with st.expander("🗂️ View Daily Menu Log"):
            date_range = st.date_input("Select Date Range", [min_date.date(), max_date.date()])
            selected_dish = st.selectbox("Filter by Gujarati Dish (Optional)", ["All"] + sorted(log_df["Shack 1"].dropna().unique().tolist()))
            filtered_df = log_df[
                (log_df["Date"] >= pd.to_datetime(date_range[0])) &
                (log_df["Date"] <= pd.to_datetime(date_range[1]))
            ]
            if selected_dish != "All":
                filtered_df = filtered_df[filtered_df["Shack 1"] == selected_dish]
            st.dataframe(filtered_df)
            st.download_button("📥 Download Filtered Log", filtered_df.to_csv(index=False), "filtered_menu_log.csv")

        st.subheader("📊 Show Calendar with Used Dates")
        try:
            events = get_calendar_events(filtered_df)
            calendar_options = {
                "initialView": "dayGridMonth",
                "editable": False,
                "headerToolbar": {
                    "left": "prev,next today",
                    "center": "title",
                    "right": "dayGridMonth,listMonth"
                },
                "height": 550
            }
            calendar(events=events, options=calendar_options)
        except Exception:
            st.warning("Unable to load calendar events.")
    else:
        st.info("No logs found yet.")
