function pay(){
        console.log("aaaaaa")
        fetch("/api/pay", {
                method: "post"

        }).then( res => res.json() ).then( data => {
                if ( data.code == 200 ){
                     var s = document.getElementById("success")
                       s.innerText = "Thành công"
                }
        })
}

function pay_cus(){
        console.log("goi ham thanh cong")
        fetch("/api/pay_cus", {
                method: "post"

        }).then( res => res.json() ).then( data => {
                if ( data.code == 200 ){
                     var s = document.getElementById("success")
                       s.innerText = "Thành công"
                }
        })
}