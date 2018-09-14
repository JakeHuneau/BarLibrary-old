import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from barlibrary.models.meta import Base
from barlibrary.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from barlibrary.models import Ingredient, RecipeIngredient, Recipe, User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)


        basic = User(name='Jake')
        basic.set_password('password')
        dbsession.add(basic)

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
                               directions='Saturate sugar cube with bitters and a bit of water.'
                                          'Muddle until dissolved. Fill glass with ice and whiskey.'
                                          'Garnish with orange slice and cherry.')
        dbsession.add(old_fashioned)
        dbsession.flush()

        link1 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=bourbon.id,
                                 quantity=1.5,
                                 unit='oz',
                                 requred=1)
        link2 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=sugar.id,
                                 quantity=1,
                                 unit='cube',
                                 requred=1)
        link3 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=angostura.id,
                                 quantity=3,
                                 unit='dash',
                                 requred=1)
        link4 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=water.id,
                                 quantity=1,
                                 unit='splash',
                                 requred=0)
        link5 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=orange.id,
                                 quantity=1,
                                 unit='slice',
                                 requred=1)
        link6 = RecipeIngredient(recipe_id=old_fashioned.id,
                                 ingredient_id=cherry.id,
                                 quantity=1,
                                 unit='',
                                 requred=0)
        dbsession.add_all([link1, link2, link3, link4, link5, link6])
