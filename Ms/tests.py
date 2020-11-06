from django.test import TestCase

from django.contrib.auth import get_user_model

from .models import Channel,  ChanelMensaje, ChanelUser

User = get_user_model()

class  ChannelLookUpTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create(username='jorgito', password='jorgeluiz')
        self.user_b = User.objects.create(username='twoUser', password="hihowareyou")
        self.user_c = User.objects.create(username='ThreeUser', password="hihow")

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 3)
    
    def test_single_user_channel(self):
        qs = User.objects.all()
        for user in qs:
            channel_obj = Channel.objects.create()
            channel_obj.users.add(user)
        
        channel_qs = Channel.objects.all()
        self.assertEqual(channel_qs.count(), 3)
        channel_qs_1 =channel_qs.only_one()
        self.assertEqual(channel_qs_1.count(), channel_qs.count())
    
    def test_dual_user_channel(self):
        channel_obj = Channel.objects.create()
        ChanelUser.objects.create(user=self.user_a, channel=channel_obj)
        ChanelUser.objects.create(user=self.user_b, channel=channel_obj)
        channel_obj2 = Channel.objects.create()
        ChanelUser.objects.create(user=self.user_c, channel=channel_obj2)
        qs = Channel.objects.all()
        self.assertEqual(qs.count(), 2)
        with_two = qs.only_two()
        self.assertEqual(with_two.count(), 1)