from django.template.response import TemplateResponse


def shop_detail(request, id):
    return TemplateResponse(request, "single_shop.html", {})