const API_URL = "http://localhost:8000";

let itensVenda = [];

function mostrarTela(id) {
  document.querySelectorAll(".tela").forEach(t => t.classList.remove("active"));
  document.getElementById(id).classList.add("active");

  if (id === "listar") {
    carregarVendas();
  }
}

function adicionarItem() {
  const produtoId = produtoIdInput().value;
  const quantidade = quantidadeInput().value;

  if (!produtoId || !quantidade) {
    alert("Preencha produto e quantidade");
    return;
  }

  itensVenda.push({
    produto_id: Number(produtoId),
    quantidade: Number(quantidade)
  });

  atualizarLista();
}

function atualizarLista() {
  const lista = document.getElementById("listaItens");
  lista.innerHTML = "";

  itensVenda.forEach(item => {
    const li = document.createElement("li");
    li.textContent = `Produto ${item.produto_id} - Quantidade ${item.quantidade}`;
    lista.appendChild(li);
  });
}

async function salvarVenda() {
  const venda = {
    cliente_id: Number(document.getElementById("clienteId").value),
    vendedor_id: Number(document.getElementById("vendedorId").value),
    metodo_pagamento: document.getElementById("metodoPagamento").value,
    itens: itensVenda
  };

  try {
    const res = await fetch(`${API_URL}/vendas/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(venda)
    });

    if (!res.ok) throw new Error();

    alert("Venda cadastrada com sucesso!");
    itensVenda = [];
    atualizarLista();

  } catch {
    alert("Erro ao salvar venda");
  }
}

async function carregarVendas() {
  const tabela = document.getElementById("tabelaVendas");
  tabela.innerHTML = "";

  const res = await fetch(`${API_URL}/vendas/`);
  const vendas = await res.json();

  vendas.forEach(v => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${v.id}</td>
      <td>${v.cliente_id}</td>
      <td>${v.vendedor_id}</td>
      <td>${v.metodo_pagamento}</td>
    `;
    tabela.appendChild(tr);
  });
}

function produtoIdInput() {
  return document.getElementById("produtoId");
}

function quantidadeInput() {
  return document.getElementById("quantidade");
}
