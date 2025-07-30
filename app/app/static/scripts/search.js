import {createModal} from "./utils.js";

const navbarSearchID = "#navbar-search";
const navbarSearch = document.querySelector(navbarSearchID);

navbarSearch.addEventListener('click', async function () {
    console.log("click")
    await createModal({
        modalId: 'modalId-1',
        callback: async (confirmed) => confirmed
    });
});