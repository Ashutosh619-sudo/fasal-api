from pydoc import describe
from django.forms import ValidationError
from rest_framework import serializers
from .models import Movie,MovieList
from fasal_auth.serializers import UserSerializer
from fasal_auth.models import User
from rest_framework.serializers import ValidationError

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):

    movies = MovieSerializer(many=True,read_only=True)

    class Meta:
        model = MovieList
        fields = "__all__"
    
    def create(self, validated_data):
        try:
            movieList = MovieList.objects.get(user=validated_data["user"],name=validated_data["name"])
            raise ValidationError("you already have a list with this name")
        except MovieList.DoesNotExist:
            movieList = MovieList.objects.create(user=validated_data["user"],name=validated_data["name"],private=validated_data["private"],description=validated_data["description"])
            movieList.movies.set([])
            return movieList
        
        
