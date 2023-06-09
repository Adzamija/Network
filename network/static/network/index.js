document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for edit and like buttons
    const editButtons = document.querySelectorAll('.edit');
    const likeButtons = document.querySelectorAll('.like');
    // Handling the all buttons
    editButtons.forEach(button => {
        button.addEventListener('click', edit);
    });
    likeButtons.forEach(button => {
        button.addEventListener('click', like);
    });
    edit();
});


function edit() {
    const editButtons = document.querySelectorAll(".edit");

    const buttonPressed = e => {
        const post_id = e.target.id;

        fetch(`/posts/${post_id}`)
            .then(response => response.json())
            .then(post => {
                const text_post = post[0]["fields"]["body"];
                const postElement = document.querySelector(`#post_${post_id}`);
                postElement.innerHTML = '';
                const textArea = document.createElement('textarea');
                textArea.value = text_post;
                textArea.style.height = '100px';
                textArea.style.width = '100%';
                textArea.id = 'edited_body'
                postElement.appendChild(textArea);

                // Remove the button
                const editButton = document.getElementById(post_id);
                editButton.remove();

                // Save button
                const saveButton = document.createElement('button');
                saveButton.type = 'button';
                saveButton.id = 'save';
                saveButton.classList.add('btn', 'btn-success', 'mt-1', 'save');
                saveButton.style.width = '20%';
                saveButton.innerText = 'Save';
                postElement.appendChild(saveButton);
                // Saving the edited post
                document.querySelector('#save').addEventListener('click', function(){
                    const new_text = document.querySelector('#edited_body').value;
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    fetch(`/posts/${post_id}`, {
                        method: 'PUT',
                        headers: {'X-CSRFToken': csrftoken},
                        mode: 'same-origin',
                        body: JSON.stringify({
                            new_body: new_text,
                        })
                    })
                    .then(() => {
                        const postElement = document.querySelector(`#post_${post_id}`);
                        const textarea = postElement.querySelector('textarea');
                        if (textarea) {
                          postElement.removeChild(textarea);
                        }
                        
                        const paragraph = document.createElement('p');
                        paragraph.classList.add('fw-medium', 'mb-1');
                        paragraph.id = `post_${post_id}`;
                        paragraph.textContent = new_text;
                        postElement.appendChild(paragraph);
                        
                        const buttonHtml = `<button type="button" id="${post_id}" class="btn btn-primary mt-1 edit" style="width: 20%;">Edit</button>`;
                        postElement.insertAdjacentHTML('beforeend', buttonHtml);
                        
                        const saveButton = postElement.querySelector('.save');
                        if (saveButton) {
                          postElement.removeChild(saveButton);
                        }
                    })

                })
            });

    };

    for (let editButton of editButtons) {
        editButton.addEventListener("click", buttonPressed);
    }
}
function like(e) {
    e.preventDefault();
    const post_id = e.target.value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/like/${post_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            const likeButton = document.getElementById(`like_${post_id}`);
            const likeCount = document.getElementById(`like_count_${post_id}`);
            console.log(data);
            if (data.liked) {
                likeButton.style.color = 'red';
            } else {
                likeButton.style.color = 'black';
            }

            likeCount.innerText = data.count;
        })
        .catch(error => {
            console.log('Error:', error);
        });
}
