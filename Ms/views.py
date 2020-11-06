from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Channel, ChanelMensaje, ChanelUser

from .forms import MsForm
from django.views.generic.edit import FormMixin

from  django.views.generic import DetailView
from django.views.generic import View 

class ChanelFormMixin(FormMixin):
    form_class  = MsForm
    #success_url = "./"

    def get_success_url(self):
        return self.request.path

    #handle the form with this mixin 
    def post(self, request, *args,**kwargs):

        if not request.user.is_authenticated:
            raise PermissionDenied
        #obj = self.get_object()
        form = self.get_form()
        if form.is_valid():
            channel = self.get_object()
            user    = self.request.user
            content = form.cleaned_data.get("content")
            channel_obj = ChanelMensaje.objects.create(channel=channel, usuario=user, content=content)

            if request.is_ajax():
                return JsonResponse({'content': channel_obj.content, 
                    'username': channel_obj.usuario.username }, status=201)

            return super().form_valid(form)
        else:

            if request.is_ajax():
                return JsonResponse({"errors": form.errors}, status=400)

            return super().form_invalid(form)


class ChanelDetail(LoginRequiredMixin, ChanelFormMixin, DetailView):
    template_name = "Ms/DetailMs.html"
    queryset      = Channel.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context)

        obj = context["object"]
        # if self.request.user not in obj.users.all():
        #     raise PermissionDenied
        context['is_channel_member'] = self.request.user in obj.users.all()
        return context


class DetailMs(LoginRequiredMixin, ChanelFormMixin,  DetailView):
    template_name = "Ms/DetailMs.html"

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        my_username = self.request.user.username

        if username == my_username:
            
            my_channel_obj, _ = Channel.objects.get_or_create_actual_usuario_ms(self.request.user)

            return my_channel_obj

        channel_obj, _ = Channel.objects.get_or_private_ms(my_username, username)
        if channel_obj == None:
            raise Http404

        return channel_obj

def mensajes_privados_view(request, username, *args, **kwargs):
    
    if not request.user.is_authenticated:
        return HttpResponse("Nothin....")

    my_username = request.user.username
    
    channel_obj, created = Channel.objects.get_or_private_ms(my_username, username)

    if created:
        print("Si, Trabajo")

    channel_user= channel_obj.chaneluser_set.all().values("user__username")
    print(channel_user)
    channel_ms  = channel_obj.chanelmensaje_set.all()
    print(channel_ms.values("content"))

    return HttpResponse(f"Canales Item - {channel_obj.id}")


class inicio(View):
    def get(self, request):

        dialogos = Channel.objects.filter(chaneluser__user__in=[request.user.id])


        context = {

            'dialogo':dialogos,
        }
        return render(request, 'inicio.html', context)