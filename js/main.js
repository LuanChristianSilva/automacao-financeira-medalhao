document.addEventListener('DOMContentLoaded', () => {
    // Dados mockados de transações para o dashboard
    const transactions = [
        { id: 1, title: "Supermercado", date: "Hoje, 14:30", amount: -250.00, type: "expense" },
        { id: 2, title: "Salário", date: "Ontem, 09:00", amount: 5000.00, type: "income" },
        { id: 3, title: "Conta de Luz", date: "05 Mar, 10:15", amount: -120.50, type: "expense" },
        { id: 4, title: "Freelance", date: "02 Mar, 16:45", amount: 1500.00, type: "income" }
    ];

    const transactionList = document.getElementById('transactionList');

    // Função para formatar moeda (Real)
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    // Renderiza a lista de transações na interface
    const renderTransactions = () => {
        transactionList.innerHTML = ''; // Limpa a lista existente

        transactions.forEach(transaction => {
            const item = document.createElement('div');
            item.className = 'transaction-item';
            
            const isPositive = transaction.type === 'income';
            const amountClass = isPositive ? 'positive' : 'negative';
            const amountSign = isPositive ? '+' : '';

            item.innerHTML = `
                <div class="transaction-info">
                    <p>${transaction.title}</p>
                    <span>${transaction.date}</span>
                </div>
                <div class="transaction-amount ${amountClass}">
                    ${amountSign}${formatCurrency(transaction.amount)}
                </div>
            `;
            
            transactionList.appendChild(item);
        });
    };

    // Inicializa a renderização
    renderTransactions();

    /* 
     * O bloco de código acima gerencia a exibição dinâmica de transações na interface.
     * Conforme a regra de adicionar comentários explicativos.
    */

    // Event Listener para simular a adição de transação
    const btn = document.getElementById('addTransactionBtn');
    if (btn) {
        btn.addEventListener('click', () => {
            alert('A funcionalidade de adicionar transação estaria aqui!');
        });
    }
});
