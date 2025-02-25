function changeImage(src) {
    document.getElementById('main-image').src = src;
}
document.addEventListener('DOMContentLoaded', function () {
const button = document.getElementById('btn-info-ev'); 
const modal = document.getElementById('modal1'); 
const overlay = document.querySelector('.modal__overlay');

button.addEventListener('click', function () {
    modal.style.display = 'flex';
    });

overlay.addEventListener('click', function () {
    modal.style.display = 'none';
    });
});
function toggleReview() {
let content = document.querySelector(".review-content");
let button = document.querySelector(".toggle-btn");

if (content.classList.contains("expanded")) {
    content.classList.remove("expanded");
    button.textContent = "Xem thêm bài viết";
} else {
    content.classList.add("expanded");
    button.textContent = "Ẩn bớt";
}
}