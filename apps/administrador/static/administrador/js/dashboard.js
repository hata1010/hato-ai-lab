(function () {
    const STORAGE_KEY = "hato_theme";
    const themes = ["rocio", "lavanda", "alborada", "noche"];
    const body = document.body;

    function applyTheme(theme) {
        const selected = themes.includes(theme) ? theme : "noche";
        body.dataset.theme = selected;
        try {
            localStorage.setItem(STORAGE_KEY, selected);
        } catch (error) {
            // Si el navegador bloquea almacenamiento, el tema sigue funcionando durante la sesión.
        }
        document.querySelectorAll("[data-theme-choice]").forEach(button => {
            button.classList.toggle("is-active", button.dataset.themeChoice === selected);
        });
    }

    let savedTheme = "noche";
    try {
        savedTheme = localStorage.getItem(STORAGE_KEY) || "noche";
    } catch (error) {
        // Mantener tema por defecto.
    }

    applyTheme(savedTheme);

    document.querySelectorAll("[data-theme-choice]").forEach(button => {
        button.addEventListener("click", () => applyTheme(button.dataset.themeChoice));
    });
})();
