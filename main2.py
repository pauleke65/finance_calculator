# import requests
# import yaml
# import json
# from flasgger import Swagger
# from flask import Flask, render_template, request, jsonify
# import os


# from app_secrets import AppSecrets
# from modules.github.routes import github_routes

# app = Flask(__name__)


# app.config['SWAGGER'] = {
#     'title': 'My API',
#     'uiversion': 3
# }
# swagger = Swagger(app)

# github_routes(app)


# # # Function to calculate budget allocations and remaining balance
# # def calculate_budget(one_time_amount, debt_amount, isDigital=True):
# #     # Create a dictionary to store the budget percentages for each category
# #     budget_percentages = {
# #         'Income Increase': 0.0,
# #         'Investing': 0.35,
# #         'Emergency Fund': 0.15,
# #         'Debt Repayment': debt_amount,
# #         'Tithe': 0.10,
# #         'Kingdom Investment': 0.05,
# #         'Transaction Fees': isDigital and 0.025 or 0.0,
# #     }

# #     # Calculate the budget amounts for each category
# #     budget = {}
# #     total_budget = 0
# #     for category, percentage in budget_percentages.items():
# #         if category == 'Debt Repayment':
# #             budget[category] = percentage
# #         else:
# #             budget[category] = one_time_amount * percentage
# #         total_budget += budget[category]

# #     # Calculate the remaining balance
# #     remaining_balance = one_time_amount - total_budget

# #     # Return the budget allocations and remaining balance
# #     return budget, remaining_balance

# # # Route for the home page

# print(app.config)


# swagger = app.config.get('SWAGGER', {})
# print(swagger)


# @app.route('/api/spec')
# def spec():
#     return jsonify(swagger.template)


# @app.route('/')
# def home():
#     return render_template('index.html')


# # Route for handling the form submission


# # @app.route('/calculate', methods=['POST'])
# # def calculate():
# #     one_time_amount = float(request.form['amount'])
# #     debt_amount = float(request.form['debt'])
# #     is_digital = request.form.get('digital', False)

# #     budget, remaining_balance = calculate_budget(
# #         one_time_amount, debt_amount, is_digital)

# #     return render_template('result.html', budget=budget, remaining_balance=remaining_balance)


# if __name__ == '__main__':
#     app.run(debug=True, port=os.getenv("PORT", default=5000))
import os
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

from app_secrets import AppSecrets
from modules.github.routes import github_routes

app = APIFlask(__name__, title='My API')

app.servers = [
    {
        'url': 'http://127.0.0.1:5000' if AppSecrets.environment == 'dev' else 'http://api.paulimoke.com',
        'description': 'Server URL'
    }
]
pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get('/')
@app.doc(operation_id='SayHello', tags=['Pets'])
def say_hello():
    # returning a dict or list equals to use jsonify()
    return {'message': 'Hello!'}


@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
@app.doc(responses={404: {'description': 'Pet not found'}}, operation_id='GetPet')
def get_pet(pet_id):
    if pet_id > len(pets) - 1:
        abort(404)
    # you can also return an ORM/ODM model class instance directly
    # APIFlask will serialize the object into JSON format
    return pets[pet_id]


@app.get('/pets')
@app.output(PetOut(many=True))
@app.doc(operation_id='GetPets')
def get_pets():
    return pets


@app.patch('/pets/<int:pet_id>')
@app.input(PetIn(partial=True))  # -> json_data
@app.output(PetOut)
@app.doc(responses={404: {'description': 'Pet not found'}}, operation_id='UpdatePet', tags=['Pets'])
def update_pet(pet_id, json_data):
    # the validated and parsed input data will
    # be injected into the view function as a dict
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in json_data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]


github_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
