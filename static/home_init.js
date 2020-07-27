
const $feedback_list_home = $(".feedback-list");

async function getFeedback(){
    // uploads the feedback in the database to the DOM
    let jsonFeedback = await axios.get('/feedback');
    let feedback = jsonFeedback.data.feedback;
    for(feed of feedback){
        let res = create_feedback_html(feed);
        $feedback_list_home.append(res);
    }
}



function create_feedback_html(post){
    // Turn feed object into formatted html for table
  
    let html = `
        <div class="card m-3 col-6 mx-auto" data-id='${post.id}'>
            <div class="card-header">
              ${post.username}
            </div>
            <div class="card-body">
              <h5 class="card-title">${post.title}</h5>

              <p class="card-text">${post.content}</p>
            </div>
          </div>`;
    return html;
}

$(document).ready(getFeedback);
