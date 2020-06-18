from django.urls import reverse_lazy

NAV_POSTS = 'Posts'
NAV_ABOUT = 'About'

NAV_ITEMS = (
    (NAV_POSTS, reverse_lazy('home')),  # reverse_lazy makes url generated at the time of calling the function
    (NAV_ABOUT, reverse_lazy('about')),
)
#   reverse_lazy allows to resolve the url only at the time of use
#   avoid circular importation


def navigation_items(selected_item):
    items = []
    for name, url in NAV_ITEMS:
        items.append({
            'name': name,
            'url': url,
            'active': True if selected_item == name else False
            # active allows Highlight the correct item in the navigation bar.
        })
    return items
