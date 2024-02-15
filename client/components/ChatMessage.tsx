import { Message } from "ai";
import { BsChatRightDotsFill } from "react-icons/bs";
import { CiUser } from "react-icons/ci";
import { IconContext } from "react-icons";

export function ChatMessage(props: { message: Message }) {
  const messageWithLineBreaks = props.message.content.replace(/\n/g, "<br>");

  return (
    <div key={props.message.id} className="w-full mt-4 ">
      {props.message.role === "user" ? (
        <div className="flex gap-x-2">
          <div className="bg-secondary h-12 w-12 rounded-lg">
            {" "}
            <IconContext.Provider
              value={{
                className: "w-full h-full text-neutral p-2",
              }}
            >
              <CiUser />
            </IconContext.Provider>
          </div>
          <p className="bg-secondary rounded-lg p-3 w-full text-sm mt-auto mb-auto text-neutral text-left"> {props.message.content}</p>
        </div>
      ) : (
        <div className="flex gap-x-2">
          <div className="bg-primary h-12 w-12 rounded-lg ">
            <IconContext.Provider
              value={{
                className: "w-full h-full text-neutral p-3",
              }}
            >
              <BsChatRightDotsFill />
            </IconContext.Provider>
          </div>

          <p className="rounded-lg p-3 w-full bg-primary text-sm mt-auto mb-auto text-neutral" dangerouslySetInnerHTML={{ __html: messageWithLineBreaks }}></p>
        </div>
      )}
    </div>
  );
}
