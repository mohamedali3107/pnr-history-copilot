import React, { useState, ChangeEvent, useRef } from "react";
import { FaRegFilePdf } from "react-icons/fa6";
import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";
import { useChatStore } from "./chatStore";
import { useLoadingStore } from "./Loading";

const truncateFileName = (fileName: string, maxLength: number) => {
  return fileName.length > maxLength ? `${fileName.substring(0, maxLength)}...` : fileName;
};

export function BrowsePdfButton() {
  const {addToHistory} = useChatStore();
  const { setIsLoading } = useLoadingStore();

  const [selectedPdf, setSelectedPdf] = useState<File | null>(null);
  const pdfInputRef = useRef<HTMLInputElement>(null);
  const uploadPdf = async (pdf: File) => {
    setIsLoading(true)
    const formData = new FormData();
    formData.append("pdf", pdf);

    const urls = [
      "http://127.0.0.1:8000/upload_pdf",
      "https://f23-p2-airules.paris-digital-lab.fr/back/upload_pdf"
    ]

    let response;

    for (const url of urls) {
      try {
        response = await fetch(url, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          try {
            const data = await response.json();
            console.log(data);
            addToHistory({ content: data.paragraph, role: "assistant", id: "pdf" })
            setIsLoading(false)
          } catch (error) {
            console.error("Error uploading pdf:", error);
          }
          // If the response is successful, break out of the loop
          break;
        }
      } catch (error) {
        console.error(`Error fetching data from ${url}:`, error);
      }
    }
  };

  const handlePdfChange = (event: ChangeEvent<HTMLInputElement>) => {
    const pdf = event.target.files?.[0];
    setSelectedPdf(pdf || null);

    if (pdf) {
      uploadPdf(pdf);
    }
  };

  const handleDeletePdf = () => {
    setSelectedPdf(null);
    // Reset the pdf input value
    if (pdfInputRef.current) {
      pdfInputRef.current.value = "";
    }
  };

  return (
    <div className="flex flex-col text-center relative items-center justify-center">
      <Button className="rounded-md bg-secondary mt-8 text-neutral hover:bg-hover p-3 cursor-pointer" onClick={() => pdfInputRef.current?.click()}>
        Browse File
      </Button>

      <input ref={pdfInputRef} type="file" id="fileInput" className="hidden" onChange={handlePdfChange} />

      {selectedPdf && (
        <div className="flex mt-2 space-x-2">
          <FaRegFilePdf className="bg-primary text-neutral" />
          <p className="font-body text-sm text-neutral text-ellipsis">{truncateFileName(selectedPdf.name, 15)}</p>

          <button onClick={handleDeletePdf} className="text-neutral hover:underline focus:outline-none ml-2">
            <Trash className="text-neutral bg-primary h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  );
}
