import random
from typing import List, Tuple, Dict, Any

import yaml
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def fuzzy_coords(real_coords_list: List[str], fixed_shift: Tuple[int, int] = (20, 20), max_random_offset: int = 5) -> \
        List[str]:
    """
    Apply a fixed shift and a random offset to a list of coordinates to obfuscate them.
    """
    # Initialize an empty list to store obfuscated coordinate strings.
    obfuscated_coords_list: List[str] = []

    # Iterate over each coordinate string in the input list.
    for real_coords in real_coords_list:
        # Convert the comma-separated string of coordinates into a list of integers.
        coords: List[int] = list(map(int, real_coords.split(',')))
        # Unpack the coordinates for clarity.

        # Apply the fixed shift to each coordinate.
        shifted_coords: List[int] = [c + shift for c, shift in zip(coords, fixed_shift * 2)]

        # Add a random offset to each of the shifted coordinates.
        obfuscated_coords: List[int] = [c + random.randint(-max_random_offset, max_random_offset) for c in
                                        shifted_coords]

        # Convert the obfuscated coordinates back into a comma-separated string and add it to the list.
        obfuscated_coords_list.append(
            f"{obfuscated_coords[0]},{obfuscated_coords[1]},{obfuscated_coords[2]},{obfuscated_coords[3]}")

    return obfuscated_coords_list


def index(request: HttpRequest) -> HttpResponse:
    # Load components data...
    with open('src/assets/schematics/example.yaml', 'r') as file:
        components: Dict[str, Any] = yaml.safe_load(file)

    component_details = []
    for component_name, details in components.items():
        coords_list = details.get('coords', [])
        if len(coords_list) > 1:
            # If there are multiple coordinates, handle each separately
            for index, coords in enumerate(coords_list, start=1):
                obfuscated_coords = fuzzy_coords([coords])
                x, y, width, height = map(int, obfuscated_coords[0].split(','))
                component_details.append({
                    'name': f"{component_name} ({index})",
                    'details': details['details'],
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'is_multiple': True,  # Indicates this is part of a multiple set
                })
        else:
            # Handle single coordinate components
            if coords_list:  # Check if there's at least one coordinate
                obfuscated_coords = fuzzy_coords(coords_list)
                x, y, width, height = map(int, obfuscated_coords[0].split(','))
            else:
                x, y = random.randint(0, 792), random.randint(0, 612)
                width = height = 0  # Default/fallback values
            component_details.append({
                'name': component_name,
                'details': details['details'],
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'is_multiple': False,
            })

    return render(request, "index.html", {"components": component_details})
