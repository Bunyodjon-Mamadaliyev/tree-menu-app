from django import template
from apps.tree_menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_tree': []}

    items = list(menu.items.all())
    current_path = request.path

    def build_tree(parent=None):
        tree = []
        for item in sorted([i for i in items if i.parent == parent], key=lambda x: x.order):
            node = {
                'item': item,
                'children': build_tree(parent=item),
                'is_active': item.get_absolute_url() == current_path,
            }
            if any(child['is_active'] for child in node['children']):
                node['is_active'] = True
            tree.append(node)
        return tree

    return {'menu_tree': build_tree()}
