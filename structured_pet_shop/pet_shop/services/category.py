def get_all():
    from pet_shop.models.category import get_all_categories
    categories, error = get_all_categories()
    return categories, error


def get_by_id(id):
    from pet_shop.models.category import get_category_by_id
    category, error = get_category_by_id(id)
    return category, error


def save(data: dict):
    from pet_shop.models.category import create_category, update_category
    error = ''
    if data:
        if data.get('name') and not data.get('id'):
            _, error = create_category(data)
        if data.get('name') and data.get('id'):
            _, error = update_category(data)
    return _, error


def delete(id):
    from pet_shop.models.category import delete_category
    category, error = delete_category(id)
    return category, error
