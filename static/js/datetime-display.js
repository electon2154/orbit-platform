/**
 * Baghdad DateTime Display Utility
 * Shows current date and time in Baghdad timezone with Arabic formatting
 */

class BaghdadDateTime {
    constructor() {
        this.options = {
            timeZone: 'Asia/Baghdad',
            locale: 'ar-IQ',
            dateOptions: {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
            },
            timeOptions: {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            }
        };
        this.intervalId = null;
    }

    /**
     * Get current Baghdad time
     */
    getCurrentBaghdadTime() {
        const now = new Date();
        return new Date(now.toLocaleString("en-US", {timeZone: "Asia/Baghdad"}));
    }

    /**
     * Format date in Arabic
     */
    formatDate(date) {
        return date.toLocaleDateString(this.options.locale, this.options.dateOptions);
    }

    /**
     * Format time in Arabic
     */
    formatTime(date) {
        return date.toLocaleTimeString(this.options.locale, this.options.timeOptions);
    }

    /**
     * Get formatted date and time object
     */
    getFormattedDateTime() {
        const baghdadTime = this.getCurrentBaghdadTime();
        return {
            date: this.formatDate(baghdadTime),
            time: this.formatTime(baghdadTime),
            iso: baghdadTime.toISOString(),
            timestamp: baghdadTime.getTime(),
            raw: baghdadTime
        };
    }

    /**
     * Update datetime display elements
     */
    updateDisplay() {
        const datetime = this.getFormattedDateTime();
        
        // Update date element
        const dateElement = document.getElementById('baghdad-date');
        if (dateElement) {
            dateElement.textContent = datetime.date;
            dateElement.setAttribute('data-timestamp', datetime.timestamp);
        }

        // Update time element
        const timeElement = document.getElementById('baghdad-time');
        if (timeElement) {
            timeElement.textContent = datetime.time;
            timeElement.setAttribute('data-timestamp', datetime.timestamp);
        }

        // Update combined datetime element
        const datetimeElement = document.getElementById('baghdad-datetime');
        if (datetimeElement) {
            datetimeElement.textContent = `${datetime.date} - ${datetime.time}`;
            datetimeElement.setAttribute('data-timestamp', datetime.timestamp);
            datetimeElement.setAttribute('data-iso', datetime.iso);
        }

        // Update compact datetime element
        const compactElement = document.getElementById('baghdad-datetime-compact');
        if (compactElement) {
            const compactDate = datetime.raw.toLocaleDateString('ar-IQ', {
                month: 'short',
                day: 'numeric'
            });
            const compactTime = datetime.raw.toLocaleTimeString('ar-IQ', {
                hour: '2-digit',
                minute: '2-digit'
            });
            compactElement.textContent = `${compactDate} ${compactTime}`;
            compactElement.setAttribute('data-timestamp', datetime.timestamp);
            compactElement.setAttribute('data-iso', datetime.iso);
        }

        // Trigger custom event for other components that might need the time
        const event = new CustomEvent('baghdadTimeUpdate', {
            detail: datetime
        });
        document.dispatchEvent(event);
    }

    /**
     * Start automatic time updates
     */
    startAutoUpdate(interval = 1000) {
        this.stopAutoUpdate(); // Clear any existing interval
        
        // Initial update
        this.updateDisplay();
        
        // Set up interval for updates
        this.intervalId = setInterval(() => {
            this.updateDisplay();
        }, interval);
    }

    /**
     * Stop automatic time updates
     */
    stopAutoUpdate() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    /**
     * Get time for form submissions (ISO format)
     */
    getTimeForForms() {
        return this.getCurrentBaghdadTime().toISOString();
    }

    /**
     * Format time for database storage
     */
    getTimeForDatabase() {
        const baghdadTime = this.getCurrentBaghdadTime();
        return {
            datetime: baghdadTime.toISOString(),
            timezone: 'Asia/Baghdad',
            formatted: this.formatDate(baghdadTime) + ' ' + this.formatTime(baghdadTime)
        };
    }
}

// Create global instance
window.BaghdadDateTime = new BaghdadDateTime();

// Auto-start when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Start automatic updates
    window.BaghdadDateTime.startAutoUpdate();
    
    // Add click event to datetime elements for manual refresh
    document.addEventListener('click', function(e) {
        if (e.target.id && e.target.id.includes('baghdad-')) {
            window.BaghdadDateTime.updateDisplay();
        }
    });
});

// Utility functions for forms
window.getBaghdadTimeForForms = function() {
    return window.BaghdadDateTime.getTimeForForms();
};

window.getBaghdadTimeForDatabase = function() {
    return window.BaghdadDateTime.getTimeForDatabase();
}; 