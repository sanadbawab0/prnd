import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def car_image_interior_path(instance, filename):
    return f'interior/{instance.car.id}/{filename}'
def car_image_exterior_path(instance, filename):
    return f'exterior/{instance.car.id}/{filename}'

def paginatePosts(request, queryset, results_per_page, page):
    paginator = Paginator(queryset, results_per_page)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        paginated_queryset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        paginated_queryset = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, paginated_queryset


cars_data = pd.read_csv("Data.csv") 

basic_colors = [
    "black", "white", "red", "green", "blue", "yellow", "orange", "purple", "pink", "brown",
    "gray", "lightgray", "darkgray", "cyan", "magenta", "gold"
]

unique_makes = cars_data["Make"].unique()
unique_model = cars_data["Model"].unique()
unique_model.sort()


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

BRAND_CHOICES = [(make, make) for make in unique_makes]
