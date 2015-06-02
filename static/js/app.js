(function(){
  Number.prototype.toMoney = function(decimals, decimal_sep, thousands_sep) {
    var n = this,
    c = isNaN(decimals) ? 2 : Math.abs(decimals),
    d = decimal_sep || '.',
    t = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    sign = (n < 0) ? '-' : '',
    i = parseInt(n = Math.abs(n).toFixed(c)) + '',
    j = ((j = i.length) > 3) ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + t : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : '');
  };
  $('form select').chosen();
  $('form').submit(function (event) {
    $.getJSON('/json', function(data) {
      var from_country = Number($('#from_country').val()),
      to_country = Number($('#to_country').val()),
      salary = $('#salary'),
      from_country_data = [],
      to_country_data = [];
      if (salary.val() === '') {
        salary.addClass('error');
        $('#error_salary').removeClass('hidden');
        $('#error_salary').addClass('error');
      } else {
        $('#error_salary').removeClass('error');
        $('#error_salary').addClass('hidden');
        salary.removeClass('error');
        salary = salary.val();
        $.each(data.countries, function(key, country) {
          if(country.id === from_country) {
            from_country_data = country;
          } else if(country.id === to_country) {
            to_country_data = country;
          }
        });
        var equivalent_salary = (Number(salary) / from_country_data.ppp) * to_country_data.ppp;
        var output = "In " + to_country_data.name + ", " + equivalent_salary.toMoney() + " " + to_country_data.currency + " will allow you to buy the same things you'd buy with " + Number(salary).toMoney() + " " + from_country_data.currency + " in " + from_country_data.name + '.';
        $('#resultDiv').html(output);
        $('#displayResult').removeClass('hidden');
      }
    });
    return false;
  });
})();
