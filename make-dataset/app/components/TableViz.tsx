import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const processData = (cellText: string) => {
  cellText = cellText.trim();
  // remove leading and trailing '' if present
  if (cellText.startsWith("'") && cellText.endsWith("'")) {
    return cellText.slice(1, -1);
  }
  if (cellText.startsWith("(") && cellText.endsWith(")")) {
    return cellText.slice(1, -1);
  }
  // if datetime.datetime, replace the datetime.datetime with ''
  cellText = cellText.replace("datetime.datetime", "");
  cellText = cellText.replace("datetime.date", "");
  cellText = cellText.replace("datetime.time", "");
  cellText = cellText.replace("datetime", "");

  return cellText;
};

export function TableViz({ data }: { data: Object[] }) {
  return (
    <Table className="w-full overflow-auto">
      {/* <TableCaption>A visualization of the query output.</TableCaption> */}
      <TableHeader>
        {data.map(
          (dataFrame, index) =>
            index === 0 && (
              <TableRow key={index} className="hover:cursor-help">
                {Object.entries(dataFrame).map(([key, value]) => (
                  <TableHead 
                    key={key + index} 
                    className="bg-slate-100 text-slate-950 font-semibold relative group"
                  >
                    {(processData(value) || '').slice(0, 12)}
                    <span className="absolute hidden group-hover:block bg-black text-white p-1 rounded text-xs -bottom-6 left-1/2 transform -translate-x-1/2">
                      {processData(value)}
                    </span>
                  </TableHead>
                ))}
              </TableRow>
            )
        )}
      </TableHeader>
      <TableBody>
        {data.map(
          (dataFrame, index) =>
            index !== 0 && (
              <TableRow key={index}>
                {Object.entries(dataFrame).map(([key, value]) => (
                  <TableCell key={key + index}>{processData(value)}</TableCell>
                ))}
              </TableRow>
            )
        )}
      </TableBody>
    </Table>
  );
}
