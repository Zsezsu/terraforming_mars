import {dataHandler} from "./data/dataHandler.js";

const leagueImage = document.getElementById('slideshow-image');
let images;
let maxImageIndex;
let currentImageIndex = 0;

main();

async function main() {
    images = await dataHandler.getImages();
    maxImageIndex = images.length;
    changeImage();
    const previousButton = document.getElementById('slideshow-previous');
    const nextButton = document.getElementById('slideshow-next');
    previousButton.addEventListener('click', previousImage);
    nextButton.addEventListener('click', nextImage);
}

function changeImage() {
    leagueImage.src = images[currentImageIndex];
}

function nextImage() {
    currentImageIndex += 1;
    if (currentImageIndex >= maxImageIndex) {
        currentImageIndex = 0;
    }
    changeImage();
}

function previousImage() {
    currentImageIndex -= 1;
    if (currentImageIndex < 0) {
        currentImageIndex = maxImageIndex - 1;
    }
    changeImage();
}

