import { TableViz } from "./TableViz";

interface SQLResultTableProps {
  resultString: string;
}

const SQLResultTable: React.FC<SQLResultTableProps> = ({ resultString }) => {
  if (!resultString || resultString.trim() === '') {
    return null;
  }

  try {
    // Function to split row content preserving nested parentheses
    const splitPreservingParentheses = (str: string) => {
      const result = [];
      let current = '';
      let depth = 0;

      for (let i = 0; i < str.length; i++) {
        const char = str[i];
        if (char === '(') {
          depth++;
          current += char;
        } else if (char === ')') {
          depth--;
          current += char;
        } else if (char === ',' && depth === 0) {
          result.push(current.trim());
          current = '';
        } else {
          current += char;
        }
      }
      if (current.trim()) {
        result.push(current.trim());
      }
      return result;
    };

    // Function to extract content between balanced parentheses
    const extractRows = (str: string) => {
      const rows = [];
      let depth = 0;
      let start = -1;
      let current = '';

      for (let i = 0; i < str.length; i++) {
        if (str[i] === '(') {
          depth++;
          if (depth === 1) {
            start = i;
          }
        } else if (str[i] === ')') {
          depth--;
          if (depth === 0 && start !== -1) {
            current = str.slice(start + 1, i);
            if (current.trim()) {
              rows.push(splitPreservingParentheses(current));
            }
            start = -1;
          }
        }
      }
      return rows;
    };

    const rows = extractRows(resultString);
    if (rows.length === 0) return null;

    // Get columns from first row
    const columns = rows[0].map((_, index) => `${index + 1}`);
    
    return (
      <div className="w-full overflow-scroll mt-2">
        <TableViz data={rows} />
        {/* <table className="min-w-full bg-white">
          <thead>
            <tr className="bg-[#071e35]">
              {columns.map((column, index) => (
                <th key={index} className="px-4 py-2 text-left text-[#DBE2EF] font-semibold">
                  {column}
                </th>
              ))}
            </tr>
          </thead>          
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex} className="border-b border-gray-200 hover:bg-gray-50">
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} className="px-4 py-2 text-gray-800">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table> */}
      </div>
    );
  } catch (error) {
    console.error('Error parsing SQL result:', error);
    return null;
  }
};

export default SQLResultTable;