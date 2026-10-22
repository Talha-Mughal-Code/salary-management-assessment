import type { Money } from "@/types/api";

export const formatMoney = (amount: Money | null, currency: string) =>
  amount === null
    ? "—"
    : new Intl.NumberFormat("en-US", {
        style: "currency",
        currency,
        maximumFractionDigits: 0,
      }).format(Number(amount));

export const USD = "USD";

export const formatUsd = (amount: Money | null) => formatMoney(amount, USD);

export const formatCompactUsd = (amount: Money) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: USD,
    notation: "compact",
  }).format(Number(amount));

export const formatCount = (value: number) =>
  new Intl.NumberFormat("en-US").format(value);

export const formatDate = (isoDate: string) =>
  new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeZone: "UTC",
  }).format(new Date(isoDate));
