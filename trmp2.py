from api_monitor import ApiMonitor
import requests

monitor = ApiMonitor(cred_path="/path/to/firebase_cred.json")

MAX_LIMIT = 2500
MAX_FAILURES = 5

count, failures, is_down = monitor.get_status("tomtom")

if count >= MAX_LIMIT or failures >= MAX_FAILURES:
    monitor.mark_api_status("tomtom", True)
    print("TomTom API is down.")
else:
    try:
        response = requests.get("https://api.tomtom.com/...")
        response.raise_for_status()

        monitor.increment_api_count("tomtom")
        monitor.reset_failure_count("tomtom")
        monitor.mark_api_status("tomtom", False)

    except requests.RequestException:
        monitor.increment_failure("tomtom")
        print("TomTom API call failed.")
