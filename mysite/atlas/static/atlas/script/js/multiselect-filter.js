 $('.multi').multi_select({
    //   selectColor: '#0077b5',
      selectSize: 'small',
      selectText: 'Select Brand',
      duration: 300,
      easing: 'slide',
      listMaxHeight: 300,
      selectedCount: 2,
      sortByText: true,
      fillButton: true,
      data: {
//        "BD": "Bangladesh",
//        "BE": "Belgium",
//        "BF": "Burkina Faso",
//        "BG": "Bulgaria",
//        "BA": "Bosnia and Herzegovina",
//        "BB": "Barbados",
//        "WF": "Wallis and Futuna",
//        "BL": "Saint Barthelemy",
//        "BM": "Bermuda",
      },
      onSelect: function(values) {
        console.log('return values: ', values);
      }
});
//
//$('#brand1 .list-items').on('click', function(event) {
//
//    console.log($('#brand1 .list-items.selected'));
////        $('#brand1').multi_select({'selectText': "Select(65)"});
//});

//$('#brand1').on('click', function(event) {
//      $('#brand1').multi_select('clearValues');
//      $('.data-display').slideUp(300, function() {
//        $(this).remove();
//      });
//});

$('.multi2').multi_select({
    //   selectColor: '#0077b5',
      selectSize: 'small',
      selectText: 'Select Source',
      duration: 300,
      easing: 'slide',
      listMaxHeight: 300,
      selectedCount: 2,
      sortByText: true,
      fillButton: true,
      data: {
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "WF": "Wallis and Futuna",
        "BL": "Saint Barthelemy",
        "BM": "Bermuda",
      },
      onSelect: function(values) {
        console.log('return values: ', values);
      }
  });

$('#get_values').on('click', function(event) {
    console.log($('#multi2').multi_select('getSelectedValues'));
    $('.data-display').remove();
    var json = { items: $('#multi2').multi_select('getSelectedValues') };
    if (json.items.length) {
      var ul = $('<ul>', { 'class': 'data-display' }).appendTo('body');
      $(json.items).each(function(index, item) {
        ul.append(
          '<li style="display: block;">' + item + '</li>'
        );
      });
    }
});

$('#clear_values').on('click', function(event) {
  $('#multi2').multi_select('clearValues');
  $('.data-display').slideUp(300, function() {
    $(this).remove();
  });
});


$('.multi3').multi_select({
    //   selectColor: '#0077b5',
      selectSize: 'small',
      selectText: 'Select SKU',
      duration: 300,
      easing: 'slide',
      listMaxHeight: 300,
      selectedCount: 2,
      sortByText: true,
      fillButton: true,
      data: {
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "WF": "Wallis and Futuna",
        "BL": "Saint Barthelemy",
        "BM": "Bermuda",
      },
      onSelect: function(values) {
        console.log('return values: ', values);
      }
      });

$('#get_values').on('click', function(event) {
        console.log($('#multi3').multi_select('getSelectedValues'));
$('.data-display').remove();
var json = { items: $('#multi3').multi_select('getSelectedValues') };
if (json.items.length) {
  var ul = $('<ul>', { 'class': 'data-display' }).appendTo('body');
  $(json.items).each(function(index, item) {
    ul.append(
      '<li style="display: block;">' + item + '</li>'
    );
  });
}
});

$('#clear_values').on('click', function(event) {
  $('#multi3').multi_select('clearValues');
  $('.data-display').slideUp(300, function() {
    $(this).remove();
  });
});