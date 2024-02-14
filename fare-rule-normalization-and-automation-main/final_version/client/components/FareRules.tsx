import React from "react";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const fare_rules_json = [
  {
    depart: "Nice",
    arrival: "Charles de Gaulle",

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
  },
  {
    depart: "Barcelone",
    arrival: "Orly",

    changes_conditions: {
      before_departure: "70.00 €",
      no_show_at_first_flight: "Not allowed",
      after_departure: "75.00 €",
      no_show_at_subsequent_flight: "Not applicable",
    },
    refund_conditions: {
      before_departure: "Not allowed",
      no_show_at_first_flight: "Not allowed",
      after_departure: "Not allowed",
      no_show_at_subsequent_flight: "Not applicable",
    },
  },
];

export function FareRules({ selectedPnr }: { selectedPnr: File | null }) {
  return (
    <div className="flex flex-col w-11/12 mx-auto">
      {selectedPnr && (
        <AccordionItem value="item-1">
          <p className="text-secondary font-semibold mt-2">Flights :</p>
          {fare_rules_json?.map((flight, index) => (
            <AccordionItem key={index} value={`flight-${index}`}>
              <AccordionTrigger className="text-sm text-white">{`${flight.depart} to ${flight.arrival}`}</AccordionTrigger>
              <AccordionContent>
                <p className="text-secondary font-semibold ">
                  Change conditions :
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • Before departure:{" "}
                  </span>
                  {flight["changes_conditions"]["before_departure"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • No show at first flight:{" "}
                  </span>
                  {flight["changes_conditions"]["no_show_at_first_flight"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • After departure:{" "}
                  </span>
                  {flight["changes_conditions"]["after_departure"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • No show at subsequent flight:{" "}
                  </span>
                  {flight["changes_conditions"]["no_show_at_subsequent_flight"]}
                </p>
                <p className="text-secondary font-semibold mt-4">
                  Refund conditions :
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • Before departure:{" "}
                  </span>
                  {flight["refund_conditions"]["before_departure"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • No show at first flight:{" "}
                  </span>
                  {flight["refund_conditions"]["no_show_at_first_flight"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • After departure:{" "}
                  </span>
                  {flight["refund_conditions"]["after_departure"]}
                </p>
                <p className="text-white text-sm">
                  <span className="font-semibold  ml-2">
                    • No show at subsequent flight:{" "}
                  </span>
                  {flight["refund_conditions"]["no_show_at_subsequent_flight"]}
                </p>
              </AccordionContent>
            </AccordionItem>
          ))}
        </AccordionItem>
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
