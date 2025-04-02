const formularioDados = document.querySelector("#formulario-dados");
const btnCadastrar = document.querySelector("#btn-cadastrar");
const resultadosDiv = document.querySelector("#resultados table tbody"); // Selecionamos o tbody

btnCadastrar.addEventListener("click", () => {
    // Obter valores do formulário
    const dia = document.querySelector("#dia").value;
    const km_rodados = parseFloat(document.querySelector("#km_rodados").value);
    const horas_trabalhadas = parseFloat(document.querySelector("#horas_trabalhadas").value);

    // Calcular ganhos
    const ganhos = (horas_trabalhadas === 0) ? 0 : km_rodados * 1.89 / horas_trabalhadas;

    // Criar a nova linha da tabela
    const novaLinha = document.createElement("tr");
    novaLinha.innerHTML = `
        <td>${dia}</td>
        <td>${km_rodados}</td>
        <td>${horas_trabalhadas}</td>
        <td>${ganhos.toFixed(2)}</td>
        <td></td> <td>25</td> <td>14</td> <td>17</td> <td>82</td> <td>75</td> <td></td> <td></td> `;

    // Adicionar a linha na tabela
    resultadosDiv.appendChild(novaLinha);

    // Limpar o formulário
    formularioDados.reset();
});