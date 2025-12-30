// Initialize the application
let expandedSections = ['macronutrients'];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderNavigation();
    setupEventListeners();
    loadContent('introduction');
    updateActiveNav('introduction');
    
    // Expand macronutrients by default
    toggleChildMenu('macronutrients');
});

// Setup event listeners
function setupEventListeners() {
    const nav = document.getElementById('navigation');
    
    nav.addEventListener('click', (e) => {
        const button = e.target.closest('.nav-item');
        if (!button) return;
        
        const pageId = button.dataset.page;
        const isParent = button.dataset.parent === 'true';
        
        // Load content
        loadContent(pageId);
        updateActiveNav(pageId);
        
        // Toggle child menu if parent has children
        if (isParent) {
            const hasChildren = navigationData.find(item => item.id === pageId)?.children.length > 0;
            if (hasChildren) {
                toggleChildMenu(pageId);
            }
        }
    });
}

// Toggle child menu visibility
function toggleChildMenu(parentId) {
    const menu = document.getElementById('menu-' + parentId);
    const button = document.querySelector(`[data-page="${parentId}"][data-parent="true"]`);
    const chevron = button?.querySelector('.chevron');
    
    if (menu && button && chevron) {
        menu.classList.toggle('show');
        chevron.classList.toggle('expanded');
        
        // Update expanded sections
        if (menu.classList.contains('show')) {
            if (!expandedSections.includes(parentId)) {
                expandedSections.push(parentId);
            }
        } else {
            expandedSections = expandedSections.filter(id => id !== parentId);
        }
    }
}