import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Work OS",
  description: "Transform Goals into Results with AI Agent Teams",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
