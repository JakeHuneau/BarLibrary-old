import transaction

from barlibrary.models.meta import Base
from barlibrary.models import (
    get_session_factory,
    get_tm_session,
    )
from barlibrary.models import Ingredient, RecipeIngredient, Recipe, User, Kitchen

from sqlalchemy import create_engine


def main():
    engine = create_engine('sqlite:///../../recipeDB.db', echo=True)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)


        jake = User(name='Jake')
        jake.set_password('password')
        dbsession.add(jake)

        whiskey = Ingredient(name='whiskey')
        bourbon = Ingredient(name='bourbon')
        rye = Ingredient(name='rye')
        vodka = Ingredient(name='vodka')
        tequila = Ingredient(name='tequila')
        rum = Ingredient(name='rum')
        gin = Ingredient(name='gin')
        dbsession.add_all([whiskey, bourbon, rye, vodka, tequila, rum, gin])

        angostura = Ingredient(name='angostura bitters')
        for bitter in [angostura]:
            dbsession.add(bitter)

        sugar = Ingredient(name='sugar')
        dbsession.add(sugar)

        water = Ingredient(name='water')
        dbsession.add(water)

        orange = Ingredient(name='orange')
        dbsession.add(orange)

        cherry = Ingredient(name='cherry')
        dbsession.add(cherry)

        old_fashioned = Recipe(name='old fashioned',
                               directions='1. Saturate sugar cube with bitters and a bit of water.\n'
                                          '2. Muddle until dissolved.\n3. Fill glass with ice and whiskey.\n'
                                          '4. Garnish with orange slice and cherry.')
        dbsession.add(old_fashioned)
        dbsession.flush()

        link1 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=bourbon.id,
                                 quantity=1.5,
                                 unit='oz',
                                 required=1)
        link2 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=sugar.id,
                                 quantity=1,
                                 unit='cube',
                                 required=1)
        link3 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=angostura.id,
                                 quantity=3,
                                 unit='dash',
                                 required=1)
        link4 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=water.id,
                                 quantity=1,
                                 unit='splash',
                                 required=0)
        link5 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=orange.id,
                                 quantity=1,
                                 unit='slice',
                                 required=1)
        link6 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=cherry.id,
                                 quantity=1,
                                 unit='',
                                 required=0)
        dbsession.add_all([link1, link2, link3, link4, link5, link6])

        k_link1 = Kitchen(user_id=jake.id,
                          ingredient_id=whiskey.id)
        dbsession.add(k_link1)


if __name__ == '__main__':
    main()