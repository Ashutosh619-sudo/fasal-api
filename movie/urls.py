from django.urls import include, path
from . import views

movie_list_views = views.MovieListViewSet.as_view({
    'get':'list',
    'post':'create'
})

urlpatterns = [
    path('movie-list/',view=movie_list_views),
    path('add-to-list/',view=views.AddMovieToList.as_view()),
    path('get-movie-list/<int:id>',view=views.GetMovieList.as_view())
]