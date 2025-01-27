'use client';

import Link from 'next/link';
import SearchWidget from '@/components/search/search';
import HamburgerButton from '@/layouts/hamburger-button';
import Logo from '@/components/logo';
import { PiMagnifyingGlass } from 'react-icons/pi';
import cn from '@/utils/class-names';
import Sidebar from '@/layouts/beryllium/beryllium-sidebar-drawer';
import HeaderMenuRight from '@/layouts/header-menu-right';
import StickyHeader from '@/layouts/sticky-header';

export default function Header({ className }: { className?: string }) {
  return (
    <StickyHeader
      className={cn(
        'z-[990] justify-between bg-white dark:bg-gray-50/50  xl:pe-8',
        className
      )}
    >
      <div className="hidden items-center gap-3 xl:flex">
        <Link
          aria-label="Site Logo"
          href={'/'}
          className="shrink-2 me-4 hidden w-[275px] text-gray-800 hover:text-gray-900 lg:me-5 xl:block"
        >
          <Logo className="max-w-[275px]" />
        </Link>
      </div>

      <div className="flex w-full items-center justify-between gap-3 xl:w-[calc(100%_-_190px)] 2xl:w-[calc(100%_-_310px)] 3xl:gap-6">
        <div className="max-w-auto flex items-center xl:w-11/12">
          <HamburgerButton
            view={<Sidebar className="static w-full 2xl:w-full" />}
          />
          <Link
            aria-label="Site Logo"
            href="/"
            className="w-15 me-4 shrink-0 text-gray-800 hover:text-gray-900 lg:me-5 xl:hidden"
          >
            <Logo iconOnly={true} />
          </Link>
          <SearchWidget
            icon={<PiMagnifyingGlass className="me-3 h-[20px] w-[20px]" />}
            className="xl:w-full"
          />
        </div>

        <div className="xl:auto flex items-center">
          <HeaderMenuRight />
        </div>
      </div>
    </StickyHeader>
  );
}
