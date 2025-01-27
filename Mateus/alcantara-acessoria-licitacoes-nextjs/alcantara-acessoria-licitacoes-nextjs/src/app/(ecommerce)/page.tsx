"use client";

import { metaObject } from "@/config/site.config";
import PageHeader from "@/app/shared/page-header";
import Carousel from "@/app/shared/carousel";
import BidCategory from "@/app/(ecommerce)/biddings/bid-category";
import ProductsGrid from "@/app/shared/products-grid";
import Footer from "@/components/footer/footer";
import { useAppContext } from "../../context";

// export const metadata = {
//   ...metaObject("Alcântara Mendes"),
// };

const pageHeader = {
  title: "Licitações",
  breadcrumb: [
    {
      name: "Compras",
      href: "/",
    },
    {
      name: "Serviços",
      href: "/",
    },
    {
      name: "Outros",
      href: "/",
    },
  ],
};

export default function Home() {
  return (
    <div className="@container">
      <PageHeader title={pageHeader.title} breadcrumb={pageHeader.breadcrumb} />
      <Carousel />
      <BidCategory />
      <ProductsGrid />
      <Footer />
    </div>
  );
}
