from django.db import models
from django.utils.translation import gettext_lazy as _
from biuropodrozy.utils import generate_slug
from django.urls import reverse
from biuropodrozy.outer_api.weather_api import get_weather
from biuropodrozy.outer_api.exchange_rates_api import get_rate_in_pln
from biuropodrozy.outer_api.covid_api import get_covid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from datetime import date


class Trip(models.Model):
    """Trip model class"""

    class Climates(models.TextChoices):
        GORSKI = 'Górski', _('Górski')
        MORSKI = 'Morski', _('Morski')
        KONTYNENTALNY = 'Kontynentalny', _('Kontynentalny')
        SRODZIEMNOMORSKI = 'Śródziemnomorski', _('Śródziemnomorski')
        MONSUNOWY = 'Monsunowy', _('Monsunowy')
        STEPOWY = 'Stepowy', _('Stepowy')
        PUSTYNNY = 'Pustynny', _('Pustynny')

    class Landscapes(models.TextChoices):
        GORY = 'Góry', _('Góry')
        PLAZA = 'Plaża', _('Plaża')
        PUSTYNIA = 'Pustynia', _('Pustynia')
        LAS = 'Las', _('Las')
        MIASTO = 'Miasto', _('Miasto')
        WIES = 'Wieś', _('Wieś')
        MORZE = 'Morze', _('Morze')

    class Types(models.TextChoices):
        AKTYWNY_WYPOCZYNEK = 'Aktywny wypoczynek', _('Aktywny wypoczynek')
        WYPOCZYNEK = 'Wypoczynek', _('Wypoczynek')
        ZWIEDZANIE = 'Zwiedzanie', _('Zwiedzanie')

    class Transports(models.TextChoices):
        SAMOLOT = 'Samolot', _('Samolot')
        DOJAZD_WLASNY = 'Dojazd Własny', _('Dojazd Własny')
        AUTOBUS = 'Autobus', _('Autobus')

    STARS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

    title = models.CharField(max_length=256, verbose_name=_("Nazwa wycieczki"))
    hotelstars = models.IntegerField(choices=STARS, blank=True, verbose_name="Gwiazdki hotelu")
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, verbose_name="Ocena wycieczki")
    head_description = models.TextField(max_length=1000, verbose_name=_("Główny opis"))
    location_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Opis miejsca"))
    beach_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Opis Plaży"))
    hotel_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Opis Hotelu"))
    room_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Opis pokoju"))
    sport_and_entertainment_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Sport i rozrywka"))
    all_inclusive_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Opis all inclusive"))
    for_free_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Gratisy"))
    trip_plan_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Plan wycieczki"))
    benefits_description = models.TextField(max_length=1000, blank=True, verbose_name=_("Swiadczenia"))
    country = models.CharField(max_length=50, verbose_name=_("Kraj wycieczki"))
    city = models.CharField(max_length=50, verbose_name=_("Miasto wycieczki"))
    countryEN = models.CharField(max_length=50, verbose_name=_("Kraj wycieczki po angielsku"))
    currency = models.CharField(max_length=5, verbose_name=_("Skrót waluty"))
    timezone = models.CharField(max_length=7, verbose_name=_("Strefa czasowa"))
    climate = models.CharField(max_length=20, choices=Climates.choices, verbose_name="Klimat")
    landscape = models.CharField(max_length=15, choices=Landscapes.choices, verbose_name="Krajobraz")
    type = models.CharField(max_length=20, choices=Types.choices, verbose_name="Rodzaj wycieczki")
    transport = models.CharField(max_length=20, choices=Transports.choices, verbose_name="Rodzaj transportu")
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)], verbose_name="Cena wycieczki")
    duration = models.IntegerField(verbose_name="Ilość dni wycieczki")
    slug = models.SlugField(max_length=256, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.title.strip()
            for candidate in generate_slug(base):
                if not Trip.objects.filter(slug=candidate).exists():
                    self.slug = candidate
                    break
            else:
                raise Exception("Can't create new Trip object")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("trips:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    @property
    def weather_api(self):
        weather = get_weather(self.countryEN)
        return weather

    @property
    def exchange_rates_api(self):
        rate = get_rate_in_pln(self.currency)
        return rate

    @property
    def covid_api(self):
        covid = get_covid(self.countryEN)
        return covid


class TripPicture(models.Model):
    """TripPictures model class"""
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    picture = models.ImageField()

    @property
    def picture_url(self):
        return self.picture.url if bool(self.picture) else None


class TripDates(models.Model):
    """TripDates model class"""
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data rozpoczęcia")
    end_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data zakończenia")

    def save(self, *args, **kwargs):
        duration = self.end_date - self.start_date
        days = duration.days
        if not self.trip.duration == days:
            raise Exception("Can't create new TripDates object - duration is incorrect")
        super().save(*args, **kwargs)


class TripReservation(models.Model):
    """Reservation model class"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    trip = models.ForeignKey('Trip', on_delete=models.PROTECT)
    persons = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Ilość osób")
    phone = models.CharField(max_length=12, verbose_name="Numer kontaktowy")
    guide = models.BooleanField(default=0, verbose_name="Prywatny przewodnik")
    room = models.BooleanField(default=0, verbose_name="Pokój premium")
    price = models.DecimalField(blank=True, max_digits=8, decimal_places=2, verbose_name="Cena wycieczki")

    def save(self, *args, **kwargs):
        self.price = self.persons * self.trip.price
        super().save(*args, **kwargs)
