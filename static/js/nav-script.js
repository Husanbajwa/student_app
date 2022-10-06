const menuBtn = document.querySelector(".menu-icon span");
const searchBtn = document.querySelector(".search-icon");
const cancelBtn = document.querySelector(".cancel-icon");
const menuitems = document.querySelector(".nav-items");
const form = document.querySelector("form");
const profileBtn = document.querySelector(".profile");
const dropUpBtn = document.querySelector(".dropupbtn");
const dropDownBtn = document.querySelector(".dropdownbtn");
const dropDownItem = document.querySelector(".dropdown");
const contenShift = document.querySelector(".content");
menuBtn.onclick = () => {
    menuitems.classList.add("active");
    menuBtn.classList.add("hide");
    searchBtn.classList.add("hide");
    cancelBtn.classList.add("show");
    cancelBtn.style.color = "#ff3d00";
}
cancelBtn.onclick = () => {
    menuitems.classList.remove("active");
    menuBtn.classList.remove("hide");
    searchBtn.classList.remove("hide");
    cancelBtn.classList.remove("show");
    form.classList.remove("active");
    dropDownItem.classList.remove("active");
    dropDownBtn.classList.remove("hide");
    dropUpBtn.classList.remove("show");
    contenShift.classList.remove("active");
}
searchBtn.onclick = () => {
    contenShift.classList.add("active");
    form.classList.add("active");
    searchBtn.classList.add("hide");
    cancelBtn.classList.add("show");
    dropDownItem.classList.remove("active");
    dropDownBtn.classList.remove("hide");
    dropUpBtn.classList.remove("show");
    
}
dropDownBtn.onclick = () => {
    dropDownItem.classList.add("active");
    dropDownBtn.classList.add("hide");
    dropUpBtn.classList.add("show");
    menuitems.classList.remove("active");
    cancelBtn.classList.remove("show");
    menuBtn.classList.remove("hide");
    searchBtn.classList.remove("hide");
    contenShift.classList.remove("active");
    form.classList.remove("active");
}
dropUpBtn.onclick =() => {
    dropDownItem.classList.remove("active");
    dropDownBtn.classList.remove("hide");
    dropUpBtn.classList.remove("show");
    menuBtn.classList.remove("hide");
    searchBtn.classList.remove("hide");
}