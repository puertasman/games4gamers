import os
from django.core.management.base import BaseCommand
from juegos.models import Juego

class Command(BaseCommand):
    help = 'Updates the imagen field for existing games based on a predefined list.'

    def handle(self, *args, **options):
        game_images = {
            "Hard Run": "img/juegos/hard_run/hard_run_mini.png",
            "Seek and hit": "img/juegos/seek_and_hit/seek_and_hit_mini.png",
            "Bastions of Dusk": "img/juegos/bastions_of_dusk/bastions_of_dusk_mini.png",
            # Add other games here if known
        }

        self.stdout.write("Starting to update game images...")

        for game_name, image_path in game_images.items():
            try:
                juego = Juego.objects.get(nombre=game_name)
                juego.imagen = image_path
                juego.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated image for "{game_name}" to "{image_path}"'))
            except Juego.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Game "{game_name}" not found. Skipping.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating game "{game_name}": {e}'))

        # Update any other games to a default image if their image field is still the initial default
        default_initial_image = 'img/juegos/default_game.png'
        generic_image_to_set = 'img/juegos/logo.png' # A generic image for games not in the specific list
        
        games_to_update_to_generic = Juego.objects.filter(imagen=default_initial_image)
        if not game_images: # If game_images is empty, all games with default_initial_image should get generic_image_to_set
            games_needing_generic_update_count = games_to_update_to_generic.count()
            if games_needing_generic_update_count > 0:
                self.stdout.write(f"Found {games_needing_generic_update_count} games with the initial default image. Updating them to '{generic_image_to_set}'.")
                for juego in games_to_update_to_generic:
                    juego.imagen = generic_image_to_set
                    juego.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated image for "{juego.nombre}" to "{generic_image_to_set}"'))
        else: # If game_images is not empty, only update games not in game_images and still having default_initial_image
            games_not_in_list = Juego.objects.filter(imagen=default_initial_image).exclude(nombre__in=game_images.keys())
            games_needing_generic_update_count = games_not_in_list.count()
            if games_needing_generic_update_count > 0:
                self.stdout.write(f"Found {games_needing_generic_update_count} other games with the initial default image. Updating them to '{generic_image_to_set}'.")
                for juego in games_not_in_list:
                    juego.imagen = generic_image_to_set
                    juego.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated image for "{juego.nombre}" to "{generic_image_to_set}"'))


        self.stdout.write(self.style.SUCCESS("Finished updating game images."))
