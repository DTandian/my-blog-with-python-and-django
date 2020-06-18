from blog.models import Post, PostCategory

# we can create a default category called All
post_category_all = PostCategory(name='All')


#  we filter a post depending a parameter as status, category
def get_category_and_posts(category_name):
    # posts contents all posts published
    posts = Post.objects.filter(published=True)
    # use pass variable if don't know what treatment done
    if category_name == post_category_all.slug():
        category = post_category_all
    #  if category differ to post_category_all
    else:
        try:
            category = PostCategory.objects.get(name__iexact=category_name)
            # test of category name not consider case sensitive (name__iexact)
            posts = posts.filter(category=category)
        except PostCategory.DoesNotExist:
            #  create fictive category
            category = PostCategory(name=category_name)
            posts = Post.objects.none()  # empty list in Django iterable to make possible use order_by

    #  reverse chronology order
    posts = posts.order_by('-date')
    return category, posts


#  allows to return list all categories
def get_categories():
    categories = list(PostCategory.objects.all().order_by('name'))
    # list allows to convert in Python list object
    categories.insert(0, post_category_all)
    return categories
