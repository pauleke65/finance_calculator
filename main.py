from flask import Flask, render_template, request
import os

app = Flask(__name__)


# Function to calculate budget allocations and remaining balance
def calculate_budget(one_time_amount, debt_amount, isDigital=True):
    # Create a dictionary to store the budget percentages for each category
    budget_percentages = {
        'Income Increase': 0.0,
        'Investing': 0.35,
        'Emergency Fund': 0.15,
        'Debt Repayment': debt_amount,
        'Tithe': 0.10,
        'Kingdom Investment': 0.05,
        'Transaction Fees': isDigital and 0.025 or 0.0,
    }

    # Calculate the budget amounts for each category
    budget = {}
    total_budget = 0
    for category, percentage in budget_percentages.items():
        if category == 'Debt Repayment':
            budget[category] = percentage
        else:
            budget[category] = one_time_amount * percentage
        total_budget += budget[category]

    # Calculate the remaining balance
    remaining_balance = one_time_amount - total_budget

    # Return the budget allocations and remaining balance
    return budget, remaining_balance

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling the form submission
@app.route('/calculate', methods=['POST'])
def calculate():
    one_time_amount = float(request.form['amount'])
    debt_amount = float(request.form['debt'])
    is_digital = request.form.get('digital', False)

    budget, remaining_balance = calculate_budget(one_time_amount, debt_amount, is_digital)

    return render_template('result.html', budget=budget, remaining_balance=remaining_balance)



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
