// Make all tables striped by default.
$("table").addClass("table table-striped");


// Handle foldable boxes (on title click and at start)
$(document).ready(function() {

  // Container selectors for foldable blocks
  var foldableSelector = ".solution, .tip, .comment, .details, solution, tip, comment, details";
  var titleSelector = "solution-title, tip-title, comment-title, details-title";

  // Initialize each foldable block
  $(foldableSelector).each(function() {
    var container = $(this);
    
    // Hide all children except the title element
    $(">*:not(" + titleSelector + ")", container).hide();

    // Add fold/unfold icon to the title (avoid duplicates)
    var title = container.children(titleSelector).first();
    if (title.find(".fold-unfold").length === 0) {
      title.append("<i class='fold-unfold bi bi-chevron-expand float-end'></i>");
    }
  });

  // Remove previous handlers
  $(foldableSelector).off("click");

  // Toggle only when clicking the title
  $(document).on("click", titleSelector, function(event) {
    event.preventDefault();
    event.stopPropagation();

    var title = $(this);
    var container = title.closest(foldableSelector);
    var body = container.children(":not(" + titleSelector + ")");
    var icon = title.children("i.fold-unfold");

    // Toggle all content except title
    body.toggle(400);

    // Toggle the icon class
    icon.toggleClass("bi-chevron-expand bi-chevron-contract");
  });

  // Prevent clicks inside the content from toggling
  $(document).on("click", foldableSelector + " > :not(" + titleSelector + ")", function(event) {
    event.stopPropagation();
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


// Add this JavaScript to handle the click functionality
document.addEventListener('DOMContentLoaded', function() {
  const faqContainers = document.querySelectorAll('.faq-container');
  
  faqContainers.forEach(container => {
    const summary = container.querySelector('.faq-summary');
    
    summary.addEventListener('click', function() {
      container.toggleAttribute('open');
    });
  });
});


// Highlight the current section in the table of contents
document.addEventListener("DOMContentLoaded", () => {
    const headings = document.querySelectorAll("h2, h3, h4, h5");
    const tocLinks = document.querySelectorAll(".toc-list a");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const id = entry.target.id;

            tocLinks.forEach(link => {
                link.classList.toggle(
                    "active",
                    link.getAttribute("href") === "#" + id
                );
            });
        });
    }, {
        rootMargin: "-120px 0px -60% 0px",
        threshold: 0
    });

    headings.forEach(h => {
        if (h.id) observer.observe(h);
    });
});