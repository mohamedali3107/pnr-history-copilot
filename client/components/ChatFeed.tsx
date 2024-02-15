import React from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { useChatStore } from "@/components/chatStore";
import { ScrollArea } from "@/components/ui/scroll-area";

export function ChatFeed() {
  const { chatHistory, addToHistory } = useChatStore();

  return chatHistory.length !== 0 ? (
    <div className="h-3/5 mt-20 space-y-5 w-[75%] overflow-y-auto flex flex-col justify-end">
      <ScrollArea id="chat-feed">
        {chatHistory.map((message) => (
          <div key={message.id}>{ChatMessage({ message: message })}</div>
        ))}
      </ScrollArea>
    </div>
  ) : (
    <div className="flex flex-row  w-[60%] gap-4 justify-center absolute bottom-28">
      <div className="border-2 border-primary rounded-md w-[50%]">
        <p className="text-primary text-center text-sm p-5">
          Upload your PNR history to get a summarize version{" "}
        </p>
      </div>

      <div className="border-2 border-primary rounded-md w-[50%]">
        <p className="text-primary text-center text-sm p-5">
          Ask questions to the ChatBot for more informations{" "}
        </p>
      </div>
    </div>
  );
}
