import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import BerylliumLayout from "@/layouts/beryllium/beryllium-layout";
import { inter, lexendDeca } from "@/app/fonts";
import GlobalDrawer from "@/app/shared/drawer-views/container";
import GlobalModal from "@/app/shared/modal-views/container";
import { cn } from "@/utils/class-names";
import "@/app/globals.css";
import { AppWrapper } from "@/context";

export const metadata: Metadata = {
  title: "Alcântara Mendes - Consultoria e Assessoria",
  description: `Seu Parceiro Completo para Sucesso em Licitações Públicas`,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      // 💡 Prevent next-themes hydration warning
      suppressHydrationWarning
    >
      <body
        // 💡 Prevent hydration warnings caused by third-party extensions, such as Grammarly.
        suppressHydrationWarning
        className={cn(inter.variable, lexendDeca.variable, "font-inter")}
      >
        <ThemeProvider>
          <AppWrapper>
            {children}
            <GlobalDrawer />
            <GlobalModal />
          </AppWrapper>
        </ThemeProvider>
      </body>
    </html>
  );
}
