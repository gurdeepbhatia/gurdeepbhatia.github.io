const navigationData = [
    { id: 'introduction', label: 'INTRODUCTION', children: [] },
    { 
        id: 'macronutrients', 
        label: 'MACRONUTRIENTS', 
        children: [
            { id: 'carbohydrates', label: 'CARBOHYDATES' },
            { id: 'protein', label: 'PROTEIN' },
            { id: 'fats', label: 'FATS' },
            { id: 'fiber', label: 'FIBER' }
        ]
    },
    { id: 'micronutrients', label: 'MICRONUTRIENTS', children: [] },
    { id: 'water', label: 'WATER', children: [] },
    { id: 'energy-balance', label: 'ENERGY BALANCE', children: [] },
    { id: 'calorie-density', label: 'CALORIE DENSITY', children: [] },
    { id: 'reading-labels', label: 'READING FOOD LABELS', children: [] },
    { id: 'healthy-cooking', label: 'HEALTHY COOKING', children: [] },
    { id: 'meal-planning', label: 'MEAL PLANNING', children: [] },
    { id: 'supplements', label: 'SUPPLEMENTS', children: [] },
    { id: 'myths-facts', label: 'MYTHS & FACTS', children: [] }
];

// Generate navigation HTML
function renderNavigation() {
    const nav = document.getElementById('navigation');
    let html = '';

    navigationData.forEach(item => {
        const hasChildren = item.children.length > 0;
        const chevron = hasChildren ? '<span class="chevron">▶</span>' : '';
        
        html += `
            <button class="nav-item" data-page="${item.id}" data-parent="true">
                <span>${item.label}</span>
                ${chevron}
            </button>
        `;

        if (hasChildren) {
            html += '<div class="child-menu" id="menu-' + item.id + '">';
            item.children.forEach(child => {
                html += `
                    <button class="nav-item child" data-page="${child.id}">
                        -- ${child.label}
                    </button>
                `;
            });
            html += '</div>';
        }
    });

    nav.innerHTML = html;
}