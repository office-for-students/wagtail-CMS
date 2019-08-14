$(document).ready(function() {
  // Course finder

  if (sessionStorage.getItem("subjectJSON") === null) {
    $.getJSON("/static/jsonfiles/subject-codes.json", (result) => {
      result.sort(function(a, b){
          if(a.englishname < b.englishname) { return -1; }
          if(a.englishname > b.englishname) { return 1; }
          return 0;
      })
      sessionStorage.setItem("subjectJSON", JSON.stringify(result));
      $.each(result, function(index, item) {
        if(item.level === "1") {
          $('#subjectArea').append(`<option value='${item.code}'>${item.englishname}</option>`)
        }
        if(item.level === "2") {
          $('#subject').append(`<option value='${item.code}'>${item.englishname}</option>`)
        }
        if(item.level === "3") {
          $('#subjectCode').append(`<option value='${item.code}'>${item.englishname}</option>`)
        }
      })
    })
  }

  $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, item) {
    if(item.level === "1") {
      $('#subjectArea').append(`<option value='${item.code}'>${item.englishname}</option>`)
    }
    if(item.level === "2") {
      $('#subject').append(`<option value='${item.code}'>${item.englishname}</option>`)
    }
    if(item.level === "3") {
      $('#subjectCode').append(`<option value='${item.code}'>${item.englishname}</option>`)
    }
  })

  handleSubjectAreaSelect = (value) => {
    $('#subject').empty()
    $('#subjectCode').empty()
    $('#subject').append('<option value="disabled" disabled selected>Subject</option>')
    $('#subjectCode').append('<option value selected>Show all</option>')
    $('.template-course-finder-choose-subject .course-finder-content__question-selector:nth-of-type(3)').css('display', 'none')
    $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, item) {
      if(item.level === "2" && item.code.includes(value)) {
        $('#subject').append(`<option value='${item.code}'>${item.englishname}</option>`)
      }
    })
    $('#subject').trigger('loadeddata')

  }

  handleSubjectSelect = (value) => {
    $('#subjectCode').empty()
    $('.template-course-finder-choose-subject .course-finder-content__question-selector:nth-of-type(3)').css('display', 'block')
    let all = ""
    $.each(JSON.parse(sessionStorage.getItem("subjectJSON")), function(index, item) {
      if(item.level === "3" && item.code.includes(value)) {
        $('#subjectCode').append(`<option value='${item.code}'>${item.englishname}</option>`)
        all += item.code + ","
      }
    })
    $('#subjectCode').prepend(`<option value=${all} selected>Show all</option>`)
    $('#subjectCode').trigger('loadeddata')
  }

  if (sessionStorage.getItem("uniJSON") === null) {
    $.getJSON("/static/jsonfiles/institutions.json", (result) => {
      result.sort(function(a, b){
          if(a.order_by_name < b.order_by_name) { return -1; }
          if(a.order_by_name > b.order_by_name) { return 1; }
          return 0;
      })
      sessionStorage.setItem("uniJSON", JSON.stringify(result));
      $.each(result, function(index, item) {
          $('#uni').append(`<option value='${item.name}'>${item.name}</option>`)
      })
    })

  }

  $.each(JSON.parse(sessionStorage.getItem("uniJSON")), function(index, item) {
      $('#uni').append(`<option value='${item.name}'>${item.name}</option>`)
  })

  handleStartAgain = () => {
    sessionStorage.clear()
  }

  handleFormSubmit = () => {
    $('form').submit()
  }

  handleCountrySelection = (data) => {
    let countries = []
    for(i=0; i < data.country.length; i++) {
      if(data.country[i].checked) {
        countries.push(data.country[i].value)
      }
     }
    sessionStorage.setItem("countries", countries);
  }

  handleModeSelection = (data) => {
    let modes = []
    for(i=0; i < data.mode.length; i++) {
      if(data.mode[i].checked) {
        modes.push(data.mode[i].value)
      }
    }
    sessionStorage.setItem("modes", modes);
  }

  handleSubjectSubmit = (data) => {
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

  handleUniSelection = (data) => {
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

  handleResultsRequest = () => {
    let subject_query = sessionStorage.getItem('subjectCodes')
    let institution_query = sessionStorage.getItem('uni')
    let mode_query = sessionStorage.getItem('modes')
    let countries_query = sessionStorage.getItem('countries')

    $("input[name='subject_query']").val(subject_query)
    $("input[name='institution_query']").val(institution_query)
    $("input[name='mode_query']").val(mode_query)
    $("input[name='countries_query']").val(countries_query)
  }

  handleResultClick = (e) => {
    if(e.currentTarget.classList.contains('open-result')) {
      e.currentTarget.classList.remove('open-result')
      e.currentTarget.children[0].style.borderBottom=""
    } else {
      e.currentTarget.classList.add('open-result')
      e.currentTarget.children[0].style.borderBottom="1px solid #4C4D6C"
    }
  }

  $('.result').click((e) => {
    handleResultClick(e)
  })

  $('.result').keydown((e) => {
    if(e.which === 13 || e.which === 32) {
      handleResultClick(e)
    }
  })

});
