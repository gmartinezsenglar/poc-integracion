import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Roomies PoC · Laboratorio de integración",
  description: "PoC Vercel + Render + Supabase, independiente de producción.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body>{children}</body></html>;
}
