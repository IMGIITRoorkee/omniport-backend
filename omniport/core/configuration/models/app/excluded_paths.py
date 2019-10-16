class ExcludedPath:

    def __init__(self, *args, **kwargs):

        super().__init__()
        self.excluded_paths = []
        dictionary = kwargs.get('dictionary') or dict()
        list_excluded_paths = dictionary.get('excluded_paths')

        if list_excluded_paths is not None:
            for i in list_excluded_paths:
                self.excluded_paths.append(i) 
