const currentYear = new Date().getFullYear();
new Calendar('#calendario',{
    dataSource: [
      {
        startDate: new Date(currentYear, 2, 5),
        endDate: new Date(currentYear, 2, 20)
      },
      {
        startDate: new Date(currentYear, 5, 10),
        endDate: new Date(currentYear, 7, 10)
      }
    ]
  });

document.querySelector('#calendario').addEventListener('clickDay', function(e) {
    
    new Calendar('#calendario',{
        dataSource: [
          {
            startDate: e.date,
            endDate: e.date
          },
          
        ]
      });
});