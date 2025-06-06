import streamlit as st
import random
import os
import pickle
import pandas as pd
from datetime import date, datetime
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

# File paths
used_combo_file = "used_combinations.pkl"
daily_log_file = "daily_menu_log.csv"

# Load used combinations
if os.path.exists(used_combo_file):
    with open(used_combo_file, "rb") as f:
        used_combinations = pickle.load(f)
else:
    used_combinations = set()

# Gujarati curries with (J) for Jain-safe
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

def filter_gujarati(diet_type):
    if diet_type == "Jain":
        return [dish for dish in gujarati_curries if "(J)" in dish]
    return gujarati_curries

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
                "Date": str(date.today()),
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
    if os.path.exists(daily_log_file):
        df = pd.read_csv(daily_log_file)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([menu])], ignore_index=True)
    df.to_csv(daily_log_file, index=False)

def draw_calendar_heatmap(log_df):
    log_df["Date"] = pd.to_datetime(log_df["Date"])
    log_df["Month"] = log_df["Date"].dt.month
    log_df["Day"] = log_df["Date"].dt.day
    log_df["Count"] = 1
    pivot_table = log_df.pivot_table(index="Day", columns="Month", values="Count", aggfunc="sum", fill_value=0)
    plt.figure(figsize=(12, 4))
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlOrBr", cbar=False, linewidths=.5)
    plt.title("📅 Menu Entry Heatmap by Calendar")
    plt.xlabel("Month")
    plt.ylabel("Day")
    st.pyplot(plt)

st.set_page_config(page_title="Shack Menu Generator", page_icon="📋", layout="wide")

st.markdown("""
    <div style='background-color:#1f2937; padding:15px 10px; border-radius:10px; text-align:center; border: 1px solid #f97316;'>
        <h2 style='color:#f97316; margin:0;'>📋 Shack Menu Generator</h2>
        <p style='font-size:15px; color:#f3f4f6;'>Designed for restaurant staff to create daily & weekly curry combinations with dietary filters</p>
    </div>
    <br>
""", unsafe_allow_html=True)

st.markdown("---")
menu_option = st.sidebar.radio("Choose View", ["Daily Menu", "Weekly Planner", "Admin"])

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
            st.markdown("### ✅ TODAY’S MENU (LOCKED)")
            menu = st.session_state.locked_menu
            if menu:
                st.markdown(f"<div style='background-color:#2d3748;padding:10px;border-radius:5px;margin-bottom:10px;color:#f3f4f6;'>Gujarati Type: <b>{menu['Gujarati Type']}</b></div>", unsafe_allow_html=True)
                shack_icons = ["🥬", "🥘", "🫘", "🍛", "🍲", "🍲"]
                shack_colors = ["#38bdf8", "#38bdf8", "#a3e635", "#a3e635", "#facc15", "#facc15"]
                for i in range(1, 7):
                    label = f"Shack {i}"
                    dish = menu[label]
                    icon = shack_icons[i - 1]
                    color = shack_colors[i - 1]
                    st.markdown(f"""
                        <div style='background-color:{color};padding:10px 15px;border-radius:8px;margin-bottom:5px;'>
                        <b>{icon} {label}:</b> {dish}
                        </div>
                    """, unsafe_allow_html=True)
            if st.button("🔓 Unlock & Regenerate"):
                st.session_state.menu_locked = False
                st.session_state.locked_menu = None

elif menu_option == "Weekly Planner":
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
        df = pd.DataFrame(menu_plan)
        def highlight_jain(val):
            if val == "Jain":
                return 'background-color: #eafaf1; font-weight: bold; color: #1e4620'
            return ''
        styled_df = df[["Day", "Gujarati Type", "Shack 1", "Shack 2", "Shack 3", "Shack 4", "Shack 5", "Shack 6"]].style.applymap(
            highlight_jain, subset=["Gujarati Type"]
        )
        with st.expander("📋 View Weekly Plan"):
            st.dataframe(styled_df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Weekly Menu (CSV)", csv, "weekly_shack_menu.csv", "text/csv")
    else:
        st.warning("No menus could be generated.")

elif menu_option == "Admin":
    st.header("🛠️ Admin Panel")
    with st.expander("🗂️ View Daily Menu Log"):
        if os.path.exists(daily_log_file):
            log_df = pd.read_csv(daily_log_file)
            log_df["Date"] = pd.to_datetime(log_df["Date"])
            min_date = log_df["Date"].min()
            max_date = log_df["Date"].max()
            date_range = st.date_input("Select Date Range", [min_date.date(), max_date.date()])
            selected_dish = st.selectbox("Filter by Gujarati Dish (Optional)", ["All"] + sorted(log_df["Shack 1"].unique().tolist()))
            filtered_df = log_df[
                (log_df["Date"] >= pd.to_datetime(date_range[0])) &
                (log_df["Date"] <= pd.to_datetime(date_range[1]))
            ]
            if selected_dish != "All":
                filtered_df = filtered_df[filtered_df["Shack 1"] == selected_dish]
            st.dataframe(filtered_df)
            st.download_button("📥 Download Filtered Log", filtered_df.to_csv(index=False), "filtered_menu_log.csv")
            with st.expander("📊 Show Heatmap by Calendar"):
                draw_calendar_heatmap(filtered_df)
        else:
            st.info("No logs found yet.")
