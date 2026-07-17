import json
import urllib.parse
import urllib.request
import urllib.error
import os


API_URL = "https://voip.ms/api/v1/rest.php"

API_USERNAME = os.environ["VOIPMS_API_USERNAME"]
API_PASSWORD = os.environ["VOIPMS_API_PASSWORD"]


def get_phonebook():
    """Retrieve VoIP.ms phonebook entries."""

    params = {
        "api_username": API_USERNAME,
        "api_password": API_PASSWORD,
        "method": "getPhonebook",
    }

    url = API_URL + "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urllib.request.urlopen(request) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)


def set_phonebook(name, number):
    """Create a VoIP.ms phonebook entry."""

    params = {
        "api_username": API_USERNAME,
        "api_password": API_PASSWORD,
        "method": "setPhonebook",
        "phonebook": "",
        "speed_dial": "",
        "name": name,
        "number": number,
        "callerid": "",
        "note": "",
        "group": "0",
    }

    data = urllib.parse.urlencode(params).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    with urllib.request.urlopen(request) as response:
        result = response.read().decode("utf-8")

    return json.loads(result)


def del_phonebook(phonebook_id):
    """Delete a VoIP.ms phonebook entry."""

    params = {
        "api_username": API_USERNAME,
        "api_password": API_PASSWORD,
        "method": "delPhonebook",
        "phonebook": phonebook_id,
    }

    url = API_URL + "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urllib.request.urlopen(request) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)


print()
print("Getting VoIP.ms phonebook...")
print()

result = get_phonebook()

print(json.dumps(result, indent=2))
print(del_phonebook("1467930"))
