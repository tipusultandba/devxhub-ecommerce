const form = document.getElementById("id_checkout_form");
const paypal_btn = document.getElementById("paypal-button-container");
const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const validateFormAndCheckout = () => {
    const url = '/orders/checkout/';
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: new FormData(form)
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data.success) {
            console.log("Success Submitted");
            paypal_btn.style.display = 'block';
            form.style.display = 'none';
        }
        else {
            console.log(data);
        }
    }).catch(error => {
        console.log(error);
    })
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    validateFormAndCheckout();
})


paypal.Buttons({
    createOrder: function (data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: '25.50',
                }
            }]
        });
    },
    // Execute the payment
    onApprove: function (data, actions) {
        return actions.order.capture().then(function (orderData) {
            // Show a confirmation message to the buyer
            window.alert('Thank you for your purchase!', orderData);
        });
    }
}).render('#paypal-button-container');