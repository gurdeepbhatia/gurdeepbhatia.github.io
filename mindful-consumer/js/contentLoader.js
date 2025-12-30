// Load content from HTML files
async function loadContent(pageId) {
    const contentWrapper = document.querySelector('.content-wrapper');
    
    try {
        const response = await fetch(`content/${pageId}.html`);
        if (!response.ok) throw new Error('Content not found');
        
        const html = await response.text();
        contentWrapper.innerHTML = html;
        
        // Scroll to top
        document.querySelector('.main-content').scrollTop = 0;
    } catch (error) {
        contentWrapper.innerHTML = `
            <h1>Error Loading Content</h1>
            <p>Could not load the content for this page. Please make sure the file exists at: content/${pageId}.html</p>
        `;
    }
}

// Update active state in navigation
function updateActiveNav(pageId) {
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to current nav item
    const activeBtn = document.querySelector(`[data-page="${pageId}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}