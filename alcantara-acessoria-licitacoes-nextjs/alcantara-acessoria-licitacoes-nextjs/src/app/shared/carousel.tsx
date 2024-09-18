"use client";

import { useState } from "react";
import { BsChevronCompactLeft, BsChevronCompactRight } from "react-icons/bs";
import { RxDotFilled } from "react-icons/rx";

const Carousel = () => {
  const slides = [
    {
      url: "https://t3.ftcdn.net/jpg/06/23/78/88/360_F_623788874_AkPJl27fwKD8DGW4Eg6R2JSZ5eFIUYl6.jpg",
    },
    {
      url: "https://t4.ftcdn.net/jpg/01/53/76/51/360_F_153765115_EIIUcaDnt9ZSrcx4XDdsCOhBgGNtRDVW.jpg",
    },
    {
      url: "https://t4.ftcdn.net/jpg/02/56/17/43/360_F_256174312_XpCm7TxSRMP78LoAKZdPz3FFTVR4a85y.jpg",
    },
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  const previousSlide = () => {
    const isFirstSlide = currentIndex === 0;
    const newIndex = isFirstSlide ? slides.length - 1 : currentIndex - 1;

    setCurrentIndex(newIndex);
  };

  const nextSlide = () => {
    const isLastSlide = currentIndex === slides.length - 1;
    const newIndex = isLastSlide ? 0 : currentIndex + 1;

    setCurrentIndex(newIndex);
  };

  const goToSlide = (slideIndex: number) => setCurrentIndex(slideIndex);

  return (
    <div className="group relative m-auto h-[640px] w-full max-w-full pb-16">
      <div
        style={{ backgroundImage: `url(${slides[currentIndex].url})` }}
        className="h-full w-full rounded-2xl bg-cover duration-500"
      />
      <div className="absolute left-5 top-[50%] hidden -translate-x-0 translate-y-[-50%] cursor-pointer rounded-full bg-black/20 p-2 text-2xl text-white group-hover:block">
        <BsChevronCompactLeft onClick={previousSlide} size={30} />
      </div>
      <div className="absolute right-5 top-[50%] hidden -translate-x-0 translate-y-[-50%] cursor-pointer rounded-full bg-black/20 p-2 text-2xl text-white group-hover:block">
        <BsChevronCompactRight onClick={nextSlide} size={30} />
      </div>
      <div className="top-4 flex justify-center py-2">
        {slides.map((_slide, slideIndex) => (
          <div
            key={slideIndex}
            onClick={() => goToSlide(slideIndex)}
            className="cursor-pointer text-2xl"
          >
            <RxDotFilled />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Carousel;
