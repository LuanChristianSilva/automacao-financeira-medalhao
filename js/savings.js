document.addEventListener('DOMContentLoaded', () => {

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    const toggleLoading = (isLoading) => {
        const loader = document.getElementById('dashboard-loader');
        if (!loader) return;
        isLoading ? loader.classList.remove('d-none') : loader.classList.add('d-none');
    };

    const loadData = async () => {
        toggleLoading(true);
        try {
            const response = await fetch('Dados/3_Gold/metas_poupanca.json');
            const data = await response.json();
            const goal = data[0];

            if (goal) {
                renderGoal(goal);
            }
        } catch (error) {
            console.error('Erro ao carregar metas:', error);
        } finally {
            toggleLoading(false);
        }
    };

    const renderGoal = (data) => {
        // Main Values
        document.getElementById('goal-accumulated').textContent = formatCurrency(data.Valor_Acumulado);
        document.getElementById('goal-remaining').textContent = formatCurrency(data.Necessidade_Restante);
        document.getElementById('goal-pct-text').textContent = `${Math.round(data.Percentual)}%`;
        
        // Progress Bar
        const progressEl = document.getElementById('goal-remaining-progress');
        if (progressEl) progressEl.style.width = `${data.Percentual}%`;

        // Pace & Projection
        document.getElementById('goal-monthly-pace').textContent = formatCurrency(data.Necessidade_Restante / 12); // Mock: 12 months remaining
        document.getElementById('goal-projected-date').textContent = new Date(data.Data_Alvo).toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });

        renderMainGauge(data.Percentual);
        renderEvolutionChart();
    };

    const renderMainGauge = (value) => {
        const ctx = document.getElementById('savingsGoalGauge');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [value, 100 - value],
                    backgroundColor: ['#3b82f6', '#f1f5f9'],
                    borderWidth: 0,
                    borderRadius: 10,
                }]
            },
            options: {
                cutout: '85%',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    };

    const renderEvolutionChart = () => {
        const ctx = document.getElementById('savingsEvolutionChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Acumulado',
                    data: [5000, 8000, 12000, 15000, 19000, 24000],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { display: false },
                    x: { grid: { display: false } }
                }
            }
        });
    };

    loadData();
});
