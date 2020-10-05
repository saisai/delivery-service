from rest_framework.renderers import JSONRenderer


class UTF8JsonRenderer(JSONRenderer):
    charset = 'utf-8'