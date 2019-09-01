defaults = {
    "fetch_likes_plays": False,
    "fetch_likers": False,
    "fetch_comments": False,
    "fetch_mentions": False,
    "fetch_hashtags": False,
    "fetch_details": False
}


def apply_defaults(cls):
    for name, value in defaults.items():
        setattr(cls, name, value)
    return cls


@apply_defaults
class settings(object):
    pass


def override_settings(args):
    for name in defaults.keys():
        setattr(settings, name, getattr(args, name))


def prepare_override_settings(parser):
    for name in defaults.keys():
        parser.add_argument("--" + name, action="store_true")
