import React, { useState, ChangeEvent, useRef, useEffect } from "react";
import { FaRegFilePdf } from "react-icons/fa6";
import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";
import { useChatStore } from "./chatStore";
import { useLoadingStore } from "./Loading";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ScrollArea } from "@/components/ui/scroll-area-shadcn";

const truncateFileName = (fileName: string, maxLength: number) => {
  return fileName.length > maxLength
    ? `${fileName.substring(0, maxLength)}...`
    : fileName;
};

type Flight = {
  depart: string;
  arrival: string;
  date: string;
  "flight number": string;
  "Special Service Requests": string[];
  "remarks about the fly": string[];
};

type PassengerData = {
  "passengers name": string[];
  flights: Flight[];
  "ticket numnber": string[];
  "general remarks": string[];
};

type UpdateType = {
  "modification date": string;
  object: string;
  author: string;
};

type AnswerType = {
  summary: PassengerData;
  updates: UpdateType[];
};

export function PnrUpload({
  setPnrInfo,
  pnrInfo,
}: {
  setPnrInfo: React.Dispatch<React.SetStateAction<string | null>>;
  pnrInfo: string | null;
}) {
  const { addToHistory } = useChatStore();
  const { setIsLoading } = useLoadingStore();
  const [pnrSummary, setPnrSummary] = useState<string | null>(null);
  const [selectedPnr, setSelectedPnr] = useState<File | null>(null);
  const pnrInputRef = useRef<HTMLInputElement>(null);
  let pnrData: AnswerType | null = null;
  let pnrSum: PassengerData | null = null;

  console.log("pnrInputRef : ", pnrInputRef);

  //Fonction pour envoyer le PNR au back et récupérer le summary et la timeline
  const uploadPnr = async (pnr: File) => {
    let response;
    setIsLoading(true);
    const formData = new FormData();
    formData.append("pnr", pnr);
    const urls = [
      "http://127.0.0.1:8000/upload_pnr",
      "https://f23-p3-amadeus.paris-digital-lab.fr/back/upload_pnr",
    ];
    for (const url of urls) {
      try {
        response = await fetch(url, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          try {
            const data = await response.json();
            console.log("data2 : ", data.paragraph);
            setPnrInfo(data.paragraph);
            // setPnrSummary(data.paragraph);
            setIsLoading(false);
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

  //Code qui définit le summary et la timeline
  if (pnrInfo !== null) {
    pnrData = JSON.parse(pnrInfo);
    if (pnrData !== null) {
      pnrSum = pnrData["summary"];
      console.log("pnrSum : ", pnrSum);
      console.log("timeline : ", pnrData["updates"]);
    }
  }

  //Fonction pour uploader un PNR
  const handlePnrChange = (event: ChangeEvent<HTMLInputElement>) => {
    const pnr = event.target.files?.[0];
    setSelectedPnr(pnr || null);
    if (pnr) {
      uploadPnr(pnr);
    }
  };

  //Fonction pour supprimer un PNR
  const handleDeletePnr = () => {
    setSelectedPnr(null);
    // Reset the pnr input value
    if (pnrInputRef.current) {
      pnrInputRef.current.value = "";
    }
  };

  return (
    <div className="flex flex-col">
      <div className="flex flex-col text-center relative items-center justify-center mb-4">
        <Button
          className="rounded-md bg-secondary my-5 text-neutral hover:bg-hover p-3 cursor-pointer"
          onClick={() => pnrInputRef.current?.click()}
        >
          <svg
            width="15"
            height="15"
            viewBox="0 0 15 15"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="mr-2"
          >
            <path
              d="M7.81825 1.18188C7.64251 1.00615 7.35759 1.00615 7.18185 1.18188L4.18185 4.18188C4.00611 4.35762 4.00611 4.64254 4.18185 4.81828C4.35759 4.99401 4.64251 4.99401 4.81825 4.81828L7.05005 2.58648V9.49996C7.05005 9.74849 7.25152 9.94996 7.50005 9.94996C7.74858 9.94996 7.95005 9.74849 7.95005 9.49996V2.58648L10.1819 4.81828C10.3576 4.99401 10.6425 4.99401 10.8182 4.81828C10.994 4.64254 10.994 4.35762 10.8182 4.18188L7.81825 1.18188ZM2.5 9.99997C2.77614 9.99997 3 10.2238 3 10.5V12C3 12.5538 3.44565 13 3.99635 13H11.0012C11.5529 13 12 12.5528 12 12V10.5C12 10.2238 12.2239 9.99997 12.5 9.99997C12.7761 9.99997 13 10.2238 13 10.5V12C13 13.104 12.1062 14 11.0012 14H3.99635C2.89019 14 2 13.103 2 12V10.5C2 10.2238 2.22386 9.99997 2.5 9.99997Z"
              fill="currentColor"
              fill-rule="evenodd"
              clip-rule="evenodd"
            ></path>
          </svg>{" "}
          Upload PNR History
        </Button>

        <input
          ref={pnrInputRef}
          type="file"
          id="fileInput"
          className="hidden"
          onChange={handlePnrChange}
        />

        {selectedPnr && (
          <div className="flex mt-2 space-x-2">
            <FaRegFilePdf className="bg-primary text-neutral" />
            <p className="font-body text-sm text-neutral text-ellipsis">
              {truncateFileName(selectedPnr.name, 15)}
            </p>

            <button
              onClick={handleDeletePnr}
              className="text-neutral hover:underline focus:outline-none ml-2"
            >
              <Trash className="text-neutral bg-primary h-4 w-4" />
            </button>
          </div>
        )}
      </div>
      {pnrInfo && selectedPnr && (
        <ScrollArea type="always" style={{ height: 500 }}>
          <p className="text-secondary font-semibold">Passengers :</p>
          <ul>
            {pnrData &&
              pnrSum &&
              pnrSum["passengers name"].map((passenger, index) => (
                <li key={index} className="text-white text-sm ml-4">
                  • {passenger}
                </li>
              ))}
          </ul>
          <AccordionItem value="item-1">
            <p className="text-secondary font-semibold mt-2">Flights :</p>
            {pnrSum?.flights.map((flight, index) => (
              <AccordionItem key={index} value={`flight-${index}`}>
                <AccordionTrigger className="text-sm text-white">{`${flight.depart} to ${flight.arrival}`}</AccordionTrigger>
                <AccordionContent>
                  <p className="text-white">
                    <span className="font-semibold">Date: </span>
                    {flight.date}
                  </p>
                  <p className="text-white">
                    <span className="font-semibold">Flight number: </span>{" "}
                    {flight["flight number"]}
                  </p>
                  <p className="text-white font-semibold">Options :</p>
                  <ul>
                    {flight["Special Service Requests"].map((option, i) => (
                      <li key={i} className="text-white ml-2">
                        • {option}
                      </li>
                    ))}
                  </ul>
                  <p className="text-white font-semibold">Remarks :</p>
                  <ul>
                    {flight["remarks about the fly"].map((remark, i) => (
                      <li key={i} className="text-white ml-2">
                        • {remark}
                      </li>
                    ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            ))}
          </AccordionItem>

          <p className="text-secondary font-semibold mt-2">General remarks :</p>
          <ul>
            {pnrData &&
              pnrSum &&
              pnrSum["general remarks"].map((remark, index) => (
                <li key={index} className="text-white text-sm indent-4">
                  • {remark}
                </li>
              ))}
          </ul>
        </ScrollArea>
      )}
    </div>
  );
}
