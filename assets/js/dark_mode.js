  const toggleButton = document.getElementById('theme-toggle');
        toggleButton.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
        });

        // Scroll animation for fade-in effect
        const fadeInElements = document.querySelectorAll('.fade-in');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        fadeInElements.forEach(element => {
            observer.observe(element);
        });