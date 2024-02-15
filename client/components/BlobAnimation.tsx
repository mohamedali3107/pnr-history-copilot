export function BlobAnimation() {
  return (
    <>
      <div className="absolute w-[25%] aspect-square bg-tertiary rounded-full mix-blend-multiply filter opacity-70 animate-blob"></div>
      <div className="absolute w-[25%] aspect-square bg-tertiary rounded-full mix-blend-multiply filter opacity-70 animate-blob animation-delay-2000"></div>
      <div className="absolute w-[25%] aspect-square bg-tertiary rounded-full mix-blend-multiply filter opacity-70 animate-blob animation-delay-4000"></div>
    </>
  );
}
