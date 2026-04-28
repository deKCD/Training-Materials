// Make all tables striped by default.
$("table").addClass("table table-striped");


// Handle foldable boxes (on click and at start)
$(document).ready(function() {

  // Container selectors for foldable blocks
  var foldableSelector = ".solution, .tip, .comment, .details, solution, tip, comment, details";
  var titleSelector = "solution-title, tip-title, comment-title, details-title";

  // Initialize each foldable block
  $(foldableSelector).each(function() {
    var container = $(this);

    // Hide all children except the title element
    $(">*:not(" + titleSelector + ")", container).hide();

    // Add fold/unfold icon to the title
    $(titleSelector + ":first", container).append(
      "<span class='fold-unfold glyphicon glyphicon-collapse-down'></span>"
    );

    // Optional: make cursor pointer
    $(titleSelector + ":first", container).css("cursor", "pointer");
  });

  // Toggle on click (whole box fold/unfold)
  $(foldableSelector).on("click", function(event) {
    // Do not toggle when clicking inside a nested box or external links/buttons
    if (!$(event.target).closest(foldableSelector).is(this)) {
      return;
    }

    var container = $(this);
    var title = container.children(titleSelector).first();
    var body = container.children(":not(" + titleSelector + ")");
    var icon = title.children("span.fold-unfold");

    // Toggle all content except title
    body.toggle(400);

    // Toggle the icon class
    icon.toggleClass("glyphicon-collapse-down glyphicon-collapse-up");
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
