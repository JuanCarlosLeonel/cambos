// gerar cores aleaorias
function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }
    return [bg_color, border_color];
}


// grafico de despesa mensal
function renderiza_despesa_mensal(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.getElementById('despesa_mensal').getContext('2d');
        var cores_despesa_mensal = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Despesas Mensais",
                    data: data.data,
                    backgroundColor: cores_despesa_mensal[0],
                    borderColor: cores_despesa_mensal[1],
                    borderWidth: 1
                }]
            },  
        });
    })
}


// Despesa por veiculo(ABASTECIMENTO)
function renderiza_abastecimento_porveiculo(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.getElementById('despesa_abastecimento_porveiculo').getContext('2d');
        var cores_abastecimento = gera_cor(qtd=7)
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Despesas',
                    data: data.data,
                    backgroundColor: cores_abastecimento[0],
                    borderColor: cores_abastecimento[1],
                    borderWidth: 1
                }]
            }, 
        });
    }) 
}


// Despesa por veiculo(MANUTENÇÃO)
function renderiza_manutencao_porveiculo(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        const ctx = document.getElementById('despesa_manutencao_porveiculo').getContext('2d');
        var cores_manutencao = gera_cor(qtd=7)
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Despesas',
                    data: data.data,
                    backgroundColor: cores_manutencao[0],
                    borderColor: cores_manutencao[1],
                    borderWidth: 1
                }]
            }, 
        });
    }) 
}