const API = "http://localhost:8000";

let carrinho = [];

function adicionarCarrinho() {
    const produtoId = Number(document.getElementById("produto").value);
    const quantidade = Number(document.getElementById("quantidade").value);
    const preco = Number(document.getElementById("preco").value);

    if (produtoId <= 0 || quantidade <= 0 || preco <= 0) {
        alert("Dados inválidos.");
        return;
    }

    carrinho.push({
        produto_id: produtoId,
        quantidade: quantidade,
        preco_unitario: preco
    });

    atualizarCarrinho();
}

function atualizarCarrinho() {
    const tbody = document.getElementById("lista-carrinho");
    tbody.innerHTML = "";

    let total = 0;

    carrinho.forEach(item => {
        const subtotal = item.quantidade * item.preco_unitario;
        total += subtotal;

        tbody.innerHTML += `
            <tr>
                <td>${item.produto_id}</td>
                <td>${item.quantidade}</td>
                <td>R$ ${item.preco_unitario}</td>
                <td>R$ ${subtotal}</td>
            </tr>
        `;
    });

    document.getElementById("total").innerText =
        `Total: R$ ${total.toFixed(2)}`;
}

async function finalizarVenda() {
    if (carrinho.length === 0) {
        alert("Carrinho vazio.");
        return;
    }

    const venda = {
        cliente_id: Number(document.getElementById("cliente").value),
        vendedor_id: Number(document.getElementById("vendedor").value),
        metodo_pagamento: document.getElementById("pagamento").value,
        itens: carrinho
    };

    const res = await fetch(`${API}/vendas/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(venda)
    });

    const data = await res.json();

    document.getElementById("resultado").innerHTML = `
        <p style="color:#00e676;">
            Venda registrada! Total: R$ ${data.total}
        </p>
    `;

    carrinho = [];
    atualizarCarrinho();
}
