import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from vehicles.models import Make, Year, Model, Segment, Aplication, Category, Part, PartProperty  # Ajusta el import según tu app

class Command(BaseCommand):
    help = 'Load data from Excel file into Django models, with trimming, duplicate checks, and rollback support'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Inicia una transacción
        try:
            # Ruta al archivo .xlsx
            file_path = '/path/to/descargas/a subir.xlsx'
            data = pd.read_excel(file_path)

            # Eliminar espacios en blanco de los registros
            data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Crear un conjunto para almacenar combinaciones únicas de aplicaciones
            seen_combinations = set()

            for index, row in data.iterrows():
                # Procesar los datos para cada modelo
                make, _ = Make.objects.get_or_create(make=row['make'])
                year, _ = Year.objects.get_or_create(year=row['year'])
                model, _ = Model.objects.get_or_create(model=row['model'])
                segment, _ = Segment.objects.get_or_create(segment=row['Segment'])

                # Procesar la categoría si existe
                category, _ = Category.objects.get_or_create(category=row['category'])

                # Crear o obtener la aplicación correspondiente
                combination = (row['market'], segment.id, make.id, year.id, model.id)
                if combination in seen_combinations:
                    continue
                seen_combinations.add(combination)

                aplication, _ = Aplication.objects.get_or_create(
                    segment=segment,
                    make=make,
                    year=year,
                    model=model,
                    market=row['market']
                )

                # Crear o obtener la parte correspondiente
                part, _ = Part.objects.get_or_create(
                    sku=row['sku'],
                    name=row['category'],  # Asumiendo que el nombre de la parte es la categoría
                    description=row.get('notes', ''),
                )

                # Agregar categorías a la parte
                part.categories.add(category)

                # Agregar aplicaciones a la parte
                part.applications.add(aplication)

                # Si existen propiedades para la parte, procesarlas
                if pd.notna(row['property']) and pd.notna(row['value']):
                    PartProperty.objects.get_or_create(
                        part=part,
                        property=row['property'],
                        value=row['value']
                    )

                # Guardar la parte para asegurar que las relaciones many-to-many se guarden correctamente
                part.save()

            self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))

        except Exception as e:
            # Si ocurre algún error, se revierte toda la transacción
            transaction.set_rollback(True)
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
