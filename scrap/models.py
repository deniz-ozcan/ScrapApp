from django.db import models
from django.utils.text import slugify

class Ram(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    type = models.CharField(max_length=5)

    def __str__(self):
        return self.type


class Storage(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    type = models.CharField(max_length=5)

    def __str__(self):
        return self.type


class Processor(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type 


class System(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class Screen(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class Brand(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    name = models.CharField(max_length=10)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.model}"


class Product(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    name = models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name="Brands",blank=False,null=False)
    ram = models.ForeignKey(Ram,on_delete=models.CASCADE,verbose_name="Ram",blank=False,null=False)
    storage = models.ForeignKey(Storage,on_delete=models.CASCADE,verbose_name="Storage",blank=False,null=False)
    processor = models.ForeignKey(Processor,on_delete=models.CASCADE,verbose_name="Processor",blank=False,null=False)
    system = models.ForeignKey(System,on_delete=models.CASCADE,verbose_name="System",blank=False,null=False)
    screen = models.ForeignKey(Screen,on_delete=models.CASCADE,verbose_name="Screen",blank=False,null=False)
    image = models.CharField(max_length=250,blank=False,null=False)
    slug = models.SlugField(max_length=250,blank=False,null=False,unique=True,editable=False,db_index=True) 
    def __str__(self):

        return f"{self.name.name} {self.name.model} {self.ram.type} {self.storage.type} {self.processor.type} {self.system.type} {self.screen.type}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.name+" "+self.name.model + " " + self.ram.type + " " + self.storage.type + " " + self.processor.type + " " + self.system.type + " " + self.screen.type)
        super().save(*args, **kwargs)


class SitesInformation(models.Model):
    id = models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
    link = models.URLField(max_length=200)
    rate = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    whichproduct = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Laptop",blank=False,null=False)
    sitename = models.CharField(max_length=10,blank=False,null=False)
    def __str__(self):
        return str(self.rate) + " " + str(self.price)
    
