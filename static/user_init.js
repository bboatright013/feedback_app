const $feedback_list = $(".feedback-list");
const $userbox = $(".userbox");

$feedback_list.on('click', async function(e){
    if(e.target.classList.contains('fa-trash')){
    console.log(e);
    if(e.target.parentNode.parentNode.attributes['data-id'].value != null){
        try{
            const post = e.target.parentNode.parentNode.attributes['data-id'].value;
            let res = await axios.post(`/feedback/${post}/delete`);
            $feedback_list.empty();
            await loadFeed();
            return ;
        } catch(e){
            alert(e.message);
        }

    }
    else{
        return;
    }
    }

    else {
        return;
    }
})




async function getUserFeedback(user_id){
    // uploads the user feed in the database to the DOM
    let jsonFeedback = await axios.get(`/feedback/${user_id}`);
    let feedback = jsonFeedback.data.feedback;
    for(feed of feedback){
        let res = create_userfeedback_html(feed);
        $feedback_list.append(res);
    }
}

function create_userfeedback_html(post){
    // Turn feed object into formatted html for table
  
    let html = `
        <div class="card m-3 col-6 mx-auto" data-id='${post.id}'>
            <div class="card-header">
              ${post.username}
            </div>
            <div class="card-body">
              <h5 class="card-title">${post.title}</h5><a href="/feedback/${post.id}/update"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a>
              <i class="fa fa-trash" aria-hidden="true"></i>

              <p class="card-text">${post.content}</p>
            </div>
          </div>`;
    return html;
}

async function loadFeed(){
    username = await axios.get('/user');
    console.log(username);
    getUserFeedback(username.data);
}


$(document).ready(loadFeed);