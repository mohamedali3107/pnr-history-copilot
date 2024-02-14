"use client";
import { Sidebar } from "@/components/Sidebar";
import React, { useState } from "react";
import { ConversationArea } from "@/components/ConversationArea";

type UpdateType = {
  "modification date": string;
  object: string;
  author: string;
  agency: string;
};

const defaultTimeline = [
  {
    "modification date": "12/13/23",
    object: "Option for ticketing added with deadline",
    author: "0001AA",
    agency: "NCE1A0955",
  },
  {
    "modification date": "12/13/23",
    object: "Cancellation policy added due to no ticket",
    author: "0001AA",
    agency: "NCE1A0955",
  },
];

export default function Home() {
  const [pnrInfo, setPnrInfo] = useState<string | null>(null);
  const [pnrTimeline, setPnrTimeline] = useState<UpdateType[] | null>(
    defaultTimeline
  );
  const handleTimeline = (timeline: UpdateType[]) => {
    setPnrTimeline(timeline);
  };
  return (
    <div className="h-screen flex">
      <Sidebar setPnrInfo={setPnrInfo} pnrInfo={pnrInfo} />
      <ConversationArea pnrInfo={pnrInfo} />
    </div>
  );
}
