"use client";

import React, { useState } from "react";
import { BlobAnimation } from "@/components/BlobAnimation";
import { useChatStore } from "@/components/chatStore";
import Image from "next/image";
import logo from "../public/logo_bleu.png";
import { ChatFeed } from "./ChatFeed";
import { useLoadingStore } from "./Loading";
import { LoadingAnimation } from "./LoadingAnimation";
import { BlobStatic } from "@/components/BlobStatic";
import Box from "@mui/material/Box";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

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
  agency: string;
};

type AnswerType = {
  summary: PassengerData;
  updates: UpdateType[];
};

export function ConversationArea({ pnrInfo }: { pnrInfo: string | null }) {
  const [question, setQuestion] = useState<string>("");
  const { chatHistory, addToHistory } = useChatStore();
  const { isLoading, setIsLoading } = useLoadingStore();
  let pnrData: AnswerType | null = null;
  let pnrTimeline: UpdateType[] | null = null;

  if (pnrInfo !== null) {
    let pnrProcess: string = pnrInfo;
    if (pnrInfo[0] === "`") {
      pnrProcess = pnrInfo.substring(7, pnrInfo.length - 3);
    }
    console.log("pnrProcess= ", pnrProcess);
    pnrData = JSON.parse(pnrProcess);
    if (pnrData !== null) {
      pnrTimeline = pnrData["updates"];
      console.log("pnrSum : ", pnrTimeline);
      console.log("timeline : ", pnrData["updates"]);
    }
  }

  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();
    addToHistory({ content: question, role: "user", id: "1" });
    setQuestion("");
    setIsLoading(true);
    const urls = [
      "http://127.0.0.1:8000/answer_chat",
      "https://f23-p3-amadeus.paris-digital-lab.fr/back/answer_chat",
    ];

    let response;

    for (const url of urls) {
      try {
        response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
            session_id: sessionStorage.getItem("sessionId"),
          }),
        });
        console.log("response :", response);
        if (response.ok) {
          try {
            const data = await response.json();
            console.log("data : ", data);
            setIsLoading(false);

            addToHistory({ content: data.answer, role: "system", id: "2" });
          } catch (error) {
            console.log(error);
          }
          // If the response is successful, break out of the loop
          break;
        }
      } catch (error) {
        console.error(`Error fetching data from ${url}:`, error);
      }
    }
  };

  const handleTimelineClick = (index: number) => {
    // const up: string = `Date  : ${sampleTimeline[index]["modification date"]} \nModification : ${sampleTimeline[index].object}, \nAuthor : ${sampleTimeline[index].author}`;
    // addToHistory({ content: up, role: "system", id: "2" });
    if (pnrTimeline !== null) {
      const updateSummary: string = `Date  : ${pnrTimeline[index]["modification date"]} \nModification : ${pnrTimeline[index].object} \nAuthor : ${pnrTimeline[index].author} \nAgency : ${pnrTimeline[index].agency}`;
      addToHistory({ content: updateSummary, role: "system", id: "2" });
    }
  };

  return (
    <div
      id="chat"
      className="w-3/4 flex flex-col justify-center relative items-center bg-tertiary"
    >
      {/* Logo */}
      <div className="absolute top-2 mt-8 flex flex-col items-center">
        <Image src={logo} alt="Logo" className="w-1/6" />
        <h1
          className="font-bold text-xl text-slate-500 font-body mb-3"
          style={{ textAlign: "center" }}
        >
          copilot
        </h1>
        <div className="w-full px-10 flex justify-center absolute top-24 ">
          <ScrollArea className="whitespace-nowrap">
            <Box sx={{ width: "100%" }} className="py-2">
              <Stepper activeStep={pnrTimeline?.length} alternativeLabel>
                {pnrTimeline?.map((modification, index) => (
                  <Step key={index}>
                    <StepLabel
                      onClick={() => handleTimelineClick(index)}
                      className="transition-transform transform hover:scale-110 focus:outline-none active:shadow"
                    >
                      {modification["modification date"]}
                    </StepLabel>
                  </Step>
                ))}
              </Stepper>
            </Box>
            <ScrollBar orientation="horizontal" />
          </ScrollArea>
        </div>
      </div>

      {/* Blob animation : if chat history is empty, then if isLoading : display BlobAnimation, BlobStatic else */}
      {chatHistory.length === 0 ? (
        isLoading ? (
          <BlobStatic />
        ) : (
          <BlobAnimation />
        )
      ) : (
        <></>
      )}

      {/* Chat feed section */}

      {ChatFeed()}

      {/* Prompting bar section */}
      <form
        onSubmit={handleSubmit}
        className="p-5 bg-primary rounded-xl bottom-4 fixed w-1/2"
      >
        <div className="flex relative items-center">
          <input
            className="w-full focus:outline-none placeholder:text-primary text-sm text-primary p-3 pr-16 rounded-lg"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Send message.."
          />

          {!isLoading ? (
            <button
              type="submit"
              className="absolute bg-secondary p-1 rounded-lg right-0 mr-3"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-5 h-5 text-white"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                />
              </svg>
            </button>
          ) : (
            <div className="absolute  p-4 right-0 mr-3">
              <LoadingAnimation />
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
