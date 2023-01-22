from rest_framework import views
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
# from rest_framework_swagger.views import get_swagger_view

# class CustomSecuritySchemaView(views.APIView):
    # def get(self, request):
        # auto_schema = AutoSchema()
        # auto_schema.get_authentication_fields = lambda: ['email', 'password']
        # generator = get_swagger_view(title='My API')
        # return generator(request, auto_schema=auto_schema)
