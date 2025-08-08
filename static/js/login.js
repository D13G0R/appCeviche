function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.querySelector('.eye-icon');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>`;
    } else {
        passwordInput.type = 'password';
        eyeIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>`;
    }
}

function closeMessage() {
    const message = document.querySelector('.message-container');
    if (message) {
        message.style.animation = 'messageSlide 0.3s ease-out reverse';
        setTimeout(() => message.remove(), 300);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input.id));
        input.addEventListener('input', () => {
            if (input.classList.contains('error')) {
                document.getElementById(`${input.id}-error`).classList.remove('show');
                input.classList.remove('error');
            }
        });
    });
    
    loginForm.addEventListener('submit', (e) => {
        let isValid = true;
        inputs.forEach(input => { if (!validateField(input.id)) isValid = false; });
        if (!isValid) e.preventDefault();
    });

    // Auto-cerrar mensaje después de 8 segundos
    setTimeout(closeMessage, 8000);
});

function validateField(fieldId) {
    const input = document.getElementById(fieldId);
    const value = input.value.trim();
    const errorDiv = document.getElementById(`${fieldId}-error`);
    
    if (value.length === 0) {
        input.classList.add('error');
        errorDiv.textContent = fieldId === 'username' ? 'El nombre de usuario es obligatorio' : 'La contraseña es obligatoria';
        errorDiv.classList.add('show');
        return false;
    }
    return true;
}