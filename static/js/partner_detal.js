// Показуємо кнопку при прокручуванні
window.onscroll = function() {
    var btn = document.querySelector(".scroll-to-top-btn");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        btn.style.display = "block"; // Показуємо кнопку
    } else {
        btn.style.display = "none"; // Ховаємо кнопку
    }
};

// Прокручуємо до верху
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Плавна прокрутка
    });
}
