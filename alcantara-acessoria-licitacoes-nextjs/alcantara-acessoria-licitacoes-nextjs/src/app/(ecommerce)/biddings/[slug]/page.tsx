import { routes } from "@/config/routes";
import PageHeader from "@/app/shared/page-header";
import ProductDetails from "@/app/shared/product-details";
import { metaObject } from "@/config/site.config";
import { filterExamplesData } from "@/data/filter-examples-data";
import { generateSlug } from "@/utils/generate-slug";

export const metadata = {
  ...metaObject("Detalhes da licitação"),
};

export default function ProductDetailsPage({ params }: any) {
  const product =
    filterExamplesData.find(
      (item) => generateSlug(item.unidadeOrgao.codigoUnidade) === params.slug
    ) ?? filterExamplesData[0];

  const pageHeader = {
    title: "Licitações",
    breadcrumb: [
      {
        href: "/",
        name: "Compras",
      },
      {
        href: "/",
        name: "Serviços",
      },
      {
        name: product.unidadeOrgao?.nomeUnidade,
      },
    ],
  };
  return (
    <>
      <PageHeader title={pageHeader.title} breadcrumb={pageHeader.breadcrumb} />
      <ProductDetails />
    </>
  );
}
