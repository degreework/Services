
from waliki.rest.views import PageCreateView as CreateView
from .serializers import PageCreateSerializer as CreateSer

class PageCreateView(CreateView):
	serializer_class = CreateSer