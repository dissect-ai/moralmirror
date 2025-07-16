import streamlit as st
import random

# --- Real-world data approximations (expanded) ---
countries = [
    {"name": "India", "education_access": 0.65, "child_mortality": 0.03, "healthcare_quality": 0.6, "avg_internet_mins": 420, "avg_social_mins": 150},
    {"name": "DR Congo", "education_access": 0.43, "child_mortality": 0.09, "healthcare_quality": 0.4, "avg_internet_mins": 280, "avg_social_mins": 120},
    {"name": "Norway", "education_access": 0.98, "child_mortality": 0.005, "healthcare_quality": 0.95, "avg_internet_mins": 344, "avg_social_mins": 120},
    {"name": "Brazil", "education_access": 0.75, "child_mortality": 0.015, "healthcare_quality": 0.7, "avg_internet_mins": 552, "avg_social_mins": 229},
]

genders = ["female", "male", "non-binary"]
jobs = ["textile worker", "farmer", "factory assistant", "childcare helper", "street vendor", "delivery biker"]

# --- Simulation Engine ---
def simulate_life():
    country = random.choice(countries)
    gender = random.choice(genders)
    story = []
    state = {
        "dead": False,
        "age": 0,
        "country": country["name"],
        "gender": gender,
        "job": random.choice(jobs),
        "attended_school": False,
        "survived_illness": False,
    }

    story.append(f"You are born in {country['name']} and assigned {gender}.")

    # Childhood
    if random.random() < country['child_mortality']:
        story.append("You died before age 5 due to a preventable disease.")
        state["dead"] = True
        state["age"] = random.randint(0, 4)
        return story, country

    story.append("You survived childhood — barely. Healthcare access was limited.")
    state["age"] = 5

    # School
    if random.random() < country['education_access']:
        state["attended_school"] = True
        story.append("You start walking 3km to a government school. You love math, but miss classes often.")
    else:
        story.append("You never attend school. Instead, you collect water and care for siblings.")

    state["age"] += 7

    # Teenage illness
    if random.random() < (1 - country['healthcare_quality']):
        story.append("At age 16, you contract typhoid. There is no medicine available.")
        state["dead"] = True
        state["age"] = 16
        return story, country
    else:
        story.append("You survive a serious illness in your teens thanks to a mobile clinic.")
        state["survived_illness"] = True

    # Adulthood
    state["age"] = random.randint(25, 45)
    story.append(f"You become a {state['job']} to support your family. You earn just enough to survive.")
    
    # Optional branching
    if state["attended_school"]:
        story.append("You secretly tutor children in your neighborhood and dream of becoming a teacher.")
    else:
        story.append("You sometimes wonder what life might've been like if you'd gone to school.")

    # Death
    story.append(f"You die at age {state['age']} due to workplace exposure in a {state['job']} setting.")
    state["dead"] = True

    return story, country

# --- Judgment Phase ---
def moral_mirror(real_life_data, country):
    output = ["--- 🪞 MORAL MIRROR REFLECTION ---\n"]
    time_spent = real_life_data["time_online"] * 60
    spend = real_life_data["spend"]
    donation = real_life_data["donation"]

    overuse = max(0, time_spent - country["avg_internet_mins"])

    if overuse > 0:
        output.append(f"You spent {time_spent:.0f} minutes online today — that's {overuse:.0f} minutes more than the average in {country['name']}.")
        output.append("What if half that time was used to teach, help, or heal someone like the life you just witnessed?\n")

    if spend > 100:
        meals = int(spend // 2)
        output.append(f"You spent ${spend} on luxuries this week. That could have fed {meals} children in {country['name']}.")

    if donation == 0:
        output.append("You donated nothing. Yet even $5 could provide medicine, clean water, or school supplies.")
        output.append("You can literally save a life for the price of a milkshake.\n")
    else:
        output.append(f"You donated ${donation}. That may have added a year of life, school, or safety for someone in {country['name']}.\n")

    output.append("🌍 The simulation ends. But your power hasn’t. Choose action.\n")
    output.append("👉 [Donate Now](https://www.globalgiving.org/) 👈")

    return output

# --- Streamlit App ---
st.set_page_config("Moral Mirror", layout="centered")
st.title("🌐 Moral Mirror — Simulate a Life. Reflect on Yours.")
st.markdown("Experience one randomly-generated life from around the world. Then compare it to your own digital footprint.")

# Session state for continuity
if "life" not in st.session_state:
    st.session_state.life = None
    st.session_state.country = None

# Simulate button
if st.button("▶️ Simulate a Life"):
    story, country = simulate_life()
    st.session_state.life = story
    st.session_state.country = country

# Display life story
if st.session_state.life:
    st.subheader("📖 Life Story")
    for line in st.session_state.life:
        st.markdown(f"- {line}")

    st.markdown("---")
    st.subheader("📊 Your Real-Life Inputs")
    time = st.slider("How many hours online daily?", 0.0, 12.0, 4.5, step=0.5, key="time")
    spend = st.slider("How much did you spend on non-essentials this week? ($)", 0, 500, 100, key="spend")
    donate = st.slider("How much did you donate this week? ($)", 0, 200, 0, key="donate")

    if st.button("💡 Reflect on Your Impact"):
        user_data = {
            "time_online": st.session_state.time,
            "spend": st.session_state.spend,
            "donation": st.session_state.donate,
        }
        reflection = moral_mirror(user_data, st.session_state.country)
        st.subheader("🪞 Your Moral Mirror")
        for line in reflection:
            st.markdown(f"> {line}")
