import voluptuous as vol
from homeassistant.helpers import config_validation as cv
import csv
from datetime import datetime

DOMAIN = "heating_control"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required("temperature_csv"): cv.string,
        vol.Required("heating_csv"): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    conf = config[DOMAIN]
    hass.data[DOMAIN] = {"temperature_data": [], "heating_data": []}

    # Charger les données CSV
    load_csv_data(hass, conf["temperature_csv"], "temperature_data")
    load_csv_data(hass, conf["heating_csv"], "heating_data")

    async def async_get_heating_schedule(call):
        # Appeler l'add-on pour obtenir le planning de chauffe
        schedule = await call_addon_for_schedule(hass.data[DOMAIN])
        return schedule

    hass.services.async_register(DOMAIN, "get_heating_schedule", async_get_heating_schedule)
    return True

def load_csv_data(hass, file_path, data_key):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        hass.data[DOMAIN][data_key] = [row for row in reader]

async def call_addon_for_schedule(data):
    # Simuler l'appel à l'add-on et renvoyer un planning fictif
    # En pratique, vous feriez une requête HTTP ou utiliseriez un autre moyen de communication
    return [
        {"start": "2024-10-01T06:00:00", "end": "2024-10-01T08:00:00"},
        {"start": "2024-10-01T18:00:00", "end": "2024-10-01T22:00:00"}
    ]
