from django.db import models
from fasal_auth.models import User

# Create your models here.
class Movie(models.Model):
    Title = models.CharField(max_length=200,blank=False,unique=True)
    Year = models.CharField(max_length=10,blank=False)
    Released = models.CharField(max_length=50,blank=False)
    Runtime = models.CharField(max_length=50,blank=False)
    Genre = models.CharField(max_length=500,blank=False)
    Director = models.CharField(max_length=50,blank=False)
    Writer = models.TextField(max_length=500,blank=False)
    Actors = models.CharField(max_length=300,blank=False)
    Plot = models.TextField(max_length=500,blank=False)
    Language = models.CharField(max_length=50,blank=False)
    Country = models.CharField(max_length=50,blank=False)
    imdb_id = models.CharField(max_length=25,blank=False)
    Poster = models.CharField(max_length=1000,blank=True)


    def __str__(self):
        return self.Title

class MovieList(models.Model):
    name = models.CharField(max_length=100,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie,related_name='movieList',blank=True)
    private = models.BooleanField(default=False)
    description = models.CharField(max_length=500,blank=True)

    def __str__(self) -> str:
        return self.name