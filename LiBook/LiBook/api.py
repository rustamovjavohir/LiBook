from app.views import (UsersViews,
                       BookViews,
                       BoxViews,
                       CateogryViews,
                       AdviceViews)
from massages.views import (MessageViews, ReplyMessageViews)
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r'user', UsersViews, basename='user')
routers.register(r'cateogry', CateogryViews, basename='category')
routers.register(r'book', BookViews, basename='book')
routers.register(r'box', BoxViews, basename='box')
# routers.register(r'Message', MessageViews, basename='Message')
# routers.register(r'replymessage', ReplyMessageViews, basename='replymessage')
# routers.register(r'advice', AdviceViews, basename='advice')

urlpatterns = routers.urls
