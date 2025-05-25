from django.core.management.base import BaseCommand
from juegos.models import Juego

class Command(BaseCommand):
    help = 'Lists the ID and name of all games in the database.'

    def handle(self, *args, **options):
        self.stdout.write("Listing all games (ID and Name):")
        juegos = Juego.objects.all()
        if not juegos.exists():
            self.stdout.write(self.style.WARNING("No games found in the database."))
            return

        for juego in juegos:
            self.stdout.write(f"ID: {juego.id}, Name: {juego.nombre}")

        self.stdout.write(self.style.SUCCESS("Finished listing games."))
