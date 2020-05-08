var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    error: '',
    tutorial: true
  },
  methods: {
    registerUser() {
      fetch('/api/register', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
          'username': document.getElementById('username').value
        })
      }).then(
        (response) => response.json()
      ).then(
        (data) => {
          if (data.success) {
            window.location = '/' + data.slug
          } else {
            this.error = data.error
          }
        }
      );
    },
    copyChatRoom() {
      document.getElementById('chatroom').select()
      document.execCommand('copy')
    }
  }
});
