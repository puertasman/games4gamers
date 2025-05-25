from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError

from juegos.models import Juego
from jugadores.models import Jugadores
from .models import Torneo, InscripcionTorneo

class TorneoModelTests(TestCase):

    def setUp(self):
        # Common setup for User, Jugadores, Juego
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.jugador = Jugadores.objects.create(nombre=self.user, nivel='AMATEUR')
        self.juego = Juego.objects.create(
            nombre='Test Juego', 
            descripcion='Un juego de prueba',
            fecha_de_lanzamiento=timezone.now().date(),
            genero='Aventura'
        )

    def test_torneo_creation(self):
        """Test the creation of a Torneo instance."""
        torneo = Torneo.objects.create(
            juego=self.juego,
            nombre='Gran Torneo de Test',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timezone.timedelta(days=7)
        )
        self.assertEqual(str(torneo), 'Gran Torneo de Test')
        self.assertEqual(torneo.estado, 'PROXIMAMENTE')

class InscripcionTorneoModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.jugador = Jugadores.objects.create(nombre=self.user, nivel='AMATEUR')
        self.juego = Juego.objects.create(
            nombre='Test Juego para Inscripcion',
            descripcion='Otro juego de prueba',
            fecha_de_lanzamiento=timezone.now().date(),
            genero='Estrategia'
        )
        self.torneo = Torneo.objects.create(
            juego=self.juego,
            nombre='Torneo de Inscripciones',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timezone.timedelta(days=7)
        )

    def test_inscripcion_torneo_creation(self):
        """Test the creation of an InscripcionTorneo instance."""
        inscripcion = InscripcionTorneo.objects.create(
            torneo=self.torneo,
            jugador=self.jugador
        )
        expected_str = f"{self.jugador.nombre.username} inscrito en {self.torneo.nombre}"
        # Correcting the string representation based on model's __str__
        # The model uses self.jugador.nombre (which is the User object), so its __str__ is username
        self.assertEqual(str(inscripcion), expected_str)

        # Test unique_together constraint
        with self.assertRaises(IntegrityError):
            InscripcionTorneo.objects.create(
                torneo=self.torneo,
                jugador=self.jugador
            )

class TorneoViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.jugador_profile = Jugadores.objects.create(nombre=self.user, nivel='AMATEUR')
        self.juego = Juego.objects.create(
            nombre='Juego para Vistas', 
            descripcion='Descripción',
            fecha_de_lanzamiento=timezone.now().date(),
            genero='RPG'
        )
        self.torneo = Torneo.objects.create(
            juego=self.juego,
            nombre='Torneo de Vistas',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timezone.timedelta(days=5),
            estado='ACTIVO' # Open for registration
        )

    def test_torneos_principal_view(self):
        """Test the torneos_principal view."""
        response = self.client.get(reverse('torneos_principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'torneos/torneos_principal.html')

    def test_torneo_detalle_view(self):
        """Test the torneo_detalle view."""
        response = self.client.get(reverse('torneo_detalle', args=[self.torneo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'torneos/torneo_detalle.html')

    def test_inscribir_torneo_view(self):
        """Test the inscribir_torneo view logic."""
        self.client.login(username='testuser', password='password123')
        
        # Test successful registration
        response = self.client.get(reverse('inscribir_torneo', args=[self.torneo.id]))
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertTrue(InscripcionTorneo.objects.filter(torneo=self.torneo, jugador=self.jugador_profile).exists())
        self.assertRedirects(response, reverse('torneo_detalle', args=[self.torneo.id]))

        # Test registration when already registered (should not create new one, redirect with message)
        # The view logic prevents duplicate InscriptionTorneo, so count should remain 1
        initial_inscripciones_count = InscripcionTorneo.objects.count()
        response_already_registered = self.client.get(reverse('inscribir_torneo', args=[self.torneo.id]))
        self.assertEqual(response_already_registered.status_code, 302)
        self.assertEqual(InscripcionTorneo.objects.count(), initial_inscripciones_count) # No new inscription
        # Optionally, check for message if possible, but that's more complex for basic tests.

    def test_inscribir_torneo_view_tournament_full(self):
        """Test inscribir_torneo when the tournament is full."""
        # Create a new user and profile for this test
        other_user = User.objects.create_user(username='otheruser', password='password123')
        other_jugador = Jugadores.objects.create(nombre=other_user)
        
        torneo_limitado = Torneo.objects.create(
            juego=self.juego,
            nombre='Torneo Limitado',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timezone.timedelta(days=1),
            estado='ACTIVO',
            max_participantes=1
        )
        # First user registers
        InscripcionTorneo.objects.create(torneo=torneo_limitado, jugador=self.jugador_profile)
        
        # Second user (other_user) tries to register
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(reverse('inscribir_torneo', args=[torneo_limitado.id]))
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertFalse(InscripcionTorneo.objects.filter(torneo=torneo_limitado, jugador=other_jugador).exists())
        # Check if the message framework was used (the presence of a message is an indirect check)
        # To directly check messages, you'd iterate through response.context['messages'] or use a test client that stores them.
        # For simplicity here, we rely on the redirect and non-creation.

    def test_inscribir_torneo_view_tournament_not_open(self):
        """Test inscribir_torneo when the tournament is not open for registration."""
        torneo_finalizado = Torneo.objects.create(
            juego=self.juego,
            nombre='Torneo Finalizado',
            fecha_inicio=timezone.now() - timezone.timedelta(days=2),
            fecha_fin=timezone.now() - timezone.timedelta(days=1),
            estado='FINALIZADO'
        )
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('inscribir_torneo', args=[torneo_finalizado.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(InscripcionTorneo.objects.filter(torneo=torneo_finalizado, jugador=self.jugador_profile).exists())
