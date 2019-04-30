from django.db import models


class Moviestable(models.Model):
    """Model definition for Movies."""
    title = models.CharField(max_length=50)
    Movie_id = models.CharField(max_length=20,null=True)
    #imdb_poster = models.URLField(null=True)
    #decription = models.TextField(max_length=300)
    Movie_type = models.TextField(max_length=200) # 主要类别,逗号隔开
    #rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    #Release_date = models.TextField(max_length=200,null=True) # year

#     class Meta:
#         """Meta definition for Movies."""

#         verbose_name = "Movies"
#         verbose_name_plural = "Moviess"
    # def __str__(self):
    #     return self.title
