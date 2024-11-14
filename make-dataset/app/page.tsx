import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 h-screen w-screen px-4 text-center">
      {// eslint-disable-next-line @next/next/no-img-element
      <img
        src="/auto query white.png"
        alt="PiHR"
        className="h-44 mb-6"
      />
}
      <div className="text-2xl">Welcome to make dataset platform for PiHR</div>
      <div className="flex gap-4 mt-4 flex-wrap justify-center items-center">
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
        <Link
          href={"query"}
          className="mt-2 px-6 bg-slate-950 text-white rounded-md py-2 text-xl"
        >
          Query Now
        </Link>
        <Link
          href={"query/samples"}
          className="mt-2 px-6 bg-slate-950 text-white rounded-md py-2 text-xl"
        >
          Samples
        </Link>
      </div>
    </div>
  );
}
