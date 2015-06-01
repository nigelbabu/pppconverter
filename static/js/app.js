$('form select').chosen();
$('form').submit(function (event) {
  $.getJSON('/json', function(data) {
    var from_country = Number($('#from_country').val());
    var to_country = Number($('#to_country').val());
    var salary = $('#salary');
    console.log(salary.val());
    if (salary.val() === '') {
      salary.addClass('error');
      $('#error_salary').removeClass('hidden');
      $('#error_salary').addClass('error');
    } else {
      $('#error_salary').removeClass('error');
      $('#error_salary').addClass('hidden');
      salary.removeClass('error');
      salary = salary.val();
      var from_country_data = [];
      var to_country_data = [];
      $.each(data.countries, function(key, country) {
        if(country.id === from_country) {
          from_country_data = country;
        } else if(country.id === to_country) {
          to_country_data = country;
        }
      });
      var equivalent_salary = (Number(salary) / from_country_data.ppp) * to_country_data.ppp;
      console.log("In " + to_country_data.name + ", you should get " + equivalent_salary + " in local currency.");
      $('#resultDiv').html("In " + to_country_data.name + ", you should get " + Math.round(equivalent_salary * 100)/100 + " in local currency.");
      $('#displayResult').removeClass('hidden');
    }
  });
  return false;
});

