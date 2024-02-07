import random
import yaml
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Tuple, List, Dict, Any, Union


def fuzzy_coords(real_coords: str, fixed_shift: Tuple[int, int] = (50, 50), max_random_offset: int = 5) -> str:
    """
    Apply a fixed shift and a random offset to coordinates to obfuscate them.

    Parameters:
    real_coords (str): A string of coordinates in the format 'x1,y1,x2,y2'.
    fixed_shift (Tuple[int, int]): A tuple representing a fixed shift to be applied to each coordinate.
    max_random_offset (int): Maximum offset for the random adjustment.

    Returns:
    str: A string of the obfuscated coordinates in the format 'x1,y1,x2,y2'.
    """

    # Split the input string and convert each coordinate to an integer
    coords: List[int] = list(map(int, real_coords.split(',')))
    x1, y1, x2, y2 = coords

    # Apply the fixed shift to each coordinate
    shifted_coords: List[int] = [c + shift for c, shift in zip(coords, fixed_shift * 2)]

    # Add a random offset to each coordinate
    x1, y1, x2, y2 = [c + random.randint(-max_random_offset, max_random_offset) for c in shifted_coords]

    # Return the modified coordinates as a string
    return f"{x1},{y1},{x2},{y2}"


def index(request: HttpRequest) -> HttpResponse:
    """
    Process the request and render the index page with component details.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: The rendered HTML page.
    """

    # Load YAML data from a file
    with open('src/assets/schematics/example.yaml', 'r') as file:
        components: Dict[str, Any] = yaml.safe_load(file)

    component_details: List[Dict[str, Union[str, int, Dict[str, Any]]]] = []
    for component_name, details in components.items():
        # Extract coordinates and details, apply obfuscation
        x, y, width, height = [
            int(coord) for coord in fuzzy_coords(details['coords']).split(',')
        ]
        component_name_friendly = component_name.replace('_', ' ').title()


        # Construct a dictionary for each component
        component_detail: Dict[str, Union[str, int, Dict[str, Any]]] = {
            'name': component_name_friendly,
            'details': details['details'],
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'subcomponents': details.get('subcomponents', {})
        }

        # Add the dictionary to the list
        component_details.append(component_detail)

    # Render the HTML page with the component details
    return render(request, "index.html", {"components": component_details})
