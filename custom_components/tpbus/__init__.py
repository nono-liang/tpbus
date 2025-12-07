"""The Taipei Bus Stop Monitor integration."""
from __future__ import annotations

import logging
import time
import os
import shutil
from datetime import timedelta
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]
DOMAIN = "tpbus"

SCAN_INTERVAL = timedelta(seconds=30)
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Taipei Bus from a config entry."""
    # Copy the frontend card to www directory if it doesn't exist
    www_dir = hass.config.path("www")
    card_source = os.path.join(os.path.dirname(__file__), "www", "tpbus-card.js")
    card_dest = os.path.join(www_dir, "tpbus-card.js")
    
    if os.path.exists(card_source):
        os.makedirs(www_dir, exist_ok=True)
        if not os.path.exists(card_dest):
            await hass.async_add_executor_job(shutil.copy2, card_source, card_dest)
            _LOGGER.info("Copied tpbus-card.js to www directory")
    
    base_url = entry.data["url"]: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Taipei Bus from a config entry."""
    base_url = entry.data["url"]
    
    def get_url_with_nocache(base_url: str) -> str:
        """Append nocache parameter with current timestamp."""
        parsed = urlparse(base_url)
        params = parse_qs(parsed.query)
        params['nocache'] = [str(int(time.time() * 1000))]
        new_query = urlencode(params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    async def async_update_data():
        """Fetch data from API."""
        try:
            url = get_url_with_nocache(base_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="tpbus",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
