function addReview(name, id) {
    document.getElementById("contactparent").value = id;
    document.getElementById("text").innerText = name + ', ';
}

function changeViewOfSpoiler(id) {
    elem = document.querySelector("#review_" + id);
    button = document.querySelector("#review_button_" + id);
    if (elem.classList.contains('anime_review__item__spoiler')) {
        elem.classList.remove('anime_review__item__spoiler');
        elem.classList.add('anime_review__item__unspoiler');
        button.innerHTML = "Скрыть текст";
    }
    else {
        elem.classList.add('anime_review__item__spoiler');
        elem.classList.remove('anime_review__item__unspoiler');
        button.innerHTML = "Показать текст";
    }
}
