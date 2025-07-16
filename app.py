import streamlit as st
import requests
import random

# --- Simulation Data ---
countries = [
    {"name": "India", "education_access": 0.65, "child_mortality": 0.03, "healthcare_quality": 0.6, "avg_internet_mins": 420, "avg_social_mins": 150},
    {"name": "DR Congo", "education_access": 0.43, "child_mortality": 0.09, "healthcare_quality": 0.4, "avg_internet_mins": 280, "avg_social_mins": 120},
    {"name": "Norway", "education_access": 0.98, "child_mortality": 0.005, "healthcare_quality": 0.95, "avg_internet_mins": 344, "avg_social_mins": 120},
    {"name": "Brazil", "education_access": 0.75, "child_mortality": 0.015, "healthcare_quality": 0.7, "avg_internet_mins": 552, "avg_social_mins": 229},
]

genders = ["female", "male", "non-binary"]
jobs = ["textile worker", "farmer", "vendor", "delivery person", "seamstress"]

def simulate_life():
    country = random.choice(countries)
    gender = random.choice(genders)
    story = []
    job = random.choice(jobs)
    dead = False
    age = 0

    story.append(f"You were born in {country['name']} and assigned {gender}.")

    if random.random() < country['child_mortality']:
        story.append("You died before age 5 due to a preventable illness.")
        return story, country

    story.append("You survived childhood. Your parents struggled to afford vaccines.")
    age = 5

    if random.random() < country['education_access']:
        story.append("You began school but had to walk barefoot for 3 km.")
    else:
        story.append("You never attended school, instead helping your parents work.")

    if random.random() < (1 - country['healthcare_quality']):
        story.append("At 16, you got sick but couldn't afford medicine. You passed away.")
        return story, country

    story.append(f"You became a {job}. It barely pays, but your family depends on you.")
    story.append(f"You died at {random.randint(25, 45)} due to unsafe work conditions.")

    return story, country

def moral_mirror(data, country):
    out = ["--- 🪞 MORAL MIRROR REFLECTION ---"]
    time_mins = data["time_online"] * 60
    overuse = max(0, time_mins - country['avg_internet_mins'])

    if overuse > 0:
        out.append(f"You used {time_mins:.0f} minutes online today — {overuse:.0f} more than the average in {country['name']}.")

    if data["spend"] > 100:
        meals = int(data["spend"] // 2)
        out.append(f"You spent ${data['spend']} on luxuries. That could feed {meals} children.")

    if data["donation"] == 0:
        out.append("You donated nothing. $5 could change someone's life.")
    else:
        out.append(f"You donated ${data['donation']} — a real impact in {country['name']}.")

    out.append("🌍 The simulation ends. But your power hasn't.")
    out.append("👇 Want to donate right now? 👇")

    return out

# --- Streamlit App ---
st.set_page_config("Moral Mirror", layout="centered")
st.title("🌐 Moral Mirror — Live a Life, Reflect on Yours")

if "story" not in st.session_state:
    st.session_state.story = None
    st.session_state.country = None

if st.button("▶️ Simulate a Life"):
    story, country = simulate_life()
    st.session_state.story = story
    st.session_state.country = country

if st.session_state.story:
    st.subheader("📖 Simulated Life")
    for line in st.session_state.story:
        st.markdown(f"- {line}")

    st.markdown("---")
    st.subheader("📊 Your Digital Footprint")

    time = st.slider("Hours online daily?", 0.0, 12.0, 5.0)
    spend = st.slider("Weekly luxury spending? ($)", 0, 500, 100)
    donate = st.slider("How much did you donate? ($)", 0, 200, 0)

    if st.button("💡 Reflect"):
        data = {"time_online": time, "spend": spend, "donation": donate}
        mirror = moral_mirror(data, st.session_state.country)
        st.subheader("🪞 Moral Reflection")
        for line in mirror:
            st.markdown(f"> {line}")

        if st.button("→ DONATE NOW ←"):
            try:
                res = requests.post("http://localhost:4242/create-checkout-session")
                session_url = res.json()["url"]
                st.markdown(f"[Click here to complete your donation]({session_url})")
            except:
                st.error("Unable to connect to donation backend.")
