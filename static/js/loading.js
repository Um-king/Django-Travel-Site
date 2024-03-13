// static/js/app.js 파일에 추가
function handleLogin() {
    // 로더와 오버레이를 표시
    document.getElementById('loaderOverlay').classList.remove('hidden');
  
    // 2초 후에 로더와 오버레이를 숨기고, 로그인 처리를 합니다
    setTimeout(function() {
      document.getElementById('loaderOverlay').classList.add('hidden');
      // 로그인 로직 실행, 예를 들어 form 제출 또는 페이지 리다이렉트
      // 예: document.getElementById('loginForm').submit();
      // 또는 window.location.href = '/after-login-url';
    }, 20000);
  }