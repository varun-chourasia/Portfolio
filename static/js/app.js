// Global variables
let navbar;
let navLinks;
let hamburger;
let navMenu;
let backToTopBtn;

// Download resume function
function downloadResume() {
    // Create a temporary link element
    const link = document.createElement('a');
    link.href = '#'; // Replace with actual resume URL
    link.download = 'Varun_Choursiya_Resume.pdf';
    
    // Show a message since we don't have an actual file
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-download"></i> Downloading...';
    button.disabled = true;
    
    setTimeout(() => {
        alert('Resume download would start here. Please add your actual resume file URL.');
        button.innerHTML = originalText;
        button.disabled = false;
    }, 1000);
}
// Make downloadResume function globally available
window.downloadResume = downloadResume;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    navbar = document.getElementById('navbar');
    navLinks = document.querySelectorAll('.nav-link');
    hamburger = document.getElementById('hamburger');
    navMenu = document.getElementById('nav-menu');
    backToTopBtn = document.getElementById('backToTop');
    
    // Initialize all functionality
    initNavigation();
    initScrollAnimations();
    initParticles();
    initSkillBars();
    initContactForm();
    initTypingAnimation();
    initScrollSpy();
    initBackToTop();
    initSkillsTabs();
    initProjectFilters();
    initEnhancedAnimations();
});

// Navigation functionality
function initNavigation() {
    // Hamburger menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on links
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Account for navbar height
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);
    
    // Add animation classes to elements
    const animationElements = [
        { selector: '.stat-card', class: 'fade-in-up' },
        { selector: '.skill-category', class: 'fade-in-up' },
        { selector: '.project-card', class: 'scale-in' },
        { selector: '.timeline-item', class: 'fade-in-left' },
        { selector: '.contact-info', class: 'fade-in-left' },
        { selector: '.contact-form', class: 'fade-in-right' }
    ];
    
    animationElements.forEach(item => {
        const elements = document.querySelectorAll(item.selector);
        elements.forEach((element, index) => {
            element.classList.add(item.class);
            element.style.transitionDelay = `${index * 0.1}s`;
            observer.observe(element);
        });
    });
}

// Particle animation for hero section
function initParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    // Random size between 2-6px
    const size = Math.random() * 4 + 2;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    
    // Random position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    
    // Random animation duration
    particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
    
    // Random animation delay
    particle.style.animationDelay = Math.random() * 2 + 's';
    
    container.appendChild(particle);
}

// Skill bars animation
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.getAttribute('data-width');
                
                setTimeout(() => {
                    progressBar.style.width = width + '%';
                }, 300);
                
                skillObserver.unobserve(progressBar);
            }
        });
    }, {
        threshold: 0.5
    });
    
    skillBars.forEach(bar => {
        skillObserver.observe(bar);
    });
}

// Contact form functionality
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            message: document.getElementById('message').value
        };
        
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/contact/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (response.ok) {
                alert('Message sent successfully!');
                contactForm.reset();
            } else {
                alert('Error: ' + (result.error || 'Failed to send message'));
            }
        } catch (error) {
            alert('Failed to send message. Please check your connection.');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            submitBtn.style.background = '';
        }
    });
}

// Typing animation for hero text
function initTypingAnimation() {
    const greeting = document.querySelector('.hero-greeting');
    if (!greeting) return;
    
    const text = greeting.textContent;
    greeting.textContent = '';
    greeting.style.opacity = '1';
    
    let index = 0;
    
    function typeChar() {
        if (index < text.length) {
            greeting.textContent += text.charAt(index);
            index++;
            setTimeout(typeChar, 100);
        }
    }
    
    // Start typing animation after initial delay
    setTimeout(typeChar, 1000);
}

// Scroll spy for navigation
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (window.pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Back to top button
function initBackToTop() {
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced parallax effects
window.addEventListener('scroll', debounce(function() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    const profilePhoto = document.querySelector('.profile-photo-container');
    
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
    
    if (profilePhoto && scrolled < window.innerHeight) {
        profilePhoto.style.transform = `translateY(${scrolled * 0.1}px)`;
    }
}, 10));

// Enhanced reveal animations
function addRevealAnimation() {
    const reveals = document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .scale-in');
    
    function reveal() {
        reveals.forEach(element => {
            const windowHeight = window.innerHeight;
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('animate');
                
                // Add stagger effect for skill items
                if (element.classList.contains('skill-item')) {
                    const skillItems = element.parentElement.querySelectorAll('.skill-item');
                    skillItems.forEach((item, index) => {
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                }
            }
        });
    }
    
    window.addEventListener('scroll', debounce(reveal, 10));
    reveal(); // Check on load
}

// Intersection Observer for better performance
function initIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Special handling for skill categories
                if (entry.target.classList.contains('skill-category')) {
                    const skillBars = entry.target.querySelectorAll('.skill-progress');
                    skillBars.forEach((bar, index) => {
                        setTimeout(() => {
                            const width = bar.getAttribute('data-width');
                            bar.style.width = width + '%';
                        }, index * 100);
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all animatable elements
    document.querySelectorAll('[class*="fade-"], [class*="scale-"], .skill-category, .project-card, .cert-card').forEach(el => {
        observer.observe(el);
    });
}

// Initialize reveal animations
addRevealAnimation();
initIntersectionObserver();

// Add keyboard navigation for tabs and filters
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        const focusedElement = document.activeElement;
        
        // Handle tab buttons
        if (focusedElement.classList.contains('tab-button')) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                focusedElement.click();
            }
        }
        
        // Handle filter buttons
        if (focusedElement.classList.contains('filter-btn')) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                focusedElement.click();
            }
        }
    }
});

