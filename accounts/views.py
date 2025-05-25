from dj_rest_auth.views import UserDetailsView
from .serializers import MyPageSerializer

class MyPageView(UserDetailsView):
    serializer_class = MyPageSerializer