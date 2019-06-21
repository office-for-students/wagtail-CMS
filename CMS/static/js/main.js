$(document).ready(function() {
  // Mobile Nav
  $('#burger-menu').click(() => {
    $('.mobile-nav').toggle()
    $('#burger-menu').toggle()
    $('#close-menu').toggle()
    $('nav').css('height',"50vh")
    $('nav').css('grid-template-rows', "60px 1fr")
  })

  $('#close-menu').click(() => {
    $('.mobile-nav').toggle()
    $('#burger-menu').toggle()
    $('#close-menu').toggle()
    $('nav').css('height',"60px")
    $('nav').css('grid-template-rows', "1fr")
  })

  // Content subsections

  handleSubsectionClick = (e) => {
    if(e.currentTarget.classList.contains('open-subsection')) {
      e.currentTarget.classList.remove('open-subsection')
      e.currentTarget.children[0].children[0].style.borderBottom=""
    } else {
      e.currentTarget.classList.add('open-subsection')
      e.currentTarget.children[0].children[0].style.borderBottom="1px solid #4C4D6C"
    }
  }

  $('.subsection').click((e) => {
    handleSubsectionClick(e)
  })

  $('.subsection').keydown((e) => {
    if(e.which === 13 || e.which === 32) {
      handleSubsectionClick(e)
    }
  })

  $('.subsection>.rich-text').each(function(){
     $(':not(h4)', this).wrapAll("<div class='subsection-content'></div>");
  });


  $(':not(p) + p, * > p:first-of-type').
     each(function() {
       $(this).
           nextUntil(':not(p)').
           addBack().
           wrapAll('<div class="subsection-text" />');
     });

  // Course finder

  $('.template-course-finder-choose-subject form div:nth-of-type(2) input').on('input', () => {
    $('.template-course-finder-choose-subject div:nth-of-type(3)').css('display', 'block')
  })


  let countries = sessionStorage.getItem("countries")
  let modes = sessionStorage.getItem("modes")
  let subjects = sessionStorage.getItem("subject")
  let uni = sessionStorage.getItem("uni")

  $('#countries').text(countries)
  $('#modes').text(modes)
  $('#subjects').text(subjects)
  $('#narrow').text(uni)

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

handleSubjectSelection = (data) => {
  let subject = data.subject.value
  sessionStorage.setItem("subject", subject)
}

handleUniSelection = (data) => {
  let uni = data.uni.value
  sessionStorage.setItem("uni", uni)
}

handleResultsRequest = () => {
  let course_query = sessionStorage.getItem('subject')
  let institution_query = sessionStorage.getItem('uni')
  let mode_query = sessionStorage.getItem('modes')
  let countries_query = sessionStorage.getItem('countries')

  $("input[name='course_query']").val(course_query)
  $("input[name='institution_query']").val(institution_query)
  $("input[name='mode_query']").val(mode_query)
  $("input[name='countries_query']").val(countries_query)
  debugger
}
