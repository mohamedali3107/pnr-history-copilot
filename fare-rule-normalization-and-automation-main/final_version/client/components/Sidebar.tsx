import React, { useState } from "react";
import { PrevChatList } from "./PrevChatList";
import { FlightInfoForm } from "./FlightInfoForm";
import Image from "next/image";
import logo from "../public/logo_blanc.png";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";
import { MessagesSquare } from "lucide-react";
import { MessageSquarePlus } from "lucide-react";
type UpdateType = {
  "modification date": string;
  object: string;
  author: string;
};

export function Sidebar({
  setPnrInfo,
  pnrInfo,
}: {
  setPnrInfo: React.Dispatch<React.SetStateAction<string | null>>;
  pnrInfo: string | null;
}) {
  const previousConversation = [
    "Adding Special Seat...",
    "Flight refund for ...",
    "Cancellation condit...",
    "Special Meal Request..",
    "Help for exchange",
  ];

  // Create a function to handle the click event. Depending on the selected button on the left side of the side bar, the content of the right side of the side bar will change.
  const [selected, setSelected] = useState<string>("prev-chat");

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    const buttonValue = event.currentTarget.value;
    setSelected(buttonValue);
  };

  const handleNewChatCLick = () => {
    setSelected("form");
  };

  return (
    <div id="sidebar" className="w-1/4 bg-primary min-h-screen flex relative">
      <div className="flex flex-col">
        {/* <div className="flex flex-row gap-2 px-5 items-center justify-center">
          <Button
            className="bg-secondary mt-8 mx-auto hover:bg-hover w-full"
            key="prev-chat"
            value="prev-chat"
            onClick={handleClick}
          >
            <Home className="mr-2 h-4 w-4" /> Home
          </Button>

          <Button
            className="bg-secondary mt-8 mx-auto hover:bg-hover w-full"
            key="form"
            value="form"
            onClick={handleClick}
          >
            <MessagesSquare className="mr-2 h-4 w-4" /> Chat
          </Button>
        </div> */}
        <header className="mt-7 w-3/4 mx-auto ">
          <Image src={logo} alt="Logo" className="" />
          <h1
            className="font-bold text-xl text-secondary font-body"
            style={{ textAlign: "center" }}
          >
            copilot
          </h1>
        </header>

        {selected === "prev-chat" ? (
          <div className="flex items-center justify-center w-full">
            <Button
              className="bg-secondary mt-8 mx-auto hover:bg-hover"
              onClick={handleNewChatCLick}
            >
              <MessageSquarePlus className="mr-2 h-4 w-4" /> New Chat
            </Button>
          </div>
        ) : null}

        {selected === "prev-chat" ? (
          <PrevChatList previousConversation={previousConversation} />
        ) : (
          <FlightInfoForm setPnrInfo={setPnrInfo} pnrInfo={pnrInfo} />
        )}
      </div>
    </div>
  );
}
