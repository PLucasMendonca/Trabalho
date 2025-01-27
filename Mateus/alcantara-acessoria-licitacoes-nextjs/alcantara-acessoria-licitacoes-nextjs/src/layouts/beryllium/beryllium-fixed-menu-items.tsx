import { routes } from "@/config/routes";
import { DUMMY_ID } from "@/config/constants";
import { IconType } from "react-icons/lib";
import {
  PiAirplaneTilt,
  PiBellSimpleRinging,
  PiBinoculars,
  PiBriefcase,
  PiBrowser,
  PiCalendarDuotone,
  PiCalendarPlus,
  PiCards,
  PiCaretCircleUpDown,
  PiChartBar,
  PiChartLineUp,
  PiChatCenteredDots,
  PiCreditCard,
  PiCurrencyCircleDollar,
  PiCurrencyDollar,
  PiEnvelopeSimpleOpen,
  PiFeather,
  PiFileImage,
  PiFolderLock,
  PiFolderDuotone,
  PiGridFour,
  PiHammer,
  PiHeadset,
  PiHourglassSimple,
  PiHouse,
  PiHouseLine,
  PiLightning,
  PiListNumbers,
  PiLockKey,
  PiMagicWand,
  PiMapPinLine,
  PiNoteBlank,
  PiNotePencil,
  PiPackage,
  PiPokerChip,
  PiRocketLaunch,
  PiShieldCheck,
  PiShieldCheckered,
  PiShootingStar,
  PiShoppingCart,
  PiSquaresFour,
  PiSteps,
  PiTable,
  PiUser,
  PiUserCircle,
  PiUserGear,
  PiUserPlus,
  PiShapes,
} from "react-icons/pi";
import { atom } from "jotai";

export interface SubMenuItemType {
  name: string;
  description?: string;
  href: string;
  badge?: string;
}

export interface ItemType {
  name: string;
  icon: IconType;
  href?: string;
  description?: string;
  badge?: string;
  subMenuItems?: SubMenuItemType[];
}

export interface MenuItemsType {
  id: string;
  name: string;
  title: string;
  icon: IconType;
  menuItems: ItemType[];
}

export const berylliumMenuItems: MenuItemsType[] = [
  {
    id: "1",
    name: "Home",
    title: "Licitações",
    icon: PiHouse,
    menuItems: [
      {
        name: "Compras",
        // href: routes.searchAndFilter.realEstate,
        icon: PiPackage,
        badge: "",
        subMenuItems: [
          {
            name: "Alimentos",
            href: "#",
          },
          {
            name: "Equipamentos",
            href: "#",
          },
          {
            name: "Equipamentos Médicos e Hospitalares",
            href: "#",
          },
          {
            name: "Material Didático e Educacional",
            href: "#",
          },
          {
            name: "Material de Construção",
            href: "#",
          },
          {
            name: "Material de Escritório",
            href: "#",
          },
          {
            name: "Material de Informática",
            href: "#",
          },
          {
            name: "Produtos de Limpeza e Higiene",
            href: "#",
          },
          {
            name: "Uniformes e EPIs",
            href: "#",
          },
          {
            name: "Veículos",
            href: "#",
          },
        ],
      },
      {
        name: "Serviços",
        // href: routes.searchAndFilter.realEstate,
        icon: PiBriefcase,
        badge: "",
        subMenuItems: [
          {
            name: "Consultoria e Assessorias",
            href: "#",
          },
          {
            name: "Educação e Capacitação",
            href: "#",
          },
          {
            name: "Gestão de Resíduos",
            href: "#",
          },
          {
            name: "Manutenção Predial e de Equipamentos",
            href: "#",
          },
          {
            name: "Obras de Engenharia",
            href: "#",
          },
          {
            name: "Projetos de Engenharia",
            href: "#",
          },
          {
            name: "Publicidade e Comunicação",
            href: "#",
          },
          {
            name: "Serviços de Limpeza",
            href: "#",
          },
          {
            name: "Serviços de Saúde",
            href: "#",
          },
          {
            name: "TI",
            href: "#",
          },
          {
            name: "Transporte e Logística",
            href: "#",
          },
        ],
      },
      {
        name: "Outros",
        // href: routes.searchAndFilter.realEstate,
        icon: PiCards,
        badge: "",
        subMenuItems: [
          {
            name: "Cessão de Espaço",
            href: "#",
          },
        ],
      },
    ],
  },
  {
    id: "2",
    name: "Chat",
    title: "Chat",
    icon: PiChatCenteredDots,
    menuItems: [
      {
        name: "Chat Licitação",
        href: "/chat",
        icon: PiChatCenteredDots,
        badge: "",
        subMenuItems: [
          {
            name: "Cessão de Espaço",
            href: "#",
          },
        ],
      },
    ],
  },
  {
    id: "3",
    name: "User",
    title: "Perfil",
    icon: PiUserCircle,
    menuItems: [],
  },
];
export const berylliumMenuItemAtom = atom(berylliumMenuItems[0]);
