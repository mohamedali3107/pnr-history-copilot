import React from "react";
import { Accordion } from "@/components/ui/accordion";
import { FlightNumberSubForm } from "./FlightNumberSubForm";
import { FlightInfoSubForm } from "./FlightInfoSubForm";
import { BrowsePdfButton } from "./BrowsePdfButton";
import { PnrUpload } from "./PnrUpload";

export function FlightInfoForm() {
  return (
    <div className="w-3/4 mx-auto mt-3 font-sans">
      <Accordion type="single" collapsible defaultValue="item-1">
        {PnrUpload()}
        {/* 
        {FlightNumberSubForm()}
        {FlightInfoSubForm()}
        {BrowsePdfButton()}
         */}
      </Accordion>
    </div>
  );
}
