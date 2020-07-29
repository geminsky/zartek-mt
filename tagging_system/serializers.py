import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


from tagging_system import models


class AddTagSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=120, required=True)
    weightage = serializers.IntegerField(required=True)

    def create(self, validated_data):
        tag = models.Tags.objects.create(**validated_data)
        return tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=120, required=False)
    weightage = serializers.IntegerField()


class ListImageSerializer(serializers.Serializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return json.dumps(obj.images)


class UploadSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(use_url=True, max_length=None)
    description = serializers.CharField(max_length=1000)
    tag = TagSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    likes = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        tags = validated_data.pop("tag")
        tag_list = []
        for tag in tags:
            tag_list.append(models.Tags.objects.get(id=tag["id"]))
        image = models.Images.objects.create(**validated_data)
        image.tag.set(tag_list)
        return image

    def get_liked(self, obj):
        request = self.context['request']
        user = request.user
        try:
            liked = models.ImageStat.objects.get(image=obj, user=user).is_liked
        except ObjectDoesNotExist:
            liked = False
        return liked


class LikeImageSerializer(serializers.Serializer):

    # image = serializers.SlugRelatedField(slug_field="id", queryset=models.Images.objects.all(), required=True)
    liked = serializers.SerializerMethodField(read_only=True)
    like = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        liked = validated_data.pop("like")
        obj, create = models.ImageStat.objects.update_or_create(image=instance, user=user, defaults={"is_liked": liked})
        likes = instance.likes
        image = models.Images.objects.get(id=instance.id)
        if liked:
            instance.likes = likes+1
            instance.save()
            return instance
        elif likes > 0:
            instance.likes = likes - 1
            instance.save()
            return instance
        else:
            return instance

    def get_liked(self, obj):
        request = self.context['request']
        user = request.user
        print(user, obj)
        try:
            like = models.ImageStat.objects.get(user=user, image=obj).is_liked
        except:
            like = False
        return like


class LikedUserSerializer(serializers.Serializer):

    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
