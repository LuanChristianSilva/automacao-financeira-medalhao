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
        renderActionAlerts(data);

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
                timeEl.innerHTML = `Indefinido <span class="h6 text-negative-highlight d-block mt-1">Saldo Negativo</span>`;
            } else {
                timeEl.innerHTML = `${data.Meses_Para_Quitar} <span class="h4">meses</span>`;
            }
        }

        // Installment Table
        renderInstallmentTable(data.Detalhe_Parcelas);
    };

    const renderActionAlerts = (data) => {
        const container = document.getElementById('action-alerts-container');
        if (!container) return;

        let alertHtml = '';
        const saldo = data.Receita_Disponivel;

        if (saldo < 0) {
            // CRITICAL STATE
            alertHtml = `
                <div class="alert alert-danger b-alert rounded-4 p-4 border-0 d-flex align-items-start gap-3 shadow-sm">
                    <div class="alert-icon-circle bg-danger text-white p-2 rounded-circle">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </div>
                    <div class="flex-grow-1">
                        <h5 class="h6 fw-bold mb-1">Estado Crítico: Déficit Financeiro</h5>
                        <p class="mb-0 fs-7 opacity-75">Suas despesas superaram sua renda. Priorize o pagamento de contas essenciais e evite qualquer novo gasto no cartão.</p>
                    </div>
                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3">Plano de Contingência</button>
                </div>
            `;
        } else if (saldo < 1000) {
            // WARNING STATE
            alertHtml = `
                <div class="alert alert-warning b-alert rounded-4 p-4 border-0 d-flex align-items-start gap-3 shadow-sm">
                    <div class="alert-icon-circle bg-warning text-dark p-2 rounded-circle">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                            <line x1="12" y1="9" x2="12" y2="13"></line>
                            <line x1="12" y1="17" x2="12.01" y2="17"></line>
                        </svg>
                    </div>
                    <div class="flex-grow-1">
                        <h5 class="h6 fw-bold mb-1">Atenção: Margem Reduzida</h5>
                        <p class="mb-0 fs-7 opacity-75">Seu saldo disponível está abaixo da margem de segurança. Evite compras supérfluas até o próximo ciclo.</p>
                    </div>
                    <button class="btn btn-sm btn-outline-dark rounded-pill px-3">Monitorar</button>
                </div>
            `;
        } else {
            // HEALTHY STATE
            alertHtml = `
                <div class="alert alert-success b-alert rounded-4 p-4 border-0 d-flex align-items-start gap-3 shadow-sm" style="background-color: #f0fDF4; color: #166534;">
                    <div class="alert-icon-circle bg-success text-white p-2 rounded-circle">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <div class="flex-grow-1">
                        <h5 class="h6 fw-bold mb-1" style="color: #166534;">Saúde Financeira Excelente</h5>
                        <p class="mb-0 fs-7 opacity-75">Parabéns! Você tem uma boa sobra este mês. Considere adiantar uma parcela de dívida ou reforçar sua reserva.</p>
                    </div>
                    <button class="btn btn-sm btn-success rounded-pill px-3 border-0" style="background-color: #166534;">Investir Sobra</button>
                </div>
            `;
        }

        container.innerHTML = alertHtml;
    };

    let currentSortDesc = true; // State for installment sorting

    const renderInstallmentTable = (installments) => {
        const container = document.getElementById('action-installment-list');
        const sortLabel = document.getElementById('sort-label');
        if (!container) return;

        if (!installments || installments.length === 0) {
            container.innerHTML = '<div class="text-center py-4 opacity-50 fst-italic">Nenhum parcelamento ativo</div>';
            return;
        }

        // Apply state label
        if (sortLabel) sortLabel.textContent = currentSortDesc ? 'Maiores Prazos' : 'Menores Prazos';

        // Sort and Take Top 5
        const sorted = [...installments].sort((a, b) => {
            return currentSortDesc ? b.restantes - a.restantes : a.restantes - b.restantes;
        }).slice(0, 5);

        container.innerHTML = sorted.map(inst => `
            <div class="d-flex align-items-center justify-content-between p-3 rounded-4 bg-main-alt shadow-sm">
                <div class="d-flex flex-column">
                    <span class="fw-medium text-main">${inst.item}</span>
                    <span class="fs-xs opacity-50 text-truncate" style="max-width: 150px;">${inst.pagas}/${inst.total} parcelas | ${formatCurrency(inst.valor)}</span>
                </div>
                <div class="text-end">
                    <span class="fw-bold text-main d-block">${inst.restantes}</span>
                    <span class="fs-xs opacity-50">meses</span>
                </div>
            </div>
        `).join('');
    };

    // Event Listener for sorting toggle
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('#toggle-installment-sort');
        if (btn && allData.length > 0) {
            currentSortDesc = !currentSortDesc;
            const filter = document.getElementById('monthFilter');
            const selectedData = allData.find(i => i.Mes_Referencia === filter.value) || allData[0];
            renderInstallmentTable(selectedData.Detalhe_Parcelas);
        }
    });

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
