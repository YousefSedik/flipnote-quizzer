from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import RegisterSerializer


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


create_user = CreateUserView.as_view()

class ViewProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    
view_profile = ViewProfileAPIView.as_view()