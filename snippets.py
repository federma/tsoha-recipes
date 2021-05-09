def convert_to_int(str_list):
    """Converts a list of strings to a list integers. If item cannot be converted, returns 0 for that item"""
    int_list = []
    for s in str_list:
        try:
            x = int(s)
            int_list.append(x)
        except:
            int_list.append(0)
    return int_list


def validate_recipe_form(recipe_name, description, instructions, ingredients, amounts):
    """Checks forms fiels. Return str 'validation_ok' if there are no errors. Otherwise returns the error-message."""
    if len(recipe_name) > 100:
        return "Reseptin nimi saa sisältää enintään 100 merkkiä."

    if len(description) > 1000:
        return "Kuvaus saa sisältää enintään 1000 merkkiä."

    if len(instructions) > 2000:
        return "Ohje saa sisältää enintään 2000 merkkiä."

    if len(recipe_name) == 0 or len(description) == 0 or len(instructions) == 0:
        return "Lomakkeeseen ei saa jättää tyhjiä kenttiä."

    for i in ingredients:
        if len(i) == 0:
            return "Ainesosa oli jätetty tyhjäksi."
        if len(i) > 100:
            return "Ainesosan nimi saa sisältää enintään 100 merkkiä."

    for i in amounts:
        if i > 10000:
            return "Määrä ei saa olla yli 10000"
        if i < 0:
            return "Määrä ei saa olla negatiivinen"

    return "validation_ok"