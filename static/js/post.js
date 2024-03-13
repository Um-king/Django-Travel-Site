document.addEventListener("DOMContentLoaded", function () {
  const sliderContainer = document.querySelector(".slider-container");
  const slideLeft = document.getElementById("slideLeft");
  const slideRight = document.getElementById("slideRight");

  let currentIndex = 0;
  const cards = sliderContainer.children;
  const cardStyle = getComputedStyle(cards[0]);
  const cardWidth = cards[0].offsetWidth;
  const cardMarginRight = parseInt(cardStyle.marginRight, 10);
  const moveAmount = cardWidth + cardMarginRight; // 카드 너비 + 오른쪽 마진
  const sliderVisibleWidth = sliderContainer.offsetWidth;
  const totalWidth = cards.length * moveAmount;
  const maxScrollWidth = totalWidth - sliderVisibleWidth;

  const main_sliderContainer = document.querySelector(".main-slider-container");
  const main_slideLeft = document.getElementById("main-slideLeft");
  const main_slideRight = document.getElementById("main-slideRight");

  let main_currentIndex = 0;
  const main_cards = main_sliderContainer.children;
  const main_cardStyle = getComputedStyle(main_cards[0]);
  const main_cardWidth = main_cards[0].offsetWidth;
  const main_cardMarginRight = parseInt(main_cardStyle.marginRight, 10);
  const main_moveAmount = main_cardWidth + main_cardMarginRight; // 카드 너비 + 오른쪽 마진
  const main_sliderVisibleWidth = main_sliderContainer.offsetWidth;
  const main_totalWidth = main_cards.length * main_moveAmount;
  const main_maxScrollWidth = main_totalWidth - main_sliderVisibleWidth;

  function updateButtons() {}
  function main_updateButtons() {}

  function moveSlider() {
    const movement = currentIndex * moveAmount;
    sliderContainer.style.transform = `translateX(-${movement}px)`;
    updateButtons();
  }

  slideRight.addEventListener("click", function () {
    if ((currentIndex + 1) * moveAmount < maxScrollWidth) {
      currentIndex++;
    } else {
      currentIndex = Math.ceil(maxScrollWidth / moveAmount);
    }
    moveSlider();
  });

  slideLeft.addEventListener("click", function () {
    if (currentIndex > 0) {
      currentIndex--;
      moveSlider();
    }
  });

  function main_moveSlider() {
    const movement = main_currentIndex * main_moveAmount;
    main_sliderContainer.style.transform = `translateX(-${movement}px)`;
    updateButtons();
  }

  main_slideRight.addEventListener("click", function () {
    if ((main_currentIndex + 1) * main_moveAmount < main_maxScrollWidth) {
      main_currentIndex++;
    } else {
      main_currentIndex = Math.ceil(main_maxScrollWidth / main_moveAmount);
    }
    main_moveSlider();
  });

  main_slideLeft.addEventListener("click", function () {
    if (main_currentIndex > 0) {
      main_currentIndex--;
      main_moveSlider();
    }
  });

  main_updateButtons(); // 초기 버튼 상태 업데이트
});

const slides = document.querySelectorAll("#slides > div");
let currentSlide = 0;

function nextSlide() {
  slides[currentSlide].classList.remove("opacity-100", "transition-opacity");
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add("opacity-100", "transition-opacity");
}

setInterval(nextSlide, 3000); // 3초마다 다음 슬라이드로 전환
