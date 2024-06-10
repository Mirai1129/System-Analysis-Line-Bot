function showContent(index) {
    // 隱藏所有卡片
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.display = 'none';
    });

    // 顯示選中的卡片
    const selectedCard = document.getElementById(`content-${index}`);
    if (selectedCard) {
        selectedCard.style.display = 'flex';
    }
}

function showLogoutConfirm() {
    document.getElementById('logoutConfirm').style.display = 'block';
}

function closeLogoutConfirm() {
    document.getElementById('logoutConfirm').style.display = 'none';
}

function confirmLogout() {
    window.location.href = "/members/logout"
}

