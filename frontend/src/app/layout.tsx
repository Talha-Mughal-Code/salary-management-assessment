import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ACME Salaries",
  description: "Manage and understand salaries across ACME's countries.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <header className="border-b">
          <nav className="mx-auto flex w-full max-w-7xl items-center gap-6 px-4 py-3 text-sm">
            <span className="font-semibold">ACME Salaries</span>
            <Link
              href="/"
              className="text-muted-foreground hover:text-foreground"
            >
              Employees
            </Link>
            <Link
              href="/insights"
              className="text-muted-foreground hover:text-foreground"
            >
              Insights
            </Link>
          </nav>
        </header>
        <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-4 px-4 py-6">
          {children}
        </main>
      </body>
    </html>
  );
}
