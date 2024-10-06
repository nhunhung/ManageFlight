
document.addEventListener('DOMContentLoaded', async () => {

            const {publicKey} = await fetch("/config").then(r => r.json())
            const stripe = Stripe(publicKey)
            const {clientSecret} = await fetch("/create-payment-intent", {
                    method: "POST",
                    headers: {
                            'Content-Type': 'application/json'
                    }
            }).then(r => r.json())

            const elements = stripe.elements({clientSecret})
            const paymentElement = elements.create('payment')
            paymentElement.mount('#payment-element')
            const form = document.getElementById('payment-form')

            form.addEventListener('submit', async(e) => {
                        e.preventDefault()
                        const {error} = await stripe.confirmPayment({
                                elements,
                                confirmParams: {
                                            return_url:  "http://127.0.0.1:5000/ticket"

                                }
                        })
                        if (error){
                                const messages = document.getElementById('error-messages')
                                messages.innerText = error.message
                        }
            })
})