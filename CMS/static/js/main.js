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

  // Search Tool

  handleTabClick = (e) => {
    let headings = $('.tab-headings>li')
    let tabs = ["Country", "Place", "Postcode"]
    for (i = 0; i < headings.length; i++) {
      headings[i].classList = ''
    }
    if(e.target.classList[0] === undefined) {
      e.target.classList = 'selected'
    }
    for(i = 0; i < tabs.length; i++) {
      $(`#${tabs[i]}`).css('display', 'none')
    }
    $(`#${e.target.innerHTML}`).css('display', 'grid')
  }

  $('.tab-headings>li').click((e) => {
    handleTabClick(e);
  })

  $('.tab-headings>li').keydown((e) => {
    if(e.which === 13 || e.which === 32) {
      handleTabClick(e)
    }
  })

  handleCountryClick = (e) => {
    if(countryOptions[e.target.id] === true) {
      countryOptions[e.target.id] = false
    } else {
      countryOptions[e.target.id] = true
    }
    if(countryOptions[e.target.id] === true) {
      $(`#${e.target.id}`).css('background-color', '#f2f2f2')
    } else {
      $(`#${e.target.id}`).css('background-color', '#fff')
    }
  }

  let countryOptions = {}

  $('.country-options>li').click((e) => {
    handleCountryClick(e)
  })

  $('.country-options>li').keydown((e) => {
    if(e.which === 13 || e.which === 32) {
      handleCountryClick(e)
    }
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

});
