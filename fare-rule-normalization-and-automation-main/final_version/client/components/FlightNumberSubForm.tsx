import { Button } from "./ui/button";
import { useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormItem,
  FormField,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { useState } from "react";
import { useChatStore } from "./chatStore";
import { useLoadingStore } from "./Loading";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/utils";

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { PopoverClose } from "@radix-ui/react-popover";

export function FlightNumberSubForm() {
  const [flightNumber, setFlightNumber] = useState<string>("");
  const { addToHistory } = useChatStore();
  const { setIsLoading } = useLoadingStore();

  const flightNumbers = [
    { label: "20433914", value: "20433914" },
    { label: "46862526", value: "46862526" },
    { label: "99423583", value: "99423583" },
    { label: "35036959", value: "35036959" },
    { label: "92098075", value: "92098075" },
    { label: "51164392", value: "51164392" },
    { label: "31751388", value: "31751388" },
    { label: "17372820", value: "17372820" },
    { label: "17805374", value: "17805374" },
    { label: "58616104", value: "58616104" },
    { label: "86746617", value: "86746617" },
    { label: "78566593", value: "78566593" },
    { label: "67394757", value: "67394757" },
    // { label: "49630235", value: "49630235" },
    // { label: "56568670", value: "56568670" },
  ] as const;

  const handleSubmit = async () => {
    if (!flightNumber) {
      addToHistory({
        content: "WARNING : It seems that some fields are missing...",
        role: "system",
        id: "2",
      });
    } else {
      setIsLoading(true);
      const urls = [
        "http://127.0.0.1:8000/fill_template_DB",
        "https://f23-p3-amadeus.paris-digital-lab.fr/back/fill_template_DB",
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
              flight_number: flightNumber,
              session_id: sessionStorage.getItem("sessionId"),
            }),
          });

          if (response.ok) {
            try {
              const data = await response.json();
              setIsLoading(false);

              if (data.DB_error) {
                addToHistory({
                  content: "WARNING : Could not find the booking reference",
                  role: "system",
                  id: "2",
                });
              } else if (data.have_fare_rule) {
                data.fares_to_display.forEach((element: any) => {
                  addToHistory({ content: element, role: "system", id: "2" });
                });
                if (data.have_webtext === true) {
                  addToHistory({
                    content: data.paragraph_webtext.paragraph,
                    role: "system",
                    id: "web2",
                  });

                  addToHistory({
                    content:
                      "You can now ask questions about this flight, a PDF and the company Trade Portal.",
                    role: "system",
                    id: "2",
                  });
                } else {
                  addToHistory({
                    content:
                      "You can now ask questions about this flight and a PDF.",
                    role: "system",
                    id: "2",
                  });
                }
              } else {
                if (data.have_webtext === true) {
                  addToHistory({
                    content: data.paragraph_webtext.paragraph,
                    role: "system",
                    id: "web2",
                  });

                  addToHistory({
                    content:
                      "WARNING : No fare rules found for this flight. You can still ask questions about a PDF and the company Trade Portal.",
                    role: "system",
                    id: "2",
                  });
                } else {
                  addToHistory({
                    content:
                      "WARNING : No fare rules found for this flight. You can still ask questions about a PDF but the Trade Portal is not available. ",
                    role: "system",
                    id: "2",
                  });
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

  const form = useForm({
    // Add your validation resolver and default values if needed
    // ...
  });

  return (
    <AccordionItem value="item-1">
      <AccordionTrigger className="text-white">
        Search via Booking Number
      </AccordionTrigger>
      <AccordionContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)}>
            <FormField
              control={form.control}
              name="language"
              render={({ field }) => (
                <FormItem className="flex flex-col text-placeholder w-full">
                  <FormLabel className="text-neutral">
                    Booking Reference
                  </FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn(
                            "w-full justify-between text-primary",
                            !field.value && "text-muted-foreground"
                          )}
                        >
                          {field.value
                            ? flightNumbers.find(
                                (flightNumber) =>
                                  flightNumber.value === field.value
                              )?.label
                            : "Select booking reference"}
                          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>

                    <PopoverContent className="w-full p-0">
                      <PopoverClose>
                        <Command className="w-full">
                          <CommandInput
                            placeholder="Booking reference"
                            className="text-primary w-full"
                          />
                          <CommandEmpty>No booking found</CommandEmpty>
                          <CommandGroup>
                            {flightNumbers.map((flightNumber) => (
                              <CommandItem
                                value={flightNumber.label}
                                key={flightNumber.value}
                                onSelect={() => {
                                  field.onChange(flightNumber.value);
                                  setFlightNumber(flightNumber.value);
                                }}
                              >
                                <Check
                                  className={cn(
                                    "mr-2 h-4 w-4",
                                    flightNumber.value === field.value
                                      ? "opacity-100"
                                      : "opacity-0"
                                  )}
                                />
                                {flightNumber.label}
                              </CommandItem>
                            ))}
                          </CommandGroup>
                        </Command>{" "}
                      </PopoverClose>{" "}
                    </PopoverContent>
                  </Popover>

                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="bg-secondary text-neutral rounded-md p-2 mt-5 hover:bg-hover hover:text-white transition duration-300 ease-in-out w-full "
            >
              {" "}
              Submit
            </Button>
          </form>
        </Form>
      </AccordionContent>
    </AccordionItem>
  );
}
