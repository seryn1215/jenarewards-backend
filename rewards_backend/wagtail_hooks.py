from wagtail.wagtail_hooks import hooks

HIDE_ITEMS = ["documents", "images", "pages", "help"]


@hooks.register("construct_main_menu")
def hide_menu_items(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in HIDE_ITEMS]
