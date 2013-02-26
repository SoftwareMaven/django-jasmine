
def init_media_types():
    # Make sure our ExtendedMedia takes over for django.widgets.Media
    from .utils import *

init_media_types()
