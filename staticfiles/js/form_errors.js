window.addEventListener('DOMContentLoaded', () => {
    const errors = document.querySelectorAll('#form-error-container .toast-error');
    errors.forEach(err => {
        setTimeout(() => {
            err.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            err.style.opacity = 0;
            err.style.transform = "translateY(-20px)";
            setTimeout(() => err.remove(), 500);
        }, 3000);
    });
});