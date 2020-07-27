// const $feedback_list = $(".feedback-list");
// const $userbox = $(".userbox");

// $feedback_list.on('click', async function(e){
//     if(e.target.classList.contains('fa-trash')){
//     console.log(e);
//     if(e.target.parentNode.parentNode.attributes['data-id'].value != null){
//         try{
//             const post = e.target.parentNode.parentNode.attributes['data-id'].value;
//             let res = await axios.post(`/feedback/${post}/delete`);
//             return ;
//         } catch(e){
//             alert(e.message);
//         }

//     }
//     else{
//         return;
//     }
//     }

//     else {
//         return;
//     }
// })

// $userbox.on('click', async function(e){
//     if(e.target.classList.contains('fa-trash')){
//     console.log(e);
//     if(e.target.parentNode.parentNode.attributes['data-username'].value != null){
//         try{
//             const user = e.target.parentNode.parentNode.attributes['data-username'].value;
//             let res = await axios.post(`/users/${user}/delete`);
//             return ;
//         }catch(e){
//             alert(e.message);
//         }

//     }
//     else{
//         return ;
//     }
//     }
// })





