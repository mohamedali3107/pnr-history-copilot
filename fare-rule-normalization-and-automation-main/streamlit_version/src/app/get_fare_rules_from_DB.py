import pandas as pd


def get_fare_rules_from_DB(flight_code):
    db = pd.read_csv("db_flights_par_mad_doh.csv")
    rows = db.loc[db["primary_key"] == flight_code]

    fare_rules_list = []
    for idx, row in rows.iterrows():
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
