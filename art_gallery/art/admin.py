from django.contrib import admin

from .models import User, Art, Cart, Artworks

# Register your models here.

admin.site.register(User)
admin.site.register(Art)
admin.site.register(Cart)
admin.site.register(Artworks)