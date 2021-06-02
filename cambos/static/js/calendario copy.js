
let adicionar = document.getElementById("adicionar")
let deletar = document.getElementById("deletar")
let original = [] 
let atual = []
let add = []
let del = []


var semana = [
    "Domingo",
    "Segunda-Feira",
    "Terça-Feira",
    "Quarta-Feira",
    "Quinta-Feira",
    "Sexta-Feira",
    "Sábado"
]

var mes = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

function selecionaDia(data) {
    
    let dia = document.getElementById(data)  
    
    if (atual.includes(data)) {
        dia.setAttribute("class", "day off")
        dia.style.fontWeight =  "bold"
        dia.style.backgroundColor =  "#8e342e8c"
        atual.splice((atual.indexOf(data)),1)        
        if (add.includes(data)) {
            add.splice((add.indexOf(data)),1)
        }
        if (original.includes(data)) {  
            if (del.includes(data)) {                          
            } else {
                del.push(data)            
            } 
        }
    } else {
        dia.setAttribute("class", "day on")        
        dia.style.fontWeight =  "bold"
        dia.style.backgroundColor =  "rgba(62, 136, 95, 0.788)"
        atual.push(data)
        if (del.includes(data)) {            
            del.splice((del.indexOf(data)),1)
        }         
        if (original.includes(data)) {                                     
        } else {
            add.push(data)   
        }
    }    
    adicionar.value = add
    deletar.value = del
}

function pad(d) {
    return (d < 10) ? '0' + d.toString() : d.toString();
}

function getDaysInMonth(month, year){
    return new Date(year, month, 0).getDate()
}

function calcular() {        
    let number = window.document.getElementById('txtnumber')    
    let calendar = window.document.getElementById('calendar')    
    calendar.innerHTML = ''
    adicionar.value = ""
    deletar.value = ""    
    for(c = 0; c < 12; c++) {
        var div = document.createElement("DIV")
        div.setAttribute("class", "col-12 col-md-4 col-lg-3 ")
        var table = document.createElement("TABLE")
        var hoje = new Date(number.value, c, 1)
        var diaSemana = hoje.getDay()
        var tMes = getDaysInMonth(c+1, number.value)
        var dia = 0        
        var caption = document.createElement("CAPTION")
        caption.innerHTML += `<caption>${mes[c]}</caption>`
        div.appendChild(caption)
        var trTitulo = document.createElement("THEAD")        
        trTitulo.setAttribute("class","weekdays")                                                     
        trTitulo.innerHTML = `  <thead>
                                    <tr>
                                        <th scope="col">Dom</th>
                                        <th scope="col">Seg</th>
                                        <th scope="col">Ter</th>
                                        <th scope="col">Qua</th>
                                        <th scope="col">Qui</th>
                                        <th scope="col">Sex</th>
                                        <th scope="col">Sab</th>
                                    </tr>
                                </thead>`  
        table.appendChild(trTitulo)
        var body = document.createElement("TBODY")          
        body.setAttribute("class","days")
        
        for(semana = 0; semana < 6; semana++) {
            var linha = document.createElement("TR")
            for(d = 0; d < 7; d++) {                               
                if(semana == 0 && d == diaSemana) {
                    if (atual.includes(`${pad(1)}/${pad(c+1)}/${number.value}`)) {
                        linha.innerHTML += `<td class="day on" id=${pad(1)}/${pad(c+1)}/${number.value}
                                                onclick="selecionaDia('${pad(1)}/${pad(c+1)}/${number.value}')"
                                                style="font-weight: bold; background-color: rgba(62, 136, 95, 0.24);">
                                                <div class="date">1</div>
                                            </td>`                    
                    } else {
                        linha.innerHTML += `<td class="day" id=${pad(1)}/${pad(c+1)}/${number.value}
                                                onclick="selecionaDia('${pad(1)}/${pad(c+1)}/${number.value}')">                                            
                                                <div class="date">1</div>
                                            </td>`                    
                    }
                    dia = 2
                } else if (dia == 0 || dia>tMes) {                
                    linha.innerHTML += `<td class="other-month">
                                            <div class="date">x</div>
                                        </td>`
                } else {             
                        if (atual.includes(`${pad(dia)}/${pad(c+1)}/${number.value}`)) {
                            linha.innerHTML += `<td class="day on" id=${pad(dia)}/${pad(c+1)}/${number.value}
                                                    onclick="selecionaDia('${pad(dia)}/${pad(c+1)}/${number.value}')" 
                                                    style="font-weight: bold; background-color: rgba(62, 136, 95, 0.24);">
                                                    <div class="date">${dia}</div>
                                                </td>`                                    
                        } else {
                            linha.innerHTML += `<td class="day off" id=${pad(dia)}/${pad(c+1)}/${number.value}
                                                    onclick="selecionaDia('${pad(dia)}/${pad(c+1)}/${number.value}')">
                                                    <div class="date">${dia}</div>
                                                </td>`
                        }
                    dia ++
                }
                
            }
            body.appendChild(linha)        
        }
        table.appendChild(body)
        div.appendChild(table)
        calendar.appendChild(div)     
    }
}

