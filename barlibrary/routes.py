def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Home page which will have buttons add_recipe and search_recipes
    config.add_route('home', '/')

    # Add_recipe page and add_recipe
    config.add_route('add_recipe', '/add_recipe')

    # View a recipe. Will
    config.add_route('recipe', '/{number}')
    config.add_route('login', '/login')