import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = "Your-Open-API-Key"

# Function to get completion using OpenAI Chat
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Function to pull average rent from OpenAI
def get_average_rent(city):
    prompt = f"What's the average rent in {city}?"
    response = get_completion(prompt)
    # Extract numerical value from the response
    rent_value = ''.join(filter(str.isdigit, response))
    return float(rent_value)

# Function to calculate affordability
def calculate_affordability(income, rent, expenses, savings, investments):
    total_expenses = sum(expenses)
    total_savings = sum(savings)
    total_investments = sum(investments)
    disposable_income = (income - total_expenses - rent - total_savings - total_investments)
    return disposable_income

# Main function
def main():
    st.title("BayBalance - Bay Area Affordability Calculator")

    cities = ['Berkeley', 'Oakland', 'San Leandro', 'Hayward', 'Fremont', 'Milpitas', 'San Jose', 'Sunnyvale', 'Palo Alto', 'San Mateo', 'Daly City', 'Pacifica']
    selected_city = st.selectbox("Select a city to live in:", cities)

    income = st.number_input("Enter your gross monthly income:", min_value=0.0)

    rent_amount = st.number_input("Enter your desired monthly rent amount:", min_value=0.0)

    food_expense = st.number_input("Enter your monthly food expense:", min_value=0.0)
    transportation_expense = st.number_input("Enter your monthly transportation expense:", min_value=0.0)
    activities_expense = st.number_input("Enter your monthly activities expense:", min_value=0.0)

    saving_amount = st.number_input("Enter the amount you want to save per month:", min_value=0.0)
    investment_amount = st.number_input("Enter the amount you want to invest per month:", min_value=0.0)

    if st.button("Calculate Affordability"):
        average_rent = get_average_rent(selected_city)
        expenses = [food_expense, transportation_expense, activities_expense]
        savings = [saving_amount]
        investments = [investment_amount]

        disposable_income = calculate_affordability(income, average_rent, expenses, savings, investments)

        st.write(
            f"Your disposable income after expenses, rent, savings, and investments in {selected_city} is ${disposable_income:.2f} per month.")

if __name__ == "__main__":
    main()


