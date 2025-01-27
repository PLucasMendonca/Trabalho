"use client";

import { useState } from "react";
import toast from "react-hot-toast";
import Image from "next/image";
import { PiShoppingCartSimple } from "react-icons/pi";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { Licitacao } from "@/data/filter-examples-data";
// import { Product } from '@/types';
import { Button, Title, Text } from "rizzui";
import { toCurrency } from "@/utils/to-currency";
import WishlistButton from "@/app/shared/ecommerce/product/wishlist-button";
import {
  ProductDetailsInput,
  productDetailsSchema,
} from "@/utils/validators/product-details.schema";
import { generateCartProduct } from "@/store/generate-cart-product";

function cnpjFormatter(cnpj: string) {
  return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
}

export default function ProductDetailsSummery({
  product,
}: {
  product: Licitacao;
}) {
  // const { addItemToCart } = useCart();
  const [isLoading, setLoading] = useState(false);

  const methods = useForm<ProductDetailsInput>({
    mode: "onChange",
    // defaultValues: defaultValues(order),
    resolver: zodResolver(productDetailsSchema),
  });

  const onSubmit: SubmitHandler<ProductDetailsInput> = (data: any) => {
    const item = generateCartProduct({
      ...product,
    });

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      console.log("createOrder data ->", data);
      toast.success(<Text as="b">Product added to the cart</Text>);
    }, 600);
  };

  return (
    <>
      <div className="flex border-b border-muted pb-6 @lg:pb-8">
        <div className="mb-6 flex-none pr-12">
          <Image
            src={product?.thumbnail.src}
            alt="Brazão da União"
            width={436}
            height={360}
            priority
          />
        </div>
        <div>
          <div className="mb-6 flex-auto">
            <Title as="h2" className="mb-2.5 font-bold @6xl:text-4xl">
              {product?.unidadeOrgao.nomeUnidade}
            </Title>
            <Text as="i">
              {product?.unidadeOrgao.municipioNome} -{" "}
              {product?.unidadeOrgao.ufSigla}
            </Text>
          </div>
          <div className="space-y-2.5">
            <div className="space-y-0.5">
              <Text as="strong" className="text-sm">
                Razão Social:
              </Text>
              <Text as="p" className="text-base">
                {`${product?.orgaoEntidade?.razaoSocial}.`}
              </Text>
            </div>
            <div>
              <Text as="strong" className="text-sm">
                CNPJ:
              </Text>
              <Text as="p" className="text-base">{`${
                product?.orgaoEntidade?.cnpj
                  ? cnpjFormatter(product?.orgaoEntidade?.cnpj)
                  : "CNPJ inválido!"
              }.`}</Text>
            </div>
            <div>
              <Text as="strong" className="text-sm">
                Descrição:
              </Text>
              <Text as="p" className="text-base">
                {`${product?.objetoCompra}.`}
              </Text>
            </div>
          </div>
        </div>
      </div>

      <FormProvider {...methods}>
        <form className="pb-8 pt-5" onSubmit={methods.handleSubmit(onSubmit)}>
          <div className="mb-1.5 mt-2 flex items-end font-lexend text-base">
            <div className="-mb-0.5 text-2xl font-semibold text-gray-900 lg:text-3xl">
              <Text as="p" className="text-sm">
                Valor Total:
              </Text>
              {toCurrency(product?.valorTotalEstimado as number)}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 pt-7 @md:grid-cols-2 @xl:gap-6">
            <Button
              size="xl"
              type="submit"
              isLoading={isLoading}
              className="h-12 text-sm lg:h-14 lg:text-base"
            >
              <PiShoppingCartSimple className="me-2 h-5 w-5 lg:h-[22px] lg:w-[22px]" />{" "}
              Adicionar ao Carrinho
            </Button>
            <WishlistButton />
          </div>
        </form>
      </FormProvider>
    </>
  );
}
