const formularioDados = document.querySelector("#formulario-dados");
const btnCadastrar = document.querySelector("#btn-cadastrar");
const resultadosDiv = document.querySelector("#resultados table tbody");

// Função para formatar a data no padrão brasileiro (DD/MM/AAAA)
function formatarData(data) {
    const dataObj = new Date(data);
    const dia = String(dataObj.getDate()).padStart(2, '0');
    const mes = String(dataObj.getMonth() + 1).padStart(2, '0');
    const ano = dataObj.getFullYear();
    return `${dia}/${mes}/${ano}`;
}

// Função para buscar os dados do servidor e preencher a tabela
function buscarDados() {
    fetch('/diarias', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao buscar os dados.');
        }
        return response.json();
    })
    .then(data => {
        // Limpa a tabela antes de preencher com os novos dados
        resultadosDiv.innerHTML = '';

        data.forEach(item => {
            const novaLinha = document.createElement("tr");
            novaLinha.innerHTML = `
                <td>${formatarData(item.dia)}</td>
                <td>${item.km_rodados ? item.km_rodados.toFixed(2) : ''}</td>
                <td>${item.horas_trabalhadas ? item.horas_trabalhadas.toFixed(2) : ''}</td>
                <td>${item.ganhos ? item.ganhos.toFixed(2) : ''}</td>
                <td>${item.combustivel ? item.combustivel.toFixed(2) : ''}</td>
                <td>${item.almoco ? item.almoco.toFixed(2) : ''}</td>
                <td>${item.manutencao ? item.manutencao.toFixed(2) : ''}</td>
                <td>${item.seguro ? item.seguro.toFixed(2) : ''}</td>
                <td>${item.financ ? item.financ.toFixed(2) : ''}</td>
                <td>${item.pro_labore ? item.pro_labore.toFixed(2) : ''}</td>
                <td>${item.despesas_totais ? item.despesas_totais.toFixed(2) : ''}</td>
                <td>${item.lucro ? item.lucro.toFixed(2) : ''}</td>
            `;
            resultadosDiv.appendChild(novaLinha);
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao buscar os dados.');
        });
    }

    // Chamar a função para buscar os dados ao carregar a página
    buscarDados();

    btnCadastrar.addEventListener("click", (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        // Obter valores do formulário
        const dia = document.querySelector("#dia").value;
        const km_rodados = parseFloat(document.querySelector("#km_rodados").value);
        const horas_trabalhadas = parseFloat(document.querySelector("#horas_trabalhadas").value;
        const combustivel = parseFloat(document.querySelector("#combustivel").value);
        const almoco = parseFloat(document.querySelector("#almoco").value);
        const manutencao = parseFloat(document.querySelector("#manutencao").value);
        const seguro = parseFloat(document.querySelector("#seguro").value);
        const financ = parseFloat(document.querySelector("#financ").value);
        const pro_labore = parseFloat(document.querySelector("#pro_labore").value);

        // Validar os campos do formulário
        if (!dia || isNaN(km_rodados) || isNaN(horas_trabalhadas) || isNaN(combustivel) ||
            isNaN(almoco) || isNaN(manutencao) || isNaN(seguro) || isNaN(financ) || isNaN(pro_labore)) {
            alert("Por favor, preencha todos os campos corretamente.");
            return; // Impede o envio do formulário se a validação falhar
        }

        // Enviar dados para o servidor
        fetch('/diarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded' // Enviar como dados de formulário
            },
            body: new URLSearchParams({
                dia: dia,
                km_rodados: km_rodados,
                horas_trabalhadas: horas_trabalhadas,
                combustivel: combustivel,
                almoco: almoco,
                manutencao: manutencao,
                seguro: seguro,
                financ: financ,
                pro_labore: pro_labore
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao salvar os dados.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados salvos:', data);
            alert('Dados salvos com sucesso!');
            formularioDados.reset();
            buscarDados(); // Atualiza a tabela com os dados mais recentes
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao salvar os dados.');
        });
    });