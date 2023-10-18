from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetFixed(LimitOffsetPagination):
    """
    This is overriding the default limit offset pagination because by default there is no way to specify a max-limit
    This would expose a vulnerability where anyone could request every single one of a given object from the database at
    once, creating a super long request. To prevent this, a max limit of 1000 has been implemented.
    https://www.django-rest-framework.org/api-guide/pagination/
    https://github.com/encode/django-rest-framework/blob/cdc956a96caafddcf4ecaf6218e340ebb3ce6d72/rest_framework/pagination.py#L367

    This frustrates me more than I can ever put into words
    """

    default_limit = 10
    max_limit = 100
