import React from "react";

const fare_rules_json = {
  changes_conditions: {
    before_departure: "65.00 €",
    no_show_at_first_flight: "Not allowed",
    after_departure: "65.00 €",
    no_show_at_subsequent_flight: "Not applicable",
  },
  refund_conditions: {
    before_departure: "Not allowed",
    no_show_at_first_flight: "Not allowed",
    after_departure: "Not allowed",
    no_show_at_subsequent_flight: "Not applicable",
  },
};

export function FareRules({ selectedPnr }: { selectedPnr: File | null }) {
  return (
    <div className="flex flex-col w-11/12 mx-auto">
      {selectedPnr && (
        <div>
          <p className="text-secondary font-semibold ">Change conditions :</p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">• Before departure: </span>
            {fare_rules_json["changes_conditions"]["before_departure"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">
              • No show at first flight:{" "}
            </span>
            {fare_rules_json["changes_conditions"]["no_show_at_first_flight"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">• After departure: </span>
            {fare_rules_json["changes_conditions"]["after_departure"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">
              • No show at subsequent flight:{" "}
            </span>
            {
              fare_rules_json["changes_conditions"][
                "no_show_at_subsequent_flight"
              ]
            }
          </p>
          <p className="text-secondary font-semibold mt-4">
            Refund conditions :
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">• Before departure: </span>
            {fare_rules_json["refund_conditions"]["before_departure"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">
              • No show at first flight:{" "}
            </span>
            {fare_rules_json["refund_conditions"]["no_show_at_first_flight"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">• After departure: </span>
            {fare_rules_json["refund_conditions"]["after_departure"]}
          </p>
          <p className="text-white text-sm">
            <span className="font-semibold  ml-2">
              • No show at subsequent flight:{" "}
            </span>
            {
              fare_rules_json["refund_conditions"][
                "no_show_at_subsequent_flight"
              ]
            }
          </p>
        </div>
      )}
      {!selectedPnr && (
        <div>
          <p className="text-white text-sm font-semibold">
            Please upload your PNR History
          </p>
        </div>
      )}
    </div>
  );
}
