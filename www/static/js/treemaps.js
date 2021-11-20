function data(){
    let data = []
    for (var i = 0; i < label.length; i++) {
      data.push({
          x: label[i],
          y: value[i]          
      })
    }    
    return data
  }


var options = {
    series: [
    {
        data: data()
    }
    ],
    legend: {
    show: false
    },
    chart: {
    height: 500,
    type: 'treemap'
    },    
    colors: [
    '#3B93A5',
    '#F7B844',
    '#ADD8C7',
    '#EC3C65',
    '#CDD7B6',
    '#C1F666',
    '#D43F97',
    '#1E5D8C',
    '#421243',
    '#7F94B0',
    '#EF6537',
    '#C0ADDB'
    ],
    plotOptions: {
        treemap: {
          distributed: true,
          enableShades: false
    }
    }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
