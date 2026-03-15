document.addEventListener('DOMContentLoaded', () => {

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    const toggleLoading = (isLoading) => {
        const loader = document.getElementById('dashboard-loader');
        if (!loader) return;
        isLoading ? loader.classList.remove('d-none') : loader.classList.add('d-none');
    };

    const populateFilter = (data) => {
        const filter = document.getElementById('monthFilter');
        if (!filter) return;

        filter.innerHTML = data.map(item => {
            const parts = item.Mes_Referencia.split('-');
            const date = new Date(parts[0], parts[1] - 1, parts[2]);
            const label = date.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
            return `<option value="${item.Mes_Referencia}">${label.charAt(0).toUpperCase() + label.slice(1)}</option>`;
        }).join('');
    };

    const loadData = async () => {
        toggleLoading(true);
        try {
            const [respGoal, respAction] = await Promise.all([
                fetch('Dados/3_Gold/metas_poupanca.json'),
                fetch('Dados/3_Gold/indicadores_acao.json')
            ]);
            
            const goalData = await respGoal.json();
            const actionData = await respAction.json();

            if (actionData.length > 0) populateFilter(actionData);
            if (goalData.length > 0) renderGoal(goalData[0]);
            
        } catch (error) {
            console.error('Erro ao carregar metas:', error);
        } finally {
            toggleLoading(false);
        }
    };

    const renderGoal = (data) => {
        document.getElementById('goal-accumulated').textContent = formatCurrency(data.Valor_Acumulado);
        document.getElementById('goal-remaining').textContent = formatCurrency(data.Necessidade_Restante);
        document.getElementById('goal-pct-text').textContent = `${Math.round(data.Percentual)}%`;
        
        const progressEl = document.getElementById('goal-remaining-progress');
        if (progressEl) progressEl.style.width = `${data.Percentual}%`;

        document.getElementById('goal-monthly-pace').textContent = formatCurrency(data.Necessidade_Restante / 12);
        
        const dateObj = new Date(data.Data_Alvo + 'T00:00:00');
        document.getElementById('goal-projected-date').textContent = dateObj.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });

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
                    tension: 0.4,
                    pointRadius: 0
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
