var produtos = JSON.parse(lista);
var intervalos = JSON.parse(calendar);

function get_intervals(){
  let intervals = []
  intervals.push(
    {
      x: new Date().getTime(),
      strokeDashArray: 0,
      borderColor: "#1B998B",
      label: {
        borderColor: '#1B998B',
        style: {
          color: '#fff',
          background: '#1B998B',
        },
        text: 'agora',
      }
    }
  )
  for (var i = 0; i < intervalos.length; i++) {
    intervals.push({
      x: new Date(intervalos[i].start).getTime(),
      x2: new Date(intervalos[i].end).getTime(),      
      borderColor: "#1B998B",
      opacity: 0.2,       
    })
  }
  return intervals
}

function data(option){
  let data = []
  for (var i = 0; i < option.length; i++) {
    if (option[i].situacao == 'em_dia'){
      data.push({
        x: option[i].produto,
        y: [
          new Date(option[i].entrada).getTime(),
          new Date(option[i].entrega).getTime(),
        ],
        z:{
          name : option[i].produto,
          desc : option[i].produto,
          
        },        
        fillColor: "#008FFB" 
      })
    }
    if (option[i].situacao == 'em_atraso'){
      data.push({
        x: option[i].produto,
        y: [
          new Date(option[i].entrada).getTime(),
          new Date(option[i].entrega).getTime(),
        ],
        z:{
          name : option[i].produto,
          desc : option[i].produto,
          
        },        
        fillColor: "#FEB019"
      })
    }
    if (option[i].situacao == 'parado'){
      data.push({
        x: option[i].produto,
        y: [
          new Date(option[i].entrada).getTime(),
          new Date(option[i].entrega).getTime(),
        ],
        z:{
          name : option[i].produto,
          desc : option[i].produto,
          
        },        
        fillColor: "#d7263d"
      })
    }
      if (option[i].atraso != ''){
        data.push({
          x: option[i].produto,
          y: [
            new Date(option[i].entrega).getTime(),
            new Date(option[i].atraso).getTime(),
          ],
          z:{
            name : "teste",
            desc : option[i].produto,
            
          },
          fillColor: '#ff6657'
          
        })
      }
    }
  
  
  return data
  
}

function series(){
  var produtosEmLinha = []
  let em_dia = produtos.em_dia
  let atrasado = produtos.atrasado
  let parado = produtos.parado
  if (em_dia.length > 0){    
      produtosEmLinha.push(
        {
          name:  "Em Produção",
          data: data(em_dia)
        }
      )    
  }
  if (atrasado.length > 0){    
    produtosEmLinha.push(
      {
        name:  "Atrasado",
        data: data(atrasado)
      }
    )    
  }
  if (parado.length > 0){    
    produtosEmLinha.push(
      {
        name:  "Parado",
        data: data(parado)
      }
    )    
  }
  return produtosEmLinha
}
var options = {
  chart: {
    defaultLocale: 'en',
    locales: [{    
        "name": "en",
        "options": {
          "months": [
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
          ],
          "shortMonths": [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez"
          ],
          "days": [
            "Domingo",
            "Segunda",
            "Terça",
            "Quarta",
            "Quinta",
            "Sexta",
            "Sábado"
          ],
          "shortDays": ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
          "toolbar": {
            "exportToSVG": "Baixar SVG",
            "exportToPNG": "Baixar PNG",
            "exportToCSV": "Baixar CSV",
            "menu": "Menu",
            "selection": "Selecionar",
            "selectionZoom": "Selecionar Zoom",
            "zoomIn": "Aumentar",
            "zoomOut": "Diminuir",
            "pan": "Navegação",
            "reset": "Reiniciar Zoom"
          }
        }
    }],
        
      
   
    
    height: 450,
    type: 'rangeBar',
  events : {
    dataPointSelection: function(event, chartContext, config) {
      //alert('test');
    }

  }, stacked: false,
    zoom: {
      type: 'xy', 
      enabled: true,
      autoScaleYaxis: true,
      toolbar: {
          autoSelected: 'zoom',
          tools: {
              download: true,
              selection: true,
              zoom: true,
              zoomin: true,
              zoomout: true,
              pan: true,
              reset: true
          },
      }

    }
  },
  dataLabels: {
    enabled: true,
    formatter: function(val,obj) {
      return obj.w.config.series[obj.seriesIndex].data[obj.dataPointIndex].z.desc;
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '60%',
      rangeBarGroupRows: true
    }
  }

  /*,
  tooltip: {
    custom: function({series, seriesIndex, dataPointIndex, w}) {
      return '<div class="apexcharts-tooltip-rangebar">' + '<div> <span class="series-name" style="color: ' + color + '">' + (w.config.series[seriesIndex].name ? w.config.series[seriesIndex].name : '') + '</span></div>' + '<div> <span class="category">' + ylabel + ': </span> <span class="value start-value">' + startVal + '</span> <span class="separator">-</span> <span class="value end-value">' + endVal + '</span></div>' + '</div>'
    }
  }*/,
  series: series(),
  xaxis: {
    type: 'datetime',
  },
  yaxis: {
    show: false
  },
  colors: [
    "#008FFB", "#d7263d", "#FEB019",  "#FF4560", "#775DD0",
    "#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
    "#D7263D", "#1B998B", "#F46036", "#E2C044"
  ],
  
  legend: {
    position: 'top',
    horizontalAlign: 'left'
  },
  grid: {
    show: true,        
    position: 'back',
    xaxis: {
        lines: {
            show: true
        },    
    },   
    yaxis: {
        lines: {
            show: false
        }
    },          
  },
  annotations: {
    xaxis: get_intervals()             
  }
}

var chart = new ApexCharts(document.querySelector('#chart'), options);


chart.render();