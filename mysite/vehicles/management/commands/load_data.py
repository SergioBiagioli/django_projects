import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from vehicles.models import Make, Year, Model, Segment, Aplication, Category, Part, PartProperty

class Command(BaseCommand):
    help = 'Load data from Excel file into Django models, with simplified logic and debugging messages'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Ruta al archivo .xlsx
        file_path = r'C:\Users\sergi\Downloads\a subir.xlsx'
        try:
            data = pd.read_excel(file_path)

            # Eliminar espacios en blanco de los registros solo si son cadenas de texto usando map en lugar de applymap
            data = data.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

            # Crear un conjunto para almacenar combinaciones únicas de aplicaciones
            seen_combinations = set()

            for index, row in data.iterrows():
                try:
                    # Mensaje de depuración: Indicar la fila que se está procesando
                    self.stdout.write(f'Processing row {index + 1}')

                    # Procesar los datos para cada modelo
                    make = Make.objects.get_or_create(make=row['make'].strip() if pd.notna(row['make']) else 'Unknown')[0]
                    year = Year.objects.get_or_create(year=int(row['year']) if pd.notna(row['year']) else 0)[0]
                    model = Model.objects.get_or_create(model=row['model'].strip() if pd.notna(row['model']) else 'Unknown')[0]
                    segment = Segment.objects.get_or_create(segment=row['Segment'].strip() if pd.notna(row['Segment']) else 'Unknown')[0]

                    # Procesar la categoría si existe
                    category = None
                    if pd.notna(row['category']):
                        category = Category.objects.get_or_create(category=row['category'].strip())[0]

                    # Crear o obtener la aplicación correspondiente si todos los campos clave están presentes
                    aplication = None
                    combination = (row['market'], segment.id, make.id, year.id, model.id)
                    if combination not in seen_combinations:
                        seen_combinations.add(combination)
                        aplication = Aplication.objects.get_or_create(
                            segment=segment,
                            make=make,
                            year=year,
                            model=model,
                            market=row['market'].strip() if pd.notna(row['market']) else ''
                        )[0]

                    # Crear o obtener la parte correspondiente
                    part = Part.objects.get_or_create(
                        sku=row['sku'].strip() if pd.notna(row['sku']) else '',
                        name=row['category'].strip() if pd.notna(row['category']) else '',
                        description=row.get('notes', '').strip() if pd.notna(row['notes']) else '',
                    )[0]

                    # Agregar categorías a la parte si existe
                    if category:
                        part.categories.add(category)

                    # Agregar aplicaciones a la parte si existe
                    if aplication:
                        part.applications.add(aplication)

                    # Si existen propiedades para la parte, procesarlas
                    if pd.notna(row['property']) and pd.notna(row['value']):
                        PartProperty.objects.get_or_create(
                            part=part,
                            property=row['property'].strip(),
                            value=row['value'].strip()
                        )

                    # Guardar la parte para asegurar que las relaciones many-to-many se guarden correctamente
                    part.save()

                    self.stdout.write(self.style.SUCCESS(f'Row {index + 1} processed successfully!'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error on row {index + 1}: {e}'))
                    continue

            self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))

        except Exception as e:
            # Si ocurre algún error, se revierte toda la transacción
            transaction.set_rollback(True)
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
