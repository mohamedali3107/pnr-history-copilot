import requests
import json
import time
import streamlit as st


def get_fare_rules_from_API(
    origin_code, destination_code, iata_code, departure_date, one_way=True
):
    CLIENT_ID = "GLTb6rEfRXYXCsQ6saBi2GG0vHMBu4y8"
    CLIENT_SECRET = "Oy6g54u39aFYwMR5"

    credential_request = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    # 0. Handle lower case codes
    origin_code = origin_code.upper()
    destination_code = destination_code.upper()
    iata_code = iata_code.upper()

    # 1. Obtain Access Token
    url_credential = "https://test.api.amadeus.com/v1/security/oauth2/token"
    header_credential = {"Content-Type": "application/x-www-form-urlencoded"}
    response_credential = requests.post(
        url_credential, headers=header_credential, data=credential_request
    )
    access_token = response_credential.json()["access_token"]

    # 2. Get request to obtain flights info
    if not one_way:
        url_flight = (
            "https://test.api.amadeus.com/v2/shopping/flight-offers?"
            f"originLocationCode={origin_code}&destinationLocationCode="
            f"{destination_code}&departureDate={departure_date}"
            "&returnDate=2023-12-22&adults=1&includedAirlineCodes="
            f"{iata_code}&max=1"
        )

    else:
        url_flight = (
            "https://test.api.amadeus.com/v2/shopping/flight-offers?"
            f"originLocationCode={origin_code}&destinationLocationCode="
            f"{destination_code}&departureDate={departure_date}&adults="
            f"1&&includedAirlineCodes={iata_code}&max=10"
        )

    header_flight = {"Authorization": f"Bearer {access_token}"}
    response_flight = requests.get(url_flight, headers=header_flight)

    if response_flight.status_code == 200:
        flight_data = response_flight.json()

    else:
        print(
            f"""
            Failed to obtain flight offers with status code:
            {response_flight.status_code} : {response_flight.reason}
            """
        )
        return None

    with open("fare_data_json/full_itinerary.json", "w", encoding="utf-8") as json_file:
        json.dump(flight_data, json_file, ensure_ascii=False, indent=4)

    time.sleep(2)

    # 3. Get request to obtain fare rules
    url_fare_rules = (
        "https://test.api.amadeus.com/v1/shopping/"
        "flight-offers/pricing?include=detailed-fare-rules"
    )

    if flight_data["data"]:
        header_fare_rules = {"Authorization": f"Bearer {access_token}"}
        fare_request_body = {
            "data": {
                "type": "flight-offers-pricing",
                "flightOffers": [flight_data["data"][0]],
            }
        }
        response_fare_rules = requests.post(
            url_fare_rules, headers=header_fare_rules, json=fare_request_body
        )
        fare_data = response_fare_rules.json()

        # Save json file in /fare_data_json
        with open(
            "fare_data_json/full_flight_fare.json", "w", encoding="utf-8"
        ) as json_file:
            json.dump(fare_data, json_file, ensure_ascii=False, indent=4)

        # 4. Format answer to return a list of dictionaries with the fare rules
        fare_rules_list = []
        nb_of_flights = len(
            fare_data["data"]["flightOffers"][0]["itineraries"][0]["segments"]
        )

        for i in range(nb_of_flights):
            flight_info = {}
            flight_info["departure"] = fare_data["data"]["flightOffers"][0][
                "itineraries"
            ][0]["segments"][i]["departure"]["iataCode"]

            flight_info["arrival"] = fare_data["data"]["flightOffers"][0][
                "itineraries"
            ][0]["segments"][i]["arrival"]["iataCode"]

            flight_info["category"] = fare_data["data"]["flightOffers"][0][
                "travelerPricings"
            ][0]["fareDetailsBySegment"][i]["cabin"]

            flight_info["fare_basis"] = fare_data["data"]["flightOffers"][0][
                "travelerPricings"
            ][0]["fareDetailsBySegment"][0]["fareBasis"]

            flight_info["carrierCode"] = fare_data["data"]["flightOffers"][0][
                "itineraries"
            ][0]["segments"][i]["carrierCode"]

            if "included" in fare_data.keys():
                flight_info["fare_rules"] = ""

                tmp = fare_data["included"]["detailed-fare-rules"][str(i + 1)][
                    "fareNotes"
                ]["descriptions"]

                for i in range(len(tmp)):
                    flight_info["fare_rules"] += tmp[i]["text"]

            else:
                print("No fare note for this particular flight")

            fare_rules_list.append(flight_info)
            # Save this dic in a json file in /fare_data_json
            with open(
                f"fare_data_json/fare_rules_{i}.json", "w", encoding="utf-8"
            ) as json_file:
                json.dump(flight_info, json_file, ensure_ascii=False, indent=4)

        return fare_rules_list
    else:
        text = "The flight doesn't exist. Please change the flight information."
        st.write(text)
        return None


# fare_rules_list = get_fare_rules_from_API(
#     "PAR", "DXB", "2023-11-23", one_way=False
#     )
