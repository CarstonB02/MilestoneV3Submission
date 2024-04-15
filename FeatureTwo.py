import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with your API key
client = OpenAI(api_key='key')

# Function to fetch community insights and amenities
def fetch_community_insights(community):
    prompt = f"Provide a detailed list of amenities available in {community} community, including schools, parks, shopping centers, and healthcare facilities."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert on California communities and their amenities."},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the response containing community insight information
    amenities_info = completion.choices[0].message.content
    return amenities_info

# Streamlit UI and main function
def main():
    st.title("Community Amenities Finder")

    # Dropdown menu to select a community
    california_communities = [
        'Downtown', 'Midtown', 'Suburb', 'Riverside', 'Hillside', 'Lakeside'
    ]
    selected_community = st.selectbox("Select Community", california_communities)

    # Button to fetch community insights
    fetch_button = st.button("Fetch Community Insights")
    if fetch_button:
        community_insights = fetch_community_insights(selected_community)
        st.subheader(f"Amenities in {selected_community} Community:")
        st.write(community_insights)

if __name__ == "__main__":
    main()
