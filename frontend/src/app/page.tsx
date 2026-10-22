import { Suspense } from "react";

import { EmployeeDirectory } from "@/components/EmployeeDirectory";
import { LoadingSkeleton } from "@/components/RequestState";

export default function EmployeesPage() {
  return (
    <>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Employees</h1>
        <p className="text-sm text-muted-foreground">
          Search, filter and edit salaries for every employee.
        </p>
      </div>
      <Suspense fallback={<LoadingSkeleton />}>
        <EmployeeDirectory />
      </Suspense>
    </>
  );
}
