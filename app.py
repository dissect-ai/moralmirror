import streamlit as st
import random

# --- Country + Socioeconomic Data ---
countries = [
    {"name": "India", "education_access": 0.65, "child_mortality": 0.03, "healthcare_quality": 0.6, "avg_internet_mins": 420, "avg_social_mins": 150},
    {"name": "DR Congo", "education_access": 0.43, "child_mortality": 0.09, "healthcare_quality": 0.4, "avg_internet_mins": 280, "avg_social_mins": 120},
    {"name": "Norway", "education_access": 0.98, "child_mortality": 0.005, "healthcare_quality": 0.95, "avg_internet_mins": 344, "avg_social_mins": 120},
    {"name": "Brazil", "education_access": 0.75, "child_mortality": 0.015, "healthcare_quality": 0.7, "avg_internet_mins": 552, "avg_social_mins": 229},
]

genders = ["female", "male", "non-binary"]
jobs = ["factory worker", "farmer", "textile weaver", "delivery person", "market vendor"]

# --- Simulation Logic ---
def simulate_life():
    country = random.choice(countries)
    gender = random.choice(genders)
    job = random.choice(jobs)
    story = []
    dead = False
    age = 0

    story.append(f"You were born in **{country['name']}** and assigned **{gender}**.")

    if random.random() < country['child_mortality']:
        story.append("❌ You died before age 5 due to a preventable illness.")
        return story, country

    story.append("✅ You survived childhood despite limited healthcare.")
    age = 5

    if random.random() < country['education_access']:
        story.append("📘 You walked 3 km to a government school, often without shoes.")
    else:
        story.append("🚫 You never attended school. You worked in the fields instead.")

    if random.random() < (1 - country['healthcare_quality']):
        story.append("🛑 At 16, you became ill and couldn't access treatment. You passed away.")
        return story, country

    story.append(f"💼 You worked as a {job}, earning enough to survive but not to thrive.")
    story.append(f"⚰️ You died at {random.randint(25, 45)} due to unsafe working conditions.")

    return story, country

# --- Reflection Logic ---
def moral_mirror(data, country):
    out = ["--- 🪞 MORAL MIRROR REFLECTION ---"]
    time_mins = data["time_online"] * 60
    overuse = max(0, time_mins - country['avg_internet_mins'])

    if overuse > 0:
        out.append(f"🕒 You used **{time_mins:.0f} mins online today** — {overuse:.0f} mins more than the average in **{country['name']}**.")
        out.append("📱 Imagine using that time to volunteer, mentor, or advocate.")

    if data["spend"] > 100:
        meals = int(data["spend"] // 2)
        out.append(f"💸 You spent **${data['spend']}** on luxuries. That could fund **{meals} meals** in {country['name']}.")

    if data["donation"] == 0:
        out.append("🚫 You donated **nothing**. Even **$5** could change someone’s life.")
    else:
        out.append(f"✅ You donated **${data['donation']}** — that could fund medicine or education in {country['name']}.")

    out.append("🌍 The simulation ends. But your real-world power hasn't.")
    out.append("👇 Take action now and make a real difference 👇")

    return out

# --- Streamlit UI ---
st.set_page_config("Moral Mirror", layout="centered")
st.title("🌐 Moral Mirror")
st.markdown("Simulate a random life born anywhere in the world. Then reflect on your own.")

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
    st.subheader("📊 Your Real-Life Footprint")

    time = st.slider("Daily time online (hrs)", 0.0, 12.0, 5.0)
    spend = st.slider("Luxury spending this week ($)", 0, 500, 120)
    donate = st.slider("How much did you donate this week? ($)", 0, 200, 0)

    if st.button("💡 Reflect"):
        data = {"time_online": time, "spend": spend, "donation": donate}
        mirror = moral_mirror(data, st.session_state.country)

        st.subheader("🪞 Reflection")
        for line in mirror:
            st.markdown(f"> {line}")

        st.markdown("---")
        st.markdown("### 💝 Ready to help for real?")
        st.markdown("[👉 Click here to donate securely](https://buy.stripe.com/test_9B64gBcfl7aL8lLc7CfrW00)")
        st.markdown("You’ll be redirected to a Stripe-hosted secure donation page.")

        st.success("Thank you for making an impact. 🌱")

