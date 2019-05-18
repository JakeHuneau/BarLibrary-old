def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Home page which will have buttons add_recipe and search_recipes
    config.add_route('bar_library_home', '/')
    config.add_route('add_recipe', 'add_recipe')
    config.add_route('remove_recipe', 'remove_recipe')
    config.add_route('find_recipes', 'find_recipes')
    config.add_route('find_all', 'find_all')
    config.add_route('user_page', 'user_page')
    config.add_route('change_permission', 'change_permission')
    config.add_route('kitchen', 'kitchen')
    config.add_route('search_recipe', 'search_recipe')
    config.add_route('new_user', 'new_user')
    config.add_route('add_subtype', 'add_subtype')
    config.add_route('contact', 'contact')
