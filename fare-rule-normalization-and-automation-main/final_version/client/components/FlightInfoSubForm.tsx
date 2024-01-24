import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";
import { useForm } from "react-hook-form";
import { Form, FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { useState } from "react";
import { useChatStore } from "./chatStore";
import { useLoadingStore } from "./Loading";
import { PopoverClose } from "@radix-ui/react-popover";

export function FlightInfoSubForm() {
  const [departureDate, setDepartureDate] = useState<Date>();
  const [departureAirport, setDepartureAirport] = useState<string>("");
  const [arrivalAirport, setArrivalAirport] = useState<string>("");
  const [airline, setAirline] = useState<string>("");
  const { addToHistory } = useChatStore();
  const { setIsLoading } = useLoadingStore();

  const form = useForm({
    // Add your validation resolver and default values if needed
    // ...
  });

  const handleSubmit = async () => {
    if (!departureDate || !departureAirport || !arrivalAirport || !airline) {
      addToHistory({ content: "WARNING : It seems that some fields are missing...", role: "system", id: "2" });
    } else {
      setIsLoading(true);
      const urls = ["http://127.0.0.1:8000/fill_template_API", "https://f23-p2-airules.paris-digital-lab.fr/back/fill_template_API"];

      let response;

      for (const url of urls) {
        try {
          response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ departure_date: format(departureDate, "yyyy-MM-dd"), origin_code: departureAirport, destination_code: arrivalAirport, airline_code: airline }),
          });

          if (response.ok) {
            try {
              const data = await response.json();
              setIsLoading(false);

              if (data.API_error) {
                addToHistory({ content: "WARNING : An error occured while calling the API. Please check your flight informations, the flight may not exist.", role: "system", id: "2" });
              } else if (data.have_fare_rule) {
                data.fares_to_display.forEach((element: any) => {
                  addToHistory({ content: element, role: "system", id: "2" });
                });
                if (data.have_webtext === true) {
                  /// TODO insert here the message for Webtext
                  addToHistory({ content: data.paragraph_webtext.paragraph, role: "system", id: "web2" });
                  addToHistory({ content: "You can now ask questions about this flight, a PDF and the company Trade Portal.", role: "system", id: "2" });
                } else {
                  addToHistory({ content: "You can now ask questions about this flight and a PDF.", role: "system", id: "2" });
                }
              } else {
                if (data.have_webtext === true) {
                  /// TODO insert here the message for Webtext
                  addToHistory({ content: data.paragraph_webtext.paragraph, role: "system", id: "web2" });
                  addToHistory({ content: "WARNING : No fare rules found for this flight. You can still ask questions about a PDF and the company Trade Portal.", role: "system", id: "2" });
                } else {
                  addToHistory({ content: "WARNING : No fare rules found for this flight. You can still ask questions about a PDF but the Trade Portal is not available. ", role: "system", id: "2" });
                }
              }
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
    }
  };

  return (
    <AccordionItem value="item-2">
      <AccordionTrigger className="text-white">Search via Flight Info</AccordionTrigger>
      <AccordionContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)}>
            <FormItem className="text-white">
              <FormLabel> Departure Date </FormLabel>
              <FormControl>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button variant={"outline"} className={cn(" w-full justify-start text-left font-normal text-primary", !departureDate && "text-muted-foreground")}>
                      <CalendarIcon className="mr-2 h-4 w-4 text-primary" />
                      {departureDate ? format(departureDate, "yyyy-MM-dd") : <span className="text-placeholder">Pick a date</span>}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <PopoverClose>
                      <Calendar mode="single" selected={departureDate} onSelect={setDepartureDate} initialFocus className="text-primary" />
                    </PopoverClose>
                  </PopoverContent>
                </Popover>
              </FormControl>
              <FormMessage />
            </FormItem>

            <FormItem className="mt-5 text-white">
              <FormLabel>Origin Code</FormLabel>
              <FormControl>
                <Input onChange={(e) => setDepartureAirport(e.target.value)} placeholder="eg. LHR" className="text-primary" />
              </FormControl>
              <FormMessage />
            </FormItem>

            <FormItem className="mt-5 text-white">
              <FormLabel>Destination Code</FormLabel>
              <FormControl>
                <Input onChange={(e) => setArrivalAirport(e.target.value)} placeholder="eg. PAR" className="text-primary" />
              </FormControl>
              <FormMessage />
            </FormItem>

            <FormItem className="mt-5 text-white">
              <FormLabel>Airline Code</FormLabel>
              <FormControl>
                <Input onChange={(e) => setAirline(e.target.value)} placeholder="eg. AF" className="text-primary" />
              </FormControl>
              <FormMessage />
            </FormItem>

            <Button type="submit" className="bg-secondary text-neutral rounded-md p-2 mt-8 hover:bg-blue-700 hover:text-white transition duration-300 ease-in-out w-full ">
              Submit
            </Button>
          </form>
        </Form>
      </AccordionContent>
    </AccordionItem>
  );
}
