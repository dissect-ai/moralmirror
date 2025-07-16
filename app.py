import streamlit as st
from random import choice, randint, random

# --- Life simulation logic (same as your backend) ---
countries = [
    {"name": "India", "education_access": 0.65, "child_mortality": 0.03, "healthcare_quality": 0.6, "avg_internet_mins": 420, "avg_social_mins": 150},
    {"name": "DR Congo", "education_access": 0.43, "child_mortality": 0.09, "healthcare_quality": 0.4, "avg_internet_mins": 280, "avg_social_mins": 120},
    {"name": "Norway", "education_access": 0.98, "child_mortality": 0.005, "healthcare_quality": 0.95, "avg_internet_mins": 344, "avg_social_mins": 120},
    {"name": "Brazil", "education_access": 0.75, "child_mortality": 0.015, "healthcare_quality": 0.7, "avg_internet_mins": 552, "avg_social_mins": 229},
]

genders = ["female", "male", "non-binary"]

def simulate_life():
    country = choice(countries)
    gender = choice(genders)
    age = 0
    dead = False
    story = []

    story.append(f"You are born in {country['name']}, assigned female at birth ({gender}).")

    if random() < country['child_mortality']:
        story.append("You died before the age of 5 due to preventable illness.")
        dead = True
        age = randint(0, 5)
    else:
        story.append("You survive childhood. Access to vaccines was marginal.")
        age = 5

    if not dead:
        if random() < country['education_access']:
            story.append("You begin primary school. You have a worn uniform and must walk 3 miles.")
        else:
            story.append("You never attend school. You help your family with farm labor.")
        age += 7

    if not dead and age < 18:
        age = 18
        if random() < country['healthcare_quality']:
            story.append("You survive a major illness at 17 thanks to donated antibiotics.")
        else:
            story.append("You contract a severe illness at 17. There was no treatment available.")
            dead = True
            age = 18

    if not dead:
        story.append("You reach adulthood. You dream of becoming a nurse but support your siblings instead.")
        age = randint(25, 45)

    if not dead:
        story.append(f"You die at age {age} due to unsafe working conditions in a textile factory.")

    return story, country

def moral_mirror(data, country):
    output = ["--- 🪞 MORAL MIRROR REFLECTION ---\n"]
    time_spent = data['time_online'] * 60
    spend = data['spend']
    donation = data['donation']

    overuse = max(0, time_spent - country['avg_internet_mins'])

    if overuse > 0:
        output.append(f"You spent {time_spent:.0f} minutes online today — that's {overuse:.0f} minutes more than the average person in {country['name']}.")
        output.append("Imagine if half of that time was used to tutor or help someone like the person you just witnessed.\n")

    if spend > 100:
        meals = int(spend // 2)
        output.append(f"You spent ${spend} on non-essentials. That could’ve funded {meals} meals for children in {country['name']}.")

    if donation == 0:
        output.append("You made no donations. Just $5 can provide a malaria treatment, school kit, or clean water access.")
        output.append("You can literally save a life for less than a burger combo.\n")
    else:
        output.append(f"You donated ${donation}. That may have given someone in {country['name']} another year to live with dignity.\n")

    output.append("🌍 The simulation ends — but your real-life power doesn't.\n👉 [DONATE NOW](https://www.globalgiving.org/) 👈")
    return output

# --- Streamlit UI ---
st.set_page_config("Moral Mirror", layout="centered")
st.title("🧬 Moral Mirror — One Life. One Chance.")
st.markdown("Simulate a real-world life. Then face your digital reflection.")

if st.button("▶️ Begin Simulation"):
    story, country = simulate_life()
    st.subheader("📖 Life Story")
    for line in story:
        st.markdown(f"- {line}")

    st.markdown("---")

    st.subheader("📊 Your Real-Life Inputs")
    time = st.slider("How many hours online daily?", 0.0, 12.0, 4.5)
    spend = st.slider("How much did you spend on non-essentials this week? ($)", 0, 500, 100)
    donate = st.slider("How much did you donate? ($)", 0, 200, 0)

    if st.button("💡 Reflect on Your Impact"):
        user_data = {"time_online": time, "spend": spend, "donation": donate}
        reflection = moral_mirror(user_data, country)
        st.subheader("🪞 Moral Mirror Reflection")
        for line in reflection:
            st.markdown(f"> {line}")