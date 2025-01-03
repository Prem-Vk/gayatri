from django.db import models
from cloudinary.models import CloudinaryField



class Catergory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = CloudinaryField('category_image', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'<{self.pk} - {self.title}>'


class Product(models.Model):
    TRANSMITTER = "TR"
    ANALYSER = "AL"
    PRESSURE_GAUGE = "PG"
    VALVES = "VV"
    POSITIONERS = "PS"
    PIPE_TUBE = "PT"
    FITTINGS = "FT"
    SWITCHGEARS = "SG"
    PUMPS = "PM"
    MOTORS = "MR"
    FANS = "FA"
    WEIDING_SPARES = "WS"
    TOOLS_AND_SPARES = "TS"
    ENCODER = "EC"
    COUPLING = "CP"
    GEARBOXES = "GX"
    LAB_INSTRUMENT = "LI"
    HOSE_PIPE = "HP"
    CATEGORIES = [
        (TRANSMITTER, "Transmitter"),
        (ANALYSER, "Analyser"),
        (PRESSURE_GAUGE, 'Pressure Gauge'),
        (VALVES, 'Valves'),
        (POSITIONERS, 'Postioners'),
        (PIPE_TUBE, "Pipe Tube"),
        (FITTINGS, "Fittings"),
        (SWITCHGEARS, "Switchgears"),
        (PUMPS, "Pumps"),
        (MOTORS, "Motors"),
        (FANS, "Fans"),
        (WEIDING_SPARES, "Weilding Spares"),
        (TOOLS_AND_SPARES, "Tools and Spares"),
        (ENCODER, 'Encoder'),
        (COUPLING, 'Coupling'),
        (GEARBOXES, "GearBoxes"),
        (LAB_INSTRUMENT, "Lab Instrument"),
        (HOSE_PIPE, "Hose Pipe")
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Catergory, on_delete=models.PROTECT, null=True, blank=True)
    image = CloudinaryField('product_image')

    def __str__(self):
        return f'<{self.pk}-{self.name}'


class Client(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    subject = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    admin_comment = models.TextField(null=True, blank=True)
