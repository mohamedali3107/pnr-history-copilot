import React from "react";
import { Oval } from "react-loader-spinner";

export function LoadingAnimation() {
  return (
    <div className="absolute top-0 left-0 w-full h-full flex justify-center items-center">
      <Oval height={20} width={20} color="#000835" wrapperStyle={{}} wrapperClass="" visible={true} ariaLabel="oval-loading" secondaryColor="#3A8BFF" strokeWidth={2} strokeWidthSecondary={2} />
    </div>
  );
}
