import streamlit as st
import openai

# OpenAI API key
openai.api_key='Your-API-Key-Here'

# Dictionary mapping cities to their OpenAI identifiers
city_mapping = {
    'Berkeley': 'city of berkeley',
    'Oakland': 'city of oakland',
    'San Leandro': 'city of san leandro',
    'Hayward': 'city of hayward',
    'Fremont': 'city of fremont',
    'Santa Clara': 'city of santa clara',
    'Milpitas': 'city of milpitas',
    'San Jose': 'city of san jose',
    'Sunnyvale': 'city of sunnyvale',
    'Palo Alto': 'city of palo alto',
    'San Mateo': 'city of san mateo',
    'Daly City': 'city of daly city',
    'Pacifica': 'city of pacifica'
}

# Function to get average monthly rent for a city from OpenAI
import re

def get_average_rent(city, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the prompt to your best abilities"},
            {"role": "user", "content": "What is the average monthly rent in " + city + "?"},
        ]
    )
    rent_response = response['choices'][0]['message']['content'].strip()
    rent = re.findall(r'\d+,\d+', rent_response)
    if rent:
        rent = float(rent[0].replace(',', ''))
    else:
        rent = None
    return rent

# Function to get average loan interest rate for a city from OpenAI
def get_average_interest_rate(city, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the prompt to your best abilities"},
            {"role": "user", "content": "What is the average loan interest rate in " + city + "?"},
        ]
    )
    rate_response = response['choices'][0]['message']['content'].strip()
    rate = re.findall(r'\d+.\d+', rate_response)
    if rate:
        rate = float(rate[0])
    else:
        rate = None
    return rate

