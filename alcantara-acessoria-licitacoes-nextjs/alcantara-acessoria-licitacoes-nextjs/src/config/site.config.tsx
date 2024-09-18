import { Metadata } from "next";
import { LAYOUT_OPTIONS } from "@/config/enums";
import { OpenGraph } from "next/dist/lib/metadata/types/opengraph-types";
import logoImg from "../../public/am-logo.png";
import logoIconImg from "../../public/am-icon.png";

enum MODE {
  DARK = "dark",
  LIGHT = "light",
}

export const siteConfig = {
  title: "Alcântara Mendes - Consultoria e Assessoria",
  description: `Seu Parceiro Completo para Sucesso em Licitações Públicas`,
  logo: logoImg,
  icon: logoIconImg,
  mode: MODE.LIGHT,
  layout: LAYOUT_OPTIONS.BERYLLIUM,
  // TODO: favicon
};

export const metaObject = (
  title?: string,
  openGraph?: OpenGraph,
  description: string = siteConfig.description
): Metadata => {
  return {
    title: title ? `${title}` : siteConfig.title,
    description,
    openGraph: openGraph ?? {
      title: title ? `${title}` : title,
      description,
      url: "https://isomorphic-furyroad.vercel.app",
      siteName: "Alcântara Mendes", // https://developers.google.com/search/docs/appearance/site-names
      images: {
        url: "https://s3.amazonaws.com/redqteam.com/isomorphic-furyroad/itemdep/isobanner.png",
        width: 1200,
        height: 630,
      },
      locale: "pt_BR",
      type: "website",
    },
  };
};
