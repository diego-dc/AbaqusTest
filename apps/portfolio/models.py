from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100, unique=True)
    initial_value = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = ('asset', 'date')
        ordering = ['date']


class Weight(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        unique_together = ('asset', 'portfolio', 'date')
        ordering = ['date']


class Quantity(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        unique_together = ('asset', 'portfolio', 'date')
        ordering = ['date']


class PortfolioValue(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('portfolio', 'date')
        ordering = ['date']