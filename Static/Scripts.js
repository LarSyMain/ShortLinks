
document.getElementById("URLold").addEventListener("keydown", async function(event){
                
                
    if (event.key === "Enter"){
        const inputElement = document.getElementById("URLold");
        const UrlOld = inputElement.value;
        const response = await fetch("/old", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({ 
            URLOld: UrlOld
        })
        });
    
        let response_db = await fetch("/dbdata");

        if (response_db.ok) {
            let text = await response_db.text(); // Получаем текст ответа
            let json = JSON.parse(text); // Парсим его
            console.log(json[`${UrlOld}`]);
            var paragraph = document.getElementById("Result");
            paragraph.textContent=`http://127.0.0.1:1488/${json[`${UrlOld}`]}`;
        } else {
            console.log("Error");
        }

    }
});

//https://pythonru.com/osnovy/python-join
