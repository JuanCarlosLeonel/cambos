let pcp = document.getElementById("editar")
let form = document.getElementById("form")


window.onload = function(){
    let opcoes = ''
    let resposta = []
    for (var i = 0; i < processo.length; i++) {
        opcoes += `<div class="form-check">
                        <input type="checkbox" class="form-check-input" id="exampleCheck1">
                        <label class="form-check-label text-success" for="exampleCheck1">${i +1 }</label>
                        <label class="form-check-label" for="exampleCheck1">${processo[i].fields.nome}    </label>
                    </div> `
      }
      form.innerHTML= opcoes
    resposta.push(
        {
            "lacre":pedido.Lacre,
            'prazo':pedido.DataEntrega
        }
    )
    
    pcp.value = JSON.stringify(resposta)
}