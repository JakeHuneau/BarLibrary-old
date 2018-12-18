from wtforms import Form, StringField, validators


class NewRecipeForm(Form):
    recipe_name = StringField('Recipe Name', [validators.InputRequired()])
    ingredient_list = StringField('Ingredients', [validators.InputRequired()])
    directions = StringField('Directions', [validators.InputRequired()])