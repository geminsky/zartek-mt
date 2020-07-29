from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
# Create your views here.
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from tagging_system.pagination import ServerSidePagination
from tagging_system import models
from tagging_system.serializers import UploadSerializer, LikeImageSerializer, AddTagSerializer, LikedUserSerializer


class ListImage(ListAPIView):

    serializer_class = UploadSerializer
    permission_classes = (IsAuthenticated, )
    queryset = models.Images.objects.all()
    pagination_class = ServerSidePagination

    def get(self, request, *args, **kwargs):
        image_stats = models.ImageStat.objects.filter(user=request.user, is_liked=True)
        # user_images = [i.image for i in image_stats]
        tags = [i.image.tag.values("name") for i in image_stats]
        tag_name = list(set([tags[i][0]["name"] for i in range(0, len(tags))]))
        images_tag = models.Images.tag.through.objects.filter(tags__name__in=tag_name).order_by("-tags__weightage")
        if images_tag:
            off_images_tag = models.Images.tag.through.objects.exclude(tags__name__in=tag_name)
            images_tag |= off_images_tag
            self.queryset = [i.images for i in images_tag]
        self.pagination_class.page_size = int(request.GET.get('size', 10))
        return self.list(request, *args, **kwargs)


class AddImage(ListCreateAPIView):

    serializer_class = UploadSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, )
    queryset = models.Images.objects.all()
    pagination_class = ServerSidePagination

    def get(self, request, *args, **kwargs):
        self.pagination_class.page_size = int(request.GET.get('size', 10))
        return self.list(request, *args, **kwargs)


class LikeDislikeAPI(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LikeImageSerializer
    queryset = models.Images.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class AddTag(ListCreateAPIView):
    serializer_class = AddTagSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = models.Tags.objects.all()
    pagination_class = ServerSidePagination

    def get(self, request, *args, **kwargs):

        self.pagination_class.page_size = int(request.GET.get('size', 10))
        return self.list(request, *args, **kwargs)


class LikedUsersAPI(ListAPIView):
    serializer_class = LikedUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.ImageStat.objects.all()
    pagination_class = ServerSidePagination

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.queryset = self.queryset.filter(image_id=pk, is_liked=True)
        self.pagination_class.page_size = int(request.GET.get('size', 10))
        return self.list(request, *args, **kwargs)
