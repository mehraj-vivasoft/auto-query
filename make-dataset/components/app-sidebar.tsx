"use client";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { ChevronDown } from "lucide-react";
import { useTableDataContext } from "@/context/TablesContext";

export function AppSidebar() {
  const { documents, loading, error, selectedTable, setSelectedTable, selectedSchema, setSelectedSchema } =
    useTableDataContext();  

  return (
    <Sidebar>
      <SidebarHeader className="bg-slate-600 text-white">
        <SidebarMenu className="w-full">
          <SidebarMenuItem className="w-full">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton className="font-bold text-center text-xl w-full flex justify-between">
                  {documents.length > 0
                    ? documents[selectedSchema]?.schemaName
                    : "Select Schema"}
                  <ChevronDown className="ml-auto" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
                {loading && <DropdownMenuItem>Loading...</DropdownMenuItem>}
                {error && <DropdownMenuItem>{error}</DropdownMenuItem>}
                {documents.map((schema, index) => (
                  <DropdownMenuItem key={index}>
                    <span
                      className={`${
                        schema.tables.length < 1 && "text-red-600 text-xs"
                      } w-full cursor-pointer`}
                      onClick={() => {
                        setSelectedSchema(index);
                      }}
                    >
                      {schema.schemaName} ({schema.tables.length})
                    </span>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
          {/* <SidebarMenuItem className="text-xl font-bold tracking-wider w-full my-3 text-center bg-slate-200 py-1 rounded-md">
            {documents.length > 0 && documents[selectedSchema]?.schemaName}
          </SidebarMenuItem> */}
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent className="flex flex-col overflow-auto">
        <SidebarMenuItem className="flex flex-col gap-1.5 pt-3 overflow-auto">
          {documents.length > 0 && documents[selectedSchema].tables.length > 0 ? (
            documents[selectedSchema].tables.map((table, index) => (
              <div
                key={index}
                className={`cursor-pointer break-words my-0.5 mx-1.5 rounded-md px-3 py-1 tracking-wider text-md shadow-sm ${
                  selectedTable === table
                    ? "bg-slate-950 text-white"
                    : "text-slate-950"
                }`}
                onClick={() => setSelectedTable(table)}
              >
                {table}
              </div>
            ))
          ) : (
            <div className="text-xl p-4">NO TABLES FOUND</div>
          )}
        </SidebarMenuItem>
      </SidebarContent>
    </Sidebar>
  );
}
