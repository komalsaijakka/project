// Scroll animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.journey-title, .journey-intro, .timeline-item, .journey-cta');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.2 });

    elements.forEach(el => observer.observe(el));
});