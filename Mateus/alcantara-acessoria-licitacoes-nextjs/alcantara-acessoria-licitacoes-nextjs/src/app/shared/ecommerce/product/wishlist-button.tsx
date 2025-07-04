'use client';

import { useState } from 'react';
import { Button } from 'rizzui';
import cn from '@/utils/class-names';

export default function WishlistButton({ className }: { className?: string }) {
  const [favorite, setFavorite] = useState<boolean>(false);
  const [addToWishlistLoader, setAddToWishlistLoader] =
    useState<boolean>(false);

  function addToWishlist() {
    setAddToWishlistLoader(true);
    setFavorite(!favorite);
    setTimeout(() => {
      setAddToWishlistLoader(false);
    }, 1500);
  }
  return (
    <Button
      variant="outline"
      size="xl"
      onClick={addToWishlist}
      // isLoading={addToWishlistLoader}
      className={cn('h-12 text-sm lg:h-14 lg:text-base', className)}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 32 32"
        className="me-1 h-6 w-6 lg:h-8 lg:w-8"
      >
        <path
          fill={favorite === true ? '#e00' : 'currentColor'}
          fillOpacity={favorite === true ? 1 : 0}
          d="M26.492 10.7a6.065 6.065 0 0 0-1.383-1.931 6.457 6.457 0 0 0-2.042-1.295A6.686 6.686 0 0 0 20.577 7a6.697 6.697 0 0 0-3.383.91 6.345 6.345 0 0 0-.693.469 6.345 6.345 0 0 0-.693-.47A6.697 6.697 0 0 0 12.425 7c-.863 0-1.7.159-2.49.474a6.442 6.442 0 0 0-2.041 1.294A6.028 6.028 0 0 0 6.51 10.7 5.776 5.776 0 0 0 6 13.078c0 .777.165 1.586.493 2.41a10.65 10.65 0 0 0 1.172 2.123c.797 1.14 1.894 2.33 3.255 3.537 2.256 2 4.49 3.38 4.585 3.437l.576.354a.809.809 0 0 0 .838 0l.576-.354a36.744 36.744 0 0 0 4.585-3.437c1.361-1.206 2.458-2.396 3.255-3.537.503-.721.9-1.435 1.171-2.123.329-.824.494-1.633.494-2.41a5.736 5.736 0 0 0-.508-2.378Z"
        />
        <path
          fill={favorite === true ? '#e00' : 'currentColor'}
          fillOpacity={favorite === true ? 1 : 0}
          stroke={favorite === true ? '#e00' : 'currentColor'}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M11.25 7C8.35 7 6 9.244 6 12.012c0 2.234.919 7.538 9.962 12.9a1.063 1.063 0 0 0 1.076 0C26.08 19.55 27 14.246 27 12.011 27 9.244 24.649 7 21.75 7c-2.9 0-5.25 3.037-5.25 3.037S14.149 7 11.25 7Z"
        />
      </svg>
      Lista de Desejos
    </Button>
  );
}
