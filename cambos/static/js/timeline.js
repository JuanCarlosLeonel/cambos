var produtos = JSON.parse(lista);

function series(){
  var produtosEmLinha = []
  for (var i = 0; i < produtos.length; i++) {
    produtosEmLinha.push(
      {
        name:   produtos[i].situacao,
        data: [
          
          {
            x: produtos[i].produto,
            y: [
              new Date(produtos[i].entrada).getTime(),
              new Date(produtos[i].entrega).getTime(),
            ],
            z:{
              name : produtos[i].produto,
              desc : produtos[i].produto,
              
            },
            fillColor: '#008FFB'
          },
          
          
        ]
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
      barHeight: '80%'
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
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      type: 'vertical',
      shadeIntensity: 0.25,
      gradientToColors: undefined,
      inverseColors: true,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [50, 0, 100, 100]
    }
  },
  legend: {
    position: 'top',
    horizontalAlign: 'left'
  }
}

var chart = new ApexCharts(document.querySelector('#chart'), options);


chart.render();