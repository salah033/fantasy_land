def fetch_games(url):
    from requests.exceptions import RequestException
    import requests

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for 4xx/5xx
        data = response.json()
        return data.get('results', [])
    except RequestException as e:
        print(f"Request error: {e}")
        return []
    except ValueError:
        print("Error decoding JSON.")
        return []