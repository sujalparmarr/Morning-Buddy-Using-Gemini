import streamlit as st
st.set_page_config(
    page_title="Morning Buddy",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* FULL PURE BLACK MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: #000000 !important;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] > div:first-child {
    background: #111111 !important;
    padding-top: 20px;
    border-right: 1px solid rgba(255,255,255,0.07);
}

/* MAKE THE TOP HEADER TOOLBAR PURE BLACK */
[data-testid="stHeader"] {
    background: #000000 !important;
}

[data-testid="stToolbar"] {
    background: #000000 !important;
}

/* REMOVE SIDEBAR COLLAPSE ARROW */
button[kind="header"] {
    display: none !important;
}

/* PREVENT SIDEBAR COLLAPSE */
[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

</style>
""", unsafe_allow_html=True)



import random
from applications import temperature_of_city, get_news, news_summarizer, smart_plan

# --- Page Configuration ---

# --- Helper Functions ---
def get_random_quote():
    quotes = [
        "Every morning is a new page. Write something worth reading.",
        "Small steps today become big wins tomorrow.",
        "A fresh morning is life’s way of giving you another chance.",
        "Start your day with intention, not pressure.",
        "You don’t need a perfect morning — just a peaceful one.",
        "One good thought in the morning can change your whole day.",
        "Rise with purpose, move with patience, end with gratitude.",
        "Your mind is strongest in the morning — feed it something good.",
        "The day feels lighter when your first thought is hopeful.",
        "Even a slow morning can lead to a powerful day.",
        "The morning is quiet — that’s your advantage.",
        "Today is full of small opportunities disguised as routine.",
        "Begin with clarity. Continue with courage.",
        "You don’t need motivation. Just start — the motivation follows.",
        "A new morning means a new version of you."
    ]
    return random.choice(quotes)


def get_random_image():
    # Lightweight morning/aesthetic images (compressed for fast loading)
    image_urls = [
        "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1505483531331-2811a6a5b0a4?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1470123808288-1e59739c28a6?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1482192596544-9eb780fc7f66?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1483683804023-6ccdb62f86ef?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1501549538849-2ffce8821fbe?w=1200&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1520038410233-7141be7e6f97?w=1200&auto=format&fit=crop&q=60"
    ]
    return random.choice(image_urls)



# --- Page Definitions ---

def home_page():
    """Displays the home page with a quote and image."""
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap" rel="stylesheet">

    <style>
    .glass-title {
    font-family:'Montserrat', sans-serif;
    font-size:66px;
    font-weight:900;
    text-align:center;
    color:#e0e0e0;

    text-shadow:
        0 0 10px rgba(255,255,255,0.6),
        0 0 25px rgba(255,255,255,0.4),
        0 0 40px rgba(255,255,255,0.2);
    margin-bottom: 10px;
    margin-top: -10px;
    }
    </style>

    <h1 class="glass-title">☀️ Your Morning Buddy</h1>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("A Thought for Your Day")
    st.info(f'"{get_random_quote()}"')
    st.image(get_random_image(), caption="A beautiful morning to start your day", use_container_width=True)
    st.markdown("---")
    st.write("Use the sidebar on the left to get your daily updates!")

def weather_news_page():
    """Displays the page for getting weather and news by city."""
    st.header("Get Weather of the city")
    city = st.text_input("Enter your city name:")

    if st.button("Fetch Information"):
        if city:
            temperature_output= temperature_of_city(city)
            st.subheader(f"Weather Info: {temperature_output}")
            st.success("Weather  fetched successfully!!!!")
        else:
            st.error("Please enter a city name.")

def interest_news_page():
    """Displays the page for getting news by interest."""
    st.header("Get News Based on Your Interests")
    interest = st.text_input("Enter your area of interest (e.g., Technology, Sports, Health):", "Technology")

    if st.button("Fetch News"):

    if interest:
        articles = get_news(interest)

        # If no articles at all
        if not articles:
            st.error("No news found. Please try a different topic.")
            return

        # Limit to max 5
        articles = articles[:5]

        st.subheader("Latest News")

        for i, article in enumerate(articles):
            title_item = article.get("title", "No Title")
            url_item = article.get("url", "")
            img_item = article.get("urlToImage", None)

            # Fix invalid or missing images
            if not img_item or img_item.endswith(".gif"):
                img_item = "https://via.placeholder.com/400x250.png?text=No+Image"

            with st.container():
                st.markdown(f"### 📰 {title_item}")
                st.image(img_item, use_container_width=True)
                st.write("🔗 Read Article:", url_item)
                st.write("📝 Summary:", news_summarizer(url_item))
                st.markdown("---")

    else:
        st.error("Please enter an interest topic.")



def smart_planner():
    """Displays the page for viewing the day's schedule."""
    st.header("Your Smart Planner Day")
    city = st.text_input("Enter your city name:")
    if st.button("Let's Plan"):
        if city:
            smart_plans= smart_plan(city)
            st.subheader(smart_plans)
            st.success("Have a nice day.")
        else:
            st.error("Please enter  a  city name")


# --- Sidebar Navigation ---
st.sidebar.title("Morning Toolkit")
st.sidebar.markdown("---")
page_option = st.sidebar.radio("Choose a page:", ("Home", "Get Weather of your City", "News by Interest", "Plan My Day"))
st.sidebar.markdown("---")


# --- Page Routing ---
if page_option == "Home":
    home_page()
elif page_option == "Get Weather of your City":
    weather_news_page()
elif page_option == "News by Interest":
    interest_news_page()
elif page_option == "Plan My Day":
    smart_planner()
    

    
