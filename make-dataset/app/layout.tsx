import type { Metadata } from "next";
import { Domine } from "next/font/google";
import { Toaster } from 'react-hot-toast';
import "./globals.css";

const tinos = Domine({
  weight: "400",
  subsets: ["latin"]
});

export const metadata: Metadata = {
  title: "AutoQuery - Natural Language to SQL",
  description: "Auto Query is a tool that converts natural language questions into SQL queries and then returns the response in natural language by executing them on your database.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${tinos.className} antialiased`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
