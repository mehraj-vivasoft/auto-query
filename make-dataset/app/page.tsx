import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 h-screen w-screen">
      {// eslint-disable-next-line @next/next/no-img-element
      <img
        src="https://mypihr.com/wp-content/uploads/2022/06/Logo.svg"
        alt="PiHR"
        className="h-14 mb-6"
      />
}
      <div className="text-2xl">Welcome to make dataset platform for PiHR</div>
      <div className="flex gap-4 mt-4">
        <Link
          href={"tables"}
          className="mt-2 px-6 bg-slate-950 text-white rounded-md py-2 text-xl"
        >
          See Tables
        </Link>
        <Link
          href={"dataset/table-metadata"}
          className="mt-2 px-6 bg-slate-950 text-white rounded-md py-2 text-xl"
        >
          See Dataset
        </Link>
      </div>
    </div>
  );
}
