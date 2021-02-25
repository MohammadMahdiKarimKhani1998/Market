function logout_alert() {
    alert("شما از پروفایل خود خارج شدید!");
}

function authenticated_alert() {
    alert("شما قبلا به فروشگاه وارد شده اید!");
}

function authenticated_basket_alert() {
    alert("برای خرید از فروشگاه ابتدا به پروفایل خود وارد شوید.")
}

function delete_show(){
    $('#show_search_results').children().remove()
}

function search_product(){
    let word = document.getElementById("search").value;
    const data = JSON.stringify({word:word});
    $('#show_search_results').children().remove()
    $.ajax({
        type: "post",
        url: "http://127.0.0.1:8000/home/search/",
        data: data,
        success: function (response) {
            const data = JSON.parse(response);
            const results = data['list'];
            const slugs = data['slugs'];
            const shops = data['shops'];

            for(let i=0; i<data['list'].length; i++ ){
                $('#show_search_results').prepend(`
                    <a class="dropdown-item text-right card_text" href="http://127.0.0.1:8000/products/single/${slugs[i]}/${shops[i]}/" dir="rtl">${results[i]}</a>
                    <hr>
                `)
            }
            console.log(typeof data['list'].length)
        }});
}