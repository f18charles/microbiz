/* =========================
   HEADLINE WORD SWAP
========================= */
const swapWord = document.getElementById("swap-word");

if (swapWord) {
    const words = ["RIGHT", "SMART", "PROFITABLE", "PERFECT"];
    let wordIndex = 0;

    setInterval(() => {
        swapWord.style.opacity = 0;

        setTimeout(() => {
            wordIndex = (wordIndex + 1) % words.length;
            swapWord.textContent = words[wordIndex];
            swapWord.style.opacity = 1;
        }, 400);
    }, 2500);
}

/* =========================
   TYPING ANIMATION
========================= */
const typedText = document.getElementById("typed-text");

if (typedText) {
    const typingTexts = [
        "Check if your business fits your location",
        "Know how far your capital can take you",
        "Discover smarter business ideas for your area",
        "Make confident decisions before you invest"
    ];

    let textIndex = 0;
    let charIndex = 0;

    function typeEffect() {
        if (charIndex < typingTexts[textIndex].length) {
            typedText.textContent += typingTexts[textIndex].charAt(charIndex);
            charIndex++;
            setTimeout(typeEffect, 60);
        } else {
            setTimeout(eraseEffect, 1800);
        }
    }

    function eraseEffect() {
        if (charIndex > 0) {
            typedText.textContent = typingTexts[textIndex].substring(0, charIndex - 1);
            charIndex--;
            setTimeout(eraseEffect, 40);
        } else {
            textIndex = (textIndex + 1) % typingTexts.length;
            setTimeout(typeEffect, 500);
        }
    }

    typeEffect();
}

/* =========================
   FADE IN MESSAGE ON SCROLL
========================= */
const messageSection = document.querySelector(".message-section");

window.addEventListener("scroll", () => {
    const sectionTop = messageSection.getBoundingClientRect().top;
    const screenHeight = window.innerHeight;

    if (sectionTop < screenHeight - 100) {
        messageSection.classList.add("show");
    }
});
