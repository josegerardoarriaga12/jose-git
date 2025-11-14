const commentsList = document.getElementById('comments-list');
const form = document.getElementById('comment-form');

function createCommentCard(author, text, isReply=false) {
    const card = document.createElement('div');
    card.classList.add(isReply ? 'reply-card' : 'comment-card');

    const date = new Date();
    const formattedDate = `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`;

    card.innerHTML = `
        <div class="avatar">${author[0].toUpperCase()}</div>
        <div class="comment-content">
            <div class="comment-header">
                <span class="comment-author">${author}</span>
                <span class="comment-date">${formattedDate}</span>
            </div>
            <div class="comment-text">${text}</div>
            <div class="comment-actions">
                <button class="like-btn">❤️ Me gusta</button>
                <button class="reply-btn">💬 Responder</button>
            </div>
            <div class="replies"></div>
        </div>
    `;

    const likeBtn = card.querySelector('.like-btn');
    let likes = 0;
    likeBtn.addEventListener('click', () => {
        likes++;
        likeBtn.textContent = `❤️ Me gusta (${likes})`;
    });

    const replyBtn = card.querySelector('.reply-btn');
    const repliesContainer = card.querySelector('.replies');
    replyBtn.addEventListener('click', () => {
        const replyAuthor = prompt("Nombre:");
        const replyText = prompt("Comentario:");
        if(replyAuthor && replyText){
            const replyCard = createCommentCard(replyAuthor, replyText, true);
            repliesContainer.appendChild(replyCard);
        }
    });

    return card;
}

form.addEventListener('submit', function(e){
    e.preventDefault();
    const author = document.getElementById('author').value.trim();
    const comment = document.getElementById('comment').value.trim();
    if(author && comment){
        const newComment = createCommentCard(author, comment);
        commentsList.appendChild(newComment);
        form.reset();
        newComment.scrollIntoView({ behavior: "smooth" });
    }
});

commentsList.appendChild(createCommentCard("Coco_Crochet", "¿Cuál es tu opinión de los productos que se venden?"));