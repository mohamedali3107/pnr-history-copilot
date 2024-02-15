import React, { useState } from "react";
import { Accordion } from "@/components/ui/accordion";
import { PnrUpload } from "./PnrUpload";
import * as Tabs from "@radix-ui/react-tabs";
import { FareRules } from "./FareRules";
import { FlightInfo } from "./types";

export function FlightInfoForm({
  setPnrInfo,
  pnrInfo,
}: {
  setPnrInfo: React.Dispatch<React.SetStateAction<string | null>>;
  pnrInfo: string | null;
}) {
  const [selectedPnr, setSelectedPnr] = useState<File | null>(null);
  const [fareRules, setFareRules] = useState<FlightInfo[] | null>(null);
  return (
    <div className="mt-3 font-sans">
      <div>
        <Tabs.Root className="flex flex-col mt-2" defaultValue="tab1">
          <Tabs.List
            className="shrink-0 flex border-b border-white"
            aria-label="Manage your account"
          >
            <Tabs.Trigger
              className="bg-transparent text-white px-5 h-[45px] flex-1 flex items-center justify-center text-[15px] leading-none text-mauve11 select-none first:rounded-tl-md last:rounded-tr-md hover:text-violet11 outline-none cursor-default data-[state=active]:text-secondary"
              value="tab1"
            >
              PNR History{" "}
            </Tabs.Trigger>
            <Tabs.Trigger
              className="bg-transparent text-white px-5 h-[45px] flex-1 flex items-center justify-center text-[15px] leading-none text-mauve11 select-none first:rounded-tl-md last:rounded-tr-md hover:text-violet11 outline-none cursor-default data-[state=active]:text-secondary"
              value="tab2"
            >
              Fare rules
            </Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content
            className="grow p-5 bg-transparent text-white"
            value="tab1"
          >
            <div className=" items-center w-11/12 mx-auto">
              <Accordion type="single" collapsible defaultValue="item-1">
                <PnrUpload
                  setPnrInfo={setPnrInfo}
                  pnrInfo={pnrInfo}
                  selectedPnr={selectedPnr}
                  setSelectedPnr={setSelectedPnr}
                />
              </Accordion>
            </div>
          </Tabs.Content>
          <Tabs.Content
            className="grow p-5 bg-transparent text-white"
            value="tab2"
          >
            <Accordion type="single" collapsible defaultValue="item-1">
              {/* {FlightNumberSubForm()}
              {FlightInfoSubForm()}
              {BrowsePdfButton()} */}
              <FareRules
                selectedPnr={selectedPnr}
                fareRules={fareRules}
                setFareRules={setFareRules}
                pnrInfo={pnrInfo}
              />
            </Accordion>
          </Tabs.Content>
        </Tabs.Root>
      </div>
    </div>
  );
}
