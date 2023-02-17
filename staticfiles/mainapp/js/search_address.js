let search = document.getElementById("search");
search.addEventListener(
    "click",
    () => {
        let api = "https://zipcloud.ibsnet.co.jp/api/search?zipcode=";
        let error = document.getElementById("error");
        let input = document.getElementById("zipcode");
        let address1 = document.getElementById("address1");
        let address2 = document.getElementById("address2");
        let address3 = document.getElementById("address3");

        let prefSelect = document.getElementById('pref_name');
        let options = prefSelect.options;

        let param = input.value.replace("-", ""); //入力された郵便番号から「-」を削除
        let url = api + param;
        fetchJsonp(url, {
            timeout: 10000, //タイムアウト時間
        })
            .then((response) => {
                error.textContent = ""; //HTML側のエラーメッセージ初期化
                return response.json();
            })
            .then((data) => {
                if (data.status === 400) {
                    //エラー時
                    error.textContent = "郵便番号を入力してください。";
                } else if (data.results === null) {
                    error.textContent = "郵便番号から住所が見つかりませんでした。";
                } else {
                    address1.value = data.results[0].address1;
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].innerText === data.results[0].address1) {
                            options[i].selected = true;
                        }
                    }


                    address2.value = data.results[0].address2;
                    address3.value = data.results[0].address3;
                }
            })
            .catch((ex) => {
                //例外処理
                console.log(ex);
            });
    },
    false
);

let prefSelect = document.getElementById('pref_name');
prefSelect.addEventListener('change', () => {
    let address1 = document.getElementById("address1");
    let selectedIndex = prefSelect.selectedIndex
    address1.value = prefSelect.options[selectedIndex].innerText
})