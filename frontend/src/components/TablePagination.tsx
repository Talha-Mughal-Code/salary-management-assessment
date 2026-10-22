"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { type ChangeEvent, useCallback } from "react";

import { Button } from "@/components/ui/button";
import {
  NativeSelect,
  NativeSelectOption,
} from "@/components/ui/native-select";
import { PAGE_SIZES, type QueryChanges } from "@/hooks/useEmployeeQuery";
import { formatCount } from "@/lib/format";

type TablePaginationProps = {
  page: number;
  pageSize: number;
  total: number;
  onChange: (changes: QueryChanges) => void;
};

export function TablePagination({
  page,
  pageSize,
  total,
  onChange,
}: TablePaginationProps) {
  const pages = Math.max(1, Math.ceil(total / pageSize));
  const handlePageSize = useCallback(
    (event: ChangeEvent<HTMLSelectElement>) =>
      onChange({ page_size: event.target.value }),
    [onChange],
  );

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-muted-foreground">
      <span>
        {formatCount((page - 1) * pageSize + 1)}–
        {formatCount(Math.min(page * pageSize, total))} of {formatCount(total)}
      </span>
      <div className="flex items-center gap-2">
        <NativeSelect
          size="sm"
          aria-label="Rows per page"
          value={pageSize}
          onChange={handlePageSize}
        >
          {PAGE_SIZES.map((size) => (
            <NativeSelectOption key={size} value={size}>
              {size} per page
            </NativeSelectOption>
          ))}
        </NativeSelect>
        <Button
          variant="outline"
          size="icon-sm"
          aria-label="Previous page"
          disabled={page <= 1}
          onClick={() => onChange({ page: page - 1 })}
        >
          <ChevronLeft />
        </Button>
        <span className="tabular-nums">
          Page {formatCount(page)} of {formatCount(pages)}
        </span>
        <Button
          variant="outline"
          size="icon-sm"
          aria-label="Next page"
          disabled={page >= pages}
          onClick={() => onChange({ page: page + 1 })}
        >
          <ChevronRight />
        </Button>
      </div>
    </div>
  );
}
