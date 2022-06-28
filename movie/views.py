from rest_framework.views import APIView
from movie import serializers
from movie.customPermission import PrivatePublicPermissions
from movie.models import Movie
from movie.models import MovieList
from movie.serializers import MovieListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db import transaction

# Create your views here.

class MovieListViewSet(ModelViewSet):
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieList.objects.prefetch_related("movies").filter(user=self.request.user)
    

class GetMovieList(APIView):

    permission_classes = [IsAuthenticated,PrivatePublicPermissions]

    def get(self,request,id):
        try:
            movie_list = MovieList.objects.prefetch_related("movies").get(pk=id)
            self.check_object_permissions(request=request,obj=movie_list)
            serializer = MovieListSerializer(movie_list)
            return Response({"data":serializer.data})
        except MovieList.DoesNotExist:
            return Response({"data":"MovieList Doesn't exists"}) 
    
    def delete(self,request,id):
        try:
            movie_list = MovieList.objects.prefetch_related("movies").get(pk=id)
            self.check_object_permissions(request=request,obj=movie_list)
            movie_list.delete()
            return Response({"data":"Succesfully deleted movie list"})
        except MovieList.DoesNotExist:
            return Response({"data":"MovieList Doesn't exists"}) 



class AddMovieToList(APIView):
    permission_classes = [IsAuthenticated,PrivatePublicPermissions]

    def post(self,request):
        print(request.data)

        with transaction.atomic():
            try:
                movieList = MovieList.objects.prefetch_related("movies").get(id=request.data["movieList"])
                self.check_object_permissions(request=request,obj=movieList)
                try:
                    movie = Movie.objects.get(Title=request.data["Title"])
                    movieList.movies.add(movie)
                except Movie.DoesNotExist:
                    movie = Movie.objects.create(Title=request.data["Title"],Year=request.data["Year"],Released=request.data["Released"],Runtime=request.data["Runtime"],Genre=request.data["Genre"],Director=request.data["Director"],Writer=request.data["Writer"],Actors=request.data["Actors"],Plot=request.data["Plot"],Language=request.data["Language"],Country=request.data["Country"],imdb_id=request.data["imdbID"],Poster=request.data["Poster"])
                    movie.save()
                    movieList.movies.add(movie)
                    movieList.save()
                
                return Response({"data":"movie added to the list"},status=status.HTTP_201_CREATED)
            except MovieList.DoesNotExist:
                return Response({"data":"Movie list doesn't exists"},status=status.HTTP_400_BAD_REQUEST)

