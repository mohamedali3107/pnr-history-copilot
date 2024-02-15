import { ConvButton } from "./convButton";

export function PrevChatList(props: { previousConversation: string[] }) {
  const previousConvOnClick = () => {
    console.log("Previous conv clicked");
  };

  return (
    <div id="prev-conv" className="flex flex-col justify-center items-center">
      <h3 className="mt-10 text-lg font-body text-white"> Chat History</h3>
      <p className="text-xs text-white italic"> (Not functional yet)</p>
      {props.previousConversation.map((conv, index) =>
        ConvButton({ onClick: previousConvOnClick, convTitle: conv, id: index })
      )}
    </div>
  );
}
