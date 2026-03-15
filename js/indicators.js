document.addEventListener('DOMContentLoaded', () => {

    let allData = [];
    let debtChart = null;

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

        const currentMonthStr = '2026-03-01';

        filter.innerHTML = data.map(item => {
            const parts = item.Mes_Referencia.split('-');
            const date = new Date(parts[0], parts[1] - 1, parts[2]);
            const label = date.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
            const selected = item.Mes_Referencia === currentMonthStr ? 'selected' : '';
            return `<option value="${item.Mes_Referencia}" ${selected}>${label.charAt(0).toUpperCase() + label.slice(1)}</option>`;
        }).join('');

        filter.addEventListener('change', (e) => {
            const selected = data.find(i => i.Mes_Referencia === e.target.value);
            if (selected) renderIndicators(selected);
        });
    };

    const loadData = async () => {
        toggleLoading(true);
        try {
            const response = await fetch('Dados/3_Gold/indicadores_acao.json');
            allData = await response.json();
            
            if (allData.length > 0) {
                populateFilter(allData);
                
                // Try to find current month (March 2026)
                const currentMonthStr = '2026-03-01';
                const currentData = allData.find(i => i.Mes_Referencia === currentMonthStr) || allData[0];
                
                renderIndicators(currentData);
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
        if (incomeEl) {
            incomeEl.textContent = formatCurrency(data.Receita_Disponivel);
            if (data.Receita_Disponivel < 0) {
                incomeEl.classList.add('text-negative-highlight');
            } else {
                incomeEl.classList.remove('text-negative-highlight');
            }
        }

        // Progress Bar
        const progressEl = document.getElementById('available-income-progress');
        const pctEl = document.getElementById('available-income-pct');
        if (progressEl && pctEl) {
            const pct = Math.min(Math.max((data.Receita_Disponivel / 5000) * 100, 0), 100);
            progressEl.style.width = `${pct}%`;
            pctEl.textContent = `${Math.round(pct)}%`;
            
            if (data.Receita_Disponivel < 0) progressEl.className = 'progress-bar bg-danger';
            else if (pct < 50) progressEl.className = 'progress-bar bg-warning';
            else progressEl.className = 'progress-bar bg-success';
        }

        // Days Left
        const daysEl = document.getElementById('action-days-left');
        if (daysEl) {
            daysEl.textContent = Math.max(Math.round(data.Dias_Restantes), 30); // Default to 30 if positive
            if (data.Receita_Disponivel < 0) {
                daysEl.textContent = "0";
                daysEl.classList.add('text-danger');
            } else {
                daysEl.classList.remove('text-danger');
            }
        }

        // Alerts
        const alertNegative = document.getElementById('alert-negative-risk');
        if (alertNegative) {
            data.Receita_Disponivel < 500 ? alertNegative.classList.remove('d-none') : alertNegative.classList.add('d-none');
        }

        // Top Expenses
        const expensesContainer = document.getElementById('action-top-expenses');
        if (expensesContainer && data.Top_Gastos) {
            expensesContainer.innerHTML = data.Top_Gastos.map((item, index) => `
                <div class="d-flex align-items-center justify-content-between p-3 rounded-4 bg-main-alt shadow-sm">
                    <div class="d-flex align-items-center gap-3">
                        <div class="rank-text">#${index + 1}</div>
                        <span class="fw-medium text-main">${item.item}</span>
                    </div>
                    <span class="fw-bold text-main">${formatCurrency(item.valor)}</span>
                </div>
            `).join('');
        }

        // Debt Impact Gauge
        renderDebtGauge(data.Impacto_Divida_Pct);

        // Time to Pay
        const timeEl = document.getElementById('action-debt-time');
        if (timeEl) {
            if (data.Meses_Para_Quitar === -1) {
                timeEl.innerHTML = `Indefinido <span class="h6 text-danger d-block mt-1">Saldo Negativo</span>`;
            } else {
                timeEl.innerHTML = `${data.Meses_Para_Quitar.toFixed(1)} <span class="h4">meses</span>`;
            }
        }
    };

    const renderDebtGauge = (value) => {
        const ctx = document.getElementById('debtImpactGauge');
        if (!ctx) return;

        if (debtChart) debtChart.destroy();

        debtChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [value, 100 - value],
                    backgroundColor: [value >= 100 ? '#ef4444' : (value > 70 ? '#f59e0b' : '#3b82f6'), '#f1f5f9'],
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
        
        // Syncing with HTML ID: action-debt-pct
        const pctText = document.getElementById('action-debt-pct');
        if (pctText) pctText.textContent = `${Math.round(value)}%`;
    };

    loadData();
});
