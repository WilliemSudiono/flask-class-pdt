function square() {
    var numberClient = document.getElementById("number").value;

    var url = "/square";

    axios({
        method: "post",
        url: url,
        data: {
            number: numberClient,
        },
        headers: {
            "Content-Type": "application/json",
        }
    }).then(
        (response) => {
            var result = response.data;
            console.log(response);
            document.getElementById("result").innerHTML = result["result"];
            document.getElementById("message").innerHTML = result["message"];
        },
        (error) => {
            console.log(error);
        }
    );
}
