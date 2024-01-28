from flasgger import swag_from
from flask import jsonify


def github_routes(app):
    @app.route('/api/items', methods=['GET'])
    def get_items():
        """
        Example endpoint returning a list of items.
        ---
        tags:
          - items
        responses:
          200:
            description: A list of items
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: string
        """
        return jsonify({"items": ["item1", "item2"]})
