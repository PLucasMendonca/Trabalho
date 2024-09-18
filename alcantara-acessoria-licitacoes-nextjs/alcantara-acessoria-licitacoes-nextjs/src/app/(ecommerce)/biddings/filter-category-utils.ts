import React from "react";
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

export type InitialStateType = {
  filter: string;
};

export const initialState: InitialStateType = {
  filter: "",
};

// Options
export const filterOptions = [
  {
    id: 2,
    name: "Compras",
    value: "compras",
    icon: PiPackage,
  },
  {
    id: 3,
    name: "Serviços",
    value: "serviços",
    icon: PiBriefcase,
  },
  {
    id: 4,
    name: "Outros",
    value: "outros",
    icon: PiCards,
  },
];
