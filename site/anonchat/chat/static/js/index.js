function post(endpoint, body, callback) {
  fetch('/api/' + endpoint, {
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
    body: JSON.stringify(body)
  }).then(
    (response) => response.json()
  ).then(
    (data) => {
      if (data.success) {
        callback(data)
      } else {
        app.error = data.error
      }
    }
  )
}

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    error: '',
    messages: [],
    tutorial: true,
    registerModal: false
  },
  methods: {
    sendMessage() {
      let button = document.getElementById('send-button');
      button.classList.add('is-loading');
      let message = document.getElementById('message');
      post(
        'rooms' + window.location.pathname + '/post',
        {content: message.value},
        function(data) {
          socket.send(JSON.stringify(data.message));
          document.body.scrollIntoView(false);
        }
      );
      message.value = "";
      button.classList.remove('is-loading');
    },
    registerUser() {
      let username = document.getElementById('username').value
      post(
        'register',
        {username: username},
        function (data) {
          window.location.reload()
        }
      )
    },
    copyChatRoom() {
      document.getElementById('chatroom').select()
      document.execCommand('copy')
    }
  }
});

let path = window.location.pathname.substring(1)
if (path.length) {
  let protocol = window.location.protocol == 'https:' ? 'wss://' : 'ws://'
  socket = new WebSocket(
    protocol + window.location.hostname + ':' + window.location.port + '/ws/rooms' + window.location.pathname 
  )
  socket.onmessage = function (event) {
    app.messages.push(JSON.parse(event.data))
  }
}
