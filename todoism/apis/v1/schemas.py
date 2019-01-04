import flask

from todoism.models import Item


def user_schema(user):
    return {
        'id': user.id,
        'self': flask.url_for('.user', _external=True),
        'kind': 'User',
        'username': user.username,
        'all_items_url': flask.url_for('.items', _external=True),
        'active_items_url': flask.url_for('.active_items', _external=True),
        'completed_items_url': flask.url_for('.completed_items', _external=True),
        'all_item_count': len(user.items),
        'active_item_count': Item.query.with_parent(user).filter_by(done=False).count(),
        'completed_item_count': Item.query.with_parent(user).filter_by(done=True).count(),
    }


def item_schema(item):
    return {
        'id': item.id,
        'self': flask.url_for('.item', item_id=item.id, _external=True),
        'kind': 'Item',
        'body': item.body,
        'done': item.done,
        'author': {
            'id': 1,
            'url': flask.url_for('.user', _external=True),
            'username': item.author.username,
            'kind': 'User',
        },
    }


def items_schema(items, current, prev, next, pagination):
    return {
        'self': current,
        'kind': 'ItemCollection',
        'items': [item_schema(item) for item in items],
        'prev': prev,
        'last': flask.url_for('.items', page=pagination.pages, _external=True),
        'first': flask.url_for('.items', page=1, _external=True),
        'next': next,
        'count': pagination.total
    }