// Add touch gestures for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
        const activeTab = document.querySelector('.tab-button.active');
        const tabButtons = document.querySelectorAll('.tab-button');
        
        if (activeTab && tabButtons.length > 1) {
            const currentIndex = Array.from(tabButtons).indexOf(activeTab);
            let nextIndex;
            
            if (diff > 0) { // Swipe left
                nextIndex = (currentIndex + 1) % tabButtons.length;
            } else { // Swipe right
                nextIndex = (currentIndex - 1 + tabButtons.length) % tabButtons.length;
            }
            
            tabButtons[nextIndex].click();
        }
    }
}

// Make the website PWA ready
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker would be registered here for PWA functionality
        console.log('Portfolio website loaded successfully');
    });
}

// Skills tabs functionality
function initSkillsTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const skillCategories = document.querySelectorAll('.skill-category');
    
    if (!tabButtons.length || !skillCategories.length) return;
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all categories
            skillCategories.forEach(category => {
                category.classList.remove('active');
                category.style.display = 'none';
            });
            
            // Show target category
            const targetCategory = document.querySelector(`[data-category="${targetTab}"]`);
            if (targetCategory) {
                targetCategory.style.display = 'block';
                setTimeout(() => {
                    targetCategory.classList.add('active');
                }, 10);
            }
        });
    });
}

// Project filters functionality
function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    if (!filterButtons.length || !projectCards.length) return;
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter projects
            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filter === 'all' || category === filter) {
                    card.classList.remove('hidden');
                    card.style.display = 'block';
                } else {
                    card.classList.add('hidden');
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Enhanced animations for new elements
function initEnhancedAnimations() {
    // Animate certifications on scroll
    const certCards = document.querySelectorAll('.cert-card');
    const certObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                certObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    certCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        certObserver.observe(card);
    });
    
    // Enhanced project card hover effects
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) rotateX(5deg)';
            this.style.boxShadow = '0 30px 60px rgba(0, 217, 255, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0deg)';
            this.style.boxShadow = '';
        });
    });
    
    // Profile photo particle animation enhancement
    const photoParticles = document.querySelectorAll('.photo-particles div');
    photoParticles.forEach((particle, index) => {
        setInterval(() => {
            const randomX = Math.random() * 20 - 10;
            const randomY = Math.random() * 20 - 10;
            particle.style.transform = `translate(${randomX}px, ${randomY}px)`;
        }, 2000 + index * 500);
    });
}

// Enhanced contact form with phone validation
function validateContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;
    
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            const phonePattern = /^[\\+]?[1-9][\\d]{0,15}$/;
            if (!phonePattern.test(this.value) && this.value.length > 0) {
                this.style.borderColor = '#ff6b6b';
            } else {
                this.style.borderColor = '';
            }
        });
    }
}

// Add smooth scrolling enhancement
function enhanceSmoothScrolling() {
    // Add parallax effect to background elements
    window.addEventListener('scroll', debounce(function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    }, 10));
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    validateContactForm();
    enhanceSmoothScrolling();
});

// Add loading animation
window.addEventListener('load', function() {
    const loader = document.createElement('div');
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #0a192f;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: opacity 0.5s ease;
    `;
    
    loader.innerHTML = `
        <div style="
            width: 50px;
            height: 50px;
            border: 3px solid rgba(0, 217, 255, 0.3);
            border-top: 3px solid #00d9ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
    `;
    
    // Add spin animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(loader);
    
    // Remove loader after delay
    setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.remove();
            // Trigger photo entrance animation
            const profilePhoto = document.querySelector('.profile-photo');
            if (profilePhoto) {
                profilePhoto.style.animationDelay = '0.5s';
            }
        }, 500);
    }, 1000);
});
