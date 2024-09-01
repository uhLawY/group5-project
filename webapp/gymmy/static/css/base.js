document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const navLinks = document.querySelector('.nav-links');

  burger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    burger.classList.toggle('active');
  });
});

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.favourite-form').forEach(form => {
      form.addEventListener('submit', event => {
          event.preventDefault(); 

          const url = form.getAttribute('data-url');
          const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;
          const button = form.querySelector('button');

          fetch(url, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken,
                  'X-Requested-With': 'XMLHttpRequest'
              },
              body: JSON.stringify({}) 
          })
          .then(response => response.json())
          .then(data => {
              if (data.added) {
                  button.textContent = 'Remove from Favourite';
              } else {
                  button.textContent = 'Add to Favourite';
              }
          })
          .catch(error => console.error('Error:', error));
      });
  });
});

