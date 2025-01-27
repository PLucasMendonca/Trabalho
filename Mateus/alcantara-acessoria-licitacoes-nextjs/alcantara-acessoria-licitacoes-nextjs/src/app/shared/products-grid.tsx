'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Button } from 'rizzui';
import ListingCard from '@/components/cards/listing-card';
import hasSearchedParams from '@/utils/has-searched-params';
import { filterExamplesData, Licitacao } from '@/data/filter-examples-data';

const countPerPage = 6;

export default function ProductsGrid() {
  const [isLoading, setLoading] = useState(false);
  const [nextPage, setNextPage] = useState(countPerPage);

  const searchParams = useSearchParams();

  const getParamsName = (key: string | undefined) => {
    if (!key) return '';

    return searchParams.get(key);
  };

  function handleLoadMore() {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setNextPage(nextPage + countPerPage);
    }, 600);
  }

  const categoryFilter = (items: Licitacao[]): Licitacao[] => {
    const param = getParamsName('filter');

    return items.filter(
      (item) => item.CategoriaPrincipal?.toLowerCase() === param
    );
  };

  const filteredData = hasSearchedParams()
    ? categoryFilter(filterExamplesData)
    : filterExamplesData;

  return (
    <>
      <div className="grid grid-cols-1 gap-x-5 gap-y-6 @md:grid-cols-[repeat(auto-fill,minmax(250px,1fr))] @xl:gap-x-7 @xl:gap-y-9 @4xl:grid-cols-[repeat(auto-fill,minmax(300px,1fr))] @6xl:grid-cols-[repeat(auto-fill,minmax(364px,1fr))]">
        {filteredData
          ?.slice(0, nextPage)
          ?.map((item: Licitacao, index: number) => (
            <ListingCard key={`filterItem-${index}`} licitacao={item} />
          ))}
      </div>

      {nextPage < filteredData?.length && (
        <div className="mb-4 mt-5 flex flex-col items-center xs:pt-6 sm:pt-8">
          <Button isLoading={isLoading} onClick={() => handleLoadMore()}>
            Carregar mais
          </Button>
        </div>
      )}
    </>
  );
}
