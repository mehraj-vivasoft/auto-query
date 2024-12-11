import React from "react";
import { BarChartBasic } from "./BarChart";

const js = {
  bars: [
    { keyName: "Md Ariful Islam", value: 8 },
    { keyName: "Alim Uddin Rafi", value: 7 },
    { keyName: "Md. Ariful islam Manik", value: 7 },
    { keyName: "Kawsar Hossain Eidul", value: 7 },
    { keyName: "Afraeem Ahmed", value: 3 },
    { keyName: "S.M Shamiun Noor", value: 2 },
    { keyName: "Md.Shoukut Akbar Shuvo", value: 1 },
    { keyName: "Mehedi Al Masud", value: 1 },
    { keyName: "Shayekh Ebne Mizan", value: 1 },
    { keyName: "Jahid Bin Moshiur", value: 0 },
    { keyName: "Prodipta sen", value: 0 },
    { keyName: "Jayakumar . Jayaraman", value: 0 },
    { keyName: "PiHR2 QA1", value: 0 },
    { keyName: "Diganta Das", value: 0 },
    { keyName: "Md. Abdullah AL Kafi", value: 0 },
    { keyName: "Oahidul Islam", value: 0 },
    { keyName: "Rajib Kumar Saha", value: 0 },
    { keyName: "Biplab Sarker", value: 0 },
    { keyName: "Ayesha Siddique", value: 0 },
    { keyName: "Mohammad Aminul Islam", value: 0 },
    { keyName: "Sergio Busquets", value: 0 },
    { keyName: "akbar shouvo", value: 0 },
    { keyName: "Nahid hossain", value: 0 },
  ],
  key_title: "Employee Name",
  value_title: "Total Leave Days",
  bar_chart_title: "Employee Leave Days Over the Last 3 Months",
  bar_chart_description:
    "This bar chart displays the total leave days taken by each employee in the last three months, sorted by the leave days count from highest to lowest.",
};


function transformChartData(input: {
  bars: { keyName: string; value: number }[];
  key_title: string;
  value_title: string;
  bar_chart_title: string;
  bar_chart_description: string;
}) {
  // Dynamically map key and value titles
  const keyTitle = input.key_title.replace(/\s+/g, ""); // Remove spaces
  const valueTitle = input.value_title.replace(/\s+/g, ""); // Remove spaces

  return {
    chartData: input.bars
      .filter((item) => item.value > 0) // Exclude entries with value 0
      .map((item) => ({
        [keyTitle]: item.keyName, // Use dynamic key for EmployeeName
        [valueTitle]: item.value, // Use dynamic key for TotalLeaveDays
      })),
    title: input.bar_chart_title,
    subtitle: input.bar_chart_description,
  };
}

const page = () => {
  const transformedData = transformChartData(js);
  return (
    <div className="flex flex-col gap-4 w-screen h-screen items-center justify-center">
      <div className="w-1/3 h-1/3">
        <BarChartBasic
          chartData={transformedData.chartData}
          title={transformedData.title}
          subtitle={transformedData.subtitle}
        />
      </div>
    </div>
  );
};

export default page;

