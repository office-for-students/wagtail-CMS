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

            $.each(result, function(index, item) {
                var option = document.createElement("option");
                option.setAttribute("value", item.name);
                option.innerHTML = item.name;
                $('#uni').append(option);
            })
        })

    }

    $.each(JSON.parse(sessionStorage.getItem("uniJSON")), function(index, item) {
        var option = document.createElement("option");
        option.setAttribute("value", item.name);
        option.innerHTML = item.name;
        $('#uni').append(option);
    })

  function handleStartAgain() {
    sessionStorage.clear()
  }

  function handleFormSubmit() {
    $('form').submit()
  }

  function handleSubjectSubmit(data) {
    let subject = ""
    let subjectCodes = ""

    if (data.subject.value != "disabled") {
      subject = data.subjectCode.value
    } else if (data.subjectArea.value === "disabled" && data.subject.value === "disabled") {
      subject = ""
    } else {
      subject = data.subjectArea.value
    }

    if (data.subjectArea.value != "disabled" && data.subject.value === "disabled") {
      $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, item) {
        if(item.level === "3" && item.code.includes(data.subjectArea.value)) {
          subjectCodes += item.code + ","
        }
      })
    } else if (data.subjectArea.value === "disabled" && data.subject.value === "disabled") {
      subjectCodes = ""
    } else {
      subjectCodes = data.subjectCode.value
    }
    sessionStorage.setItem("subject", subject)
    sessionStorage.setItem("subjectCodes", subjectCodes)
  }

  function handlePostcodeSubmit(data) {
    let postcode = data.postcode.value.replace(' ', '');
    let distance = data.distance.value;
    let  queryValue = [postcode,  distance].join(',');

    sessionStorage.setItem("postcode", queryValue);
  }

  function handleUniSelection(data) {
    let uni = data.uni.value
    sessionStorage.setItem("uni", uni)
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

  function handleResultsRequest() {
    let subject_query = sessionStorage.getItem('subjectCodes')
    let institution_query = sessionStorage.getItem('uni')
    let mode_query = sessionStorage.getItem('modes')
    let countries_query = sessionStorage.getItem('countries')
    let postcode_query = sessionStorage.getItem('postcode')

    $("input[name='subject_query']").val(subject_query)
    $("input[name='institution_query']").val(institution_query)
    $("input[name='mode_query']").val(mode_query)
    $("input[name='countries_query']").val(countries_query)
    $("input[name='postcode_query']").val(postcode_query)
  }
});
