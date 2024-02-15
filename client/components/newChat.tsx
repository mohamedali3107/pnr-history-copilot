import { Button } from "@/components/ui/button";
import { MessageSquarePlus } from "lucide-react";

export function newChat() {
  return (
    <div className="flex items-center justify-center w-full">
      <Button className="bg-secondary mt-8 mx-auto hover:bg-hover">
        <MessageSquarePlus className="mr-2 h-4 w-4" /> New Chat
      </Button>
    </div>
  );
}
