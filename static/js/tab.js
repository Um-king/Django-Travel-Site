document.addEventListener('DOMContentLoaded', function () {
      
    // 탭 클릭 이벤트를 처리하는 함수
    function openTab(event, tabName) {
      event.preventDefault(); // 링크의 기본 행동을 방지
      var i, tabcontent, tablinks;
  
      // 모든 탭 내용을 숨김
      tabcontent = document.getElementsByClassName("tab-content");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
  
      // 모든 탭 링크의 "활성" 클래스를 제거
      tablinks = document.getElementsByClassName("tab-link");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove('bg-white', 'text-black-700', 'border-b', 'border-blue-500', 'font-semibold');
        tablinks[i].classList.add('text-black-500', 'hover:bg-gray-100');
      }
  
      // 클릭된 탭의 내용을 보이게 하고, 클릭된 탭 링크에 "활성" 클래스를 추가
      document.getElementById(tabName).style.display = "block";
      event.currentTarget.classList.add('bg-white', 'text-black-700', 'border-b', 'border-blue-500', 'font-semibold');
      event.currentTarget.classList.remove('text-black-500', 'hover:bg-gray-100');
    }
  
    // 첫 번째 탭을 기본으로 열기
    const firstTabLink = document.querySelector('.tab-link');
    const firstTabContent = document.querySelector('.tab-content');
    if (firstTabLink && firstTabContent) {
      firstTabLink.classList.add('bg-white', 'text-black-700', 'border-b', 'border-blue-500');
      firstTabLink.classList.remove('text-black-500', 'hover:bg-gray-100');
      firstTabContent.style.display = 'block'; // 첫 번째 탭 컨텐츠를 보이게 설정
    }
  
    // 모든 탭 링크에 클릭 이벤트 리스너를 추가
    const tabs = document.querySelectorAll(".tab-link");
    tabs.forEach(tab => {
      tab.addEventListener('click', function(event) {
        openTab(event, this.dataset.target); // data-target 속성을 dataset을 통해 접근
      });
    });
  });
        