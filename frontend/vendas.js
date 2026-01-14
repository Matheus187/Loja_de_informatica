const API_URL = "http://localhost:8000";

let itensVenda = [];
let editarItens = [];

function mostrarTela(id) {
  document.querySelectorAll(".tela").forEach(t => t.classList.remove("active"));
  document.getElementById(id).classList.add("active");

  if (id === "listar") {
    carregarVendas();
  }
  if (id === "relatorioMaisVendida") {
    carregarCategoriaMaisVendidaTela();
  }

  if (id === "relatorioMaisProdutos") {
    carregarCategoriaComMaisProdutosTela();
  }

}

// Garantir que handlers referenciados por `onclick` inline estejam disponíveis globalmente
if (typeof window !== 'undefined') {
  window.mostrarTela = mostrarTela;
  window.adicionarItem = adicionarItem;
  window.salvarVenda = salvarVenda;
  window.abrirEditarVenda = abrirEditarVenda;
  window.adicionarItemEdicao = adicionarItemEdicao;
  window.salvarEdicao = salvarEdicao;
  window.deletarVendaEdicao = deletarVendaEdicao;
  
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

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || "Erro HTTP ao criar venda");
    }

    alert("Venda cadastrada com sucesso!");
    itensVenda = [];
    atualizarLista();
    // se estiver na tela de listagem, atualizar
    if (document.getElementById('listar').classList.contains('active')) {
      carregarVendas();
    }

  } catch {
    alert("Erro ao salvar venda");
  }
}

async function carregarVendas() {
  const tabela = document.getElementById("tabelaVendas");
  tabela.innerHTML = "";
  try {
    const res = await fetch(`${API_URL}/vendas/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const vendas = await res.json();

    vendas.forEach(v => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${v.id}</td>
        <td>${v.cliente ?? v.cliente}</td>
        <td>${v.vendedor ?? v.vendedor}</td>
        <td>${v.metodo_pagamento}</td>
        <td>${v.total ?? ''}</td>
        <td><button onclick="abrirEditarVenda(${v.id})">Editar</button></td>
      `;
      tabela.appendChild(tr);
    });
  } catch (err) {
    console.error('Erro ao carregar vendas:', err);
    tabela.innerHTML = '<tr><td colspan="6">Erro ao carregar vendas</td></tr>';
  }
}

function produtoIdInput() {
  return document.getElementById("produtoId");
}

function quantidadeInput() {
  return document.getElementById("quantidade");
}

// EDIÇÃO
function abrirEditarVenda(id) {
  fetch(`${API_URL}/vendas/${id}`)
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(data => {
      document.getElementById('editId').value = data.id;
      document.getElementById('clienteIdEdit').value = data.cliente_id || '';
      document.getElementById('vendedorIdEdit').value = data.vendedor_id || '';
      document.getElementById('metodoPagamentoEdit').value = data.metodo_pagamento || '';

      editarItens = [];
      if (Array.isArray(data.itens)) {
        data.itens.forEach(it => {
          editarItens.push({ produto_id: it.produto_id, quantidade: it.quantidade });
        });
      }
      atualizarListaEdicao();
      mostrarTela('editar');
    })
    .catch(err => {
      console.error('Erro ao obter venda:', err);
      alert('Erro ao carregar dados da venda');
    });
}

function adicionarItemEdicao() {
  const pid = Number(document.getElementById('produtoIdEdit').value);
  const qtd = Number(document.getElementById('quantidadeEdit').value);
  if (!pid || !qtd) { alert('Preencha produto e quantidade'); return; }
  editarItens.push({ produto_id: pid, quantidade: qtd });
  atualizarListaEdicao();
  document.getElementById('produtoIdEdit').value = '';
  document.getElementById('quantidadeEdit').value = '';
}

function atualizarListaEdicao() {
  const lista = document.getElementById('listaItensEdit');
  lista.innerHTML = '';
  editarItens.forEach((item, i) => {
    const li = document.createElement('li');
    li.innerHTML = `Produto ${item.produto_id} - Quantidade <input type="number" value="${item.quantidade}" onchange="editarItens[${i}].quantidade = Number(this.value)"> <button onclick="removerItemEdicao(${i})">Remover</button>`;
    lista.appendChild(li);
  });
}

function removerItemEdicao(i) {
  editarItens.splice(i,1);
  atualizarListaEdicao();
}

async function salvarEdicao() {
  const id = Number(document.getElementById('editId').value);
  const payload = {
    cliente_id: Number(document.getElementById('clienteIdEdit').value),
    vendedor_id: Number(document.getElementById('vendedorIdEdit').value),
    metodo_pagamento: document.getElementById('metodoPagamentoEdit').value,
    itens: editarItens
  };
  try {
    const res = await fetch(`${API_URL}/vendas/${id}`, {
      method: 'PUT',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `HTTP ${res.status}`);
    }
    alert('Venda atualizada com sucesso');
    mostrarTela('listar');
  } catch (err) {
    console.error('Erro ao salvar edição:', err);
    alert('Erro ao salvar edição');
  }
}

async function deletarVendaEdicao() {
  const id = Number(document.getElementById('editId').value);
  if (!id) { alert('ID da venda inválido'); return; }
  if (!confirm(`Confirma exclusão da venda ${id}?`)) return;
  try {
    const res = await fetch(`${API_URL}/vendas/${id}`, { method: 'DELETE' });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `HTTP ${res.status}`);
    }
    const data = await res.json().catch(()=>null);
    alert((data && data.message) ? data.message : 'Venda excluída com sucesso');
    mostrarTela('listar');
  } catch (err) {
    console.error('Erro ao deletar venda:', err);
    alert('Erro ao deletar venda');
  }
}

// Carregadores para as telas de relatório
async function carregarCategoriaMaisVendidaTela() {
  const el = document.getElementById('conteudoMaisVendida');
  if (!el) return;
  el.innerHTML = 'Carregando...';
  try {
    const res = await fetch(`${API_URL}/relatorios/categoria-mais-vendida`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.message) { el.innerHTML = `<p>${data.message}</p>`; return; }
    const nome = data.categoria;
    const quantidade = data.total_vendas ?? 0;
    const html = `
      <p><strong>Categoria:</strong> ${nome ?? '—'}</p>
      <p><strong>Total (vendas):</strong> ${Number(quantidade || 0).toLocaleString()}</p>
    `;
    el.innerHTML = html;
  } catch (err) {
    console.error('Erro ao carregar categoria mais vendida:', err);
    el.innerHTML = '<p>Erro ao carregar relatório</p>';
  }
}

async function carregarCategoriaComMaisProdutosTela() {
  const el = document.getElementById('conteudoMaisProdutos');
  if (!el) return;
  el.innerHTML = 'Carregando...';
  try {
    const res = await fetch(`${API_URL}/relatorios/categoria-com-mais-produtos`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.message) { el.innerHTML = `<p>${data.message}</p>`; return; }
    const nome = data.categoria;
    const quantidade = data.total_itens_estoque ?? 0;
    const html = `
      <p><strong>Categoria:</strong> ${nome ?? '—'}</p>
      <p><strong>Quantidade total em estoque:</strong> ${Number(quantidade || 0).toLocaleString()}</p>
    `;
    el.innerHTML = html;
  } catch (err) {
    console.error('Erro ao carregar categoria com mais produtos:', err);
    el.innerHTML = '<p>Erro ao carregar relatório</p>';
  }
}