 // 프로필 이미지 미리보기 함수
 function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            // 미리보기 이미지 업데이트
            document.getElementById('profile-image-preview').src = e.target.result;
        };
        
        reader.readAsDataURL(input.files[0]); // input에서 선택된 파일을 읽어옵니다.
    }
}