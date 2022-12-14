from datetime import date
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post
from rareapi.models import Rare_User
from rareapi.models import Subscription

from django.contrib.auth.models import User


class RareUserView(ViewSet):

    def retrieve(self, request, pk):

        rare_user = Rare_User.objects.get(pk=pk)
        logged_in_user = Rare_User.objects.get(user=request.auth.user)
        if logged_in_user.user_id is rare_user.user_id:
            rare_user.my_profile = True
        else:
            rare_user.my_profile = False

        try:
            sub = Subscription.objects.get(
                follower=logged_in_user.pk, author=rare_user.pk, ended_on=None)
            rare_user.sub_info = {
                "is_subscribed": True,
                "subscription": sub.id
            }

        except Subscription.DoesNotExist:
            rare_user.sub_info = {
                "is_subscribed": False,
                "subscription": None
            }

        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        rare_users = Rare_User.objects.all()

        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_rare_user = Rare_User()
        new_rare_user.user = request.auth.user
        new_rare_user.active = request.data["active"]
        new_rare_user.profile_image_url = request.data["profile_image_url"]
        new_rare_user.created_on = date.today()
        new_rare_user.bio = request.data["bio"]
        new_rare_user.save()

        serializer = RareUserSerializer(new_rare_user)
        return Response(serializer.data)

    def destroy(self, request, pk):
        rare_user = Rare_User.objects.get(pk=pk)
        rare_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rare_User
        fields = ('id', 'user', 'active', 'profile_image_url',
                  'created_on', 'bio', 'full_name', 'username',
                  'email', 'is_staff', 'my_profile', 'sub_info')
