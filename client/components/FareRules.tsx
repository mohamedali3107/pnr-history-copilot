import React, { useEffect, useState } from "react";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Flight,
  PassengerData,
  UpdateType,
  AnswerType,
  FlightInfo,
} from "./types";

export function FareRules({
  selectedPnr,
  pnrInfo,
  fareRules,
  setFareRules,
}: {
  selectedPnr: File | null;
  pnrInfo: string | null;
  fareRules: FlightInfo[] | null;
  setFareRules: React.Dispatch<React.SetStateAction<FlightInfo[] | null>>;
}) {
  let pnrData: AnswerType | null = null;
  let pnrSum: PassengerData | null = null;
  let pnrNumber: string | null = null;
  const [chokbar, setChokbar] = useState<boolean | null>(true);

  //Code qui définit le summary et la timeline
  if (pnrInfo !== null) {
    let pnrProcess: string = pnrInfo;
    if (pnrInfo[0] === "`") {
      pnrProcess = pnrInfo.substring(7, pnrInfo.length - 3);
    }
    pnrData = JSON.parse(pnrProcess);
    if (pnrData !== null) {
      pnrSum = pnrData["summary"];
      pnrNumber = pnrData["pnr_number"];
    }
  }

  const fetchFareRules = async () => {
    let response;
    const headers = {
      "Content-Type": "application/json",
    };
    let requestData = {};
    if (pnrSum) {
      requestData = {
        departure_date: pnrSum["flights"][0]["date"],
        origin_code: pnrSum["flights"][0]["depart code"],
        destination_code: pnrSum["flights"][0]["arrival code"],
        airline_code: pnrSum["flights"][0]["airline code"],
        session_id: sessionStorage.getItem("sessionId"),
      };
    } else {
      console.error("pnrSum is null");
      return;
    }
    const urls = [
      "http://127.0.0.1:8000/fill_template_API",
      "https://f23-p3-amadeus.paris-digital-lab.fr/back/fill_template_API",
    ];
    for (const url of urls) {
      try {
        response = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify(requestData),
        });

        if (response.ok) {
          try {
            const data = await response.json();
            if ("fares_to_display" in data) {
              setFareRules(data.fares_to_display);
              setChokbar(true);
            } else {
              setChokbar(false);
            }
          } catch (error) {
            console.error("Error uploading pnr:", error);
          }
          // If the response is successful, break out of the loop
          break;
        }
      } catch (error) {
        console.error(`Error fetching data from ${url}:`, error);
      }
    }
  };

  useEffect(() => {
    fetchFareRules();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div className="flex flex-col w-11/12 mx-auto">
      {selectedPnr &&
        chokbar &&
        (fareRules ? (
          <AccordionItem value="item-1">
            <p className="text-secondary font-semibold mt-2">Flights :</p>
            {fareRules?.map((flight, index) => (
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
                    {
                      flight["changes_conditions"][
                        "no_show_at_subsequent_flight"
                      ]
                    }
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
                    {
                      flight["refund_conditions"][
                        "no_show_at_subsequent_flight"
                      ]
                    }
                  </p>
                </AccordionContent>
              </AccordionItem>
            ))}
          </AccordionItem>
        ) : (
          <p> Loading... </p>
        ))}
      {selectedPnr && !chokbar && (
        <div className="text-sm">
          <p>Sorry, we couldn&apost find the fare rules. </p>
          <p className="mt-2">
            Please make sure you have chosen a PNR History with real flights...
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
