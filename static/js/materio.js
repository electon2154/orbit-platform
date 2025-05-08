// Materio Theme JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Toggle Sidebar
  const menuToggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const contentWrapper = document.querySelector('.content-wrapper');
  
  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      sidebar.classList.toggle('collapsed');
      contentWrapper.classList.toggle('expanded');
      
      // For mobile
      sidebar.classList.toggle('mobile-open');
    });
  }
  
  // Dropdown Menus
  const dropdowns = document.querySelectorAll('.dropdown-toggle');
  
  dropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', function(e) {
      e.preventDefault();
      const dropdownMenu = this.nextElementSibling;
      
      // Close other dropdowns
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        if (menu !== dropdownMenu) {
          menu.classList.remove('show');
        }
      });
      
      // Toggle this dropdown
      dropdownMenu.classList.toggle('show');
    });
  });
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        menu.classList.remove('show');
      });
    }
  });
  
  // Active Links
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });
  
  // Tooltips initialization
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Popovers initialization
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Animation on scroll (optional)
  function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    elements.forEach(element => {
      const elementPosition = element.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      
      if (elementPosition < windowHeight - 50) {
        element.classList.add('animated');
      }
    });
  }
  
  window.addEventListener('scroll', animateOnScroll);
  animateOnScroll(); // Run once on page load
}); 