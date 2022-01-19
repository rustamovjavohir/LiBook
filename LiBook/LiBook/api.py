from rest_framework.routers import DefaultRouter
from app.views import (UserViews,
                         BookViews,
                         BoxViews,
                         MessageViews,
                         ReplyMessageViews,
                       CateogryViews,
                       AdviceViews)

routers = DefaultRouter()
routers.register(r'user',UserViews,basename='user')
routers.register(r'cateogry',CateogryViews,basename='category')
routers.register(r'book',BookViews,basename='book')
routers.register(r'box',BoxViews,basename='box')
routers.register(r'Message',MessageViews,basename='Message')
routers.register(r'replymessage',ReplyMessageViews,basename='replymessage')
# routers.register(r'akkount',AkkountViews,basename='akkount')
routers.register(r'advice',AdviceViews,basename='advice')