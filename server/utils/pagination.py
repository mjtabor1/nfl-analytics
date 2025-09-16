from flask import request

def get_pagination(default_page=1, default_per_page=10, max_per_page=100):
    try:
        page = int(request.args.get("page", default_page))
        per_page = min(int(request.args.get("per_page", default_per_page)), max_per_page)
    except ValueError:
        page, per_page = default_page, default_per_page
    return page, per_page