function CalculaFalta() {
    let inicioFun       = window.document.getElementById('inicioFun')  
    let fimFun      = window.document.getElementById('fimFun')    
    let duracaoForm     = window.document.getElementById('duracao')
    let duracaoHoraForm = window.document.getElementById('duracaoHora')    
    let tipo            = window.document.getElementById('tipo_falta')
    let inicio          = window.document.getElementById('inicio')
    let fim             = window.document.getElementById('fim')
    let saldoForm       = window.document.getElementById('saldo')
    let saldoHora       = window.document.getElementById('saldo_hora') 
    let saldoDever       = window.document.getElementById('dever')
    
    inicio.value = inicioFun.value
    fim.value = fimFun.value

    let dataInicio  = new Date(`${inicio.value.slice(3,5)} ${inicio.value.slice(0,2)} ${inicio.value.slice(6,10)}GMT-0300`).getTime()
    let dataFim     = new Date(`${fim.value.slice(3,5)} ${fim.value.slice(0,2)} ${fim.value.slice(6,10)}GMT-0300`).getTime()
    let jornInicio  = new Date(`01 01 1970 ${JornadaInicio.slice(11,13)}:${JornadaInicio.slice(14,16)}:00 GMT`).getTime()
    let jornFim     = new Date(`01 01 1970 ${JornadaFim.slice(11,13)}:${JornadaFim.slice(14,16)}:00 GMT`).getTime()
    let intInicio   = new Date(`01 01 1970 ${IntervaloInicio.slice(11,13)}:${IntervaloInicio.slice(14,16)}:00 GMT`).getTime()
    let intFim      = new Date(`01 01 1970 ${IntervaloFim.slice(11,13)}:${IntervaloFim.slice(14,16)}:00 GMT`).getTime()
    let inicioMili  = new Date(`${inicio.value.slice(3,5)} ${inicio.value.slice(0,2)} ${inicio.value.slice(6,16)}`).getTime()
    let fimMili     = new Date(`${fim.value.slice(3,5)} ${fim.value.slice(0,2)} ${fim.value.slice(6,16)}`).getTime()
    let horaInicio  = (inicio.value.slice(11,13)*3600 + inicio.value.slice(14,16)*60)*1000
    let horaFim     = (fim.value.slice(11,13)*3600 + fim.value.slice(14,16)*60)*1000
    let duracaoDia  = 0
    let duracaoHora = 0
    let duracao     = 0
    let calendario  = varCalendario
    let jornada     = jornFim - jornInicio - (intFim - intInicio)
    
    
    if (tipo.value  == "A Haver") {
        if(!isNaN(fimMili) && !isNaN(inicioMili)){
            duracao     = (fimMili - inicioMili) / 60000
            duracaoHoraForm.setAttribute("class","ml-2 mt-2 text-info")
            saldoForm.value = parseInt(saldoMin) + parseInt(duracao)  
            saldoDever.innerHTML = descontHora      
        }

    } else {
        duracaoHoraForm.setAttribute("class","ml-2 mt-2 text-danger")         
        if (!calendario.includes(dataInicio)){
            calendario.sort((a, b) => a - b)
            for (let dia in calendario) {
                if (dataInicio < calendario[dia]) {
                    dataInicio = calendario[dia]
                    horaInicio = jornInicio
                    break
                }
            }
        }
        if (!calendario.includes(dataFim)){ 
            calendario.sort((a, b) => b - a)           
            for (let dia in calendario) {
                if (dataFim > calendario[dia]) {
                    dataFim = calendario[dia]
                    horaFim = jornFim
                    break
                }
            }
        }                
        if ((dataFim - dataInicio) > 86400000) {
            calendario.sort((a, b) => a - b)           
            duracaoDia = (calendario.indexOf(dataFim) - calendario.indexOf(dataInicio) -1) * jornada
        }
        if (horaInicio < jornInicio) {
            horaInicio = jornInicio
        } else if (horaInicio >= intInicio && horaInicio < intFim) {
            horaInicio = intFim
        } else if (horaInicio > jornFim) {
            horaInicio = jornFim
        }
        if (horaFim > jornFim) {
            horaFim = jornFim
        } else if (horaFim > intInicio && horaFim <= intFim) {
            horaFim = intInicio
        } else if (horaFim < jornInicio) {
            horaFim = jornInicio
        }
        if (dataFim == dataInicio) {
            if (horaInicio < intInicio) {
                if (horaFim <= intInicio) {
                    duracaoHora = horaFim - horaInicio
                } else {
                    duracaoHora = horaFim - horaInicio - (intFim - intInicio)
                }
            } else {
                duracaoHora = horaFim - horaInicio
            }
        } else if (dataFim > dataInicio) {
            if (horaInicio < intInicio) {
                duracaoHora = jornFim - horaInicio - (intFim - intInicio)
            } else{
                duracaoHora = jornFim - horaInicio
            }
            if (horaFim > intFim) {
                duracaoHora += horaFim - (intFim - intInicio) - jornInicio
            } else{
                duracaoHora += horaFim - jornInicio
            }
        }        
        if (tipo.value  == "Folga") {
            saldoDever.innerHTML = descontHora
            duracao = (duracaoDia + duracaoHora) / 60000
            saldoForm.value = parseInt(saldoMin) - parseInt(duracao)
        } else if (tipo.value  == "Falta Descontada") {
            duracao = (duracaoDia + duracaoHora) / 60000
            saldoForm.value = parseInt(saldoMin)
            let descHor = Math.floor((duracao + parseInt(descontMin)) / 60)
            if (descHor < 10 && descHor > -10){
                descHor = `0${descHor}`
            }
            let descMin = Math.abs(duracao + parseInt(descontMin)) % 60
            if (descMin < 10){
                descMin = `0${descMin}`
            }
            saldoDever.innerHTML = `${descHor}:${descMin}`
        }  else {
            saldoForm.value = parseInt(saldoMin)
            saldoDever.innerHTML = descontHora
            duracao = (duracaoDia + duracaoHora) / 60000
        }             
    }
    
    duracaoForm.value = duracao
    let durHora = Math.floor(duracao / 60)
    if (durHora < 10 && durHora > -10){
        durHora = `0${durHora}`
    }
    let durMin = Math.abs(duracao)  % 60
    if (durMin < 10){
        durMin = `0${durMin}`
    }
    duracaoHoraForm.innerHTML  = `${durHora}:${durMin}`
    let salHora = Math.floor(saldoForm.value / 60)
    if (salHora < 10 && salHora > -10){
        salHora = `0${salHora}`
    }
    let salMin = Math.abs(saldoForm.value)  % 60
    if (salMin < 10){
        salMin = `0${salMin}`
    }
    saldoHora.innerHTML =  `${salHora}:${salMin}`
    
}

function dateTime() {
    let maxFal       = window.document.getElementById('max_fal')
    let jorIni       = window.document.getElementById('jor_ini')
    let jorFim       = window.document.getElementById('jor_fim')
    let intIni       = window.document.getElementById('int_ini')
    let intFim       = window.document.getElementById('int_fim')
    maxFal.setAttribute('data-mask','00/00/0000 00:00')
    jorIni.setAttribute('data-mask','00/00/0000 00:00')
    jorFim.setAttribute('data-mask','00/00/0000 00:00')
    intIni.setAttribute('data-mask','00/00/0000 00:00')
    intFim.setAttribute('data-mask','00/00/0000 00:00')
    maxFal.value = `01/01/1970 ${maxFal.value}`
    jorIni.value = `01/01/1970 ${jorIni.value}`
    jorFim.value = `01/01/1970 ${jorFim.value}`
    intIni.value = `01/01/1970 ${intIni.value}`
    intFim.value = `01/01/1970 ${intFim.value}`
}