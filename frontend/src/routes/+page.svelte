<script lang="ts">

  interface Order {
    orderNumber: number;
    items: { item: Item, quantity: number }[];
    valid: boolean;
  }

  interface Item {
    name: string;
  }

  let burgers = 0;
  let fries = 0;
  let drinks = 0;
  let orders: Order[] = [];
  let loading = false;
  let userInput = "";
  let result = "";

  async function placeOrder() {
    if (!userInput || userInput.length < 3) {
      return;
    };
    loading = true;
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/place-order`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({order: userInput})
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const data = await response.json();
      result = data.placed_order;
      if (result.valid) {
        createOrder(result);
      } else {
        cancelOrder(result);
      };
      userInput = "";
    } catch (error) {
      console.error(error);
      result = "Something went wrong.";
    } finally {
      loading = false;
    }
  }

  function createOrder(result: any) { // TODO: create a Result interface
    burgers = burgers + result.burgers;
    fries = fries + result.fries;
    drinks = drinks + result.drinks;

    let newOrder: Order = {
      orderNumber: result.order_number,
      items: [
        { item: {name: "burgers"}, quantity: result.burgers },
        { item: {name: "fries"}, quantity: result.fries },
        { item: {name: "drinks"}, quantity: result.drinks }
      ],
      valid: true
    };
    orders = [...orders, newOrder];
  };

  function cancelOrder(result: any) { // TODO: create a Result interface
    if (result.order_number === 0) return;
    let orderToCancel = orders.find(order => order.orderNumber === result.order_number);
    if (orderToCancel) {
      orderToCancel.valid = false;
      let b = 0;
      let f = 0;
      let d = 0;
      orderToCancel.items.forEach(item => {
        if (item.item.name === "burgers") {
          b = item.quantity;
        } else if (item.item.name === "fries") {
          f = item.quantity;
        } else if (item.item.name === "drinks") {
          d = item.quantity;
        };
      });
      burgers = burgers - b;
      fries = fries - f;
      drinks = drinks - d;
    };
  };

</script>
<div class="flex m-10 justify-evenly">
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Burgers: {burgers}</div>
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Fries: {fries}</div>
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Drinks: {drinks}</div>
</div>

<div class="flex m-10 mt-[100px] justify-center">
  <input
    type="text"
    placeholder="What Would You Like To Order?"
    class="outline rounded-md p-3 m-9 w-1/3 text-lg"
    bind:value={userInput}
  >
  <button on:click={placeOrder} class="outline rounded-md p-3 m-10 bg-green-500">
    Place Order
  </button>
</div>

<div class="flex justify-center">
  <div class="w-3/4 justify-center">
    {#if loading}
      <p>Loading...</p>
    {:else if orders.length}
    <ul class="block ml-20 mr-20">
      <h3>Order History:</h3>
        {#each orders as order}
      <li class="flex justify-between p-3 m-3 rounded-lg outline {!order.valid && "line-through"}"><span>Order #{order.orderNumber}</span><span>{order.items.map((item) => {
        return (
          ` ${item.quantity} ${item.item.name}`
        )
      })}</span></li>
        {/each}
      </ul>
    {/if}
  </div>
</div>