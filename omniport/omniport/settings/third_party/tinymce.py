"""
This settings file exposes settings for TinyMCE
"""

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'contextmenu '
               'lists link table image codesample charmap '
               'fullscreen '
               'wordcount',
    'contextmenu': 'bold italic underline strikethrough '
                   'superscript subscript '
                   'link',
    'toolbar1': 'formatselect '
                '| bold italic underline strikethrough blockquote removeformat '
                '| alignleft aligncenter alignright alignjustify',
    'toolbar2': 'undo redo '
                '| bullist numlist outdent indent '
                '| link unlink '
                '| table image codesample charmap '
                '| fullscreen',
    'height': 512,
    'width': 'auto',
    'menubar': False,
    'branding': False,
}
