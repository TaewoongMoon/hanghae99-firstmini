// review 상자 open/close 함수
function openClose(num) {
    if ($("#comment"+num).css("display") == "block") {
        $("#comment"+num).hide();
        $("#btn-review"+num).text("후기상자 열기");
    } else {
        $("#comment"+num).show();
        $("#btn-review"+num).text("후기상자 닫기");
    }
}

// myPage 호출 함수
function showMyPage() {
    $('#wrap-card').empty();
    $.ajax({
        type: "GET",
        url: "/api/getMyPage",
        data: {},
        success: function (response) {
            console.log(response);
            mytrip_receive = response['all_reviewdata'];
            for(i = 0; i<mytrip_receive.length; i++){
                region_name = mytrip_receive[i]['region'];
                place_name = mytrip_receive[i]['place_name'];
                place_url = mytrip_receive[i]['place_url'];
                place_phone = mytrip_receive[i]['place_phone'];
                place_address = mytrip_receive[i]['place_address'];
                acc_name = mytrip_receive[i]['accommodation_name'];
                acc_url = mytrip_receive[i]['accommodation_url'];
                acc_phone = mytrip_receive[i]['accommodation_phone'];
                acc_address = mytrip_receive[i]['accommodation_address'];
                console.log(region_name, place_name, acc_name);
                temp_html = `<h2 >My Trip ${i+1}</h2>
                            <div class="trip-box" id="trip-box" >
                                <div class="card card-region" style="background-image: url('/static/imgs/${region_name}.jpeg')">
                                    <div class="card-body">
                                        <h5 class="card-region-title" id="city0">${region_name}</h5>
                                    </div>
                                </div>
                                <div class="card">
                                    <img class="card-img-top" src="/static/imgs/exam.jpeg" alt="Card image cap">
                                    <div class="card-body">
                                        <p class="card-title">${place_name}</p>
                                        <p class="card-address">${place_address}</p>
                                        <p class="card-phone">${place_phone}</p>
                                        <a class="card-url" href="${place_url}">${place_url}</a>
                                    </div>
                                </div>
                                <div class="card">
                                    <img class="card-img-top" src="/static/imgs/exam.jpeg" alt="Card image cap">
                                    <div class="card-body">
                                        <p class="card-title">${acc_name}</p>
                                        <p class="card-address">${acc_address}</p>
                                        <p class="card-phone">${acc_phone}</p>
                                        <a class="card-url" href="${acc_url}">${acc_url}</a>
                                    </div>
                                </div>
                            </div>
                            <div class="trip-btns">
                                <button onclick="openClose(${i})" type="button" class="btn btn-primary reviewbox-btn" id="btn-review${i}">후기상자 열기</button>
                                <button onclick="deleteTravel(${i})" type="button" class="btn btn-danger delete-btn" id="btn-delete">여행 삭제</button>
                            </div>
                            <div class="comment${i}" id="comment${i}" style="display:none">
                                <textarea class="review${i}">가나다라마바사아자차카타파하 </textarea>
                                <button onclick="saveReview(${i})" type="button" class="btn btn-info comment-save-btn">후기 저장</button>
                            </div>`;
                $('#wrap-card').append(temp_html);
            }
        }
    })
}

// myPage 여행 삭제 함수
function deleteTravel(num) {
    review = $("#review"+num);
    id = "";
    token = {};
    num = 0;
    $.ajax({
        type: "POST",
        url: "/api/delete",
        data: { id_give: id, token_give: token , num_give: num, review_give: review },
        success: function (response) {
            console.log(response)
            showMyPage();
        }
    })
}

// main page 명소 검색 API 요청 함수
function searchAttraction() {
    attraction = $('#region').text();
    $.ajax({
        type: "POST",
        url: "/api/search-1",
        data: { location_give: attraction },
        success: function (response) {
            console.log(response);
        }
    })
}