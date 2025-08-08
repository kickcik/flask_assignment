document.addEventListener("DOMContentLoaded", function() {
        const listItems = document.querySelectorAll("ul li");
        listItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add("slide-up");
            }, index * 200); // 0.2초 간격으로 순차 실행
        });
    });