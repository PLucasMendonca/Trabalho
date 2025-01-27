from ..app import db
from temp.models import Item


def get_all_items():
    return [item.to_dict() for item in Item.query.all()]


def add_item(data):
    item = Item(name=data['name'], description=data.get('description'))
    db.session.add(item)
    db.session.commit()
    return item.to_dict()
