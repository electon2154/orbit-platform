document.addEventListener('DOMContentLoaded', function() {
    // Get the registration form
    const form = document.querySelector('form');
    if (!form) return;
    console.log("form is found")
    // Add submit event listener
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log("form is submitted")
        // Validate form
        if (validateForm()) {
            console.log("form is valid befor submiting")
            // If validation passes, submit the form
            form.submit();
        }
    });

    // Form validation function
    function validateForm() {
        let isValid = true;
        const errors = [];

        // Validate username
        const username = form.querySelector('#id_username');
        if (!username.value.trim()) {
            errors.push('اسم المستخدم مطلوب');
            isValid = false;
        }

        // Validate email
        const email = form.querySelector('#id_email');
        if (!email.value.trim()) {
            errors.push('البريد الإلكتروني مطلوب');
            isValid = false;
        } else if (!isValidEmail(email.value)) {
            errors.push('البريد الإلكتروني غير صالح');
            isValid = false;
        }

        // Validate password
        const password1 = form.querySelector('#id_password1');
        const password2 = form.querySelector('#id_password2');
        if (!password1.value) {
            errors.push('كلمة المرور مطلوبة');
            isValid = false;
        } else if (password1.value.length < 8) {
            errors.push('يجب أن تكون كلمة المرور 8 أحرف على الأقل');
            isValid = false;
        }

        if (password1.value !== password2.value) {
            errors.push('كلمات المرور غير متطابقة');
            isValid = false;
        }

        // Validate company/customer specific fields
        const companyName = form.querySelector('#id_company_name') || form.querySelector('#id_store_name');
        if (companyName && !companyName.value.trim()) {
            errors.push('اسم الشركة/المتجر مطلوب');
            isValid = false;
        }

        const phone = form.querySelector('#id_phone_number');
        if (phone && !phone.value.trim()) {
            errors.push('رقم الهاتف مطلوب');
            isValid = false;
        }

        const city = form.querySelector('#id_city');
        if (city && !city.value.trim()) {
            errors.push('المدينة مطلوبة');
            isValid = false;
        }

        // Display errors if any
        if (errors.length > 0) {
            showErrors(errors);
        }

        return isValid;
    }

    // Email validation helper
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Error display function
    function showErrors(errors) {
        // Remove any existing error messages
        const existingErrors = document.querySelectorAll('.alert-danger');
        existingErrors.forEach(error => error.remove());

        // Create error container
        const errorContainer = document.createElement('div');
        errorContainer.className = 'alert alert-danger mt-3';
        errorContainer.setAttribute('role', 'alert');

        // Add errors to container
        const errorList = document.createElement('ul');
        errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });
        errorContainer.appendChild(errorList);

        // Insert error container before the form
        form.parentNode.insertBefore(errorContainer, form);
    }
}); 