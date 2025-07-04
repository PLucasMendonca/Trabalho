"use client";

import {
  PiCheckCircle,
  PiTrashSimple,
  PiWarningCircle,
  PiProhibitInset,
  PiDotsThreeBold,
} from "react-icons/pi";
import {
  BsFileEarmarkWord,
  BsFileEarmarkPdf,
  BsFiletypeJson,
} from "react-icons/bs";
import { ActionIcon, Dropdown } from "rizzui";

const actions = [
  {
    id: 1,
    icon: <BsFileEarmarkPdf className="h-4 w-4" />,
    name: ".pdf",
  },
  {
    id: 2,
    icon: <BsFileEarmarkWord className="h-4 w-4" />,
    name: ".docx",
  },
  {
    id: 3,
    icon: <BsFiletypeJson className="h-4 w-4" />,
    name: ".json",
  },
  {
    id: 4,
    icon: <PiWarningCircle className="h-4 w-4" />,
    name: "Mark as spam",
  }
];

export default function ActionDropdown({ className }: { className?: string }) {
  return (
    <Dropdown className={className}>
      <Dropdown.Trigger>
        <ActionIcon
          rounded="full"
          variant="outline"
          className="h-auto w-auto p-1"
        >
          <PiDotsThreeBold className="h-auto w-6" />
        </ActionIcon>
      </Dropdown.Trigger>
      <Dropdown.Menu className="!z-0">
        {actions.map((action) => (
          <Dropdown.Item key={action.id} className="gap-2 text-xs sm:text-sm">
            <>
              {action.icon}
              {action.name}
            </>
          </Dropdown.Item>
        ))}
      </Dropdown.Menu>
    </Dropdown>
  );
}
