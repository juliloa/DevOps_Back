    document.getElementById('resetPasswordForm').addEventListener('submit', function(event) {
        const pwd1 = document.getElementById('new_password1').value;
        const pwd2 = document.getElementById('new_password2').value;

        // Expresión regular para validar contraseña segura:
        // al menos 8 caracteres, una mayúscula, un número y un signo especial
        const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

        if (pwd1 !== pwd2) {
            event.preventDefault();
            alert('Las contraseñas no coinciden.');
            return;
        }

        if (!regex.test(pwd1)) {
            event.preventDefault();
            alert('La contraseña debe tener mínimo 8 caracteres, al menos una letra mayúscula, un número y un carácter especial.');
            return;
        }
    });