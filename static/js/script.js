const ratingItemsList = document.querySelectorAll('.rating__item');
const ratingItemArray = Array.prototype.slice.call(ratingItemsList);

ratingItemArray.forEach(item =>
    item.addEventListener('click', () => {
        const { itemValue } = item.dataset;
        item.parentNode.dataset.totalValue = itemValue;
    })
);
