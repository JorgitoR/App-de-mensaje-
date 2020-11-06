import uuid
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.apps import apps

User = settings.AUTH_USER_MODEL

class ModeloBase(models.Model):
    
    id        = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update    = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_datetime(self):

        return self.timestamp.strftime("%b %d %I:%M %p")  

class ChanelMensaje(ModeloBase):
    channel = models.ForeignKey("Channel", null=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

class ChanelUser(ModeloBase):
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)


class ChannelQuerySet(models.QuerySet):

    def only_one(self):
        return self.annotate(num_users = Count("users")).filter(num_users=1)

    def only_two(self):
        return self.annotate(num_users = Count("users")).filter(num_users=2)

    def filter_by_username(self, username):
        return self.filter(chaneluser__user__username=username)


class ChannelManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return ChannelQuerySet(self.model, using=self._db)

    def filter_by_private_ms(self, username_a, username_b):
        return self.get_queryset().only_two().filter_by_username(username_a).filter_by_username(username_b).order_by("timestamp")

    def get_or_create_actual_usuario_ms(self, user):
        qs = self.get_queryset().only_one().filter_by_username(user.username)
        if qs.exists():
            return qs.order_by("timestamp").first, False
        channel_obj = Channel.objects.create()
        ChanelUser.objects.create(user=user, channel=channel_obj)
        return channel_obj, True

    def get_or_private_ms(self, username_a, username_b):
        qs = self.filter_by_private_ms(username_a, username_b)
        if qs.exists():
            return qs.order_by("timestamp").first(), False #obj, created
        
        User = apps.get_model("auth", model_name='User')
        #channel_obj = self.model().save()
        user_a, user_b = None, None
        try:
        
            user_a = User.objects.get(username=username_a)
        
        except User.DoesNotExist:
            return None, False

        try:
            
            user_b = User.objects.get(username=username_b)

        except User.DoesNotExist:
            return None, False

        if user_a == None or user_b == None:
            return None, False

        channel_obj = Channel.objects.create()

        ch_u_a = ChanelUser(user=user_a, channel=channel_obj)
        ch_u_b = ChanelUser(user=user_b, channel=channel_obj)
        ChanelUser.objects.bulk_create([ch_u_a, ch_u_b])

        return channel_obj, True

class Channel(ModeloBase):

    users = models.ManyToManyField(User, blank=True, through=ChanelUser)
    objects = ChannelManager()

    class Meta:
        ordering = ['-timestamp']