document.addEventListener('DOMContentLoaded', function() {
  const search = document.getElementById('site-search');
  search.addEventListener('input', function() {
    const val = search.value.toLowerCase();
    document.querySelectorAll('.sidebar .category-list li').forEach(li => {
      const text = li.textContent.toLowerCase();
      if (
        (li.parentElement.previousElementSibling === null || li.parentElement.previousElementSibling.textContent.includes('Collection')) &&
        !text.includes(val)
      ) {
        li.style.display = 'none';
      } else {
        li.style.display = '';
      }
    });
  });
});