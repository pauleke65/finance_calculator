import os
from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

from app_secrets import AppSecrets
from modules.github.routes import github_routes

app = APIFlask(__name__, title='Paul Imoke Digital Life API')

app.servers = [
    {
        'url': 'http://127.0.0.1:5000' if AppSecrets.environment == 'dev' else 'https://api.paulimoke.com',
        'description': 'Server URL'
    }
]


@app.get('/')
@app.doc(operation_id='SayGoodBye', tags=['Home'])
def say_hello():
    # returning a dict or list equals to use jsonify()
    return {'message': 'GoodBye Boi!'}


github_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
