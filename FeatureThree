import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with your API key
client = OpenAI(api_key='Your-Open-AI-Key')

# Function to fetch average mortgage rates for each county in California from OpenAI
def fetch_mortgage_rate(county):
    # Define a prompt to fetch average mortgage rate for the selected county
    prompt = f"only give me the number and nothing else. What is the current average 30-year fixed mortgage rate for {county} county in California? only give me the number and nothing else. It is ok if its not the most current just pull information from the last available data."

    # Generate a text completion using the chat model
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a real estate agent in California"},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the response containing mortgage rate information
    mortgage_rate_text = completion.choices[0].message.content

    # Parse the response to extract the mortgage rate as a float
    mortgage_rate = float(mortgage_rate_text.strip('%'))
    return mortgage_rate

# Function to calculate monthly mortgage payments
def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    num_payments = loan_term_years * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    return monthly_payment

# Streamlit UI and main function
def main():
    st.title("Mortgage Calculator")

    # List of California counties
    california_counties = [
        'Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 'El Dorado',
        'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern', 'Kings', 'Lake', 'Lassen', 'Los Angeles',
        'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono', 'Monterey', 'Napa', 'Nevada',
        'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 'San Benito', 'San Bernardino', 'San Diego',
        'San Francisco', 'San Joaquin', 'San Luis Obispo', 'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz',
        'Shasta', 'Sierra', 'Siskiyou', 'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare',
        'Tuolumne', 'Ventura', 'Yolo', 'Yuba'
    ]

    # Dropdown menu to select a county
    selected_county = st.selectbox("Select County", california_counties)

    # Fetch mortgage rate for the selected county
    county_rate = fetch_mortgage_rate(selected_county)

    # Sidebar for loan details
    st.sidebar.title("Loan Details")
    interest_rate = st.sidebar.number_input("Interest Rate (%)", value=county_rate, min_value=0.0)
    loan_amount = st.sidebar.number_input("Loan Amount ($)", min_value=0)
    loan_term = st.sidebar.number_input("Loan Term (years)", min_value=1)

    # Calculate mortgage payments
    calculate_button = st.sidebar.button("Calculate Mortgage Payments")
    if calculate_button:
        monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        st.subheader("Monthly Mortgage Payment:")
        st.write(f"${monthly_payment:.2f}")

if __name__ == "__main__":
    main()
