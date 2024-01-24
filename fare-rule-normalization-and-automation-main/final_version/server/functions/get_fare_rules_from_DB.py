import pandas as pd


def get_fare_rules_from_DB(flight_code):
    """Return a list of dictionaries containing fare rules for a given flight reference.
    The fare rules are obtained from a csv file db_flights_par_mad_doh.csv created with ATPCO data.

    Parameters:
    - flight_code (int or str): The unique identifier of the flight in the database.

    Return:
    - fare_rules_list (list of dict): A list of dictionaries containing fare rules for the specified flight.
      Each dictionary includes information such as carrier code, departure and arrival locations, category,
      fare basis, and fare rules text.
    """
    db = pd.read_csv("db/db_flights_par_mad_doh.csv")
    rows = db.loc[db["primary_key"] == int(flight_code)]

    fare_rules_list = []
    for _, row in rows.iterrows():
        flight = {}

        flight["carrierCode"] = row.loc["iata_code_airline"]
        flight["departure"] = row.loc["flight_departure_iata"]
        flight["arrival"] = row.loc["flight_arrival_iata"]
        flight["category"] = row.loc["branded_fare"]
        flight["fare_basis"] = row.loc["fare_basis"]
        if row.loc["rules_penalties"] != "rules not found for this flight":
            flight["fare_rules"] = (
                row.loc["rules_general_info"]
                + row.loc["rules_penalties"]
                + str(row.loc["rules_ticket_endorsment"])
            )
        fare_rules_list.append(flight)

    return fare_rules_list
