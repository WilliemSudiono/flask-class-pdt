def get_all():
    from pet_shop.models.pet import get_all_pets
    pets, error = get_all_pets()
    return pets, error


def get_by_id(id):
    from pet_shop.models.pet import get_pet_by_id
    pet, error = get_pet_by_id(id)
    return pet, error


def save(data: dict):
    from pet_shop.models.pet import create_pet, update_pet
    error = ''
    if data:
        if data.get('name') and data.get('category_id') and not data.get('id'):
            _, error = create_pet(data)
        if data.get('name') and data.get('category_id') and data.get('id'):
            _, error = update_pet(data)
    return _, error


def delete(id):
    from pet_shop.models.pet import delete_pet
    pet, error = delete_pet(id)
    return pet, error
