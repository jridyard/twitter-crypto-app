from flask import Blueprint

blueprint = Blueprint(
    'base',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)
