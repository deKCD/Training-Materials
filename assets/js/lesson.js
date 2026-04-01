// Make all tables striped by default.
$("table").addClass("table table-striped");


// Handle foldable solutions (on click and at start)
$(document).ready(function() {

  // Initialize each solution
  $(".solution").each(function() {
    var container = $(this);

    // Hide all children except <solution-title>
    $(">*:not(solution-title)", container).hide();

    // Add fold/unfold icon to the title
    $("solution-title:first", container).append(
      "<span class='fold-unfold glyphicon glyphicon-collapse-down'></span>"
    );

    // Optional: make cursor pointer
    $("solution-title:first", container).css("cursor", "pointer");
  });

  // Toggle on click
  $(".solution solution-title").on("click", function(event) {
    var container = $(this).parent();

    // Toggle all content except the title
    $(">*:not(solution-title)", container).toggle(400);

    // Toggle the icon class
    $(">solution-title > span.fold-unfold", container)
      .toggleClass("glyphicon-collapse-down glyphicon-collapse-up");
  });

});


// Handle searches.
// Relies on document having 'meta' element with name 'search-domain'.
function google_search() {
  var query = document.getElementById("google-search").value;
  var domain = $("meta[name=search-domain]").attr("value");
  window.open("https://www.google.com/search?q=" + query + "+site:" + domain);
}

// function to shrink the life cycle bar when scrolling
$(function(){
    $('#life-cycle').data('size','big');
});

$(window).scroll(function(){
    if($(document).scrollTop() > 0)
    {
        if($('#life-cycle').data('size') == 'big')
        {
            $('#life-cycle').data('size','small');
            $('#life-cycle').stop().animate({
                padding: '5px'
            },100);
        }
    }
    else
    {
        if($('#life-cycle').data('size') == 'small')
        {
            $('#life-cycle').data('size','big');
            $('#life-cycle').stop().animate({
                padding: '15px'
            },100);
        }
    }
});
