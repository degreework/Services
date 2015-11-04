# -*- coding: utf-8 -*-

from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Module
from .serializers import ModuleSerializer, ModuleUpdateSerializer

from gamification.models import Scores
from  gamification.signals import calculate_points_end_badge

from project.permissions import IsTeacher

class ModuleCreateView(viewsets.ModelViewSet):
    """
    API endpoint for creating a Module
    """
    serializer_class = ModuleSerializer
    permission_classes = (IsTeacher, )


class ModuleUpdateView(viewsets.ModelViewSet):
    """
    API endpoint for retrieve, update, destroy a Module
    """
    lookup_field = 'slug'
    queryset = Module.objects.all()
    serializer_class = ModuleUpdateSerializer
    permission_classes = (IsTeacher, )
    

class ModuleReadView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retreive an Module
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'


class ModuleListView(generics.ListAPIView):
    """
    View to list all Modules in app
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated, )
    paginate_by = 10


"""Views for Forum wrap"""
from rest_framework.decorators import api_view, permission_classes
from forum.views import AskCreateView
from forum.models import Ask

from .models import Module, Forum_wrap
from django.http import Http404

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_forum_create_wrap(request, module):
    """
    wrap create Ask
    """
    try:
        module = Module.objects.get(slug=module)
        response = AskCreateView.as_view({'post':'create'})(request)
        if 201 == response.status_code:
            ask = Ask.objects.get(pk=response.data['id'])
            Forum_wrap(module=module, ask=ask).save()
        
        return response

    except Module.DoesNotExist:
        raise Http404


from forum.models import Ask
from forum.serializers import ShortAskSerializer

class ForumList(generics.ListAPIView):
    """
    View to list all Ask in the foro.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = ShortAskSerializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_ask = Forum_wrap.objects.filter(module=module).values_list('ask', flat=True)
        asks = Ask.objects.filter(pk__in=list_ask)
        return asks


"""Views for Activitie wrap"""
from activitie.views import ActivitieParentCreateView
from activitie.models import ActivitieParent
from .models import Activitie_wrap


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_activitie_create_wrap(request, module):
    """
    wrap create Activitie Parent
    """
    try:
        badge = module
        module = Module.objects.get(slug=module)
        response = ActivitieParentCreateView.as_view({'post':'create'})(request)
        if 201 == response.status_code:
            activitie = ActivitieParent.objects.get(pk=response.data['id'])
            Activitie_wrap(module=module, activitie=activitie).save()
            
            #Se crea el puntaje en la tabla de scores
            Scores(id_event=activitie.id, score=10, event="Activity").save()
            
            # Se envia la señal para aunmentar los puntos con los que se gana la medalla
            calculate_points_end_badge.send(sender=module_activitie_create_wrap, badge=badge, author=request.user, points=10, action='add', element='activitie', instance_element=activitie)

            #create Stream at User's wall
            from actstream import action
            action.send(request.user, verb='creado', action_object=activitie, target=module)

        return response

    except Module.DoesNotExist:
        raise Http404


from activitie.serializers import ActivitieParentSerializer

class ActivitieList(generics.ListAPIView):
    """
    View to list all Activitites
    """
    permission_classes = (AllowAny,)
    serializer_class = ActivitieParentSerializer
    paginate_by = 10


    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_activities = Activitie_wrap.objects.filter(module=module).values_list('activitie', flat=True)
        activities = ActivitieParent.objects.filter(pk__in=list_activities)
        return activities


"""Views for Wiki wrap"""
from .models import Wiki_wrap
#from waliki.rest.views import PageCreateView
from wiki.views import PageCreateView
from waliki.models import Page

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_wiki_create_wrap(request, module):
    """
    wrap create Wiki
    """
    try:
        module = Module.objects.get(slug=module)
        response = PageCreateView.as_view()(request)
        if 201 == response.status_code:
            page = Page.objects.get(slug=response.data['slug'])
            Wiki_wrap(module=module, page=page).save() 
        return response

    except Module.DoesNotExist:
        raise Http404

    except Page.DoesNotExist:
        return response

from wiki.models import Request
from wiki.serializers import RequestSerializer

class RequestList(generics.ListAPIView):
    """
    View to list all Wiki's request.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = RequestSerializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_wiki = Wiki_wrap.objects.filter(module=module).values_list('page', flat=True)
        request = Request.objects.filter(page__in=list_wiki, checked=False)
        return request


class HistoryList(generics.ListAPIView):
    """
    View to list History Wiki's request.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = RequestSerializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_wiki = Wiki_wrap.objects.filter(module=module).values_list('page', flat=True)
        request = Request.objects.filter(page__in=list_wiki, approved=True)
        return request

from wiki.models import PublicPage
from wiki.serializers import PublicPageSerializer

class PublishedList(generics.ListAPIView):
    """
    View to list Published Wiki's request.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PublicPageSerializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_wiki = Wiki_wrap.objects.filter(module=module).values_list('page', flat=True)
        #request = Request.objects.filter(page__in=list_wiki, approved=True)
        public = PublicPage.objects.filter(request__page=list_wiki)
        return public


"""Views for Evaluations"""
from servicio.views import Quiz_Create_View
from quiz.models import Quiz
from .models import Quiz_wrap

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_quiz_create_wrap(request, module):
    """
    wrap create Quiz
    """
    try:
        badge = module
        module = Module.objects.get(slug=module)
        response = Quiz_Create_View.as_view()(request)
        if 201 == response.status_code:
            quiz = Quiz.objects.get(id=response.data['id'])
            Quiz_wrap(module=module, quiz=quiz).save() 
            #Se crea el puntaje en la tabla de scores
            Scores(id_event=quiz.id, score=10, event="Quiz").save()
            # Se envia la señal para aunmentar los puntos con los que se gana la medalla
            calculate_points_end_badge.send(sender=module_activitie_create_wrap, author=request.user, badge=badge, points=10, action='add', element='quiz', instance_element=quiz)

        
        return response

    except Module.DoesNotExist:
        raise Http404

    except Page.DoesNotExist:
        return response


from servicio.serializers import Quiz_Retrieve_Serializer

class QuizList(generics.ListAPIView):
    """
    View to list Quizes.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = Quiz_Retrieve_Serializer
    paginate_by = 10

    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_quiz = Quiz_wrap.objects.filter(module=module).values_list('quiz', flat=True)
        public = Quiz.objects.filter(pk__in=list_quiz)
        return public


"""Views for Evaluations"""
from .models import Material_wrap
from material.models import Material
from material.views import MaterialFileCreateView, MaterialLinkCreateView, MaterialListView

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def module_material_create_wrap(request, module):
    """
    wrap create Material
    """
    try:
        module = Module.objects.get(slug=module)
        
        #if field url come in POST then to create a new Link else is a File
        if request.POST.get('url', False):
            response = MaterialLinkCreateView.as_view({'post':'create'})(request)
        
        else:
            response = MaterialFileCreateView.as_view({'post':'create'})(request)
        

        if 201 == response.status_code:
            material = Material.objects.get(pk=response.data['id'])
            Material_wrap(module=module, material=material).save()
        
        return response

    except Module.DoesNotExist:
        raise Http404


class MaterialList(MaterialListView):
    def get_queryset(self):
        module = Module.objects.get(slug=self.kwargs['module'])
        list_material = Material_wrap.objects.filter(module=module).values_list('material', flat=True)
        public = Material.objects.filter(pk__in=list_material).select_subclasses()
        return public
