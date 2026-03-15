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
            const response = await fetch('Dados/3_Gold/indicadores_acao.json');
            const data = await response.json();
            const indicators = data[0];

            if (indicators) {
                renderIndicators(indicators);
            }
        } catch (error) {
            console.error('Erro ao carregar indicadores:', error);
        } finally {
            toggleLoading(false);
        }
    };

    const renderIndicators = (data) => {
        // Available Income
        const incomeEl = document.getElementById('action-available-income');
        if (incomeEl) incomeEl.textContent = formatCurrency(data.Receita_Disponivel);

        // Progress Bar (Mock logic: assuming 5000 is a safe threshold)
        const progressEl = document.getElementById('available-income-progress');
        const pctEl = document.getElementById('available-income-pct');
        if (progressEl && pctEl) {
            const pct = Math.min(Math.max((data.Receita_Disponivel / 5000) * 100, 0), 100);
            progressEl.style.width = `${pct}%`;
            pctEl.textContent = `${Math.round(pct)}%`;
            
            if (pct < 20) progressEl.className = 'progress-bar bg-danger';
            else if (pct < 50) progressEl.className = 'progress-bar bg-warning';
            else progressEl.className = 'progress-bar bg-success';
        }

        // Days Left
        const daysEl = document.getElementById('action-days-left');
        if (daysEl) {
            daysEl.textContent = Math.max(Math.round(data.Dias_Restantes), 0);
            if (data.Dias_Restantes < 5) daysEl.classList.add('text-danger');
        }

        // Alerts
        const alertNegative = document.getElementById('alert-negative-risk');
        if (alertNegative) {
            if (data.Risco_Saldo_Negativo === 'Alto') {
                alertNegative.classList.remove('d-none');
            } else {
                alertNegative.classList.add('d-none');
            }
        }

        // Top Expenses
        const expensesContainer = document.getElementById('action-top-expenses');
        if (expensesContainer && data.Top_Gastos) {
            expensesContainer.innerHTML = data.Top_Gastos.map((item, index) => `
                <div class="d-flex align-items-center justify-content-between p-3 rounded-4 bg-main-alt shadow-sm">
                    <div class="d-flex align-items-center gap-3">
                        <div class="rank-circle ${index === 0 ? 'bg-primary' : 'bg-secondary'}">${index + 1}</div>
                        <span class="fw-medium">${item.item}</span>
                    </div>
                    <span class="fw-bold">${formatCurrency(item.valor)}</span>
                </div>
            `).join('');
        }

        renderDebtGauge(35); // Static 35% for now as logic in gold_indicators is basic
    };

    const renderDebtGauge = (value) => {
        const ctx = document.getElementById('debtImpactGauge');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [value, 100 - value],
                    backgroundColor: ['#ef4444', '#f1f5f9'],
                    borderWidth: 0,
                    circumference: 180,
                    rotation: 270,
                }]
            },
            options: {
                cutout: '80%',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    };

    loadData();
});
