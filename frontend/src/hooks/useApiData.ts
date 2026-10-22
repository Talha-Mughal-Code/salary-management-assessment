"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { ApiError } from "@/lib/api";

const SLOW_AFTER_MS = 3000;

type Request<T> = {
  load: (signal: AbortSignal) => Promise<T>;
  attempt: number;
};
type Result<T> = { request: Request<T>; data?: T; error?: ApiError };

export function useApiData<T>(load: (signal: AbortSignal) => Promise<T>) {
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState<Result<T>>();
  const [slowRequest, setSlowRequest] = useState<Request<T>>();
  const request = useMemo(() => ({ load, attempt }), [load, attempt]);

  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(() => setSlowRequest(request), SLOW_AFTER_MS);
    request
      .load(controller.signal)
      .then(
        (data) => setResult({ request, data }),
        (error: unknown) => {
          if (controller.signal.aborted) return;
          setResult((previous) => ({
            request,
            data: previous?.data,
            error:
              error instanceof ApiError
                ? error
                : new ApiError("Something went wrong.", 0),
          }));
        },
      )
      .finally(() => clearTimeout(timer));
    return () => {
      controller.abort();
      clearTimeout(timer);
    };
  }, [request]);

  const loading = result?.request !== request;
  return {
    data: result?.data,
    error: loading ? undefined : result?.error,
    loading,
    slow: loading && slowRequest === request,
    reload: useCallback(() => setAttempt((count) => count + 1), []),
  };
}
