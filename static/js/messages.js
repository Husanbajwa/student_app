let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to ;
        if (USER_ID == 1 ) {
          send_to = 2
        }
        else{
          send_to = 1
        }

        // let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to
            // 'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}



socket.onmessage = async function(e){
  console.log('message', e)
  let data = JSON.parse(e.data)
  let message = data['message']
  let sent_by_id = data['sent_by']
  // let thread_id = data['thread_id']
  newMessage(message, sent_by_id)
}

socket.onerror = async function(e){
  console.log('error', e)
}

socket.onclose = async function(e){
  console.log('close', e)
}

    
function newMessage(message , sent_by_id) {
  if ($.trim(message) === '') {
    return false;
  }
  if (sent_by_id == USER_ID ){
    message_element = `
      <div class="thread">
        <div class="thread__top">
          <div class="thread__author">
            <a href="{% url 'user-profile' message.user.id %}" class="thread__authorInfo">
              <div class="avatar avatar--medium">
                <img src=${avatar} />
              </div>
              <span>@${username}</span>
            </a>
            <span class="thread__date">now</span>
          </div>
          
        </div>
        <div class="thread__details">
          ${message}
        </div>
      </div>
	    `
  }
  else{
    message_element = `
      <div class="thread">
        <div class="thread__top">
          <div class="thread__author">
            <a href="{% url 'user-profile' message.user.id %}" class="thread__authorInfo">
              <div class="avatar avatar--medium">
                <img src=${avatar} />
              </div>
              <span>@${username}</span>
            </a>
            <span class="thread__date">now</span>
          </div>
          
        </div>
        <div class="thread__details">
          ${message}
        </div>
      </div>
	    `
  }

  console.log($(message_element))
  message_body.append($(message_element))
  message_body.animate({
    scrollDown: $(document).height()
  }, 100);
  input_message.val(null)
}
