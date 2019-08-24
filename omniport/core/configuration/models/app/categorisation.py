class Categorisation:
    """
    This class stores information about the category tree
    """

    def __init__(self, *args, **kwargs):
        """
        Parse the dictionaries generated from YAML files into a class-object
        representation
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        category_list = kwargs.get('list') or list()
        self.categories = [
            Category(
                dictionary=category
            )
            for category in category_list
        ]


class Category:
    """
    This class stores information about a category, namely its name, slug
    and subcategories
    """

    def __init__(self, *args, **kwargs):

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')
        self.slug = dictionary.get('slug')
        self.categories = [
            Category(
                dictionary=category
            )
            for category in dictionary.get('categories') or []
        ]
