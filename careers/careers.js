(function () {
    const buttons = Array.from(document.querySelectorAll('.opportunity-toggle'));

    buttons.forEach((button) => {
        const panel = document.getElementById(button.getAttribute('aria-controls'));
        if (!panel) return;

        panel.hidden = true;
        panel.setAttribute('aria-hidden', 'true');

        button.addEventListener('click', () => {
            const willOpen = button.getAttribute('aria-expanded') !== 'true';

            buttons.forEach((otherButton) => {
                const otherPanel = document.getElementById(otherButton.getAttribute('aria-controls'));
                otherButton.setAttribute('aria-expanded', 'false');
                if (otherPanel) {
                    otherPanel.hidden = true;
                    otherPanel.setAttribute('aria-hidden', 'true');
                }
            });

            button.setAttribute('aria-expanded', String(willOpen));
            panel.hidden = !willOpen;
            panel.setAttribute('aria-hidden', String(!willOpen));
        });
    });

    const mark = document.querySelector('[data-moving-mark]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (mark && !reducedMotion.matches) {
        let frame = null;
        const updateMark = () => {
            frame = null;
            const shift = Math.min(window.scrollY * 0.055, 34);
            mark.style.setProperty('--mark-shift', `${shift}px`);
        };

        window.addEventListener('scroll', () => {
            if (frame === null) frame = window.requestAnimationFrame(updateMark);
        }, { passive: true });
    }
})();
