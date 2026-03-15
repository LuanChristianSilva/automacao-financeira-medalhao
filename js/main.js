document.addEventListener('DOMContentLoaded', () => {

    // --- Configuration & Styling ---
    const chartDefaults = {
        fontFamily: "'Inter', sans-serif",
        colorMain: '#1e293b',
        colorMuted: '#94a3b8',
        colorGrid: '#f1f5f9',
        blueLine: '#3b82f6',
        redLine: '#ef4444',
        greyLine: '#cbd5e1',
        blueFill: 'rgba(59, 130, 246, 0.1)',
        greenLine: '#22c55e',
        darkPurple: '#1e1b4b'
    };

    Chart.defaults.font.family = chartDefaults.fontFamily;
    Chart.defaults.color = chartDefaults.colorMuted;
    Chart.defaults.scale.grid.color = chartDefaults.colorGrid;

    // --- Global Data Store ---
    let goldResumo = [];
    let goldDespesas = [];
    let goldRenda = [];
    let currentMonthData = null; // Currently filtered month
    let last7MonthsData = [];    // Ending at selected month (used for trends/sparklines)
    let rolling12MonthsResumo = []; // Strictly less than selected month (12 bars)

    // --- DOM Elements ---
    const monthFilter = document.getElementById('monthFilter');

    // --- Chart Instances ---
    let charts = {
        revenueTarget: null,
        expenseCategory: null,
        profitTrend: null,
        regionalComparison: null,
        contributionDoughnut: null,
        sparklines: {}
    };

    // --- Utility Functions ---
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    /**
     * Sanitiza strings para exibição segura no HTML.
     * Previne ataques de XSS substituindo caracteres especiais.
     */
    const escapeHTML = (str) => {
        if (typeof str !== 'string') return str;
        const p = document.createElement('p');
        p.textContent = str;
        return p.innerHTML;
    };

    /**
     * Gerencia a visibilidade do spinner de carregamento.
     */
    const toggleLoading = (isLoading) => {
        const loader = document.getElementById('dashboard-loader');
        const content = document.querySelector('.main-content');
        if (!loader || !content) return;
        
        if (isLoading) {
            loader.classList.remove('d-none');
            content.classList.add('loading-fade');
        } else {
            loader.classList.add('d-none');
            content.classList.remove('loading-fade');
        }
    };

    /**
     * Exibe banner de erro amigável ao usuário.
     */
    const showError = (message) => {
        const container = document.getElementById('error-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="alert alert-danger d-flex align-items-center gap-3 rounded-4 shadow-sm border-0" role="alert">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <div>
                    <h4 class="h6 mb-1 fw-bold">Ops! Algo deu errado</h4>
                    <p class="mb-0 small">${escapeHTML(message)}</p>
                </div>
                <button class="btn btn-sm btn-outline-danger ms-auto rounded-3" onclick="location.reload()">Tentar Novamente</button>
            </div>
        `;
        container.classList.remove('d-none');
    };

    const updateTrendIcon = (elementId, subtitleId, currentVal, previousVal, inverseLogic = false) => {
        const iconContainer = document.getElementById(elementId);
        const subtitleEl = document.getElementById(subtitleId);
        if (!iconContainer || !subtitleEl) return;

        if (!previousVal || previousVal === 0) {
            iconContainer.className = "icon-bg neutral";
            iconContainer.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="5" y1="12" x2="19" y2="12"></line></svg>`;
            subtitleEl.innerText = "Sem histórico";
            return;
        }

        const diff = currentVal - previousVal;
        let perc = ((diff) / Math.abs(previousVal)) * 100;
        
        let isPositiveTrend = diff > 0;
        if (inverseLogic) {
            isPositiveTrend = diff < 0; // for expenses, less is better
        }

        if (diff === 0) {
            iconContainer.className = "icon-bg neutral";
            iconContainer.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="5" y1="12" x2="19" y2="12"></line></svg>`;
            subtitleEl.innerText = "0% vs anterior";
        } else if (isPositiveTrend) {
            iconContainer.className = "icon-bg positive";
            iconContainer.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>`;
            subtitleEl.innerText = `+${Math.abs(perc).toFixed(1)}% vs anterior`;
        } else {
            iconContainer.className = "icon-bg negative";
            iconContainer.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>`;
            subtitleEl.innerText = `-${Math.abs(perc).toFixed(1)}% vs anterior`;
        }
    };

    // --- Data Fetching ---
    const fetchGoldData = async () => {
        toggleLoading(true);
        try {
            const reqResumo = fetch('Dados/3_Gold/resumo_mensal.json');
            const reqDespesa = fetch('Dados/3_Gold/detalhado_despesa.json');
            const reqRenda = fetch('Dados/3_Gold/detalhado_renda.json');

            const [resResumo, resDespesa, resRenda] = await Promise.all([reqResumo, reqDespesa, reqRenda]);
            
            if (!resResumo.ok || !resDespesa.ok || !resRenda.ok) throw new Error("Não foi possível carregar os arquivos de dados Gold.");

            goldResumo = await resResumo.json();
            goldDespesas = await resDespesa.json();
            goldRenda = await resRenda.json();

            if (goldResumo.length > 0) {
                // Populate the Month Filter Dropdown
                populateMonthFilter();
                
                // Set default to current month if exists, else latest available
                const now = new Date();
                const currentMonthStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`;
                const hasCurrentMonth = goldResumo.some(d => d.Data_Competencia === currentMonthStr);
                
                monthFilter.value = hasCurrentMonth ? currentMonthStr : goldResumo[goldResumo.length - 1].Data_Competencia;
                
                updateFilteredData();
                initDashboard();

                // Add Event Listener for future changes
                monthFilter.addEventListener('change', () => {
                    updateFilteredData();
                    initDashboard();
                });
            }

        } catch (error) {
            console.error("Erro na leitura Gold:", error);
            showError(error.message);
        } finally {
            toggleLoading(false);
        }
    };

    const populateMonthFilter = () => {
        monthFilter.innerHTML = '';
        // Add options in reverse order (newest first)
        [...goldResumo].reverse().forEach(item => {
            const option = document.createElement('option');
            option.value = item.Data_Competencia; // ex: 2024-11-01
            option.textContent = `${item.Mes_Sigla} - ${item.Ano}`;
            monthFilter.appendChild(option);
        });
    };

    const updateFilteredData = () => {
        const selectedDate = monthFilter.value;
        const selectedIndex = goldResumo.findIndex(d => d.Data_Competencia === selectedDate);
        
        if (selectedIndex !== -1) {
            currentMonthData = goldResumo[selectedIndex];
            
            // 7 Months ending at selected month (inclusive)
            let startIdx7 = Math.max(0, selectedIndex - 6);
            last7MonthsData = goldResumo.slice(startIdx7, selectedIndex + 1);

            // 12 Months strictly LESS than selected month
            let startIdx12 = Math.max(0, selectedIndex - 12);
            rolling12MonthsResumo = goldResumo.slice(startIdx12, selectedIndex);
        }
    };

    // --- Initialization Coordinator ---
    const initDashboard = () => {
        if (!currentMonthData) return;
        updateTopMetrics();
        initLineChart();
        initHorizontalBarChart();
        initProfitTrendChart();
        initRegionalChart();
        initDoughnutChart();
    };

    // --- 1. Top Metrics ---
    const updateTopMetrics = () => {
        const selectedIndex = goldResumo.findIndex(d => d.Data_Competencia === currentMonthData.Data_Competencia);
        const prevMonthData = selectedIndex > 0 ? goldResumo[selectedIndex - 1] : null;

        // 1. Revenue
        const revEl = document.getElementById('metric-revenue-val');
        if (revEl) revEl.innerText = formatCurrency(currentMonthData.Total_Renda);
        const revHistory = last7MonthsData.map(d => d.Total_Renda);
        drawSparkline('sparklineRevenue', revHistory, chartDefaults.greenLine);

        // 2. Profit Margin
        const calculateMargin = (d) => d.Total_Renda > 0 ? (d.Saldo / d.Total_Renda) * 100 : 0;
        const currentMargin = calculateMargin(currentMonthData);
        const marginEl = document.getElementById('metric-margin-val');
        if (marginEl) marginEl.innerText = `${currentMargin.toFixed(1)}%`;
        const marginHistory = last7MonthsData.map(d => calculateMargin(d));
        drawSparkline('sparklineProfit', marginHistory, chartDefaults.greenLine);

        // 3. Saldo Liquido (EBITDA override)
        const saldoEl = document.getElementById('metric-saldo-val');
        if (saldoEl) saldoEl.innerText = formatCurrency(currentMonthData.Saldo);
        const saldoHistory = last7MonthsData.map(d => d.Saldo);
        drawSparkline('sparklineEBITDA', saldoHistory, chartDefaults.redLine);

        // 4. Growth Rate logic removed per user request


        // 5. Debt (Dívida Não Paga)
        const currentMonthPrefix = currentMonthData.Data_Competencia.substring(0, 7);
        const currentMonthExpenses = goldDespesas.filter(d => {
            const dateStr = d.Data_Referencia || d.Data_Competencia;
            return dateStr && dateStr.startsWith(currentMonthPrefix);
        });
        
        const currentDebt = currentMonthExpenses.filter(d => d.Status === "Não Pago" || d.Status === "N\u00e3o Pago").reduce((sum, d) => sum + d.Valor, 0);
        
        const debtValEl = document.getElementById('metric-debt-val');
        if (debtValEl) {
            debtValEl.innerText = formatCurrency(currentDebt);
        }
        
        // Debt Sparkline history
        const debtHistory = last7MonthsData.map(resumoObj => {
            const prefix = resumoObj.Data_Competencia.substring(0, 7);
            const monthExps = goldDespesas.filter(d => {
                const dateStr = d.Data_Referencia || d.Data_Competencia;
                return dateStr && dateStr.startsWith(prefix);
            });
            return monthExps.filter(d => d.Status === "Não Pago" || d.Status === "N\u00e3o Pago").reduce((sum, d) => sum + d.Valor, 0);
        });
        
        const sparkDebtEl = document.getElementById('sparklineDebt');
        if (sparkDebtEl) {
            drawSparkline('sparklineDebt', debtHistory.length > 1 ? debtHistory : [0,0,0], chartDefaults.redLine);
        }

        // 6. Paid Debt (Dívida Paga no Mês)
        const currentPaid = currentMonthExpenses.filter(d => d.Status === "Pago").reduce((sum, d) => sum + d.Valor, 0);
        
        const paidValEl = document.getElementById('metric-paid-val');
        if (paidValEl) {
            paidValEl.innerText = formatCurrency(currentPaid);
        }
        
        // Paid Debt Sparkline history
        const paidHistory = last7MonthsData.map(resumoObj => {
            const prefix = resumoObj.Data_Competencia.substring(0, 7);
            const monthExps = goldDespesas.filter(d => {
                const dateStr = d.Data_Referencia || d.Data_Competencia;
                return dateStr && dateStr.startsWith(prefix);
            });
            return monthExps.filter(d => d.Status === "Pago").reduce((sum, d) => sum + d.Valor, 0);
        });
        
        const sparkPaidEl = document.getElementById('sparklinePaid');
        if (sparkPaidEl) {
            drawSparkline('sparklinePaid', paidHistory.length > 1 ? paidHistory : [0,0,0], chartDefaults.greenLine);
        }
    };

    const drawSparkline = (id, data, color) => {
        if (!document.getElementById(id)) return;
        if (charts.sparklines[id]) charts.sparklines[id].destroy();
        
        const minVal = Math.min(...data);
        const maxVal = Math.max(...data);
        const range = maxVal - minVal;
        const padding = range === 0 ? 1 : range * 0.15;

        charts.sparklines[id] = new Chart(document.getElementById(id), {
            type: 'line',
            data: {
                labels: Array(data.length).fill(''),
                datasets: [{
                    data: data,
                    borderColor: color,
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } },
                scales: {
                    x: { display: false },
                    y: { 
                        display: false, 
                        min: minVal - padding, 
                        max: maxVal + padding 
                    }
                },
                layout: { padding: { top: 2, bottom: 2, left: 2, right: 2 } }
            }
        });
    };

    // --- 2. Revenue vs Target ---
    // User requested last 12 months strictly less than filtered month
    const initLineChart = () => {
        const labels = rolling12MonthsResumo.map(d => `${d.Mes_Sigla} - ${d.Ano}`);
        const actual = rolling12MonthsResumo.map(d => d.Total_Renda);
        const expenses = rolling12MonthsResumo.map(d => d.Total_Despesa);
        
        // Mock target values = previous month's revenue * 1.05
        const projected = [];
        // Look back one more month for the initial target base if available
        let firstIdx = goldResumo.findIndex(d => 
            rolling12MonthsResumo.length > 0 && 
            rolling12MonthsResumo[0] && 
            d.Data_Competencia === rolling12MonthsResumo[0].Data_Competencia
        );
        let prev = firstIdx > 0 ? goldResumo[firstIdx - 1].Total_Renda : 0;
        
        rolling12MonthsResumo.forEach(d => {
            if (d) {
                projected.push(prev * 1.05);
                prev = d.Total_Renda;
            }
        });

        if (charts.revenueTarget) charts.revenueTarget.destroy();
        charts.revenueTarget = new Chart(document.getElementById('revenueTargetChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Receita',
                        data: actual,
                        borderColor: chartDefaults.colorMain,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 2
                    },
                    {
                        label: 'Despesa',
                        data: expenses,
                        borderColor: chartDefaults.redLine,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 2
                    },
                    {
                        label: 'Meta Projetada',
                        data: projected,
                        borderColor: chartDefaults.greyLine,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 0,
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    };

    // --- 3. Expense Breakdown (Tipo_Pagamento) ---
    // User requested last 12 months strictly less than filtered month
    const initHorizontalBarChart = () => {
        const rollingMonthsPrefixes = rolling12MonthsResumo.map(d => d.Data_Competencia ? d.Data_Competencia.substring(0, 7) : "");
        const rollingExpenses = goldDespesas.filter(d => {
            const dateStr = d.Data_Referencia || d.Data_Competencia;
            return dateStr && rollingMonthsPrefixes.includes(dateStr.substring(0, 7));
        });
        
        let typeMap = {};
        rollingExpenses.forEach(exp => {
            const type = exp.Tipo_Pagamento || "Outros";
            typeMap[type] = (typeMap[type] || 0) + exp.Valor;
        });

        // if empty window OR no data found in window, fallback to current month
        if(Object.keys(typeMap).length === 0) {
            const currentPrefix = currentMonthData ? currentMonthData.Data_Competencia.substring(0, 7) : "";
            const currentMonthExpenses = goldDespesas.filter(d => {
                const dateStr = d.Data_Referencia || d.Data_Competencia;
                return dateStr && dateStr.startsWith(currentPrefix);
            });
            currentMonthExpenses.forEach(exp => {
                const type = exp.Tipo_Pagamento || "Outros";
                typeMap[type] = (typeMap[type] || 0) + exp.Valor;
            });
        }

        const sortedTypes = Object.keys(typeMap).sort((a,b) => typeMap[b] - typeMap[a]).slice(0, 5); // top 5
        const vals = sortedTypes.map(t => typeMap[t]);

        if (charts.expenseCategory) charts.expenseCategory.destroy();
        charts.expenseCategory = new Chart(document.getElementById('expenseChart'), {
            type: 'bar',
            data: {
                labels: sortedTypes,
                datasets: [{
                    data: vals,
                    backgroundColor: chartDefaults.colorMain,
                    barPercentage: 0.4,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { display: false },
                    y: { grid: { display: false }, ticks: { color: chartDefaults.colorMain, font: { weight: 500 } } }
                }
            }
        });
    };

    // --- 4. Profit Margin Trend ---
    // User requested last 12 months strictly less than filtered month
    const initProfitTrendChart = () => {
        const labels = rolling12MonthsResumo.map(d => `${d.Mes_Sigla} - ${d.Ano}`);
        const margins = rolling12MonthsResumo.map(d => d.Total_Renda > 0 ? (d.Saldo / d.Total_Renda) * 100 : 0);

        if (charts.profitTrend) charts.profitTrend.destroy();
        charts.profitTrend = new Chart(document.getElementById('profitTrendChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data: margins,
                    label: 'Margem %',
                    borderColor: chartDefaults.colorMain,
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 3,
                    backgroundColor: chartDefaults.blueFill,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: false },
                    x: { grid: { display: false } }
                }
            }
        });
    };

    // --- 5. Regional Comparison -> Income Vs Expense History (Bar) ---
    // User requested last 12 months strictly less than filtered month
    const initRegionalChart = () => {
        const labels = rolling12MonthsResumo.map(d => `${d.Mes_Sigla} - ${d.Ano}`);
        const incomes = rolling12MonthsResumo.map(d => d.Total_Renda);
        const expenses = rolling12MonthsResumo.map(d => d.Total_Despesa);

        if (charts.regionalComparison) charts.regionalComparison.destroy();
        charts.regionalComparison = new Chart(document.getElementById('regionalChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Receitas',
                        data: incomes,
                        backgroundColor: chartDefaults.greyLine,
                        barPercentage: 0.6,
                        categoryPercentage: 0.6,
                        borderRadius: 4
                    },
                    {
                        label: 'Despesas',
                        data: expenses,
                        backgroundColor: chartDefaults.colorMain,
                        barPercentage: 0.6,
                        categoryPercentage: 0.6,
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
                scales: {
                    y: { beginAtZero: true },
                    x: { grid: { display: false } }
                }
            }
        });
    };

    // --- 6. Top Income Sources List ---
    // Filtered by 12 months rolling strictly less than selected month
    const updateTopIncomeList = () => {
        const rollingMonthsPrefixes = rolling12MonthsResumo.map(d => d.Data_Competencia.substring(0, 7));
        
        let monthIncomes = goldRenda.filter(d => {
            const dateStr = d.Data_Referencia || d.Data_Competencia;
            return dateStr && rollingMonthsPrefixes.some(p => dateStr.startsWith(p));
        });
        
        // If empty fallback to current month to avoid blank UI
        if (monthIncomes.length === 0) {
           const currentPrefix = currentMonthData.Data_Competencia.substring(0, 7);
           monthIncomes = goldRenda.filter(d => {
               const dateStr = d.Data_Referencia || d.Data_Competencia;
               return dateStr && dateStr.startsWith(currentPrefix);
           });
        }

        const incomeMap = {};
        monthIncomes.forEach(inc => {
            const item = inc.Item || "Vários";
            incomeMap[item] = (incomeMap[item] || 0) + inc.Valor;
        });

        const sortedIncomes = Object.keys(incomeMap).sort((a,b) => incomeMap[b] - incomeMap[a]).slice(0, 4);

        const listEl = document.getElementById('top-income-list');
        listEl.innerHTML = '';
        
        if (sortedIncomes.length === 0) {
            listEl.innerHTML = '<li class="text-muted small ps-3">Nenhuma fonte de renda neste período</li>';
            return;
        }

        const dotClasses = ['grey-dot', 'dark-dot', 'blue-dot', 'light-dot'];

        sortedIncomes.forEach((item, index) => {
            const val = incomeMap[item];
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="list-item-left">
                    <span class="dot ${dotClasses[index % dotClasses.length]}"></span>
                    <span>${escapeHTML(item)}</span>
                </div>
                <span class="list-value">${formatCurrency(val)}</span>
            `;
            listEl.appendChild(li);
        });
    };

    // --- 7. Contribution (Bar Chart requested) ---
    const initDoughnutChart = () => {
        const rollingMonthsPrefixes = rolling12MonthsResumo.map(d => d.Data_Competencia.substring(0, 7));
        
        let monthIncomes = goldRenda.filter(d => {
            const dateStr = d.Data_Referencia || d.Data_Competencia;
            return dateStr && rollingMonthsPrefixes.some(p => dateStr.startsWith(p));
        });
        
        if (monthIncomes.length === 0) {
            const currentPrefix = currentMonthData.Data_Competencia.substring(0, 7);
            monthIncomes = goldRenda.filter(d => {
                const dateStr = d.Data_Referencia || d.Data_Competencia;
                return dateStr && dateStr.startsWith(currentPrefix);
            });
        }

        const incomeMap = {};
        monthIncomes.forEach(inc => {
            const item = inc.Item || "Vários";
            incomeMap[item] = (incomeMap[item] || 0) + inc.Valor;
        });

        const sortedIncomes = Object.keys(incomeMap).sort((a,b) => incomeMap[b] - incomeMap[a]).slice(0, 5);
        const dataVals = sortedIncomes.map(key => incomeMap[key]);

        const container = document.getElementById('doughnut-container');
        if (!container) return;

        // User requested values in the chart, and specifically "grafico de barras"
        // We will convert the doughnut container area to a clean horizontal ranked list or bar chart
        container.innerHTML = `<div class="w-100 d-flex flex-column gap-2 py-2" id="income-distribution-bars"></div>`;
        const barContainer = document.getElementById('income-distribution-bars');

        const colors = [chartDefaults.colorMain, chartDefaults.greyLine, chartDefaults.blueLine, '#94a3b8', '#cbd5e1'];

        sortedIncomes.forEach((item, index) => {
            const val = incomeMap[item];
            const maxVal = Math.max(...dataVals);
            const percentage = maxVal > 0 ? (val / maxVal) * 100 : 0;
            
            const div = document.createElement('div');
            div.className = 'w-100 mb-1';
            div.innerHTML = `
                <div class="d-flex justify-content-between mb-1" style="font-size: 0.75rem;">
                    <span class="text-truncate fw-medium" style="max-width: 140px;">${escapeHTML(item)}</span>
                    <span class="text-muted">${formatCurrency(val)}</span>
                </div>
                <div class="progress" style="height: 6px; background-color: #f1f5f9;">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${percentage}%; background-color: ${colors[index % colors.length]}; border-radius: 3px;"></div>
                </div>
            `;
            barContainer.appendChild(div);
        });
    };
    fetchGoldData();
});
