import pandas as pd


def car_image_interior_path(instance, filename):
    return f'interior/{instance.car.id}/{filename}'
def car_image_exterior_path(instance, filename):
    return f'exterior/{instance.car.id}/{filename}'


cars_data = pd.read_csv("Data.csv") 

basic_colors = [
    "black", "white", "red", "green", "blue", "yellow", "orange", "purple", "pink", "brown",
    "gray", "lightgray", "darkgray", "cyan", "magenta", "gold"
]

COLOR_CHOICES = tuple((color, color.capitalize()) for color in basic_colors)

BODY_CHOICES = (('bus','Bus'),
                    ('convertible','Convertible'),
                    ('coupe','Coupe'),
                    ('hatchback','Hatchback'),
                    ('sedan','Sedan'),
                    ('suv','SUV'),
                    ('pick-up','PickUp'),
                    ('truck','Truck'))


TRANSMISSION_CHOICES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'))

FUEL_CHOICES = (
        ('petrol','بنزين'),
        ('diesel','ديزل'),
        ('electric','كهرباء'),
        ('hybrid','هايبرد'),
        ('mild-hybrid','مايلد هايبرد'),
        ('plugin-hybrid','هايبرد - plugin'),
    )
CONDITION_CHOICES = (('excelent','ممتازة'),
                         ('good','جيد'),
                         ('small-accident','حادث بسيط'),
                         ('accident','تعرضت لحادث'),
                         ('other','أخرى'))
    
CUSTOM_CHOICES = (('yes','مجمرك'),
                      ('no','غير مجمرك'))






