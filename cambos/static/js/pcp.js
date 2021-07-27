let pcp = document.getElementById("editar")
let form = document.getElementById("form")
let out = document.getElementById("out")
let ordemForm = document.getElementById("ordem")

function addProcesso(item){
    var lista = JSON.parse(ordemForm.value)
    lista.push({
        'nome': item,
        'inicio': ''
    })
    ordemForm.value = JSON.stringify(lista)
    ordemProcesso.processo = lista
    pcp.value=JSON.stringify(ordemProcesso)
    lista_out = listOut(lista)
    const_out(lista_out)
    return const_processos(lista)

}

function delProcesso(item){
    lista = JSON.parse(ordemForm.value)
    lista.splice(item, 1)
    lista_out = listOut(lista)
    const_out(lista_out)
    return const_processos(lista)
}

function reorder(ordem, posicao){
    var convert = JSON.parse(ordemForm.value)
    convert.splice(posicao + ordem, 0, convert.splice(posicao, 1)[0]);
    ordemForm.value = JSON.stringify(convert)
    ordemProcesso.processo = convert
    pcp.value=JSON.stringify(ordemProcesso)
    return const_processos(convert)
}


function const_processos(listaInProcesso){    
    let opcoes = ''
    for (var i = 0; i < listaInProcesso.length; i++) {
        let up = ''
        let down = ''
        let clear = `<button class="btn btn-xs" onclick="delProcesso(${i})"> 
                        <em class="fa fa-minus"></em>
                    </button>`
        if(i>0){
            up = `<button class="btn btn-xs" onclick="reorder(-1,${i})">
                    <em class="fa fa-angle-up"></em>
                 </button>`
        }
        if(i < listaInProcesso.length -1 ){
            down = `<button class="btn btn-xs" onclick="reorder(+1,${i})">
                        <em class="fa fa-angle-down"></em> 
                    </button>`
        }
        opcoes += `<div class="">                          
                        <h3 ><strong class="text-success ">${i +1 }</strong>                        
                            <span class="" >${listaInProcesso[i].nome}    </span>
                            ${up}
                            ${down}
                            ${clear}
                        </h3>
                    </div> `
    }        
    return form.innerHTML= opcoes
}

function const_out(listaOutProcesso){
    let opcoes = '<br>Sem Programação'
    for (var i = 0; i < listaOutProcesso.length; i++) {        
        opcoes += `<div class="">                          
                        <h3 ><strong class="">''</strong>                        
                        <span class="" >${listaOutProcesso[i]}    </span>
                        <button class="btn btn-success btn-xs" onclick="addProcesso('${listaOutProcesso[i]}')"> <em class="fa fa-plus"></em> </button>                        
                        </h3>
                    </div> `
    }            
    return out.innerHTML = opcoes
}

function listOut(listaInProcesso){
    let listaOutProcesso = []
    for (let i = 0; i < processo.length; i++) {
        let cont = 0
        for (let x = 0; x < listaInProcesso.length; x++) {
            if (listaInProcesso[x].nome == processo[i].fields.nome){                
                cont = 1
            }               
        }
        if(cont == 0){
            listaOutProcesso.push(processo[i].fields.nome)
        }
    }      
    return listaOutProcesso
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
        listaOutProcesso = listOut(listaInProcesso) 
    }    
    ordemProcesso.processo = listaInProcesso  
    pcp.value = JSON.stringify(ordemProcesso)
    ordemForm.value = JSON.stringify(ordemProcesso.processo)
    const_processos(listaInProcesso)
    const_out(listaOutProcesso) 
}

