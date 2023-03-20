from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=50)
    background_image = models.ImageField(upload_to='category_backgrounds/')
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name