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
    },
    {
      x: new Date(pcp.entrega).getTime(),
      strokeDashArray: 0,
      borderColor: "#b92c28",
      label: {
        borderColor: '#b92c28',
        style: {
          color: '#fff',
          background: '#b92c28',
        },
        text: 'Entrega',
      }
    }
  )  
  return intervals
}


function data(){
  let data = []
  for (var i = 0; i < pcp.processo.length; i++) {
    data.push({
        x: pcp.processo[i].nome,
        y: [
          new Date(pcp.processo[i].inicio).getTime(),
          new Date(pcp.processo[i].fim).getTime()
        ]
    })
  }
  data.push(        
    {
      x: "Prazo",
      y: [
        new Date().getTime(),
        new Date(pcp.entrega).getTime()
      ]
    })
  return data
}

function series(){
  let series = []
  series.push(
    {
      name: "prazo",
      data: data()
    }
  )
  return series
}
var options = {
  series: series(),

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

  height: 350,
  type: 'rangeBar'
},
plotOptions: {
  bar: {
    horizontal: true
  }
},
xaxis: {
  type: 'datetime'
},
annotations: {
  xaxis: get_intervals()             
}
};

var chart = new ApexCharts(document.querySelector('#chart'), options);
chart.render();
