document.addEventListener('DOMContentLoaded', function () {
    let currentIndex = 0;
    const slides = document.querySelectorAll(".image-slide");
    const totalSlides = slides.length;

    // 처음 로딩시 첫 번째 이미지를 보여줍니다.
    slides[currentIndex].style.display = "block";

    // 다음 버튼 클릭 이벤트
    document.getElementById("nextBtn").addEventListener("click", function() {
      slides[currentIndex].style.display = "none"; // 현재 이미지를 숨깁니다.
      currentIndex = (currentIndex + 1) % totalSlides;
      slides[currentIndex].style.display = "block"; // 다음 이미지를 보여줍니다.
    });

    // 이전 버튼 클릭 이벤트
    document.getElementById("prevBtn").addEventListener("click", function() {
      slides[currentIndex].style.display = "none"; // 현재 이미지를 숨깁니다.
      currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      slides[currentIndex].style.display = "block"; // 이전 이미지를 보여줍니다.
    });

    // 자동 슬라이드 기능
    setInterval(function() {
      slides[currentIndex].style.display = "none"; // 현재 이미지를 숨깁니다.
      currentIndex = (currentIndex + 1) % totalSlides;
      slides[currentIndex].style.display = "block"; // 다음 이미지를 보여줍니다.
    }, 3000);  // 3초마다 이미지 전환
  });