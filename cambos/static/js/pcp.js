let pcp = document.getElementById("editar")
let form = document.getElementById("form")


window.onload = function(){
    let opcoes = ''
    let resposta = []
    for (var i = 0; i < processo.length; i++) {
        opcoes += `<div class="">                                
                        <h3 class="text-success " >${i +1 }
                        
                        <span class="text-danger" >${processo[i].fields.nome}    </span>
                        <a class="btn btn-success btn-xs" type="submit" role="button"> u </a>
                        </h3>
                    </div> `
    }
    form.innerHTML= opcoes
    resposta.push(
        [
            {
                "lacre": 112209,
                "prazo": "2021-11-01",
                "processo": [
                    {
                        "etapa": "teset2",
                        "entrada": "2021-11-01",
                        "saida": "2021-11-01"
                    },
                    {
                        "etapa": "teset23",
                        "entrada": "2021-11-01",
                        "saida": "2021-11-01"
                    }
                ]
            },
            {
                "lacre": 112209,
                "prazo": "2021-11-01",
                "processo": [
                    {
                        "etapa": "teset2",
                        "entrada": "2021-11-01",
                        "saida": "2021-11-01"
                    },
                    {
                        "etapa": "teset23",
                        "entrada": "2021-11-01",
                        "saida": "2021-11-01"
                    }
                ]
            }
        ]
    )
    
    pcp.value = JSON.stringify(ordemProcesso)
}