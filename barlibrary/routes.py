def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Home page which will have buttons add_recipe and search_recipes
    config.add_route('home', '/')
