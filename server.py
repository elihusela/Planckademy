import utils
from flask import Flask, jsonify, request
import pandas as pd

# Technical pandas detail - cancelling non-relevant warnings for this implementations.
pd.options.mode.chained_assignment = None

relevant_keys = ['dishId', 'dishName', 'dishDescription', 'dishPrice']


def run_server(db):

    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        return "Planckademy Assignment"

    @app.before_request
    def before_request_callback():
        #DB update check
        update = utils.check_update()
        if update:
            db = utils.get_db()
        return

    @app.route('/drinks', methods=['GET'])
    def drinks():
        drinks = db.loc[db['dishType'] == 'Drink']
        drinks.drop(columns=['dishType'], inplace=True)
        return drinks.to_html()

    @app.route('/drink', methods=['GET'])
    def drink():
        drinks = db.loc[db['dishType'] == 'Drink']
        # Check if an ID was provided as part of the URL. If no ID is provided, display an error in the browser.
        if 'id' in request.args:
                # TODO: Error handling: Check id format to be a valid integer.
            id = int(request.args['id'])
            drink = drinks.loc[drinks['dishId'] == id]
                # TODO: Error handling: If id is not in the database - return err message.
            return drink.to_html()
        else:
            return page_not_found('No Id given')

    @app.route('/pizzas', methods=['GET'])
    def pizzas():
        pizzas = db[db['dishType'] == 'Pizza']
        pizzas.drop(columns=['dishType'], inplace=True)
        return pizzas.to_html()

    @app.route('/pizza', methods=['GET'])
    def pizza():
        pizzas = db[db['dishType'] == 'Pizza']
        # Check if an ID was provided as part of the URL. If no ID is provided, display an error in the browser.
        if 'id' in request.args:
                # TODO: Error handling: Check id format to be a valid integer.
            id = int(request.args['id'])
            pizza = pizzas.loc[pizzas['dishId'] == id]
                # TODO: Error handling: If id is not in the database - return err message.
            return pizza.to_html()
        else:
            return page_not_found('Incorrect dish Id')

    @app.route('/desserts', methods=['GET'])
    def desserts():
        desserts = db[db['dishType'] == 'Dessert']
        desserts.drop(columns=['dishType'], inplace=True)
        return desserts.to_html()

    @app.route('/dessert', methods=['GET'])
    def dessert():
        desserts = db[db['dishType'] == 'Dessert']
        # Check if an ID was provided as part of the URL. If no ID is provided, display an error in the browser.
        if 'id' in request.args:
                # TODO: Error handling: Check id format to be a valid integer.
            id = int(request.args['id'])
            dessert = desserts.loc[desserts['dishId'] == id]
                # TODO: Error handling: If id is not in the database - return err message.
            return dessert.to_html()
        else:
            return page_not_found('Incorrect dish Id')

    @app.route('/order', methods=['POST'])
    def get_order():
        if not request.is_json:
            page_not_found('Bad order format.')
        # Get all Ids from given format
        # TODO: Error handling: Check Ids and values for integers only.
        drink_ids = request.json['drinks']
        pizza_ids = request.json['pizzas']
        dessert_ids = request.json['desserts']
        # Concat
        ids = drink_ids + pizza_ids + dessert_ids

        # Extract relevant dishes and sum prices
        dishes = db[db['dishId'].isin(ids)]
        tot_price = dishes['dishPrice'].sum()
        return jsonify({"price": int(tot_price)})

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404.

    app.run()

