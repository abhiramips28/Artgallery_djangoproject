from django.contrib import admin

from .models import User, Art, Cart, Artworks, Compitition

# Register your models here.


admin.site.register(Art)
admin.site.register(Cart)
admin.site.register(Artworks)
admin.site.register(Compitition)