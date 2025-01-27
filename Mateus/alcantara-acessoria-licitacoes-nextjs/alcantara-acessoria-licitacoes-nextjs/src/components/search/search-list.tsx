"use client";

import { Fragment, useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  ActionIcon,
  Empty,
  SearchNotFoundIcon,
  Button,
  Title,
  Input,
  cn,
} from "rizzui";
import {
  PiFileTextDuotone,
  PiMagnifyingGlassBold,
  PiXBold,
} from "react-icons/pi";
import { pageLinks } from "@/components/search/page-links.data";
import { filterExamplesData } from "@/data/filter-examples-data";

const countPerPage = 5;

export default function SearchList({ onClose }: { onClose?: () => void }) {
  const inputRef = useRef(null);
  const [searchText, setSearchText] = useState("");
  const [isLoading, setLoading] = useState(false);
  const [nextPage, setNextPage] = useState(countPerPage);

  let menuItemsFiltered = filterExamplesData;
  if (searchText.length > 0) {
    menuItemsFiltered = filterExamplesData.filter((item: any) => {
      const label = item.unidadeOrgao.nomeUnidade;
      return (
        label.match(searchText.toLowerCase()) ||
        (label.toLowerCase().match(searchText.toLowerCase()) && label)
      );
    });
  }

  function handleLoadMore() {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setNextPage(nextPage + countPerPage);
    }, 600);
  }

  useEffect(() => {
    if (inputRef?.current) {
      // @ts-ignore
      inputRef.current.focus();
    }
    return () => {
      inputRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <div className="flex items-center px-5 py-4">
        <Input
          variant="flat"
          value={searchText}
          ref={inputRef}
          onChange={(e) => setSearchText(() => e.target.value)}
          placeholder="Procure aqui..."
          className="flex-1"
          prefix={
            <PiMagnifyingGlassBold className="h-[18px] w-[18px] text-gray-600" />
          }
          suffix={
            searchText && (
              <Button
                size="sm"
                variant="text"
                className="h-auto w-auto px-0"
                onClick={(e) => {
                  e.preventDefault();
                  setSearchText(() => "");
                }}
              >
                Limpar
              </Button>
            )
          }
        />
        <ActionIcon
          variant="text"
          size="sm"
          className="ms-3 text-gray-500 hover:text-gray-700"
          onClick={onClose}
        >
          <PiXBold className="h-5 w-5" />
        </ActionIcon>
      </div>

      <div className="custom-scrollbar max-h-[60vh] overflow-y-auto border-t border-gray-300 px-2 py-4">
        <>
          {menuItemsFiltered.length === 0 ? (
            <Empty
              className="scale-75"
              image={<SearchNotFoundIcon />}
              text="No Result Found"
              textClassName="text-xl"
            />
          ) : null}
        </>

        {menuItemsFiltered.slice(0, nextPage).map((item, index) => {
          return (
            <Fragment key={`${item.unidadeOrgao.nomeUnidade}-${index}`}>
              {item?.unidadeOrgao ? (
                <Link
                  href={`/biddings/${item.unidadeOrgao.codigoUnidade}`}
                  className="relative my-0.5 flex items-center rounded-lg px-3 py-2 text-sm hover:bg-gray-100 focus:outline-none focus-visible:bg-gray-100 dark:hover:bg-gray-50/50 dark:hover:backdrop-blur-lg"
                >
                  <span className="inline-flex items-center justify-center rounded-md border border-gray-300 p-2 text-gray-500">
                    <PiFileTextDuotone className="h-5 w-5" />
                  </span>

                  <span className="ms-3 grid gap-0.5">
                    <span className="font-medium capitalize text-gray-900 dark:text-gray-700">
                      {item.unidadeOrgao.nomeUnidade}
                    </span>
                    <span className="text-gray-500">
                      {item.CategoriaPrincipal}
                    </span>
                  </span>
                </Link>
              ) : (
                <Title
                  as="h6"
                  className={cn(
                    "mb-1 px-3 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-500",
                    index !== 0 && "mt-6 4xl:mt-7"
                  )}
                >
                  {item.unidadeOrgao.nomeUnidade}
                </Title>
              )}
            </Fragment>
          );
        })}

        {menuItemsFiltered.length > 5 && (
          <div className="flex flex-col items-center xs:pt-2 sm:pt-2">
            <Button isLoading={isLoading} onClick={() => handleLoadMore()}>
              Carregar mais
            </Button>
          </div>
        )}
      </div>
    </>
  );
}
