import { routes } from "@/config/routes";
import { metaObject } from "@/config/site.config";
import { AppWrapper } from "@/context";
import PageHeader from "@/app/shared/page-header";
import SupportInbox from "@/app/shared/support/inbox";
import ImportButton from "@/app/shared/import-button";

export const metadata = {
  ...metaObject("Chat Licitação"),
};

const pageHeader = {
  title: "AlcantaAI",
  breadcrumb: [
    {
      href: "/",
      name: "Home",
    },
    {
      href: routes.support.dashboard,
      name: "Support",
    },
    {
      name: "Inbox",
    },
  ],
};

export default function SupportInboxPage() {
  return (
    <>
      <PageHeader title={pageHeader.title} breadcrumb={pageHeader.breadcrumb}>
        <div className="w-full @lg:w-auto flex gap-3">
          <ImportButton />
        </div>
      </PageHeader>
      <SupportInbox />
    </>
  );
}
