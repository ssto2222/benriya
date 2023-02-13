let nav = document.querySelector('#navArea');
let btn = document.querySelector(".toggle-btn");
let navbar = document.querySelector('.menu');

btn.onclick = () => {
    nav.classList.toggle('open');
}

navbar.onclick = () => {
    nav.classList.toggle('open');
}


