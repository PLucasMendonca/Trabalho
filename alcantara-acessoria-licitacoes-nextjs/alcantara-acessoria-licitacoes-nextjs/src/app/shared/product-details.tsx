"use client";

import { useParams } from "next/navigation";
import ProductDetailsSummery from "@/app/shared/product-details-summery";
import { filterExamplesData } from "@/data/filter-examples-data";
import { generateSlug } from "@/utils/generate-slug";

export default function ProductDetails() {
  const params = useParams();

  const product =
    filterExamplesData.find(
      (item) => generateSlug(item.unidadeOrgao.codigoUnidade) === params.slug
    ) ?? filterExamplesData[0];

  return (
    <div className="@container">
      <div className="@3xl:grid @3xl:grid-cols-12">
        <div className="col-span-10 @container">
          <ProductDetailsSummery product={product} />
        </div>
      </div>
    </div>
  );
}
