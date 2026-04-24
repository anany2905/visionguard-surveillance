// ===================================
// CONTACT PAGE JAVASCRIPT
// ===================================

// ===== CONTACT FORM HANDLER =====
function handleContactForm(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    const formMessage = document.getElementById('formMessage');
    
    // Validation
    if (!name || !email || !subject || !message) {
        formMessage.textContent = 'Please fill in all required fields';
        formMessage.className = 'form-message error';
        return;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        formMessage.textContent = 'Please enter a valid email address';
        formMessage.className = 'form-message error';
        return;
    }
    
    // Save contact inquiry
    const inquiry = {
        id: 'INQ_' + Date.now(),
        name,
        email,
        phone,
        subject,
        message,
        timestamp: new Date().toISOString(),
        status: 'new'
    };
    
    // Get existing inquiries
    let inquiries = JSON.parse(localStorage.getItem('visionguard_inquiries')) || [];
    inquiries.push(inquiry);
    localStorage.setItem('visionguard_inquiries', JSON.stringify(inquiries));
    
    // Show success message
    formMessage.textContent = 'Thank you for your message! We\'ll get back to you soon.';
    formMessage.className = 'form-message success';
    
    // Reset form
    document.getElementById('contactForm').reset();
    
    // Log if user is authenticated
    const user = getUser();
    if (user) {
        saveDetectionLog('contact_inquiry', {
            name,
            email,
            subject
        });
    }
    
    // Clear message after 5 seconds
    setTimeout(() => {
        formMessage.className = 'form-message';
        formMessage.textContent = '';
    }, 5000);
}

// ===== FAQ ACCORDION =====
document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Close other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            item.classList.toggle('active');
        });
    });
    
    // Load remembered email if exists
    const rememberEmail = localStorage.getItem('rememberEmail');
    if (rememberEmail && document.getElementById('email')) {
        document.getElementById('email').value = rememberEmail;
    }
});

// ===== SEND EMAIL DIRECTLY =====
function sendDirectEmail() {
    const email = 'contact@visionguard.com';
    window.location.href = 'mailto:' + email;
}

// ===== CALL PHONE =====
function callPhone() {
    const phone = '+1 (555) 123-4567';
    window.location.href = 'tel:+15551234567';
}

// ===== OPEN GOOGLE MAPS =====
function openGoogleMaps() {
    window.open('https://share.google/1TZwcCa6c88Zf5oUi', '_blank');
}

// ===== CONTACT OPTIONS =====
const contactOptions = {
    phone: '+1 (555) 123-4567',
    email: 'contact@visionguard.com',
    support: 'support@visionguard.com',
    location: 'https://share.google/1TZwcCa6c88Zf5oUi'
};

// Export for use in other modules
window.contactOptions = contactOptions;
