// This is your test publishable API key.
const stripe = Stripe('pk_test_51Jdy9BDGjgnmtiVoojq4uz56gyZncAd1RJwwwmY7dZTbwldbueovPhwhXqzE588VUTSoMKypc7jLuG65p69fXze500cnJBaWGy');

// The items the customer wants to buy

let elements;

initialize();


var emailAddress = "";
// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch("/create-checkout-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const { clientSecret } = await response.json();

  const appearance = {
    theme: "stripe",
  };
  elements = stripe.elements({ appearance, clientSecret });

  const linkAuthenticationElement = elements.create("linkAuthentication");
  linkAuthenticationElement.mount("#link-authentication-element");

  linkAuthenticationElement.on("change", (event) => {
    emailAddress = event.value.email;
  });

  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");
}

const form = document.getElementById('payment-form')
form.addEventListener("submit", async (event) => {
  e.preventDefault();
  setLoading(true);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: "{% url 'mainapp:success' %}",
      receipt_email: emailAddress,
    },
  });

  async function handleSubmit(e) {

  };

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
});
// Fetches the payment intent status after payment submission

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}
