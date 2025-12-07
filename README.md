# Taipei Bus Stop Monitor for Home Assistant

A custom Home Assistant integration that fetches and displays real-time Taipei bus stop information on your dashboard.

## Features

- 🚌 Fetch real-time bus stop data from Taipei's public transport API
- ⚙️ Easy configuration through Home Assistant UI
- 🔄 Automatic updates every 30 seconds
- ⏱️ Displays bus arrival time in minutes

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
2. Restart Home Assistant

## Configuration

### Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Taipei Bus Stop Monitor"
3. Enter:
   - **Name**: A friendly name for this bus stop (e.g., "Main Street Stop")
   - **API URL**: The base URL to the bus stop API (nocache parameter will be added automatically)
     - Example: `https://pda5284.gov.taipei/MQS/StopDyna?stopid=212756`

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

- **state**: Arrival time in minutes (or "unavailable" if no arrival data)
- **unit_of_measurement**: minutes (min)

### Attributes:
- **arrival_time_seconds**: Original arrival time in seconds from API (null if unavailable or -1)
- **update_time**: Timestamp of the last API update (format: "YYYY-MM-DD HH:MM:SS")
- **stop_id**: Bus stop identifier
- **url**: The configured API URL
- **raw_data**: Complete raw data from API (n1 field)

## Dashboard Display

You can display the sensor data using standard Home Assistant entity cards. The sensor state shows the arrival time in minutes, and additional information is available in the attributes.

## Troubleshooting

### Integration not showing up

1. Make sure you copied the files to the correct directories
2. Restart Home Assistant
3. Clear your browser cache

### No data or "Unknown" state

1. Verify the API URL is correct and accessible
2. Check Home Assistant logs for error messages
3. Test the URL in your browser to ensure it returns JSON data

## Development

### File Structure

```
tpbus/
└── custom_components/
    └── tpbus/
        ├── __init__.py
        ├── manifest.json
        ├── const.py
        ├── sensor.py
        ├── config_flow.py
        └── strings.json
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
