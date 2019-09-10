$(document).ready(function() {
    $.urlParam = function (name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)')
                          .exec(window.location.search);

        return (results !== null) ? results[1] || 0 : false;
    }

    // Course finder

    if (sessionStorage.getItem("uniJSON") === null) {
        $.getJSON("/static/jsonfiles/institutions.json", function(result) {
            result.sort(function(a, b){
                if(a.order_by_name < b.order_by_name) { return -1; }
                if(a.order_by_name > b.order_by_name) { return 1; }
                return 0;
            });

            sessionStorage.setItem("uniJSON", JSON.stringify(result));
        })

    }

  if (sessionStorage.getItem("countries") != null) {
    let countries = sessionStorage.getItem("countries")
    $('#countries').text(countries.split(",").join(", "))
  }
  if (sessionStorage.getItem("modes") != null) {
    let modes = sessionStorage.getItem("modes")
    $('#modes').text(modes.split(",").join(", "))
  }

  if (sessionStorage.getItem("subject") != null) {
    let subjects = sessionStorage.getItem("subject")
    let subjectNames = []
    subjectsArray = subjects.split(",")
    $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, a) {
      $.each(subjectsArray, function(index, b) {
        if(a.code === b) {
          subjectNames.push(a.englishname)
          $('#subjects').text(subjectNames)
        }
      })
    })
  }

  if (sessionStorage.getItem("uni") != null) {
    let uni = sessionStorage.getItem("uni")
    $('#narrow').text(uni.split(",").join(", "))
  }

  if (sessionStorage.getItem("postcode") != null) {
    let postcode = sessionStorage.getItem("postcode")
    $('#narrow').text(postcode.split(",").join(", "))
  }
});
