import React from "react";
import { Accordion } from "@/components/ui/accordion";
import { FlightNumberSubForm } from "./FlightNumberSubForm";
import { FlightInfoSubForm } from "./FlightInfoSubForm";
import { BrowsePdfButton } from "./BrowsePdfButton";
import { PnrUpload } from "./PnrUpload";

type UpdateType = {
  "modification date": string;
  object: string;
  author: string;
};

export function FlightInfoForm({
  setPnrInfo,
  pnrInfo,
}: {
  setPnrInfo: React.Dispatch<React.SetStateAction<string | null>>;
  pnrInfo: string | null;
}) {
  return (
    <div className="w-3/4 mx-auto mt-3 font-sans">
      <Accordion type="single" collapsible defaultValue="item-1">
        <PnrUpload setPnrInfo={setPnrInfo} pnrInfo={pnrInfo} />
        {/* 
        {PnrUpload()}
        {FlightNumberSubForm()}
        {FlightInfoSubForm()}
        {BrowsePdfButton()}
         */}
      </Accordion>
    </div>
  );
}
