var options = {
    series: [
    {
        data: [
        {
            x: 'LOJAS MARISA',
            y: 218 
        },
        {
            x: 'C&A',
            y: 149
        },
        {
            x: 'CAEDU',
            y: 184
        },
        {
            x: 'TORRA-TORRA',
            y: 55
        },
        {
            x: 'LOJA XAVANTES',
            y: 84
        },
        {
            x: 'RIP CURL',
            y: 31
        },
        {
            x: 'LOJA MENDES JUNIOR',
            y: 70
        },
        {
            x: 'TESOURA DE OURO',
            y: 30
        },
        {
            x: 'SOB MEDIDA',
            y: 44
        },
        {
            x: 'PURA ESSÊNCIA',
            y: 68
        },
        {
            x: 'LINS FERRÃO',
            y: 28
        },
        {
            x: 'SINO MODAS',
            y: 19
        },
        {
            x: 'CANAL CONCEPT',
            y: 30
        }
        ]
    }
    ],
    legend: {
    show: false
    },
    chart: {
    height: 500,
    type: 'treemap'
    },
    title: {
    text: 'RELAÇÃO DE CLIENTES',
    align: 'center'
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
