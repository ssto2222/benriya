function card(stripe_published_key, customer_email, client_secret){
    document.addEventListener("DOMContentLoaded", (e)=>{
        let stripe = Stripe(stripe_published_key);
        initialize()
        const appearance = {
            theme: 'stripe',
            };
        elements = stripe.elements({ appearance, client_secret });

        let style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing:'antialiased',
                fontSize: '16px',
                '::placeholder': {
                color: '#aab7c4'
                },
            },
            invalid: {
                color:'#fa755a',
                iconColor:'#fa755a'
            }
        };

        
        //create an instance of the card Element.
        //let linkAuthenticationElement = elements.create("linkAuthentication");
        let card = elements.create('card', {style: style});
        card.mount("#payment-element");
        //linkAuthenticationElement.mount("#link-authentication-element")
        
        card.addEventListener('chenge', (event)=>{
            let displayError = document.getElementById('card-errors');
            if(event.error){
                displayError.textContent =event.error.message;
            }else{
                displayError.textContent = '';
            }
        })

        linkAuthenticationElement.on('change', (event) => {
            emailAddress = event.value.email;
          });

        const paymentElementOptions = {
            layout: "tabs",
          };
        
        const paymentElement = elements.create("payment", paymentElementOptions);
        paymentElement.mount("#payment-element");

    })

    async function initialize() {
        const response = await fetch("/create-checkout-intent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          
      
        });
        const { clientSecret } = await response.json();
      
        const appearance = {
          theme: 'stripe',
        };
        elements = stripe.elements({ appearance, clientSecret });
      
        const linkAuthenticationElement = elements.create("linkAuthentication");
        linkAuthenticationElement.mount("#link-authentication-element");
      
        linkAuthenticationElement.on('change', (event) => {
          emailAddress = event.value.email;
        });
      
        const paymentElementOptions = {
          layout: "tabs",
        };
      
        const paymentElement = elements.create("payment", paymentElementOptions);
        paymentElement.mount("#payment-element");
      }
}