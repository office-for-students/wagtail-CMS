
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
