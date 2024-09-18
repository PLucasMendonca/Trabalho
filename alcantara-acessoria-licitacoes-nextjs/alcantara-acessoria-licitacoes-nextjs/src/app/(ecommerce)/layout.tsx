"use client";

import BerylLiumLayout from "@/layouts/beryllium/beryllium-layout";

type LayoutProps = {
  children: React.ReactNode;
};

export default function DefaultLayout({ children }: LayoutProps) {
  return <BerylLiumLayout>{children}</BerylLiumLayout>;
}
