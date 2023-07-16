from django.db import models

# Create your models here.


class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email_id = models.CharField(max_length=25)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.firstname+" "+self.lastname

class Art(models.Model):
    CATEGORY = (
        ('Paintings', 'Paintings'),
        ('Prints', 'Prints'),
        ('Watercolor', 'Watercolor'),
        ('Pastel', 'Pastel'),
        ('Glasswork', 'Glasswork'),
    )

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY)
    description = models.TextField()
    price = models.FloatField(null=True,blank=True)
    image_url = models.CharField(max_length=2083,blank=True)
    Stock = models.IntegerField(default=2)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    items = models.CharField(max_length=5000,blank=True)
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=100,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Admin(models.Model):
    name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=25)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)


    def __str__(self):
        return self.firstname+" "+self.lastname


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Items = models.ManyToManyField(Art)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

class CartItem(models.Model):
    arts = models.ForeignKey(Art,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.arts.quantity} x {self.arts}'

    @property
    def total_price(self):
        return self.arts.price * self.quantity


class Request_Art(models.Model):
    art_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.art_name

class Artworks(models.Model):
    artwork = models.CharField(max_length=200)
    team1 =models.CharField(max_length=200)
    team2 =models.CharField(max_length=200)
    team3 =models.CharField(max_length=200)
    team4 =models.CharField(max_length=200)
    team5 =models.CharField(max_length=200)
    team6 =models.CharField(max_length=200)
    team7 =models.CharField(max_length=200)
    team8 =models.CharField(max_length=200)

    def __str__(self):
        return self.artwork

class Compitition(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    feedback = models.TextField()
    image_url = models.ImageField(upload_to='pics')

    def __str__(self):
        return self.name