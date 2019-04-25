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
