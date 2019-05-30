from django.db import models

class Moviestable(models.Model):
    """Model definition for Movies."""
    imdbID = models.CharField(max_length=20,primary_key=True)
    title = models.CharField(max_length=50,null=True)
    released = models.CharField(max_length=50,null=True)
    poster = models.URLField(null=True)
    genre = models.CharField(max_length=100,null=True)
    #imdb_poster = models.URLField(null=True)
    #decription = models.TextField(max_length=300)
    #rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    # # year

#     class Meta:
#         """Meta definition for Movies."""

#         verbose_name = "Movies"
#         verbose_name_plural = "Moviess"
    # def __str__(self):
    #     return self.title
