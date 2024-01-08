function reserveTable() {
    var formData = {
        guest_name: document.getElementById('name').value,
        guest_phone_number: document.getElementById('phone').value,
        num_of_guest : document.getElementById('select-option').value,
        reservation_date: document.getElementById('date').value,
        reservation_time: document.getElementById('time').value
    };

    var jsonData = JSON.stringify(formData);
    console.log(jsonData)
    fetch('https://your-api-endpoint.com/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function cancelReservation(){
    var formData = {
        guest_phone_number: document.getElementById('phone').value
    };

    var jsonData = JSON.stringify(formData);
    console.log(jsonData)
    fetch('https://your-api-endpoint.com/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
