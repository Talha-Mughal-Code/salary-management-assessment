import { CircleAlert, LoaderCircle } from "lucide-react";
import type { ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import type { ApiError } from "@/lib/api";

type RequestStateProps = {
  loading: boolean;
  slow: boolean;
  error?: ApiError;
  hasData: boolean;
  onRetry: () => void;
  children: ReactNode;
};

export function RequestState({
  loading,
  slow,
  error,
  hasData,
  onRetry,
  children,
}: RequestStateProps) {
  return (
    <div className="flex flex-col gap-3">
      {slow && (
        <p className="flex items-center gap-2 rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">
          <LoaderCircle className="animate-spin" />
          Waking up the server. The first request after a quiet period can take
          a few seconds.
        </p>
      )}
      {error && (
        <div className="flex items-center justify-between gap-3 rounded-lg border border-destructive/30 bg-destructive/5 px-3 py-2 text-sm text-destructive">
          <span className="flex items-center gap-2">
            <CircleAlert className="size-4" />
            {error.message}
          </span>
          <Button variant="outline" size="sm" onClick={onRetry}>
            Retry
          </Button>
        </div>
      )}
      {hasData ? (
        <div className={loading ? "opacity-60 transition-opacity" : undefined}>
          {children}
        </div>
      ) : (
        !error && <LoadingSkeleton />
      )}
    </div>
  );
}

export function LoadingSkeleton() {
  return (
    <div className="flex flex-col gap-2">
      {Array.from({ length: 8 }, (_, index) => (
        <Skeleton key={index} className="h-9 w-full" />
      ))}
    </div>
  );
}
