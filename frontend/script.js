const API = "http://localhost:8000";

let carrinho = [];

// CARREGA APENAS IDs DOS PRODUTOS
async function carregarProdutos() {
    const res = await fetch(`${API}/produtos/`);
    const produtos = await res.json();

    const select = document.getElementById("produto");
    select.innerHTML = "";

    produtos.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `Produto ID ${p.id}`;
        select.appendChild(opt);
    });
}

// ADICIONA AO CARRINHO
function adicionarCarrinho() {
    const produtoId = Number(document.getElementById("produto").value);
    const quantidade = Number(document.getElementById("quantidade").value);
    const preco = Number(document.getElementById("preco").value);

    if (!produtoId || quantidade <= 0 || preco <= 0) {
        alert("Preencha todos os campos corretamente.");
        return;
    }

    carrinho.push({
        produto_id: produtoId,
        quantidade,
        preco_unitario: preco
    });

    atualizarCarrinho();
}

// ATUALIZA TABELA
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

// FINALIZA VENDA
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
            Venda registrada! Total calculado pelo banco: R$ ${data.total}
        </p>
    `;

    carrinho = [];
    atualizarCarrinho();
}

// INIT
carregarProdutos();
