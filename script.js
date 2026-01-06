/**
 * Main JavaScript for Attendance Management System
 * Handles dynamic interactions and AJAX requests
 */

// ==================== Utility Functions ====================

/**
 * Display alert message
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fade-in`;
    alertDiv.innerHTML = `<strong>${type === 'success' ? '✓' : type === 'danger' ? '✕' : 'ℹ'}</strong> ${message}`;
    
    const container = document.querySelector('.content');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Confirm action with user
 */
function confirmAction(message) {
    return confirm(message);
}

// ==================== Attendance Functions ====================

/**
 * Mark attendance (Present/Absent)
 */
function markAttendance(status) {
    if (!confirmAction(`Are you sure you want to mark yourself as ${status}?`)) {
        return;
    }
    
    const formData = new FormData();
    formData.append('status', status);
    
    fetch('/employee/mark-attendance', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Error marking attendance. Please try again.', 'danger');
        console.error('Error:', error);
    });
}

// ==================== Leave Management Functions ====================

/**
 * Process leave request action (approve/reject)
 */
function processLeaveRequest(leaveId, action) {
    const actionText = action === 'Approved' ? 'approve' : 'reject';
    
    if (!confirmAction(`Are you sure you want to ${actionText} this leave request?`)) {
        return;
    }
    
    const remarks = prompt('Enter remarks (optional):');
    
    const formData = new FormData();
    formData.append('action', action);
    if (remarks) {
        formData.append('remarks', remarks);
    }
    
    fetch(`/admin/leave-action/${leaveId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('Error processing request. Please try again.', 'danger');
        console.error('Error:', error);
    });
}

// ==================== Form Validation ====================

/**
 * Validate leave application form
 */
function validateLeaveForm(event) {
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const reason = document.getElementById('reason').value.trim();
    
    // Check if dates are provided
    if (!startDate || !endDate) {
        showAlert('Please select both start and end dates', 'danger');
        event.preventDefault();
        return false;
    }
    
    // Check if end date is after start date
    if (new Date(endDate) < new Date(startDate)) {
        showAlert('End date must be after start date', 'danger');
        event.preventDefault();
        return false;
    }
    
    // Check if start date is in the past
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (new Date(startDate) < today) {
        showAlert('Cannot apply for past dates', 'danger');
        event.preventDefault();
        return false;
    }
    
    // Check reason length
    if (reason.length < 10) {
        showAlert('Please provide a detailed reason (at least 10 characters)', 'danger');
        event.preventDefault();
        return false;
    }
    
    return true;
}

// ==================== Date Filtering ====================

/**
 * Handle month filter change
 */
function filterByMonth() {
    const monthSelect = document.getElementById('month-filter');
    if (monthSelect) {
        const selectedMonth = monthSelect.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('month', selectedMonth);
        window.location.href = currentUrl.toString();
    }
}

/**
 * Handle date filter change
 */
function filterByDate() {
    const dateSelect = document.getElementById('date-filter');
    if (dateSelect) {
        const selectedDate = dateSelect.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('date', selectedDate);
        window.location.href = currentUrl.toString();
    }
}

/**
 * Handle status filter change
 */
function filterByStatus() {
    const statusSelect = document.getElementById('status-filter');
    if (statusSelect) {
        const selectedStatus = statusSelect.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('status', selectedStatus);
        window.location.href = currentUrl.toString();
    }
}

/**
 * Handle year filter change
 */
function filterByYear() {
    const yearSelect = document.getElementById('year-filter');
    if (yearSelect) {
        const selectedYear = yearSelect.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('year', selectedYear);
        window.location.href = currentUrl.toString();
    }
}

// ==================== Mobile Menu Toggle ====================

/**
 * Toggle sidebar on mobile
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// ==================== Table Export ====================

/**
 * Export table to CSV
 */
function exportTableToCSV(filename = 'report.csv') {
    const table = document.querySelector('table');
    if (!table) {
        showAlert('No table found to export', 'danger');
        return;
    }
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            // Remove any HTML tags and get text content
            let text = col.textContent.trim();
            // Escape quotes
            text = text.replace(/"/g, '""');
            csvRow.push(`"${text}"`);
        });
        csv.push(csvRow.join(','));
    });
    
    // Create download link
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showAlert('Report exported successfully!', 'success');
}

/**
 * Print table
 */
function printTable() {
    window.print();
}

// ==================== Real-time Updates ====================

/**
 * Auto-refresh dashboard data every 30 seconds
 */
function startAutoRefresh() {
    setInterval(() => {
        // Only refresh on dashboard pages
        if (window.location.pathname.includes('dashboard')) {
            location.reload();
        }
    }, 30000); // 30 seconds
}

// ==================== Initialize ====================

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date for date inputs to today
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (input.id === 'start_date' || input.id === 'end_date') {
            const today = new Date().toISOString().split('T')[0];
            input.min = today;
        }
    });
    
    // Add form validation
    const leaveForm = document.getElementById('leave-form');
    if (leaveForm) {
        leaveForm.addEventListener('submit', validateLeaveForm);
    }
    
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Initialize tooltips (if using a tooltip library)
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.title = element.getAttribute('data-tooltip');
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + E to export
        if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
            event.preventDefault();
            const exportBtn = document.querySelector('[onclick*="exportTableToCSV"]');
            if (exportBtn) {
                exportBtn.click();
            }
        }
        
        // Ctrl/Cmd + P to print
        if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
            event.preventDefault();
            printTable();
        }
    });
    
    // Start auto-refresh for dashboard
    // startAutoRefresh(); // Uncomment if you want auto-refresh
});

// ==================== Logout Confirmation ====================

function confirmLogout() {
    return confirmAction('Are you sure you want to logout?');
}

// ==================== Date Calculations ====================

/**
 * Calculate number of days between two dates
 */
function calculateDays(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    return diffDays;
}

/**
 * Update leave days display
 */
function updateLeaveDays() {
    const startDate = document.getElementById('start_date')?.value;
    const endDate = document.getElementById('end_date')?.value;
    const daysDisplay = document.getElementById('leave-days');
    
    if (startDate && endDate && daysDisplay) {
        const days = calculateDays(startDate, endDate);
        daysDisplay.textContent = `Total Days: ${days}`;
        daysDisplay.style.display = 'block';
    }
}

// ==================== Search Functionality ====================

/**
 * Search table rows
 */
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    const filter = input.value.toLowerCase();
    const rows = table.getElementsByTagName('tr');
    
    // Start from 1 to skip header row
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        row.style.display = found ? '' : 'none';
    }
}

// ==================== Loading Indicator ====================

/**
 * Show loading indicator
 */
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loading-overlay';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    loader.innerHTML = '<div style="color: white; font-size: 1.5rem;">Loading...</div>';
    document.body.appendChild(loader);
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loader = document.getElementById('loading-overlay');
    if (loader) {
        loader.remove();
    }
}

// ==================== Console Info ====================

console.log('%c Attendance Management System ', 'background: #2563eb; color: white; font-size: 16px; padding: 10px;');
console.log('%c Developed with ❤️ ', 'color: #64748b; font-size: 12px;');
