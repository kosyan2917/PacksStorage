from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import PacksModel
from .permissions import *


class PaginationList(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetPacksAPI(generics.ListAPIView):
    queryset = PacksModel.objects.all()
    serializer_class = PacksSerializer
    pagination_class = PaginationList


# TODO: Валидация пака
class UploadPackAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if "pack" in request.data:
            data = {}
            data["pack"] = request.data["pack"]
            print(type(data["pack"]))
            data["owner"] = request.user.username
            serializer = UploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Sasi"
                })
            else:
                return Response({
                    "message": serializer.errors
                })
        else:
            return Response({
                "message": "Имя пака или файл с паком не заданы",
                "code": 400
            }, status=400)
        
        
class DeletePackAPI(generics.DestroyAPIView):
    permission_classes = (IsOwnerOrAdmin, )
    queryset = PacksModel.objects.all()
    serializer_class = PacksSerializer


class DownloadPackAPI(generics.RetrieveAPIView):
    queryset = PacksModel.objects.all()
    serializer_class = DownloadSerializer


class ProfileAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


class UpdateProfilePicAPI(generics.UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = UpdatePicSerializer


class GetCardsAPI(views.APIView):
    
    def get(self, request, pack):
        query = CardsModel.objects.filter(pack=pack)
        serializer = CardsSerializer(query, many=True)
        return Response(serializer.data)
        
class Card(views.APIView):
    def post(self, request):
        o = CardsModel(name="sss", pack=PacksModel.objects.get(name="a"), image=request.data["image"], mana_cost=0, attack=0, defence=0)
        o.save()