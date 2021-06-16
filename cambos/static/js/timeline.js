var produtos = JSON.parse(lista);

function data(option){
  let data = []
  for (var i = 0; i < option.length; i++) {
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
      
    })
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
          name:  "Em Dia",
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
    type: 'datetime'
  },
  yaxis: {
    show: false
  },
  colors: [
    "#008FFB", "#FEB019", "#d7263d", "#FF4560", "#775DD0",
    "#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
    "#D7263D", "#1B998B", "#F46036", "#E2C044"
  ],
  
  legend: {
    position: 'top',
    horizontalAlign: 'left'
  }
}

var chart = new ApexCharts(document.querySelector('#chart'), options);


chart.render();