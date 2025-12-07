# Taipei Bus Stop Monitor for Home Assistant

A custom Home Assistant integration that fetches and displays real-time Taipei bus stop information on your dashboard.

## Features

- 🚌 Fetch real-time bus stop data from Taipei's public transport API
- ⚙️ Easy configuration through Home Assistant UI
- 📊 Custom Lovelace card for beautiful dashboard display
- 🔄 Automatic updates every 30 seconds
- 📱 Responsive design that works on mobile and desktop

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/tpbus` directory to your Home Assistant's `custom_components` directory
2. Copy the `www/tpbus-card.js` file to your Home Assistant's `www` directory
3. Restart Home Assistant

## Configuration

### Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Taipei Bus Stop Monitor"
3. Enter:
   - **Name**: A friendly name for this bus stop (e.g., "Main Street Stop")
   - **API URL**: The base URL to the bus stop API (nocache parameter will be added automatically)
     - Example: `https://pda5284.gov.taipei/MQS/StopDyna?stopid=212756`

### Add Dashboard Card

1. First, register the custom card:
   - Go to **Settings** → **Dashboards** → **Resources**
   - Click **+ Add Resource**
   - URL: `/local/tpbus-card.js`
   - Resource type: **JavaScript Module**
   - Click **Create**

2. Add the card to your dashboard:
   - Edit your dashboard
   - Click **+ Add Card**
   - Scroll down and select **Custom: Taipei Bus Card**
   - Or manually add with YAML:

```yaml
type: custom:tpbus-card
entity: sensor.taipei_bus_stop
title: Main Street Bus Stop
```

## URL Format

The integration accepts URLs from the Taipei Public Transport API. The typical format is:

```
https://pda5284.gov.taipei/MQS/StopDyna?stopid=XXXXX
```

Where:
- `stopid`: The bus stop ID you want to monitor

**Note:** The `nocache` parameter is automatically appended with the current timestamp on each request to prevent caching, so you don't need to include it in your URL

## Available Data

The sensor provides the following data:

- **state**: Arrival time in seconds (or "unavailable" if no arrival data)
- **unit_of_measurement**: seconds (s)

### Attributes:
- **arrival_time_seconds**: Arrival time in seconds (null if unavailable or -1)
- **update_time**: Timestamp of the last API update (format: "YYYY-MM-DD HH:MM:SS")
- **stop_id**: Bus stop identifier
- **url**: The configured API URL
- **raw_data**: Complete raw data from API (n1 field)

## Dashboard Card

The custom Lovelace card displays:
- Bus stop name with bus stop icon
- Large, prominent arrival time countdown (formatted as "Xm Ys" or "Xs")
- Human-readable update time (e.g., "Updated 2 minutes ago")
- Shows "N/A" in red when arrival information is unavailable

## Example Screenshot

The card will look like this on your dashboard:

```
┌─────────────────────────────┐
│ 🚌 Main Street Bus Stop     │
├─────────────────────────────┤
│                             │
│          3m 45s             │
│                             │
├─────────────────────────────┤
│   Updated 2 minutes ago     │
└─────────────────────────────┘
```

## Troubleshooting

### Integration not showing up

1. Make sure you copied the files to the correct directories
2. Restart Home Assistant
3. Clear your browser cache

### Card not rendering

1. Verify the resource is added in **Settings** → **Dashboards** → **Resources**
2. Clear browser cache (Ctrl+F5)
3. Check browser console for errors (F12)

### No data or "Unknown" state

1. Verify the API URL is correct and accessible
2. Check Home Assistant logs for error messages
3. Test the URL in your browser to ensure it returns JSON data

## Development

### File Structure

```
tpbus/
├── custom_components/
│   └── tpbus/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── sensor.py
│       ├── config_flow.py
│       └── strings.json
└── www/
    └── tpbus-card.js
```

### Logs

To enable debug logging, add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.tpbus: debug
```

## Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check existing issues for solutions

## License

MIT License - feel free to use and modify as needed.

## Credits

Created for monitoring Taipei's public bus system through their open data API.
