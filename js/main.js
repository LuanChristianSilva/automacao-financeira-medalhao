document.addEventListener('DOMContentLoaded', () => {
    
    // Configurações do ChartJS (cores que combinam com o CSS)
    const CHART_COLORS = {
        income: '#6366f1',  // var(--accent-color)
        expense: '#ef4444', // var(--negative)
        gridLines: 'rgba(255, 255, 255, 0.05)',
        text: '#9094a6'     // var(--text-secondary)
    };

    let globalResumoData = [];
    let globalDespesasData = [];
    let cashflowChartInstance = null;
    const monthFilter = document.getElementById('monthFilter');

    // Função auxiliar formato moeda
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    // 1. Fetching dos dados Gold JSON
    const fetchGoldData = async () => {
        try {
            const resumoReq = await fetch('Dados/3_Gold/resumo_mensal.json');
            const despesasReq = await fetch('Dados/3_Gold/detalhado_despesa.json');

            if (!resumoReq.ok || !despesasReq.ok) {
                throw new Error("Não foi possível carregar os arquivos JSON.");
            }

            globalResumoData = await resumoReq.json();
            globalDespesasData = await despesasReq.json();

            if(globalResumoData.length > 0) {
                populateMonthFilter();
                // O último mês é renderizado por padrão
                const lastIndex = globalResumoData.length - 1;
                renderDashboard(lastIndex);
            }

        } catch (error) {
            console.error("Erro ao consumir a camada Gold:", error);
            document.getElementById('overview-saldo').innerText = "Erro no Carregamento";
        }
    };

    // Popula o dropdown com os meses
    const populateMonthFilter = () => {
        monthFilter.innerHTML = '';
        globalResumoData.forEach((monthData, index) => {
            const option = document.createElement('option');
            option.value = index;
            // Ex: "MAR 2026"
            option.text = `${monthData.Mes_Sigla} ${monthData.Ano}`;
            // Seleciona o último mês por padrão
            if (index === globalResumoData.length - 1) {
                option.selected = true;
            }
            monthFilter.appendChild(option);
        });

        // Event listener para quando o usuário trocar o mês no dropdown
        monthFilter.addEventListener('change', (e) => {
            const selectedIndex = parseInt(e.target.value);
            renderDashboard(selectedIndex);
        });
    };

    // Agrupa as chamadas de renderização baseadas no índice
    const renderDashboard = (index) => {
        updateOverviewCards(index);
        renderChart(index);
        
        // Pega o Ano-Mes selecionado para filtrar a lista de transações
        const selectedMonthData = globalResumoData[index];
        // Data_Competencia vem como YYYY-MM-DD. Queremos apenas YYYY-MM
        const prefixoAnoMes = selectedMonthData.Data_Competencia.substring(0, 7); 
        renderTransactions(prefixoAnoMes);
    };

    // 2. Atualização dos Overview Cards (Saldo Cima)
    const updateOverviewCards = (index) => {
        const currentMonth = globalResumoData[index];
        const previousMonth = index > 0 ? globalResumoData[index - 1] : null;

        document.getElementById('overview-saldo').innerText = formatCurrency(currentMonth.Saldo);
        document.getElementById('overview-receitas').innerText = formatCurrency(currentMonth.Total_Renda);
        document.getElementById('overview-despesas').innerText = formatCurrency(currentMonth.Total_Despesa);
        
        const economiaPerc = currentMonth.Total_Renda > 0 
            ? ((currentMonth.Saldo / currentMonth.Total_Renda) * 100).toFixed(1) 
            : 0;
        document.getElementById('overview-economias').innerText = `${economiaPerc}%`;

        const applyTrend = (currValue, prevValue, elementId, targetId, inverseLogic = false) => {
            const el = document.getElementById(targetId);
            if (!prevValue || prevValue === 0) {
                el.innerText = "Sem histórico passado";
                el.className = "trend neutral";
                return;
            }
            
            const diff = currValue - prevValue;
            let perc = (Math.abs(diff) / prevValue) * 100;
            perc = perc.toFixed(1);

            if (diff > 0) {
                let isPositiveTrend = inverseLogic ? false : true;
                el.innerText = `↑ ${perc}% vs anterior`;
                el.className = isPositiveTrend ? "trend positive" : "trend negative";
            } else if (diff < 0) {
                 let isPositiveTrend = inverseLogic ? true : false;
                 el.innerText = `↓ ${perc}% vs anterior`;
                 el.className = isPositiveTrend ? "trend positive" : "trend negative";
            } else {
                 el.innerText = `0% vs anterior`;
                 el.className = "trend neutral";
            }
        };

        if(previousMonth) {
             applyTrend(currentMonth.Saldo, previousMonth.Saldo, 'overview-saldo', 'trend-saldo');
             applyTrend(currentMonth.Total_Renda, previousMonth.Total_Renda, 'overview-receitas', 'trend-receitas');
             applyTrend(currentMonth.Total_Despesa, previousMonth.Total_Despesa, 'overview-despesas', 'trend-despesas', true);
             
             const prevPerc = previousMonth.Total_Renda > 0 ? (previousMonth.Saldo / previousMonth.Total_Renda) * 100 : 0;
             const diffPerc = (economiaPerc - prevPerc).toFixed(1);
             const elEcon = document.getElementById('trend-economias');
             if(diffPerc > 0) {
                elEcon.innerText = `↑ ${diffPerc} p.p`;
                elEcon.className = "trend positive";
             } else if (diffPerc < 0) {
                elEcon.innerText = `↓ ${Math.abs(diffPerc)} p.p`;
                elEcon.className = "trend negative";
             } else {
                elEcon.innerText = `Manteve`;
                elEcon.className = "trend neutral";
             }
        } else {
             document.getElementById('trend-saldo').innerText = "--";
             document.getElementById('trend-saldo').className = "trend neutral";
             document.getElementById('trend-receitas').innerText = "--";
             document.getElementById('trend-receitas').className = "trend neutral";
             document.getElementById('trend-despesas').innerText = "--";
             document.getElementById('trend-despesas').className = "trend neutral";
             document.getElementById('trend-economias').innerText = "--";
             document.getElementById('trend-economias').className = "trend neutral";
        }
    };

    // 3. Renderização Dinâmica das Transações Recentes baseada no mês
    const renderTransactions = (prefixoAnoMes) => {
        const transactionList = document.getElementById('transactionList');
        transactionList.innerHTML = '';

        // Filtra despesas apenas do mês/ano correspondente (ex: '2026-03') e ignora nulos
        const monthTransactions = globalDespesasData.filter(t => t.Data_Referencia && t.Data_Referencia.startsWith(prefixoAnoMes));
        
        // Pega as top 5 desse mes
        const recentTrans = monthTransactions.slice(0, 5);

        if (recentTrans.length === 0) {
            transactionList.innerHTML = "<p>Nenhuma transação registrada neste mês.</p>";
            return;
        }

        recentTrans.forEach(trans => {
            const item = document.createElement('div');
            item.className = 'transaction-item';
            
            const amount = parseFloat(trans.Valor);
            const dateObj = new Date(trans.Data_Referencia + "T00:00:00"); 
            const formattedDate = dateObj.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });

            item.innerHTML = `
                <div class="transaction-info">
                    <p>${trans.Item} ${trans.Credor ? `(${trans.Credor})` : ''}</p>
                    <span>${formattedDate} - ${trans.Tipo_Pagamento}</span>
                </div>
                <div class="transaction-amount negative">
                    - ${formatCurrency(amount)}
                </div>
            `;
            transactionList.appendChild(item);
        });
    };

    // 4. Renderização Dinâmica do Gráfico (Chart.js) retroativa
    const renderChart = (index) => {
        // Corta os dados a partir do início até o mês selecionado
        const historicalData = globalResumoData.slice(0, index + 1);
        
        // Limitamos aos 8 meses mais recentes DENTRO desse recorte histórico para caber no gráfico
        const chartDataArray = historicalData.slice(-8);

        const labels = chartDataArray.map(d => `${d.Mes_Sigla} ${d.Ano}`);
        const incomes = chartDataArray.map(d => d.Total_Renda);
        const expenses = chartDataArray.map(d => d.Total_Despesa);

        const ctx = document.getElementById('cashflowChart').getContext('2d');
        
        // Destroi o chart anterior caso já exista para recriar as barras
        if (cashflowChartInstance) {
            cashflowChartInstance.destroy();
        }

        cashflowChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Receitas',
                        data: incomes,
                        backgroundColor: CHART_COLORS.income,
                        borderRadius: 6,
                        barPercentage: 0.6,
                        categoryPercentage: 0.8
                    },
                    {
                        label: 'Despesas',
                        data: expenses,
                        backgroundColor: CHART_COLORS.expense,
                        borderRadius: 6,
                        barPercentage: 0.6,
                        categoryPercentage: 0.8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: CHART_COLORS.text,
                            font: { family: 'Inter' }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(28, 30, 38, 0.9)',
                        titleColor: '#fff',
                        bodyColor: CHART_COLORS.text,
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) label += ': ';
                                if (context.parsed.y !== null) label += formatCurrency(context.parsed.y);
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            color: CHART_COLORS.text,
                            callback: function(value) { return 'R$ ' + value; }
                        },
                        grid: { color: CHART_COLORS.gridLines }
                    },
                    x: {
                        ticks: { color: CHART_COLORS.text },
                        grid: { display: false }
                    }
                }
            }
        });
    };

    // Botão Adicional mock
    const btn = document.getElementById('addTransactionBtn');
    if (btn) btn.addEventListener('click', () => { alert('Integração de Escrita de Novas Transações em planejamento!'); });

    // Dispara a coleta e carregamento da primeira página
    fetchGoldData();
});
