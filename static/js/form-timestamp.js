/**
 * Form Timestamp Utility for Baghdad Time
 * Automatically adds Baghdad timezone timestamps to form submissions
 */

class FormTimestamp {
    constructor() {
        this.initialize();
    }

    initialize() {
        // Add timestamp fields to all forms on submit
        document.addEventListener('submit', (e) => {
            if (e.target.tagName === 'FORM') {
                this.addTimestampToForm(e.target);
            }
        });

        // Initialize timestamp fields if they exist
        this.initializeTimestampFields();
    }

    /**
     * Add timestamp fields to form before submission
     */
    addTimestampToForm(form) {
        const currentTime = window.BaghdadDateTime ? 
            window.BaghdadDateTime.getTimeForForms() : 
            new Date().toISOString();

        // Add or update timestamp fields
        this.addHiddenField(form, 'timestamp', currentTime);
        this.addHiddenField(form, 'created_at_baghdad', currentTime);
        this.addHiddenField(form, 'updated_at_baghdad', currentTime);
        
        // Add timezone info
        this.addHiddenField(form, 'timezone', 'Asia/Baghdad');
        
        console.log('Added Baghdad timestamp to form:', currentTime);
    }

    /**
     * Add hidden field to form
     */
    addHiddenField(form, name, value) {
        // Check if field already exists
        let field = form.querySelector(`input[name="${name}"]`);
        
        if (!field) {
            // Create new hidden field
            field = document.createElement('input');
            field.type = 'hidden';
            field.name = name;
            form.appendChild(field);
        }
        
        field.value = value;
    }

    /**
     * Initialize existing timestamp fields with Baghdad time
     */
    initializeTimestampFields() {
        const timestampFields = document.querySelectorAll(
            'input[name*="created_at"], input[name*="updated_at"], input[name*="timestamp"]'
        );

        timestampFields.forEach(field => {
            if (!field.value || field.value === '') {
                const currentTime = window.BaghdadDateTime ? 
                    window.BaghdadDateTime.getTimeForForms() : 
                    new Date().toISOString();
                field.value = currentTime;
            }
        });
    }

    /**
     * Display Baghdad time in specified element
     */
    static displayBaghdadTime(elementId, format = 'full') {
        const element = document.getElementById(elementId);
        if (!element) return;

        if (window.BaghdadDateTime) {
            const datetime = window.BaghdadDateTime.getFormattedDateTime();
            
            switch (format) {
                case 'date':
                    element.textContent = datetime.date;
                    break;
                case 'time':
                    element.textContent = datetime.time;
                    break;
                case 'compact':
                    element.textContent = `${datetime.date} ${datetime.time}`;
                    break;
                default:
                    element.textContent = `${datetime.date} - ${datetime.time}`;
            }
            
            element.setAttribute('data-timestamp', datetime.timestamp);
            element.setAttribute('data-iso', datetime.iso);
        }
    }

    /**
     * Format timestamp for display in Arabic
     */
    static formatTimestampArabic(timestamp) {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        const baghdadTime = new Date(date.toLocaleString("en-US", {timeZone: "Asia/Baghdad"}));
        
        const arabicMonths = {
            0: 'يناير', 1: 'فبراير', 2: 'مارس', 3: 'أبريل',
            4: 'مايو', 5: 'يونيو', 6: 'يوليو', 7: 'أغسطس',
            8: 'سبتمبر', 9: 'أكتوبر', 10: 'نوفمبر', 11: 'ديسمبر'
        };
        
        const arabicDays = {
            0: 'الأحد', 1: 'الإثنين', 2: 'الثلاثاء', 3: 'الأربعاء',
            4: 'الخميس', 5: 'الجمعة', 6: 'السبت'
        };
        
        const dayName = arabicDays[baghdadTime.getDay()];
        const monthName = arabicMonths[baghdadTime.getMonth()];
        
        const year = baghdadTime.getFullYear();
        const day = baghdadTime.getDate();
        const hour = baghdadTime.getHours();
        const minute = baghdadTime.getMinutes();
        
        // Convert to 12-hour format
        let hour12 = hour;
        let period = 'ص';
        
        if (hour === 0) {
            hour12 = 12;
        } else if (hour > 12) {
            hour12 = hour - 12;
            period = 'م';
        } else if (hour === 12) {
            period = 'م';
        }
        
        return `${dayName}، ${day} ${monthName} ${year} - ${hour12.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')} ${period}`;
    }

    /**
     * Update all timestamp displays on page
     */
    static updateAllTimestampDisplays() {
        // Update created_at displays
        document.querySelectorAll('[data-created-at]').forEach(element => {
            const timestamp = element.getAttribute('data-created-at');
            element.textContent = FormTimestamp.formatTimestampArabic(timestamp);
        });

        // Update updated_at displays
        document.querySelectorAll('[data-updated-at]').forEach(element => {
            const timestamp = element.getAttribute('data-updated-at');
            element.textContent = FormTimestamp.formatTimestampArabic(timestamp);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new FormTimestamp();
    
    // Update timestamp displays
    FormTimestamp.updateAllTimestampDisplays();
    
    // Listen for Baghdad time updates
    document.addEventListener('baghdadTimeUpdate', function(e) {
        FormTimestamp.updateAllTimestampDisplays();
    });
});

// Global utility functions
window.FormTimestamp = FormTimestamp; 