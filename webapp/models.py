from django.db import models
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField



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
    details = ArrayField(models.CharField(max_length=512), default=list)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    category = models.CharField(choices=CATEGORIES, max_length=2, null=True, blank=True)
    image = CloudinaryField('product_image')
