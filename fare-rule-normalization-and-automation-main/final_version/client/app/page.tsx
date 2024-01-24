"use client";
import { Sidebar } from "@/components/Sidebar";
import { ConversationArea } from "@/components/ConversationArea";

export default function Home() {
  return (
    <div className="h-screen flex">
      {Sidebar()}

      {ConversationArea()}
    </div>
  );
}
