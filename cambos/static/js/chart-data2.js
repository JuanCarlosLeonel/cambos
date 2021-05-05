const totalizer = {
    id: 'totalizer',
    beforeUpdate: chart => {
        let totals = {}
        let utmost = 0

            chart.data.datasets.forEach((dataset, datasetIndex) => {
                if (chart.isDatasetVisible(datasetIndex)) {
                    utmost = datasetIndex
                        dataset.data.forEach((value, index) => {
                            totals[index] = (totals[index] || 0) + value
                        })
                }
            })
            chart.$totalizer = {
            totals: totals,
            utmost: utmost
        }
    }
}

var chart1 = document.getElementById("chartCarteira").getContext("2d");
var carteira = new Chart(chart1, {
	type: 'bar',
	data: {
		labels: labels1,
		datasets : [{	
			label: 'Atrasado',
			data: [data3],
			backgroundColor:'rgba(255, 99, 132, 0.2)',              
			borderColor:'rgba(255, 99, 132, 1)',               
			borderWidth: 1
		},		
		{	
			label: 'Em atraso',
			data: data2,
			backgroundColor:'rgba(255, 159, 64, 0.2)',        
            borderColor:'rgba(255, 159, 64, 1)',            
			borderWidth: 1
			
		},
		{	
			label: 'Em dia',
			data: data1,
			backgroundColor: 'rgba(80, 180, 86, 0.2)',            
            borderColor: 'rgba(80, 180, 86, 1)',
            borderWidth: 1
		},	
		{
			label: 'Total',
			data: [0, 0, 0,0,0,0,0,0,0,0,0,0],
			backgroundColor: 'rgba(24,91,62,0)',
			datalabels: {
				font: function(context) {
					var width = context.chart.width;
					var size = Math.round(width / 100);
	
					return {
						weight: 'bold',
						size: size
					};
				},				
				formatter: (value, ctx) => {
					const total = ctx.chart.$totalizer.totals[ctx.dataIndex];
					if (total > 0) {
						return total.toLocaleString('pt-BR', {})
					}else {
						return ""
					}
				},
				align: 'end',
				anchor: 'end',
				display: function (ctx) {
					return ctx.datasetIndex === ctx.chart.$totalizer.utmost
				}
			}

		}
	]
    },
	options: {		
		tooltips: {
			mode: 'label',
			intersect: false,
			filter: function (tooltipItem) {
				return tooltipItem.datasetIndex in [0,1,2];
			},
			callbacks: {
				title: function(tooltipItems, data) {
					return 'Semana: ' + tooltipItems[0].xLabel ;
				  },
				afterTitle: function() {
					window.total = 0;
				},
				label: function(tooltipItem, data) {
					var corporation = data.datasets[tooltipItem.datasetIndex].label;
					var valor = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
					window.total += valor;
					return corporation + ": " + valor.toLocaleString('pt-BR', {});            
				},
				footer: function() {
					return "TOTAL: " + window.total.toLocaleString('pt-BR', {});            
				},				
			},
		},
		legend: {
			position: 'top',
			labels: {
				fontSize: 16,
				filter: function(legendItem, chartData) {
				 if (legendItem.datasetIndex === 3) {
				   return false;
				 }
				return true;
				}
			 }
		},
		
        scales: {
			xAxes: [{ stacked: true,
				gridLines: false }],
			yAxes: [{
				stacked: true,
				display: false,				
			 }]
		},
		plugins: {
            datalabels: {                
                display: function (context) {
                    return context.chart.isDatasetVisible(context.datasetIndex);
                },                
                font: function(context) {
					var width = context.chart.width;
					var size = Math.round(width / 132);
	
					return {
						weight: 'bold',
						size: size
					};
				},
				formatter: (value, ctx) => {
					if(value >0 ){					
						return value.toLocaleString('pt-BR', {})
					}else{
						return ""
					}
				},
            }
        }
    },
    plugins: [totalizer]
		
});

	var pieData = [
			{
				value: 300,
				color: "#30a5ff",
				highlight: "#7376df",
				label: "Value 1"
			},
			{
				value: 50,
				color: "#a0a0a0",
				highlight: "#999999",
				label: "Value 2"
			},
			{
				value: 100,
				color:"#dfdfdf",
				highlight: "#cccccc",
				label: "Value 3"
			},
			{
				value: 120,
				color: "#f7f7f7",
				highlight: "#eeeeee",
				label: "Value 4"
			}

		];
			
	var doughnutData = [
			{
				value: 300,
				color: "#30a5ff",
				highlight: "#7376df",
				label: "Value 1"
			},
			{
				value: 50,
				color: "#a0a0a0",
				highlight: "#999999",
				label: "Value 2"
			},
			{
				value: 100,
				color:"#dfdfdf",
				highlight: "#cccccc",
				label: "Value 3"
			},
			{
				value: 120,
				color: "#f7f7f7",
				highlight: "#eeeeee",
				label: "Value 4"
			}
		];
			
	var radarData = {
	    labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
	    datasets: [
	        {
	            label: "My First dataset",
	            fillColor: "rgba(220,220,220,0.2)",
	            strokeColor: "rgba(220,220,220,1)",
	            pointColor: "rgba(220,220,220,1)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(220,220,220,1)",
	            data: [65, 59, 90, 81, 56, 55, 40]
	        },
	        {
	            label: "My Second dataset",
	            fillColor : "rgba(48, 164, 255, 0.2)",
	            strokeColor : "rgba(48, 164, 255, 0.8)",
	            pointColor : "rgba(48, 164, 255, 1)",
	            pointStrokeColor : "#fff",
	            pointHighlightFill : "#fff",
	            pointHighlightStroke : "rgba(48, 164, 255, 1)",
	            data: [28, 48, 40, 19, 96, 27, 100]
	        }
	    ]
	};
	
	var polarData = [
	    {
	    	value: 300,
	    	color: "#30a5ff",
	    	highlight: "#7376df",
	    	label: "Value 1"
	    },
	    {
	    	value: 140,
	    	color: "#a0a0a0",
	    	highlight: "#999999",
	    	label: "Value 2"
	    },
	    {
	    	value: 220,
	    	color:"#dfdfdf",
	    	highlight: "#cccccc",
	    	label: "Value 3"
	    },
	    {
	    	value: 250,
	    	color: "#f7f7f7",
	    	highlight: "#eeeeee",
	    	label: "Value 4"
	    }
		
	];
