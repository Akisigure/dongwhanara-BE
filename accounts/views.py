from dj_rest_auth.views import UserDetailsView
from .serializers import MyPageSerializer
from rest_framework.permissions import IsAuthenticated


class MyPageView(UserDetailsView):
    serializer_class = MyPageSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user