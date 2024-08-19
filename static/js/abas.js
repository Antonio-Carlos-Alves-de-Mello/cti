// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabLinks.forEach(tabLink => {
        tabLink.addEventListener('click', () => {
            const target = tabLink.getAttribute('data-tab');

            // Remove active class from all tabs and panes
            tabLinks.forEach(link => link.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked tab and corresponding pane
            tabLink.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });
});
