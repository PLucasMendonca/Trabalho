from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
    {"id": 3, "name": "Item 3", "description": "This is item 3"}
]


@app.route('/items', methods=['GET'])
def get_items():
    """
    Retrieves the items.

    Returns:
        A JSON response containing the items.
    """
    return jsonify(items)


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Retrieves an item based on its ID.

    Parameters:
        item_id (int): The ID of the item to retrieve.

    Returns:
        If the item is found, returns a JSON response containing the item.
        If the item is not found, returns a JSON response with a "message" key
        set to "Item not found" and a status code of 404.
    """
    item = next((item for item in items if item['id'] == item_id), None)
    if item is not None:
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404


@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    new_item['id'] = len(items) + 1
    items.append(new_item)
    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Updates an item with the given item_id.

    Parameters:
    - item_id (int): The ID of the item to be updated.

    Returns:
    - dict: The updated item if found.
    - tuple: A tuple containing a message and status code if the item is not
    found.
    """
    item = next((item for item in items if item['id'] == item_id), None)
    if item is not None:
        data = request.get_json()
        item.update(data)
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Deletes an item from the list of items based on the given item_id.

    Parameters:
    - item_id (int): The ID of the item to be deleted.

    Returns:
    - tuple: A tuple containing a JSON response and a status code.
        - JSON response (dict): A dictionary containing the message
        "Item deleted".
        - Status code (int): The HTTP status code 204 (No Content).
    """
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted"}), 204


if __name__ == '__main__':
    app.run(debug=True)
