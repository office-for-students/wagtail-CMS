
// handleClick = (e) => {
//   for(i = 0; i < tabs.length; i++) {
//     document.getElementById(tabs[i]).style.display = "none"
//   }
//   document.getElementById(e.target.innerHTML).style.display = "grid"
// }
//
// let list = document.getElementsByTagName('li')
// let tabs = ["Country", "Place", "Postcode"]
// for (i = 0; i < list.length; i++) {
//   list[i].addEventListener('click', handleClick)
// }

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

$('.tab-headings>li').click((e) => {
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
})

let countryOptions = {}

$('.country-options>li').click((e) => {
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
})
