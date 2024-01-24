import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";

export function ConvButton(props: { onClick: () => void; convTitle: string; id: number }) {
  return (
    <Button className="mx-auto mt-5 w-3/5 bg-secondary text-neutral hover:bg-hover" key={props.id}>
      {props.convTitle}
      <Trash className="mr-2 h-4 w-4 absolute right-5" />
    </Button>
  );
}
