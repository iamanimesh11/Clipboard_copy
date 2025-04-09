MAX_LIMIT = 2500
MAX_FAILURES = 5

count, failures, is_down = get_status("tomtom")

if count >= MAX_LIMIT or failures >= MAX_FAILURES:
    mark_api_status("tomtom", True)
    print("TomTom API is DOWN")
else:
    try:
        # Make the API call
        response = requests.get("...")
        response.raise_for_status()

        increment_api_count("tomtom")
        reset_failure_count("tomtom")
        mark_api_status("tomtom", False)

    except Exception as e:
        increment_failure("tomtom")
        print("TomTom API failure")
