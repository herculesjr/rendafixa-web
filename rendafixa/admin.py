from django.contrib import admin

from models import Issuer, BoundType, Bound, BoundData

admin.site.register(Issuer)
admin.site.register(BoundType)
admin.site.register(Bound)
admin.site.register(BoundData)
