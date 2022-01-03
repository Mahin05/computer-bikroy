from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11,unique=True)
    location = models.CharField(max_length=100,choices=(("Chittagong","Chittagong"),("Dhaka","Dhaka"),("Sylhet","Sylhet"),("Rajshahi","Rajshahi"),("Barishal","Barishal"),("Comilla","Comilla"),("Rangpur","Rangpur"),("Gazipur","Gazipur"),("Narayanganj","Narayanganj")))

    def __str__(self):
        return f'{self.user.username} userprofile'
    class Meta:
        db_table = 'userprofile'

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    brand = models.CharField(max_length=100,choices=(("Apple","Apple"),('Acer','Acer'),('Asus','Asus'),('HP','HP'),('Dell','Dell'),('Lenovo','Lenovo'),('Sony','Sony'),('Samsung','Samsung'),('Toshiba','Toshiba'),('Compaq','Compaq'),('Walton','Walton'),('Others','Others')))
    model = models.CharField(max_length=100)
    condition = models.CharField(max_length=100,choices=(("New","New"),("Used","Used")))
    price = models.CharField(max_length=10)
    details = models.CharField(max_length=1000,null=True)
    datentime = models.DateTimeField(blank=False)
    image = models.ImageField(upload_to='computer_pic',null=True)

    def __str__(self):
        return self.user.username

    class Meta :
        db_table = 'product'


