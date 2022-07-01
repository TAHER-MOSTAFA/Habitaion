//Units-details//

$('.popup').click(function() {
    var src = $(this).attr('src');
    $('.modal').modal('show');
    $('#popup-img').attr('src',src);
    
})



