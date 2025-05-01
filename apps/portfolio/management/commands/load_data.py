# apps/portfolio/management/commands/load_excel.py

from django.core.management.base import BaseCommand
from apps.portfolio.models import Asset, Portfolio, Price, Weight
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
    help = 'Carga datos desde datos.xlsx a la base de datos'

    def handle(self, *args, **kwargs):
        EXCEL_PATH = 'datos.xlsx'  # Asegúrate que el archivo esté en la raíz del proyecto

        self.stdout.write("Leyendo archivo Excel...")

        weights_df = pd.read_excel(EXCEL_PATH, sheet_name="weights")
        prices_df = pd.read_excel(EXCEL_PATH, sheet_name="Precios")

        pf1, _ = Portfolio.objects.get_or_create(
            name="Portafolio 1",
            defaults={'initial_value': 0})
        pf2, _ = Portfolio.objects.get_or_create(
            name="Portafolio 2",
            defaults={'initial_value': 0})

        weights_date = pd.to_datetime(weights_df.iloc[0, 0]).date()
        assets = {}

        self.stdout.write("Cargando pesos iniciales...")

        for _, row in weights_df.iterrows():
            name = row['Activo'] if 'Activo' in weights_df.columns else row[1]
            asset, _ = Asset.objects.get_or_create(name=name)
            assets[name] = asset

            Weight.objects.update_or_create(
                portfolio=pf1, asset=asset, date=weights_date,
                defaults={'weight': row[2]}
            )
            Weight.objects.update_or_create(
                portfolio=pf2, asset=asset, date=weights_date,
                defaults={'weight': row[3]}
            )

        self.stdout.write("Cargando precios...")

        prices_df.iloc[:, 0] = pd.to_datetime(prices_df.iloc[:, 0]).dt.date
        for _, row in prices_df.iterrows():
            date = row.iloc[0]
            for col in prices_df.columns[1:]:
                price = row[col]
                asset = assets.get(col)
                if asset:
                    Price.objects.update_or_create(
                        asset=asset, date=date,
                        defaults={'value': price}
                    )

        self.stdout.write(self.style.SUCCESS("Datos cargados exitosamente."))