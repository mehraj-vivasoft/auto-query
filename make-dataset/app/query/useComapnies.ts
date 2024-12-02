import { NEXT_PUBLIC_AI_BACKEND } from "@/lib/consts";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

type Company = {
  id: string;
  name: string;
};

function useCompanies() {
  const [CompanyIsLoading, setCompanyIsLoading] = useState(false);
  const [companies, setCompanies] = useState<Company[]>([]);

  const fetchCompanies = async () => {
    setCompanyIsLoading(true);
    try {
      const response = await fetch(`${NEXT_PUBLIC_AI_BACKEND}/companies`);
      const data = await response.json();
      console.log(data);
      setCompanies(data);
      setCompanyIsLoading(false);
    } catch (error) {
      console.error("Error fetching companies:", error);
      toast.error("Error fetching companies");
      setCompanyIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  return { companies, CompanyIsLoading };
}

export default useCompanies;
