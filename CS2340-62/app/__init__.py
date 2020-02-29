from flask import Flask
from jinja2 import Template
import json
from .entities import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS2340'


@app.template_filter()
def region_tech_filter(region):
    return region.get_tech_level()


@app.template_filter()
def region_list_filter(universe):
    data = []
    regions = universe.get_region_list()
    for region in regions:
        tmp = {
            "name": region.get_name(),
            "x": region.get_x(),
            "y": region.get_y(),
            "techLevel": region.get_tech_level().name
        }
        data.append(tmp)
    return data


@app.template_filter()
def item_list_filter(obj):
    data = []
    items = obj.get_current_cargo()

    for item in items:
        tmp = {
            "name": item.get_name(),
            "cargo": item.get_cargo_space(),
            "price": item.get_price(),
        }
        data.append(tmp)
    return data


app.jinja_env.filters['region_tech'] = region_tech_filter
app.jinja_env.filters['region_list'] = region_list_filter
app.jinja_env.filters['item_list'] = item_list_filter

from app import routes
