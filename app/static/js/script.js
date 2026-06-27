function toggleSideMenu() {
    var links = document.getElementById("side-links");
    if (!links) return;  // safety check
    if (links.style.display === "flex") {
        links.style.display = "none";
    } else {
        links.style.display = "flex";
    }
}
