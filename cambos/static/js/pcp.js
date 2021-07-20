let pcp = document.getElementById("editar")
let form = document.getElementById("form")

function reorder(teste){
    form.innerHTML= teste
 }
 


function const_processos(listaInProcesso){
    let teste = listaInProcesso
    let opcoes = ''
    for (var i = 0; i < listaInProcesso.length; i++) {
        let up = ''
        let down = ''
        if(i>0){
            up = `<button class="btn btn-xs" onclick="reorder(${i})"> <em class="fa fa-angle-up"></em> </button>`
        }
        if(i < listaInProcesso.length -1 ){
            down = `<button class="btn btn-xs" onclick="reorder('down',${i},${listaInProcesso})"> <em class="fa fa-angle-down"></em> </button>`
        }
        opcoes += `<div class="">                          
                        <h3 ><strong class="text-success ">${i +1 }</strong>
                        
                        <span class="" >${listaInProcesso[i].nome}    </span>
                        ${up}
                        ${down}
                        <a class="btn btn-danger btn-xs" type="submit" role="button"> <em class="fa fa-times"></em> </a>
                        </h3>
                    </div> `
    }
    return form.innerHTML= opcoes
}




window.onload = function(){
   
    
    let listaInProcesso = []
    let listaOutProcesso = []
    if (ordemProcesso.processo == 'new'){
        for (var i = 0; i < processo.length; i++) {
            if (processo[i].fields.recorrente){
                listaInProcesso.push({
                    'nome': processo[i].fields.nome,
                    'inicio': ''
                })
            }else{
                listaOutProcesso.push(processo[i].fields.nome)
            }

        }          
    } else{
        listaInProcesso = ordemProcesso.processo        
    }    
    ordemProcesso.processo = listaInProcesso  
    
    const_processos(listaInProcesso)
    
    pcp.value = JSON.stringify(ordemProcesso)
}