# Function to fetch average mortgage rates for each county in California from OpenAI
def fetch_mortgage_rate(city):
    # Define a prompt to fetch average mortgage rate for the selected county
    prompt = f"only give me the number and nothing else. What is the current average 30-year fixed mortgage rate for {city} county in California? only give me the number and nothing else. It is ok if its not the most current just pull information from the last available data."

    # Generate a text completion using the chat model
    completion = openai.ChatCompletion.create(
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

# Function to adjust interest rate based on credit score
def adjust_interest_rate(interest_rate, credit_score):
    # Adjust interest rate based on credit score
    if credit_score >= 800:
        return interest_rate * 0.95  # Reduce interest rate by 0.5% for excellent credit
    elif 740 <= credit_score < 800:
        return interest_rate  # No change for good credit
    elif 680 <= credit_score < 740:
        return interest_rate * 1.05  # Increase interest rate by 0.5% for fair credit
    else:
        return interest_rate * 1.1  # Increase interest rate by 1% for poor credit


# Function to calculate monthly mortgage payments
def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    num_payments = loan_term_years * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    return monthly_payment

# Streamlit UI components
st.title("BayBalance AI")

feature = st.selectbox("Select Feature", ["Affordability Calculator", "Mortgage Loan Calculator", "Expense Categorizer"])

if feature == "Affordability Calculator":
    st.title("Affordability Calculator")

    selected_city = st.selectbox("Select a city", list(city_mapping.keys()))
    average_rent = get_average_rent(city_mapping[selected_city])
    st.info(f"The average monthly rent in {selected_city} is {average_rent}")
    monthly_income = st.number_input("Enter your gross monthly income", value=0.0, step=100.0)
    transportation_cost = st.number_input("Enter transportation cost per month", value=0.0, step=10.0)
    food_cost = st.number_input("Enter food cost per month", value=0.0, step=10.0)
    entertainment_cost = st.number_input("Enter entertainment cost per month", value=0.0, step=10.0)
    activities_cost = st.number_input("Enter activities cost per month", value=0.0, step=10.0)
    savings_amount = st.number_input("Enter how much you want to save per month", value=0.0, step=10.0)
    investment_amount = st.number_input("Enter how much you want to invest per month", value=0.0, step=10.0)

    # Calculate total expenses
    total_expenses = transportation_cost + food_cost + entertainment_cost + activities_cost + savings_amount + investment_amount

    # Get average rent for the selected city
    average_rent = get_average_rent(city_mapping[selected_city])

    # Calculate affordability
    affordability = monthly_income - float(average_rent) - total_expenses

    # Display affordability result
    if affordability < 0:
        st.error("User cannot afford to live in selected area.")
        lower_rent_areas = [city for city, city_id in city_mapping.items() if city != selected_city and float(get_average_rent(city_id)) < float(average_rent)]
        if lower_rent_areas:
            st.warning(f"Consider living in these areas with lower average rents: {', '.join(lower_rent_areas)}")
        else:
            st.warning("User can't afford to live in any other areas in the Bay Area.")
    else:
        st.success("User can afford to live in selected area.")

elif feature == "Mortgage Loan Calculator":
    st.title("Mortgage Loan Calculator")

    selected_city = st.selectbox("Select a city", list(city_mapping.keys()))
    loan_amount = st.number_input("Enter loan amount", value=0.0, step=1000.0)

    county_rate = fetch_mortgage_rate(selected_city)

       # Sidebar for loan details
    st.sidebar.title("Loan Details")
    credit_score = st.sidebar.number_input("Credit Score", min_value=300, max_value=850, value=700)
    interest_rate = st.sidebar.number_input("Interest Rate (%)", value=county_rate, min_value=0.0)
    loan_amount = st.sidebar.number_input("Loan Amount ($)", min_value=0)
    loan_term = st.sidebar.number_input("Loan Term (years)", min_value=1)

    # Adjust interest rate based on credit score when the button is clicked
    if st.sidebar.button("Adjust Interest Rate"):
        interest_rate = adjust_interest_rate(interest_rate, credit_score)

    # Calculate mortgage payments
    calculate_button = st.sidebar.button("Calculate Mortgage Payments")
    if calculate_button:
        monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        st.subheader("Monthly Mortgage Payment:")
        st.write(f"${monthly_payment:.2f}")

elif feature == "Expense Categorizer":
    st.title("Expense Categorizer")

    st.write("This tool helps you categorize your expenses into different categories.")
    st.write("Enter your expenses below and click on the 'Categorize Expenses' button to categorize them.")

    # Create a text area for entering expenses
    expenses = st.text_area("Enter your expenses (one per line)", height=200)

    # Create a button to categorize expenses
    if st.button("Categorize Expenses"):
        # Split the entered expenses into lines
        expense_lines = expenses.split("\n")

        # Define categories and keywords for each category
        categories = {
            "Food": ["food", "restaurant", "grocery", "meal"],
            "Transportation": ["transport", "car", "gas", "uber", "lyft"],
            "Housing": ["rent", "mortgage", "housing", "property"],
            "Entertainment": ["entertainment", "movie", "game", "concert"],
            "Utilities": ["utilities", "electricity", "water", "internet"],
            "Health": ["health", "doctor", "hospital", "medicine"],
            "Shopping": ["shopping", "clothes", "shoes", "electronics"],
            "Travel": ["travel", "flight", "hotel", "vacation"],
            "Education": ["education", "school", "college", "books"],
            "Other": ["other"]
        }

        # Initialize an empty dictionary to store categorized expenses
        categorized_expenses = {category: [] for category in categories}

        # Categorize each expense based on keywords
        for expense in expense_lines:
            categorized = False
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in expense.lower():
                        categorized_expenses[category].append(expense)
                        categorized = True
                        break
                if categorized:
                    break
            if not categorized:
                categorized_expenses["Other"].append(expense)

        # Display categorized expenses
        for category, expenses in categorized_expenses.items():
            if expenses:
                st.subheader(category)
                st.write("\n".join(expenses))
            else:
                st.write(f"No {category} expenses found.")
