// اعتبارسنجی فرم‌ها
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form');
    if (registerForm && registerForm.action.includes('register')) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('رمز عبور و تکرار آن مطابقت ندارند');
            }
        });
    }
});