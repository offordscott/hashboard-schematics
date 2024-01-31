import random

import yaml
from django.shortcuts import render


def fuzzy_coords(real_coords, fixed_shift=(50, 50), max_random_offset=5):
    # Convert the real coordinates string into a list of integers
    x1, y1, x2, y2 = map(int, real_coords.split(','))

    # Apply a fixed shift
    x1, y1, x2, y2 = [c + shift for c, shift in zip([x1, y1, x2, y2], fixed_shift * 2)]

    # Add a random offset within a smaller range
    x1 += random.randint(-max_random_offset, max_random_offset)
    y1 += random.randint(-max_random_offset, max_random_offset)
    x2 += random.randint(-max_random_offset, max_random_offset)
    y2 += random.randint(-max_random_offset, max_random_offset)

    # Return the obfuscated coordinates as a string
    return f"{x1},{y1},{x2},{y2}"
def index(request):
    with open('src/assets/schematics/example.yaml', 'r') as file:
        components = yaml.safe_load(file)

    component_details = []
    for component_name, details in components.items():
        # Extract coordinates and details
        x, y, width, height = map(int, details['coords'].split(','))
        component_detail = {
            'name': component_name,
            'details': details['details'],
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'subcomponents': details.get('subcomponents', {})
        }
        component_details.append(component_detail)

    return render(request, "index.html", {"components": component_details})
