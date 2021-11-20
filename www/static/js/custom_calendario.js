let data = [];
let excluir = [];
let adicionar = [];
let novaData = document.getElementById("adicionar")
let dataExcluir = document.getElementById("deletar")
for (var i = 0; i < dias.length; i++) {
  data.push(new Date(dias[i]))
}

const calendar = new Calendar('#calendario',{
    dataSource: getDataSource(),
  });

document.querySelector('#calendario').addEventListener('clickDay', function(e) {
  dia = e.date.toString();  
  var atual =  dias.toString().indexOf(formatDate(dia))
  var excluido = excluir.toString().indexOf(formatDate(dia))
  var adicionado = adicionar.toString().indexOf(formatDate(dia))
  if (atual > -1){
    if (excluido > -1){
      e.element.style="box-shadow: rgb(44, 143, 201) 0px -4px 0px 0px inset";         
      excluir.splice(excluido, 1)
    }
    else{
      e.element.style="box-shadow: rgb(201, 44, 44) 0px -4px 0px 0px inset";         
      excluir.push(formatDate(e.date))
    }    
  } 
  else {
    if (adicionado > -1){
      e.element.style="box-shadow: rgb(255, 255, 255) 0px -4px 0px 0px inset";         
    adicionar.splice(adicionado, 1)
    }
    else{      
      e.element.style="box-shadow: rgb(44, 201, 143) 0px -4px 0px 0px inset";      
      adicionar.push(formatDate(e.date))
    }
  }
  novaData.value = adicionar
  dataExcluir.value = excluir
})


function getDataSource() {
  var result= [];
  for (var i = 0; i < data.length; i++) {
    result.push({
        startDate: data[i],
        endDate: data[i],
        color: 'rgb(44, 143, 201)'
    });
  }
  return result;
};

function formatDate(date) {
  var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

  if (month.length < 2) 
      month = '0' + month;
  if (day.length < 2) 
      day = '0' + day;

  return [year, month, day].join('-');
}