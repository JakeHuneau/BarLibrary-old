def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Home page which will have buttons add_recipe and search_recipes
    config.add_route('home', '/')
    config.add_route('bar_library_home', 'bar_library')
    config.add_route('add_recipe', 'bar_library/add_recipe')
    config.add_route('remove_recipe', 'bar_library/remove_recipe')
    config.add_route('find_recipes', 'bar_library/find_recipes')
    config.add_route('find_all', 'bar_library/find_all')