from django.contrib import admin
from .models import Asset, Portfolio, Price, Weight, Quantity, PortfolioValue

admin.site.register(Asset)
admin.site.register(Portfolio)
admin.site.register(Price)
admin.site.register(Weight)
admin.site.register(Quantity)
admin.site.register(PortfolioValue)